import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Amazon Returns Analysis", page_icon="📦", layout="wide")

st.title("📦 Amazon Returns Analysis Tool")
st.markdown("Process and analyze Amazon return data with reimbursement and replacement tracking")

# ---------- Helper to avoid PyArrow type issues ----------
def make_arrow_safe(df: pd.DataFrame) -> pd.DataFrame:
    """Convert all object columns to string to avoid PyArrow ArrowTypeError."""
    df = df.copy()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str)
    return df

# File upload section
st.header("1️⃣ Upload Files")
col1, col2, col3 = st.columns(3)

with col1:
    returns_file = st.file_uploader("Upload Returns.xlsx", type=['xlsx'], key='returns')
with col2:
    reimb_file = st.file_uploader("Upload Reimbursement.xlsx", type=['xlsx'], key='reimb')
with col3:
    replacement_file = st.file_uploader("Upload Replacement.xlsx", type=['xlsx'], key='replacement')

def safe_vlookup(left_df, right_df, left_on, right_on, return_col=None, 
                 how_mode="map", duplicate_strategy="first"):
    """Safe VLOOKUP-like function"""
    left = left_df.copy()
    right = right_df.copy()
    
    # Clean keys
    left[left_on] = left[left_on].astype(str).str.strip()
    right[right_on] = right[right_on].astype(str).str.strip()
    
    map_source_col = right_on if return_col is None else return_col
    
    if how_mode == "map":
        if map_source_col not in right.columns:
            raise KeyError(f"Column '{map_source_col}' not found in lookup DataFrame")
        
        # Resolve duplicates
        if right[right_on].duplicated().any():
            if duplicate_strategy == "first":
                right_small = right.drop_duplicates(subset=[right_on], keep="first")
            elif duplicate_strategy == "last":
                right_small = right.drop_duplicates(subset=[right_on], keep="last")
            else:
                right_small = right.drop_duplicates(subset=[right_on], keep="first")
        else:
            right_small = right[[right_on, map_source_col]].copy()
        
        lookup_series = right_small.set_index(right_on)[map_source_col]
        new_col_name = map_source_col if return_col is not None else right_on
        left.loc[:, new_col_name] = left[left_on].map(lookup_series)
        return left
    
    elif how_mode == "merge":
        cols_to_bring = [right_on]
        if return_col is not None:
            cols_to_bring.append(return_col)
        cols_to_bring = list(dict.fromkeys(cols_to_bring))
        
        right_small = right[cols_to_bring].drop_duplicates(subset=[right_on])
        
        merged = left.merge(
            right_small,
            how="left",
            left_on=left_on,
            right_on=right_on,
            suffixes=("", "_lookup")
        )
        return merged

# Process data when all files are uploaded
if returns_file and reimb_file and replacement_file:
    with st.spinner("Processing data..."):
        try:
            # Read files
            returns = pd.read_excel(returns_file)
            reimb = pd.read_excel(reimb_file)
            replacement = pd.read_excel(replacement_file)

            # 🔧 Immediately normalize sku and other object columns in raw data
            if 'sku' in returns.columns:
                returns['sku'] = returns['sku'].astype(str)
            returns = make_arrow_safe(returns)
            reimb = make_arrow_safe(reimb)
            replacement = make_arrow_safe(replacement)
            
            st.success("✅ Files loaded successfully!")
            
            # Show data preview
            with st.expander("📊 View Raw Data Preview"):
                tab1, tab2, tab3 = st.tabs(["Returns", "Reimbursement", "Replacement"])
                with tab1:
                    st.dataframe(returns.head(), use_container_width=True)
                with tab2:
                    st.dataframe(reimb.head(), use_container_width=True)
                with tab3:
                    st.dataframe(replacement.head(), use_container_width=True)
            
            # Processing
            st.header("2️⃣ Data Processing")
            
            # Convert return-date to date only
            returns['return-date1'] = pd.to_datetime(returns['return-date'], errors='coerce').dt.date
            
            # Create Today column
            returns['Today'] = datetime.today().date()
            
            # Calculate date difference
            returns['Date_Diff'] = (pd.to_datetime(returns['Today']) - 
                                   pd.to_datetime(returns['return-date1'])).dt.days
            
            # 🔢 User-controlled days filter (instead of hard-coded 40)
            st.subheader("📅 Enter Days Filter")
            days_filter = st.number_input(
                "Show returns older than (days):",
                min_value=0,
                max_value=365,
                value=40,    # default value
                step=1,
                help="Enter any number of days (e.g. 10, 12, 40, 45...)"
            )
            
            # Filter where difference > user-entered days
            returns_45 = returns[returns['Date_Diff'] > days_filter].copy()
            returns_45 = make_arrow_safe(returns_45)
            
            st.metric(f"Returns older than {int(days_filter)} days", len(returns_45))
            
            # Filter reimbursement
            reimb_filtered = reimb[reimb['reason'].isin(['CustomerReturn', 'CustomerServiceIssue'])].copy()
            reimb_filtered = make_arrow_safe(reimb_filtered)
            
            # VLOOKUP for reimbursement reason
            result_merge = safe_vlookup(
                returns_45, reimb_filtered,
                left_on='order-id', right_on='amazon-order-id',
                return_col='reason', how_mode='merge'
            )
            
            # Extract Amount Total
            result_merge['Amount_Total'] = returns['order-id'].map(
                reimb_filtered.drop_duplicates(subset='amazon-order-id', keep='first')
                             .set_index('amazon-order-id')['amount-total']
            )
            
            # Filter damaged items
            returns_final = result_merge[
                result_merge['detailed-disposition'].isin(['CARRIER_DAMAGED', 'CUSTOMER_DAMAGED', 'DAMAGED'])
            ]
            
            # Filter where reimbursement order ID is N/A
            returns_final = returns_final[returns_final['amazon-order-id'].isna()].copy()
            
            st.metric("Damaged items without reimbursement", len(returns_final))
            
            # Process replacement data
            returns['order-id'] = returns['order-id'].astype(str).str.strip()
            replacement['replacement-amazon-order-id'] = replacement['replacement-amazon-order-id'].astype(str).str.strip()
            replacement['original-amazon-order-id'] = replacement['original-amazon-order-id'].astype(str).str.strip()
            
            returns_final = returns_final.copy()
            
            # Map replacement order ID
            returns_final.loc[:, 'Replacement_OrderId'] = returns_final['order-id'].map(
                replacement.drop_duplicates(subset='replacement-amazon-order-id', keep='first')
                          .set_index('replacement-amazon-order-id')['original-amazon-order-id']
            )
            
            # Get unique reimbursement data
            reimb_unique = reimb_filtered.drop_duplicates(subset='amazon-order-id', keep='first')
            
            # Map replacement reason and amount
            returns_final.loc[:, 'Replacement_Reason'] = returns_final['Replacement_OrderId'].map(
                reimb_unique.set_index('amazon-order-id')['reason']
            )
            
            returns_final.loc[:, 'Replacement_Amount'] = returns_final['Replacement_OrderId'].map(
                reimb_unique.set_index('amazon-order-id')['amount-total']
            )
            
            # Filter where replacement order ID is N/A
            returns_final = returns_final[returns_final['Replacement_OrderId'].isna()].copy()
            
            # 🔧 Make final DF Arrow-safe (including sku)
            if 'sku' in returns_final.columns:
                returns_final['sku'] = returns_final['sku'].astype(str)
            returns_final = make_arrow_safe(returns_final)
            
            st.metric("Final eligible returns", len(returns_final))
            
            # Display results
            st.header("3️⃣ Results")
            
            if len(returns_final) > 0:
                st.success(f"✅ Found {len(returns_final)} returns eligible for reimbursement claim!")
                
                # Summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    avg_days = returns_final['Date_Diff'].mean()
                    st.metric("Average Days Since Return", f"{avg_days:.0f}")
                with col2:
                    total_amount = returns_final['Amount_Total'].sum()
                    st.metric("Total Reimbursement Amount", f"₹{total_amount:,.2f}" if pd.notna(total_amount) else "N/A")
                with col3:
                    unique_skus = returns_final['sku'].nunique()
                    st.metric("Unique SKUs", unique_skus)
                
                # Show data
                st.subheader("📋 Final Returns Data")
                st.dataframe(returns_final, use_container_width=True)
                
                # Download button
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    returns_final.to_excel(writer, sheet_name='Final Returns', index=False)
                
                st.download_button(
                    label="📥 Download Final Report (Excel)",
                    data=buffer.getvalue(),
                    file_name="Final_Returns_Report_Replacement_NA.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
                # Additional analysis
                with st.expander("📊 Additional Analysis"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Top SKUs by Count")
                        top_skus = returns_final['sku'].value_counts().head(10)
                        # value_counts() gives a Series; convert to DF for safety
                        top_skus_df = top_skus.reset_index()
                        top_skus_df.columns = ['sku', 'count']
                        top_skus_df = make_arrow_safe(top_skus_df)
                        st.bar_chart(top_skus_df.set_index('sku'))
                    
                    with col2:
                        st.subheader("Returns by Fulfillment Center")
                        fc_counts = returns_final['fulfillment-center-id'].value_counts()
                        fc_df = fc_counts.reset_index()
                        fc_df.columns = ['fulfillment-center-id', 'count']
                        fc_df = make_arrow_safe(fc_df)
                        st.bar_chart(fc_df.set_index('fulfillment-center-id'))
                    
                    st.subheader("Returns by Reason")
                    reason_counts = returns_final['reason'].value_counts()
                    reason_df = reason_counts.reset_index()
                    reason_df.columns = ['reason', 'count']
                    reason_df = make_arrow_safe(reason_df)
                    st.bar_chart(reason_df.set_index('reason'))
                
            else:
                st.info("ℹ️ No returns found matching the criteria (damaged items without reimbursement or replacement)")
            
        except Exception as e:
            st.error(f"❌ Error processing data: {str(e)}")
            st.exception(e)
else:
    st.info("👆 Please upload all three required Excel files to begin processing")
    
    with st.expander("ℹ️ How to use this tool"):
        st.markdown("""
        ### Steps:
        1. **Upload Files**: Upload your Returns, Reimbursement, and Replacement Excel files
        2. **Review Data**: Check the raw data preview to ensure files are correct
        3. **View Results**: See the final eligible returns for reimbursement claims
        4. **Download Report**: Download the processed Excel report
        
        ### What this tool does:
        - Filters returns older than a user-defined number of days
        - Identifies damaged items (CARRIER_DAMAGED, CUSTOMER_DAMAGED, DAMAGED)
        - Excludes items already reimbursed
        - Excludes items with replacement orders
        - Calculates reimbursement amounts
        - Generates downloadable report
        
        ### Output:
        The final report contains returns that are eligible for reimbursement claims with Amazon.
        """)


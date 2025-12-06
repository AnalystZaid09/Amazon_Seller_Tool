import streamlit as st
from pathlib import Path
import time

st.set_page_config(
    page_title="Amazon Ops Super App",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent


st.markdown(
    """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Hero Section with Animation */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        animation: fadeInDown 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.95);
        margin-bottom: 0.5rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .hero-description {
        font-size: 1rem;
        color: rgba(255,255,255,0.85);
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Tool Cards */
    .tool-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid transparent;
        animation: fadeInUp 0.6s ease-out;
        animation-fill-mode: both;
        cursor: pointer;
        min-height: 280px;
        display: flex;
        flex-direction: column;
    }
    
    .tool-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
        border-color: #667eea;
    }
    
    .tool-icon {
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
        display: block;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .tool-card:hover .tool-icon {
        animation: none;
        transform: scale(1.2) rotate(5deg);
        transition: transform 0.3s ease;
    }
    
    .tool-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .tool-description {
        font-size: 0.95rem;
        color: #718096;
        line-height: 1.6;
        margin-bottom: 1rem;
        flex-grow: 1;
    }
    
    .tool-features {
        font-size: 0.85rem;
        color: #a0aec0;
        font-style: italic;
        margin-top: auto;
    }
    
    /* Fixed height for tool grid */
    .tool-grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .tool-grid-item {
        display: flex;
        flex-direction: column;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    }
    
    [data-testid="stSidebar"] .sidebar-title {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        text-align: center;
        padding: 1.5rem 1rem;
        background: rgba(102, 126, 234, 0.2);
        border-radius: 10px;
        margin-bottom: 1.5rem;
        animation: fadeInDown 0.5s ease-out;
    }
    
    /* Button Styling */
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stButton button:disabled {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        cursor: not-allowed;
        transform: none;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
    }
    
    /* Module Header */
    .module-header {
        background: white;
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: scaleIn 0.5s ease-out;
    }
    
    .module-title {
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .module-subtitle {
        font-size: 1rem;
        color: #718096;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #e0e7ff 0%, #cffafe 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Stagger animation delays for cards */
    .tool-card:nth-child(1) { animation-delay: 0.1s; }
    .tool-card:nth-child(2) { animation-delay: 0.2s; }
    .tool-card:nth-child(3) { animation-delay: 0.3s; }
    .tool-card:nth-child(4) { animation-delay: 0.4s; }
    .tool-card:nth-child(5) { animation-delay: 0.5s; }
    .tool-card:nth-child(6) { animation-delay: 0.6s; }
    
    /* Loading animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        margin-left: 0.5rem;
    }
    
    /* Quick stats */
    .quick-stat {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .quick-stat:hover {
        transform: translateY(-5px);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #718096;
        margin-top: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


MODULES = {
    "🏠 Home / Overview": None,
    "📊 Daily P&L Profit Analyzer": "app_dailypl.py",
    "📉 Amazon Refund Analyzer": "app_refund.py",
    "🔄 Amazon Replacement Analyzer": "app_replacement_refund.py",
    "📦 Amazon Returns Analysis Tool": "app1_return_refund.py",
    "📈 Order Analysis Dashboard": "app_sales_report.py",
    "🏷️ RIS Analysis Tool": "app_ris.py",
}

# Define the exact order for display (matches the image layout)
TOOL_ORDER = [
    "📊 Daily P&L Profit Analyzer",
    "📉 Amazon Refund Analyzer",
    "🔄 Amazon Replacement Analyzer",
    "📦 Amazon Returns Analysis Tool",
    "📈 Order Analysis Dashboard",
    "🏷️ RIS Analysis Tool",
]

MODULE_DESCRIPTIONS = {
    "📊 Daily P&L Profit Analyzer": "Upload Amazon transaction CSV + PM to get daily profit, fees, commissions and download styled Excel outputs.",
    "📉 Amazon Refund Analyzer": "Analyse refund patterns, over-refunds, Safe-T, FBA reimbursements and door-ship return behaviours.",
    "🔄 Amazon Replacement Analyzer": "Detect replacement vs return vs refund chains and Bulk RTO opportunities, so nothing slips through.",
    "📦 Amazon Returns Analysis Tool": "Combine Returns, Reimbursements and Replacements in one view to see the full story of every order.",
    "📈 Order Analysis Dashboard": "Order-level overview – brand, product, and manager wise metrics with filters and key KPIs.",
    "🏷️ RIS Analysis Tool": "Original.xlsx + FC stat + PM to understand RIS vs Non-RIS, broken by state and cluster for logistics decisions.",
}


def remove_set_page_config(code: str) -> str:
    """Remove the entire st.set_page_config(...) block, even if it's multi-line."""
    lines = code.splitlines()
    cleaned_lines = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if "st.set_page_config" in line.replace(" ", ""):
            paren_depth = line.count("(") - line.count(")")
            i += 1
            while paren_depth > 0 and i < n:
                next_line = lines[i]
                paren_depth += next_line.count("(") - next_line.count(")")
                i += 1
        else:
            cleaned_lines.append(line)
            i += 1
    return "\n".join(cleaned_lines)

def run_module(filename: str):
    """Load a .py file, strip set_page_config, and exec it in this Streamlit session."""
    module_path = BASE_DIR / filename
    if not module_path.exists():
        st.error(f"❌ File `{filename}` not found next to this main file.")
        st.info("💡 Open the MODULES dictionary at the top of this file and correct the filenames.")
        return
    
    try:
        code = module_path.read_text(encoding="utf-8")
    except Exception as e:
        st.error(f"⚠️ Error reading `{filename}`: {e}")
        return
    
    cleaned_code = remove_set_page_config(code)
    exec_globals = {
        "__name__": f"__embedded_{filename}__",
        "st": st,
    }
    
    try:
        exec(cleaned_code, exec_globals)
    except Exception as e:
        st.error(f"🔥 Error while running `{filename}`:")
        st.exception(e)


def show_home():
    # Hero Section
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-title">🧩 Amazon Operations Super App</div>
            <div class="hero-subtitle">Your All-in-One Operations Command Center</div>
            <div class="hero-description">
                One powerful platform for P&L analysis, refunds, replacements, returns, orders, RIS & more. 
                Upload your data once per tool and get clear, action-focused insights for your team.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Quick Stats Section
    st.markdown("### 📊 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="quick-stat">
                <div class="stat-value">6</div>
                <div class="stat-label">Analysis Tools</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="quick-stat">
                <div class="stat-value">∞</div>
                <div class="stat-label">Data Processing</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="quick-stat">
                <div class="stat-value">100%</div>
                <div class="stat-label">CSV/Excel Ready</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="quick-stat">
                <div class="stat-value">⚡</div>
                <div class="stat-label">Lightning Fast</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    st.markdown("### 🔧 Available Tools")
    st.caption("Click any card below to launch the tool instantly, or use the sidebar navigation.")
    
    # Create a fixed 2x3 grid layout
    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
    
    # Row 1: First 3 tools
    cols1 = st.columns(3)
    for j in range(3):
        label = TOOL_ORDER[j]
        icon = label.split()[0]
        title = " ".join(label.split()[1:])
        desc = MODULE_DESCRIPTIONS.get(label, "")
        
        with cols1[j]:
            st.markdown(
                f"""
                <div class="tool-card">
                    <span class="tool-icon">{icon}</span>
                    <div class="tool-title">{title}</div>
                    <div class="tool-description">{desc}</div>
                    <div class="tool-features">✅ CSV/Excel · 🧾 Amazon data · 📊 Export ready</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            if st.button(
                f"Launch {icon}",
                key=f"quick_{label}",
                use_container_width=True,
            ):
                st.session_state.active_module = label
                st.session_state.just_switched = True
                st.rerun()
    
    # Add spacing between rows
    st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)
    
    # Row 2: Last 3 tools
    cols2 = st.columns(3)
    for j in range(3):
        label = TOOL_ORDER[j + 3]
        icon = label.split()[0]
        title = " ".join(label.split()[1:])
        desc = MODULE_DESCRIPTIONS.get(label, "")
        
        with cols2[j]:
            st.markdown(
                f"""
                <div class="tool-card">
                    <span class="tool-icon">{icon}</span>
                    <div class="tool-title">{title}</div>
                    <div class="tool-description">{desc}</div>
                    <div class="tool-features">✅ CSV/Excel · 🧾 Amazon data · 📊 Export ready</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            if st.button(
                f"Launch {icon}",
                key=f"quick_{label}",
                use_container_width=True,
            ):
                st.session_state.active_module = label
                st.session_state.just_switched = True
                st.rerun()
    
    # Info Box
    st.markdown("""
        <div class="info-box">
            <strong>💡 Pro Tip:</strong> Each tool is designed to work independently. Upload your Amazon data files 
            to any tool and get instant insights. Results can be exported to Excel for further analysis.
        </div>
    """, unsafe_allow_html=True)


with st.sidebar:
    st.markdown('<div class="sidebar-title">🧭 Navigation</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if "active_module" not in st.session_state:
        st.session_state.active_module = "🏠 Home / Overview"
    
    # Navigation buttons
    for label, filename in MODULES.items():
        is_active = (label == st.session_state.active_module)
        
        if is_active:
            st.button(
                f"✓ {label}",
                key=f"nav_{label}",
                use_container_width=True,
                disabled=True,
            )
        else:
            if st.button(
                label,
                key=f"nav_{label}",
                use_container_width=True,
            ):
                st.session_state.active_module = label
                st.session_state.just_switched = True
                st.rerun()
    
    st.markdown("---")
    
    # Sidebar footer
    st.markdown("""
        <div class="info-box">
            <strong>ℹ️ About</strong><br>
            This app consolidates your Amazon operations tools into a unified interface. 
            Edit the <code>MODULES</code> dictionary to add or modify tools.
        </div>
    """, unsafe_allow_html=True)


current_label = st.session_state.active_module
current_file = MODULES[current_label]

# Show loading animation when switching
if st.session_state.get("just_switched", False):
    with st.spinner("Loading module..."):
        time.sleep(0.3)  # Brief delay for smooth transition
    st.session_state.just_switched = False

if current_file is None:
    show_home()
else:
    # Module header
    icon = current_label.split()[0]
    title = " ".join(current_label.split()[1:])
    
    st.markdown(
        f"""
        <div class="module-header">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="font-size: 3rem;">{icon}</span>
                <div>
                    <div class="module-title">{title}</div>
                    <div class="module-subtitle">📁 Module: <code>{current_file}</code></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Run the module
    run_module(current_file)
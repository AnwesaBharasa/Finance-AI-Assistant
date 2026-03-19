import streamlit as st
import os
import sys
import tempfile
import logging
import base64
import time
from datetime import datetime # Added datetime import

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models.agent import get_finance_agent_executor
from models.llm import get_vision_response
from utils.rag_logic import process_and_store_pdf, sync_knowledge_base, KNOWLEDGE_BASE_DIR, INDEXED_FILES_TRACKER

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_base64_of_bin_file(bin_file):
    """Encodes an uploaded image to a base64 string."""
    return base64.b64encode(bin_file.read()).decode('utf-8')

def get_chat_response(agent_executor, query):
    """Get response from the tool-calling agent, along with tool usage steps."""
    try:
        response = agent_executor.invoke({"input": query})
        output = response.get("output", str(response))
        steps = response.get("intermediate_steps", [])
        
        json_steps = []
        for step in steps:
            action, obs = step
            json_steps.append({
                "tool": action.tool,
                "tool_input": action.tool_input,
                "result": str(obs)[:500] + "..." if len(str(obs)) > 500 else str(obs)
            })
        return output, json_steps
    except Exception as e:
        error_msg = f"Error getting response: {str(e)}"
        logger.error(error_msg)
        return error_msg, []

def login_page():
    st.markdown("<h2 style='text-align: center;'>🔐 Secure Portal Login</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.8;'>Authenticate to access the Upgraded Phase 3 AI Assistant</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if username.strip().lower() == "admin" and password == "admin":
                    st.session_state.logged_in = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

def instructions_page():
    """Instructions and setup page"""
    st.header("💰 Agentic Finance AI Assistant")
    st.markdown("Welcome! Follow these instructions to set up and use the chatbot.")
    
    st.markdown("""
    ## 🔧 Setup
    
    This Finance & Tax AI Assistant requires configuration in `config/config.py` using `.env`.
    Ensure you have `GROQ_API_KEY` and `TAVILY_API_KEY` configured.
    
    ## How to Use
    1. **Go to the Chat page** (use the navigation in the sidebar).
    2. **Choose Search Mode**: Select 'Document Search' for strict PDF/Image domains, or 'Web Search' for real-time market news.
    3. **Upload Files**: If in Document Search, upload a PDF or an Image!
    4. **Ask Questions**: Ask about EMI, SIP, Budgets, Tax Regulations.
    
    ## Tips
    - Document Search guarantees complete safety mapping to uploaded context.
    - Web Search opens the model to answer market trends globally.
    """)

def chat_page():
    """Main chat interface page"""
    st.title("💰 Agentic Finance AI Assistant")
    
    # Import tools directly for interactive panels
    from utils.calculator import calculate_emi, calculate_sip
    from utils.budget_tool import plan_budget
    from utils.investment_tool import recommend_investment
    from utils.tax_tool import calculate_tax_optimization
    from utils.market_tool import get_stock_price
    from utils.calculator_fd import calculate_fd
    from utils.currency_tool import convert_currency
    
    # Quick Action Tool Selector
    st.markdown("##### ⚡ Quick Action Tools")
    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
    if row1_col1.button("🧮 EMI Calc", use_container_width=True):
        st.session_state.active_tool = "emi"
    if row1_col2.button("💰 Budget Info", use_container_width=True):
        st.session_state.active_tool = "budget"
    if row1_col3.button("📊 Tax Optimizer", use_container_width=True):
        st.session_state.active_tool = "tax"
    if row1_col4.button("📈 Investments", use_container_width=True):
        st.session_state.active_tool = "invest"
        
    row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
    if row2_col1.button("📉 Live Market", use_container_width=True):
        st.session_state.active_tool = "market"
    if row2_col2.button("🏦 FD Calculator", use_container_width=True):
        st.session_state.active_tool = "fd"
    if row2_col3.button("💱 Currency Conv", use_container_width=True):
        st.session_state.active_tool = "currency"
    if row2_col4.button("🧹 Clear Tool", use_container_width=True):
        st.session_state.active_tool = None

    
    # Interactive Tool Panels
    active_tool = st.session_state.get("active_tool", None)
    
    if active_tool == "emi":
        st.markdown("### 🧮 EMI Calculator")
        with st.form("emi_form"):
            e_col1, e_col2, e_col3 = st.columns(3)
            principal = e_col1.number_input("Loan Amount (Rs.)", min_value=1000.0, value=500000.0, step=10000.0)
            rate = e_col2.number_input("Annual Interest Rate (%)", min_value=0.1, value=8.5, step=0.1)
            tenure = e_col3.number_input("Tenure (Years)", min_value=1, value=10, step=1)
            submitted = st.form_submit_button("🧮 Calculate EMI", use_container_width=True)
            if submitted:
                result = calculate_emi.invoke({"principal": str(principal), "annual_interest_rate": str(rate), "tenure_years": str(tenure)})
                st.success(result)
    
    elif active_tool == "budget":
        st.markdown("### 💰 Budget Planner (50/30/20 Rule)")
        with st.form("budget_form"):
            b_col1, b_col2, b_col3 = st.columns(3)
            income = b_col1.number_input("Monthly Income (Rs.)", min_value=1000.0, value=100000.0, step=5000.0)
            fixed = b_col2.number_input("Fixed Expenses (Rs.)", min_value=0.0, value=35000.0, step=1000.0)
            goal = b_col3.number_input("Savings Goal (Rs.)", min_value=0.0, value=20000.0, step=1000.0)
            submitted = st.form_submit_button("💰 Generate Budget Plan", use_container_width=True)
            if submitted:
                result = plan_budget.invoke({"monthly_income": str(income), "fixed_expenses": str(fixed), "savings_goal": str(goal)})
                st.success(result)
    
    elif active_tool == "tax":
        st.markdown("### 📊 Tax Optimizer (Old vs New Regime)")
        with st.form("tax_form"):
            t_col1, t_col2 = st.columns(2)
            annual_income = t_col1.number_input("Annual Income (Rs.)", min_value=100000.0, value=1500000.0, step=50000.0)
            deductions = t_col2.number_input("Total Deductions (Rs.) [80C, 80D, etc.]", min_value=0.0, value=150000.0, step=10000.0)
            submitted = st.form_submit_button("📊 Calculate Tax", use_container_width=True)
            if submitted:
                result = calculate_tax_optimization.invoke({"annual_income": str(annual_income), "deductions": str(deductions)})
                st.success(result)
    
    elif active_tool == "invest":
        st.markdown("### 📈 Investment Recommender")
        with st.form("invest_form"):
            i_col1, i_col2 = st.columns(2)
            risk = i_col1.selectbox("Risk Profile", ["Low", "Medium", "High"])
            duration = i_col2.number_input("Investment Duration (Years)", min_value=1, value=10, step=1)
            submitted = st.form_submit_button("📈 Get Recommendations", use_container_width=True)
            if submitted:
                result = recommend_investment.invoke({"risk_profile": risk, "investment_duration_years": str(duration)})
                st.success(result)
    
    elif active_tool == "market":
        st.markdown("### 📉 Live Market Data")
        with st.form("market_form"):
            st.markdown("**Common Tickers:** `RELIANCE.NS`, `TCS.NS`, `INFY.NS`, `^NSEI` (Nifty 50), `^BSESN` (Sensex)")
            ticker = st.text_input("Enter Ticker Symbol", value="^NSEI")
            submitted = st.form_submit_button("📉 Fetch Live Price", use_container_width=True)
            if submitted:
                with st.spinner("Fetching live data from Yahoo Finance..."):
                    result = get_stock_price.invoke({"ticker_symbol": ticker})
                    st.success(result)
                    
    elif active_tool == "fd":
        st.markdown("### 🏦 FD Calculator")
        with st.form("fd_form"):
            f_col1, f_col2 = st.columns(2)
            principal = f_col1.number_input("Principal Amount (Rs.)", min_value=1000.0, value=100000.0, step=5000.0)
            rate = f_col2.number_input("Interest Rate (% p.a.)", min_value=1.0, value=7.0, step=0.1)
            f_col3, f_col4 = st.columns(2)
            tenure = f_col3.number_input("Tenure (Years)", min_value=1.0, value=5.0, step=0.5)
            compounding = f_col4.selectbox("Compounding Frequency", ["Monthly", "Quarterly", "Half-Yearly", "Yearly"], index=1)
            submitted = st.form_submit_button("🏦 Calculate Maturity", use_container_width=True)
            if submitted:
                result = calculate_fd.invoke({
                    "principal": str(principal), 
                    "annual_rate": str(rate), 
                    "years": str(tenure), 
                    "compounding_frequency": compounding.lower()
                })
                st.success(result)
                
    elif active_tool == "currency":
        st.markdown("### 💱 Currency Converter")
        with st.form("currency_form"):
            c_col1, c_col2, c_col3 = st.columns(3)
            amount = c_col1.number_input("Amount", min_value=1.0, value=100.0, step=1.0)
            from_curr = c_col2.text_input("From (e.g. USD)", value="USD")
            to_curr = c_col3.text_input("To (e.g. INR)", value="INR")
            submitted = st.form_submit_button("💱 Convert Now", use_container_width=True)
            if submitted:
                with st.spinner("Fetching live forex rate..."):
                    result = convert_currency.invoke({
                        "amount": str(amount), 
                        "from_currency": from_curr, 
                        "to_currency": to_curr
                    })
                    st.success(result)
    
    if active_tool:
        if st.button("❌ Close Tool Panel", use_container_width=True):
            st.session_state.active_tool = None
            st.rerun()
    
    st.divider()

    system_prompt_vision = "You are a Finance Assistant. Analyze the image to help the user."
    
    # Initialize Agent if missing
    if "agent" not in st.session_state:
        current_mode = st.session_state.get("current_search_mode", "Document Search")
        resp_mode = st.session_state.get("response_mode", "Detailed")
        try:
            with st.spinner(f"Initializing {current_mode} Agent..."):
                st.session_state.agent = get_finance_agent_executor(mode=current_mode, response_style=resp_mode)
        except Exception as e:
            st.error(f"Failed to initialize Agent: {str(e)}")
            st.session_state.agent = None

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "steps" in message and message["steps"]:
                with st.expander("🛠️ Agent Actions Details"):
                    for step_dict in message["steps"]:
                        st.markdown(f"**Tool Invoked**: `{step_dict['tool']}`")
                        st.markdown(f"**Input**: `{step_dict['tool_input']}`")
                        st.markdown(f"**Result**: *{step_dict['result']}*")
                        st.divider()
            
            st.markdown(message["content"])
            if "image" in message:
                try:
                    st.image(f"data:image/jpeg;base64,{message['image']}", width=300)
                except Exception:
                    pass
    
    # Chat input
    prompt = st.chat_input("Ask about taxes, SIP, EMI, or check market news...")

    if prompt:
        if not prompt.strip():
            st.warning("Please enter a valid query.")
            return

        # Add user message to chat history
        user_msg = {"role": "user", "content": prompt}
        if st.session_state.get("current_image_base64"):
            user_msg["image"] = st.session_state.current_image_base64
            
        st.session_state.messages.append(user_msg)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            if "image" in user_msg:
                st.image(f"data:image/jpeg;base64,{user_msg['image']}", width=300)
        
        # Generate and display bot response
        with st.chat_message("assistant"):
            steps_taken = []
            if st.session_state.get("current_image_base64"):
                with st.spinner("Analyzing image..."):
                    logger.info("Routing query to Vision Model.")
                    response = get_vision_response(
                        st.session_state.current_image_base64,
                        prompt,
                        system_prompt_vision
                    )
            elif st.session_state.agent:
                with st.spinner("Analyzing query..."):
                    response, steps_taken = get_chat_response(st.session_state.agent, prompt)
                    
                    if steps_taken:
                        with st.expander("🛠️ Agent Actions Details"):
                            for step_dict in steps_taken:
                                st.markdown(f"**Tool Invoked**: `{step_dict['tool']}`")
                                st.markdown(f"**Input**: `{step_dict['tool_input']}`")
                                st.markdown(f"**Result**: *{step_dict['result']}*")
                                st.divider()
            else:
                response = "Agent is not initialized. Please check API keys in `config/config.py`."
            
            st.markdown(response)
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response, "steps": steps_taken})

def main():
    st.set_page_config(
        page_title="Finance AI Assistant",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS Injection for Modern, Responsive UI
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Adapt backgrounds using theme variables */
    .stApp {
        background-color: var(--background-color);
    }
    
    [data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
        border-right: 1px solid rgba(128, 128, 128, 0.1);
    }
    
    /* Modern Glassmorphism-style Chat Bubbles */
    [data-testid="stChatMessage"] {
        background-color: var(--secondary-background-color) !important;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    
    /* Premium Button Styling */
    .stButton>button {
        background-color: #1E3A8A; /* Kept as primary color */
        color: white !important;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .stButton>button:hover {
        background-color: #2563EB;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #1E40AF;
        transform: translateY(-1px);
    }
    
    /* User Input */
    [data-testid="stChatInput"] {
        border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border: 1px solid #E5E7EB;
    }
    
    h1, h2, h3 {
        color: #111827;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if not st.session_state.get("logged_in", False):
        login_page()
        return
        
    # Navigation
    with st.sidebar:
        st.title("Navigation & Settings")
        page = st.radio(
            "Go to:",
            ["Chat", "Instructions"],
            index=0
        )
        
        if page == "Chat":
            st.divider()
            st.subheader("⚙️ Settings")
            response_mode = st.radio(
                "Response Detail Level:",
                ["Concise", "Detailed"],
                index=1
            )
            
            st.divider()
            st.subheader("🔍 Search Interface")
            
            search_mode = st.radio(
                "Select Mode:",
                ["Document Search", "Web Search"],
                index=0,
                help="Document Search ONLY uses uploaded files. Web Search uses live internet data."
            )
            
            # Dynamically re-initialize agent if search mode changed OR response mode changed
            if st.session_state.get("current_search_mode") != search_mode or st.session_state.get("response_mode") != response_mode:
                st.session_state.current_search_mode = search_mode
                st.session_state.response_mode = response_mode
                with st.spinner(f"Switching Agent Context..."):
                    st.session_state.agent = get_finance_agent_executor(mode=search_mode, response_style=response_mode)
            
            st.divider()
            st.subheader("🛠️ Active Agent Tools")
            if search_mode == "Document Search":
                st.markdown("- 📄 **Document Search**\n- 📉 **Live Market Data**\n- 🧮 **EMI/SIP Calculators**\n- 💰 **Budget Planner**\n- 📊 **Tax/Investment Analysis**")
            else:
                st.markdown("- 🌐 **Web Search (Tavily)**\n- 📉 **Live Market Data**\n- 🧮 **EMI/SIP Calculators**\n- 💰 **Budget Planner**\n- 📊 **Tax/Investment Analysis**")
            
            # File Uploaders in Document Search Mode - unified section
            if search_mode == "Document Search":
                st.divider()
                st.subheader("📁 Document & Image Upload")
                
                uploaded_file = st.file_uploader(
                    "Upload Financial Document (PDF)",
                    type=["pdf"],
                    key="pdf_uploader"
                )
                
                if uploaded_file is not None:
                    with st.spinner("Processing Document..."):
                        try:
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                                tmp_file.write(uploaded_file.getvalue())
                                tmp_path = tmp_file.name
                            
                            success, msg = process_and_store_pdf(tmp_path)
                            os.unlink(tmp_path)
                            
                            if success:
                                st.success("✅ Document added to knowledge base.")
                            else:
                                st.error(msg)
                        except Exception as e:
                            logger.error(f"Error handling file upload: {e}")
                            st.error("Failed to process uploaded file.")
                
                uploaded_image = st.file_uploader(
                    "Upload Financial Image (JPG/PNG)",
                    type=["jpg", "jpeg", "png"],
                    key="image_uploader"
                )
                
                if uploaded_image is not None:
                    st.session_state.current_image_base64 = get_base64_of_bin_file(uploaded_image)
                    st.image(uploaded_image, caption="Ready for analysis", use_container_width=True)
                else:
                    st.session_state.current_image_base64 = None
            else:
                # Clear image state when outside Document mode
                st.session_state.current_image_base64 = None
                        
            st.divider()
            st.subheader("📚 Permanent Knowledge Base")
            
            # Sync Knowledge Base on first run
            if "kb_synced" not in st.session_state:
                with st.spinner("Syncing Knowledge Base..."):
                    count, msg = sync_knowledge_base()
                    st.session_state.kb_synced = True
                    if count > 0:
                        st.success(msg)
            
            # Display KB Stats
            kb_files = [f for f in os.listdir(KNOWLEDGE_BASE_DIR) if f.lower().endswith(".pdf")] if os.path.exists(KNOWLEDGE_BASE_DIR) else []
            indexed_count = 0
            if os.path.exists(INDEXED_FILES_TRACKER):
                with open(INDEXED_FILES_TRACKER, "r") as f:
                    indexed_count = len([line for line in f if line.strip()])
            
            st.info(f"📁 **{len(kb_files)}** PDFs in `knowledge_base/` folder.\n\n🔍 **{indexed_count}** documents currently indexed.")
            
            if st.button("🔄 Refresh Library", use_container_width=True):
                with st.spinner("Indexing new documents..."):
                    count, msg = sync_knowledge_base()
                    if count > 0:
                        st.success(msg)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.toast("Library is already up to date!")
            
            st.divider()
            st.subheader("📊 Chat Management")
            
            # Export Chat Feature
            if "messages" in st.session_state and st.session_state.messages:
                chat_text = ""
                for msg in st.session_state.messages:
                    role = "User" if msg["role"] == "user" else "Assistant"
                    chat_text += f"{role}: {msg['content']}\n\n"
                
                st.download_button(
                    label="📥 Export Chat Transcript",
                    data=chat_text,
                    file_name=f"finance_ai_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                if "agent" in st.session_state and st.session_state.agent:
                    st.session_state.agent.memory.clear()
                st.rerun()
            
            st.info("💡 Tip: Use System Settings to toggle between Dark and Light mode for the best visual experience.")
    
    # Route to appropriate page
    if page == "Instructions":
        instructions_page()
    elif page == "Chat":
        chat_page()

if __name__ == "__main__":
    main()
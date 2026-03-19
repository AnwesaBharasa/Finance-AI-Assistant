# 💰 Agentic Finance AI Assistant

A premium, production-level AI Assistant designed for deep financial analysis, tax optimization, and investment planning. Built with a sophisticated RAG (Retrieval-Augmented Generation) system, multi-modal vision capabilities, and a comprehensive suite of deterministic financial tools.

## 🚀 Key Features

### 🧠 Advanced RAG System
- **Library Folder**: Automatic indexing of permanent PDFs placed in the `knowledge_base/` directory.
- **Session Uploads**: Real-time indexing of manually uploaded financial documents.
- **Persistent Memory**: Locally stored FAISS vector store for industrial-grade retrieval accuracy.

### 👁️ Multi-Modal Analysis (Pixtral)
- **Image Intelligence**: Upload screenshots of financial charts, tax forms, or investment statements for instant, context-aware analysis.
- **Vision-to-Insights**: Powered by the advanced Pixtral high-reasoning model.

### 🧮 Deterministic Financial Tools
Integrated with high-precision calculators and tools:
- **Calculators**: EMI, SIP, and Fixed Deposit (FD) calculators with compounding options.
- **Planning**: Dynamic Budget Planner and Investment Recommendation engine.
- **Tax System**: Automated Tax Optimization analyzer.
- **Live Markets**: Real-time stock price tracking and Currency Conversion via `yfinance`.
- **Intelligent Routing**: Automatic switching between `Document Search` (Local context) and `Web Search` (Real-time news).

### 🎨 Premium UI/UX Design
- **Product-Level Styling**: Modern CSS design system featuring Inter and Outfit typography.
- **Interactive Components**: Glassmorphism sidebar, premium chat bubbles, and interactive tool panels.
- **Theme Support**: 100% compatible with both Streamlit Light and Dark modes.

### 🛡️ Secure Access System
- **Triple-Mode Auth**: Restricted access via Admin, Demo (`demo/demo123`), and Guest login.
- **Zero-Hardcode Security**: All credentials managed securely via environment variables (`.env`).

## 🛠️ Tech Stack
- **Framework**: Streamlit (Python)
- **AI Models**: Mistral AI (Small, Pixtral-12B), Tavily Search
- **Orchestration**: LangChain
- **Vector DB**: FAISS
- **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`)

## 🏁 Quick Start

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Installation
```bash
# Clone the repository
git clone <your-repo-link>
cd AI_UseCase

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory and add your API keys:
```text
MISTRAL_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
DEMO_USERNAME=demo
DEMO_PASSWORD=demo123
```

### 4. Run Locally
```bash
streamlit run app.py
```

## 🚢 Deployment
Detailed instructions for **Streamlit Cloud** and **Docker** can be found in the `deployment_guide.md` file within the system-generated artifacts.

---
*Built with ❤️ for NeoStats AI Engineering.*

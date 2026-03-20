# 💰 Agentic Finance AI Assistant

A premium, production-level AI Assistant designed for deep financial analysis, tax optimization, and investment planning. Built with a sophisticated RAG (Retrieval-Augmented Generation) system, multi-modal vision capabilities, and a comprehensive suite of deterministic financial tools.

## 🚀 Key Features

### 🧠 Advanced RAG System
- **Library Folder**: Automatic indexing of permanent PDFs placed in the `knowledge_base/` directory.
- **Session Uploads**: Real-time indexing of manually uploaded financial documents.
- **Persistent Memory**: Locally stored FAISS vector store with enhanced **Summarization Logic** for broad document queries.

### 👁️ Multi-Modal Analysis (Pixtral)
- **Image Intelligence**: Upload screenshots of financial charts, tax forms, or investment statements for instant analysis.
- **Vision-to-Insights**: Powered by the advanced Pixtral high-reasoning model.

### 🧮 Deterministic Financial Tools
- **Calculators**: EMI, SIP, and Fixed Deposit (FD) calculators with compounding options.
- **Planning**: Dynamic Budget Planner and Investment Recommendation engine.
- **Tax System**: Automated Tax Optimization analyzer.
- **Live Markets**: Real-time stock prices (with automated **NSE/BSE Ticker Normalization**) and Currency Conversion via `yfinance`.
- **Intelligent Routing**: Automatic switching between `Document Search` and `Web Search`.

### 🎨 Premium UI/UX Design
- **Product-Level Styling**: Modern CSS design featuring Inter and Outfit typography.
- **Interactive Components**: Glassmorphism sidebar, premium chat bubbles, and centered form layouts.
- **Theme Support**: 100% compatible with both Streamlit Light and Dark modes.

### 🛡️ Secure Access System
- **User Accounts**: Persistent **Sign Up** and **Sign In** system powered by `data.json`.
- **Guest Mode**: Frictionless access to AI features without registration.
- **Zero-Hardcode Security**: All administrative secrets managed via environment variables (`.env`).

## 🛠️ Tech Stack
- **Framework**: Streamlit (Python)
- **AI Models**: Mistral AI (Small, Pixtral-12B), Tavily Search
- **Orchestration**: LangChain
- **Vector DB**: FAISS
- **Database**: JSON-based persistent user storage

## 🏁 Quick Start

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Installation
```bash
git clone <your-repo-link>
cd AI_UseCase
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```text
MISTRAL_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_admin_password
```

### 4. Run Locally
```bash
streamlit run app.py
```

## 🚢 Deployment
Detailed instructions for **Streamlit Cloud** and **Docker** can be found in the `deployment_guide.md` file within the system-generated artifacts.

---
*Built with ❤️ for NeoStats AI Engineering.*

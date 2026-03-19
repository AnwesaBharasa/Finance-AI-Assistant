import os
from dotenv import load_dotenv

# Load env safely
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from models.agent import get_finance_agent_executor

def test():
    print("Testing Agent Executor...")
    agent = get_finance_agent_executor()
    
    queries = [
        "Plan a budget for 100000 monthly income",
        "Calculate EMI for 500000 principal at 8.5% for 10 years."
    ]
    
    for q in queries:
        print(f"\nQuery: {q}")
        try:
            res = agent.invoke({"input": q})
            print(f"Response: {res.get('output')}")
        except Exception as e:
            print(f"Failed to get response: {e}")

if __name__ == '__main__':
    test()

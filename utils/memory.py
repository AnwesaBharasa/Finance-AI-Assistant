from langchain_classic.memory import ConversationBufferMemory

def get_memory():
    """Returns a conversation memory buffer to maintain chat history."""
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True, input_key="input")

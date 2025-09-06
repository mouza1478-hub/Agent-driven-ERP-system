import os
from langchain_community.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOllama
from dotenv import load_dotenv


def get_llm():
    """
    Returns the first available LLM among OpenAI, Gemini, or Ollama.
    Falls back automatically if one fails.
    """

    # ====== OpenAI ======
    try:
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            openai_api_key=OPENAI_API_KEY
        )
        # test call
        llm.invoke("ping")
        print("Using OpenAI GPT")
        return llm
    except Exception as e:
        print("OpenAI not available:", e)

    # ====== Gemini ======
    try:
        GEMINI_API_KEY = "AIzaSyA_01bf0F9ZmkBjIACHGxFedMPYyiamapM"
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key=GEMINI_API_KEY
        )
        llm.invoke("ping")
        print("Using Gemini")
        return llm
    except Exception as e:
        print(" Gemini not available:", e)

    # ====== Ollama (local) ======
    try:
        llm = ChatOllama(
            model="llama2",
            temperature=0.3
        )
        llm.invoke("ping")
        print(" Using Ollama")
        return llm
    except Exception as e:
        print("Ollama not available:", e)

    raise RuntimeError(" No LLM backend available. Please check API keys or Ollama install.")
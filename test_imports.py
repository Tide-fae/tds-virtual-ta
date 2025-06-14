try:
    from fastapi import FastAPI
    from pydantic import BaseModel
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from selenium import webdriver
    print("✅ All imports work!")
except ImportError as e:
    print(f"❌ Failed: {e}")
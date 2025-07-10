---
tags:
  - Smart-Foodsheds
---
# Explanation

- PDF-to-Text Extraction  
- Embedding + Vector Database (ChromaDB + Sentence Transformers)  
- RAG-based Q&A powered by HuggingFace Transformers  
- Feedback system with editable responses and star rating  
- SQLite backend for storing evaluations  
- Streamlit frontend  

---
### **Usage Flow**

1. Select a predefined question or enter a custom one.
2. The chatbot fetches relevant chunks from uploaded documents.
3. The LLM generates a response using those chunks.
4. You can view, edit, rate, and submit feedback.
5. All feedback is stored in `feedback.db`.

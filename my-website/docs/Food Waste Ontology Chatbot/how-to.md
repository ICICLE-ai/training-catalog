---
tags:
  - Smart-Foodsheds
---

# How to Guide

#### **1. Install Dependencies**

Use Python 3.10+. Install dependencies with:

```bash
pip install -r requirements.txt
```

#### **2. HuggingFace Token**

Create a file called `hf_token.txt` in the root directory with your Hugging Face token:

```
your_huggingface_token_here
```

---

#### **3. Place PDF Files**

Put all input PDF files into the `./data/` directory.

---

#### **4. Run the App**

Run the chatbot locally:

```bash
streamlit run app.py
```

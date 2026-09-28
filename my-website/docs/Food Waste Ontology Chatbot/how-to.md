---
tags:
  - Smart-Foodsheds
title: "Food Waste Ontology Chatbot: How to Guide"
sidebar_label: "How to Guide"
pagination_label: "How to Guide"
description: "How to Guide for Food Waste Ontology Chatbot. This project provides an interactive chatbot interface to explore and build structured ontologies for food waste."
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

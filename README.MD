# Multi-PDF RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions based on the content of one or more PDF documents, built with LangChain, Chroma, and Groq.

## Overview

Instead of relying on an LLM's general knowledge, this chatbot retrieves the most relevant sections from your own PDF documents and answers strictly based on that content — reducing hallucination and keeping answers grounded in the source material.

```
PDF files (*.pdf)
        ↓
   Split into chunks
        ↓
   Embed + store in Chroma (vector database)
        ↓
   User question → retrieve top matching chunks
        ↓
   LLM answers based only on retrieved chunks
```

## Features

- Loads **all PDF files** in the project folder automatically (multi-document support)
- Tracks the **source file** for every answer, so you know exactly where information came from
- Refuses to guess: if the answer isn't in the documents, it says so instead of hallucinating
- Persists the vector database locally (`chroma_db/`), so documents aren't re-processed on every run

## Requirements

- Python 3.10+
- A free Groq API key from [Groq Console](https://console.groq.com/keys)

## Installation

```bash
pip install langchain langchain-community langchain-groq chromadb pypdf python-dotenv sentence-transformers
```

## Setup

1. Create a `.env` file in the project folder:
```
GROQ_API_KEY=your_real_api_key_here
```

2. Place any PDF file(s) you want the chatbot to answer questions about in the same folder as `main.py`.

## Running

```bash
python main.py
```

Then type your questions when prompted. Type `exit` to quit.

## Example

```
You: How much does the Growth plan cost?
Bot: The Growth plan costs $99 per month.
[Sources: product_guide.pdf]
```

## Known Limitations

- The embedding model used (`paraphrase-multilingual-MiniLM-L12-v2`) supports multiple languages, but retrieval accuracy is best when the question language matches the document language. Mixed-language setups (e.g. Arabic questions against English-only documents) may occasionally fail to retrieve the right context.
- This is a local prototype — for production use, consider adding authentication, rate limiting, and a persistent hosted vector database.

## Project Structure

```
.
├── main.py            # Core RAG pipeline
├── *.pdf               # Source documents (any number of files)
├── chroma_db/          # Auto-generated vector database (not tracked in git)
├── .env                # API key (not tracked in git)
├── .gitignore
└── README.md
```

## Future Improvements (TODO)

- [ ] Add support for other file types (Word, TXT, web pages)
- [ ] Add a simple web UI instead of terminal-only interaction
- [ ] Add conversation memory for follow-up questions
- [ ] Add source page numbers, not just file names

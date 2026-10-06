# AI RAG Bot

AI RAG Bot is a simple, locally-hosted Retrieval-Augmented Generation (RAG) system built with Python. It allows you to query a knowledge base of your own documents, including text files, PDFs, and images (using OCR). The bot processes these documents, creates vector embeddings, stores them in a local ChromaDB instance, and leverages an LLM via Ollama to generate answers grounded in the retrieved document context.

## Key Features

- **Multi-format Document Support:** Process `.txt`, `.pdf`, `.png`, `.jpg`, and `.jpeg` files.
- **Optical Character Recognition (OCR):** Extracts text from images and PDFs using Tesseract OCR, PyMuPDF, and OpenCV.
- **Smart Chunking:** Cleans and chunks document text to fit context windows efficiently.
- **Local Vector Database:** Uses `chromadb` for persistent, local storage of vector embeddings.
- **Sentence Embeddings:** Utilizes the lightweight and fast `all-MiniLM-L6-v2` model from `sentence-transformers` to generate embeddings.
- **State Tracking:** Keeps track of document modification times and sizes (`document_state.json`) to skip re-processing unmodified files, saving time on startup.
- **Local LLM Integration:** Uses `ollama` with the `phi4-mini:latest` model to generate concise answers grounded in the retrieved context.

## Project Structure

```
AI-RAG-Bot/
├── app.py                   # Main entry point and interactive query loop
├── demo.py                  # Demo script for testing PDF OCR extraction
├── documents/               # Folder to store your knowledge base files
├── generation/
│   └── llm.py               # Generates answers using Ollama
├── processing/
│   ├── chunker.py           # Logic for chunking text into smaller segments
│   ├── cleaner.py           # Cleans raw text (removes extra spaces, newlines)
│   └── ocr.py               # Text extraction from images and PDFs
├── search/
│   └── search.py            # Queries ChromaDB for relevant document chunks
└── vectors/
    ├── embedding.py         # Handles creating sentence embeddings
    └── vector_db.py         # Manages ChromaDB collections and document processing
```

## Prerequisites

Before running the project, make sure you have the following installed:

1. **Python 3.10+**
2. **Tesseract OCR:** 
   - **Windows:** Download and install from [UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki).
   - Ensure the installation path in `processing/ocr.py` matches your system configuration (currently set to `C:\Program Files\Tesseract-OCR\tesseract.exe`).
3. **Ollama:**
   - Install from [ollama.com](https://ollama.com).
   - Once installed, pull the required model:
     ```bash
     ollama pull phi4-mini:latest
     ```

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd AI-RAG-Bot
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Linux/Mac
   venv\Scripts\activate         # On Windows
   ```

3. **Install the Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Required packages include: `chromadb`, `sentence-transformers`, `ollama`, `pymupdf`, `pytesseract`, `opencv-python`, and `numpy`.*

## Usage

1. **Add Documents:**
   Place any text files, PDFs, or images you want to include in your knowledge base into the `documents/` directory.

2. **Run the Bot:**
   Execute the main script to start the bot.
   ```bash
   python app.py
   ```
   
   On the first run (or when new files are added), the bot will process the documents, extract text, create embeddings, and store them in the database.

3. **Ask Questions:**
   Once processing is complete, you will be prompted to ask questions:
   ```
   Ask a question (type 'exit' to quit): What is the main topic of the document?
   ```
   The bot will search for relevant information in your documents and provide an answer. If the information is not found, it will state so clearly.

## How It Works

1. **Extraction:** When you run `app.py`, the system scans the `documents` folder. If new or modified files are detected, it reads them. If they are PDFs or images, it uses OpenCV and Tesseract OCR to extract the text.
2. **Processing:** The extracted text is cleaned of unnecessary whitespace and chunked into smaller segments (default 500 characters per chunk).
3. **Embedding & Storage:** The chunks are converted into numerical vectors using `sentence-transformers` and stored locally in ChromaDB.
4. **Retrieval:** When a user asks a question, the question is also converted to a vector. ChromaDB is queried for the most semantically similar chunks.
5. **Generation:** The retrieved chunks are provided as context to the `phi4-mini` model via Ollama. The model generates a response strictly based on the provided context.

## 👨‍💻 Author

**Sanyam Kansal**
- GitHub: [sanyamkansal](https://github.com/sanyamkansal)

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

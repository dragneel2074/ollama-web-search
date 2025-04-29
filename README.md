# Recipe QA System

A Retrieval-Augmented Generation (RAG) based Question Answering system for recipes. This system uses:
- Sentence Transformers for semantic search
- FAISS for vector storage
- Ollama for LLM
- Jina for web search fallback
- Gradio for the web interface

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Ollama:
- Download and install Ollama from [ollama.ai](https://ollama.ai/)
- Pull the 'qwen2.5:latest' model:
```bash
ollama pull qwen2.5:latest
```

## Usage

1. Start the Ollama server:
```bash
ollama serve
```

2. Include Jina API Key. You can get the api key for free at jina.ai

3. Run the Gradio app:
```bash
python app.py
```

3. Open your browser and navigate to the URL shown in the terminal ( http://127.0.0.1:7860)

## System Architecture

1. **Knowledge Base**: Uses recipes.json as the source of recipes
2. **Embedding Model**: Uses sentence-transformers/all-MiniLM-L6-v2 for text embeddings
3. **Vector Store**: FAISS for efficient similarity search
4. **LLM**: Ollama with qwen2.5:latest model for answer generation
5. **Web Search**: Jina API as fallback when local knowledge is insufficient
6. **UI**: Gradio for user interaction


## To Do
1. ** Implement Caching For Faster Response **
2. ** Implement Better Web Search **
3. ** Test with Different Local Models **
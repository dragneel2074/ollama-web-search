# Recipe QA System - Design Report

## Overview
The Recipe QA System is a Retrieval-Augmented Generation (RAG) system designed to answer questions about recipes using a custom knowledge base. The system combines semantic search with a language model to provide accurate and contextually relevant answers.

## Key Components

### 1. Knowledge Base
- **Data Source**: Custom recipes.json file containing 50 recipes
- **Structure**: Each recipe contains detailed information including ingredients, instructions, prep time, cook time, and other metadata
- **Challenge**: Limited dataset size (50 recipes) requires efficient retrieval and fallback mechanisms

### 2. Retrieval System
- **Embedding Model**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Store**: FAISS for efficient similarity search
- **Design Choice**: Used FAISS for its fast similarity search capabilities and memory efficiency
- **Challenge**: Balancing between search speed and accuracy with limited computational resources

### 3. Language Model Integration
- **Model**: Ollama with qwen2.5:latest
- **Streaming**: Implemented streaming responses for better user experience
- **Design Choice**: Used local Ollama instance for privacy and cost efficiency
- **Challenge**: Managing model response quality and handling uncertainty

### 4. Web Search Fallback
- **Implementation**: Jina web search integration
- **Design Choice**: Added web search as a fallback when:
  - No relevant recipes are found
  - Model responds with uncertainty ("I don't know")
  - System encounters errors
- **Challenge**: Balancing between local knowledge and web search results

## Technical Challenges and Solutions

### 1. Handling Uncertainty
- **Problem**: Model sometimes responds with "I don't know" even when information exists
- **Solution**: 
  - Implemented multiple uncertainty phrase detection
  - Added web search fallback for uncertain responses
  - Combined original and web-enhanced answers for transparency

### 2. Response Quality
- **Problem**: Ensuring consistent and accurate responses
- **Solution**:
  - Structured prompt engineering
  - Context window management
  - Multiple verification steps

### 3. System Reliability
- **Problem**: Handling various failure scenarios
- **Solution**:
  - Comprehensive error handling
  - Multiple fallback mechanisms
  - Detailed logging and debugging

## Design Decisions

### 1. Architecture
- **Choice**: Modular design with separate components for retrieval, generation, and web search
- **Reason**: Allows for easy updates and maintenance of individual components

### 2. User Interface
- **Choice**: Simple Gradio interface
- **Reason**: Quick deployment and easy access for testing

### 3. Response Format
- **Choice**: Combined original and web-enhanced answers
- **Reason**: Provides transparency and allows users to see how web search improved the answer

## Future Improvements

1. **Knowledge Base Expansion**
   - Add more recipes to improve coverage
   - Implement recipe categorization

2. **Enhanced Retrieval**
   - Implement hybrid search (semantic + keyword)
   - Add filtering capabilities

3. **Response Quality**
   - Fine-tune the language model on recipe data
   - Implement answer verification

4. **User Experience**
   - Add recipe visualization
   - Implement conversation history
   - Add recipe recommendations

## Conclusion
The Recipe QA System demonstrates the effective use of RAG architecture for domain-specific question answering. While there are challenges in handling uncertainty and ensuring response quality, the implemented solutions provide a solid foundation for future improvements. The system's modular design and comprehensive fallback mechanisms make it robust and maintainable. 
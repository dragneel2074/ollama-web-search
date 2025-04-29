import gradio as gr
import json
import requests
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict


api_key = ""
print("Loading recipes data...")
# Load recipes data
with open('recipes.json', 'r') as f:
    recipes_data = json.load(f)['recipes']
print(f"Loaded {len(recipes_data)} recipes")

print("Initializing sentence transformer model...")
# Initialize sentence transformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("Model initialized successfully")

print("Creating embeddings for recipes...")
# Create embeddings for recipes
recipe_texts = []
for recipe in recipes_data:
    text = f"{recipe['name']} {recipe['instructions']} {' '.join(recipe['ingredients'])}"
    recipe_texts.append(text)

embeddings = model.encode(recipe_texts)
dimension = embeddings.shape[1]
print(f"Created embeddings with dimension {dimension}")

print("Creating FAISS index...")
# Create FAISS index
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
print("FAISS index created successfully")

def search_recipes(query: str, k: int = 3) -> List[Dict]:
    print(f"Searching for recipes with query: {query}")
    # Encode query
    query_embedding = model.encode([query])[0]
    
    # Search in FAISS index
    distances, indices = index.search(np.array([query_embedding]), k)
    print(f"Found {len(indices[0])} relevant recipes")
    
    # Get relevant recipes
    relevant_recipes = [recipes_data[i] for i in indices[0]]
    return relevant_recipes

def get_web_search_results(query: str) -> str:
    print(f"Performing web search for: {query}")
    url = f"https://s.jina.ai/?q={query}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Respond-With": "no-content"
    }
    try:
        response = requests.get(url, headers=headers)
        print("Web search completed successfully")
        return response.text
    except Exception as e:
        print(f"Error in web search: {str(e)}")
        return f"Error in web search: {str(e)}"

def format_recipe(recipe: Dict) -> str:
    return f"""
Name: {recipe['name']}
Ingredients: {', '.join(recipe['ingredients'])}
Instructions: {' '.join(recipe['instructions'])}
Cuisine: {recipe['cuisine']}
Difficulty: {recipe['difficulty']}
Prep Time: {recipe['prepTimeMinutes']} minutes
Cook Time: {recipe['cookTimeMinutes']} minutes
Servings: {recipe['servings']}
"""

def answer_question(question: str) -> str:
    print(f"\nProcessing question: {question}")
    
    # Search for relevant recipes
    relevant_recipes = search_recipes(question)
    
    if not relevant_recipes:
        print("No relevant recipes found, falling back to web search")
        return "I couldn't find any relevant recipes in the database. Let me search the web..."
    
    # Format context from relevant recipes
    context = "\n\n".join([format_recipe(recipe) for recipe in relevant_recipes])
    print("Context prepared successfully")
    
    # Prepare prompt for Ollama
    prompt = f"""Answer the question using ONLY the context below. If unsure, say "I don't know."

Context:
{context}

Question: {question}

Answer:"""
    
    print("Calling Ollama API...")
    # Call Ollama API with streaming
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:latest",
                "prompt": prompt,
                "stream": True
            },
            stream=True
        )
        response.raise_for_status()
        
        print("Ollama response received, processing stream...")
        answer = ""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode('utf-8'))
                    answer += chunk['response']
                except json.JSONDecodeError:
                    continue
        
        print(f"Initial answer received: {answer}")
        print(f"Checking for 'I don't know' in answer...")
        
        # Check if answer contains "I don't know" (case insensitive)
        if any(phrase in answer.lower() for phrase in ["i don't know", "i do not know", "i'm not sure", "i am not sure"]):
            print("Found uncertainty phrase in answer, initiating web search...")
            web_results = get_web_search_results(question)
            print(f"Web search results: {web_results[:200]}...")  # Print first 200 chars of web results
            
            # Create new prompt with web search results
            web_prompt = f"""Answer the question using the following web search results. If still unsure, say "I don't know."

Web Search Results:
{web_results}

Question: {question}

Answer:"""
            
            print("Calling Ollama API with web search results...")
            web_response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5:latest",
                    "prompt": web_prompt,
                    "stream": True
                },
                stream=True
            )
            web_response.raise_for_status()
            
            print("Processing web-enhanced response...")
            web_answer = ""
            for line in web_response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode('utf-8'))
                        web_answer += chunk['response']
                    except json.JSONDecodeError:
                        continue
            
            print(f"Web-enhanced answer received: {web_answer}")
            
            if any(phrase in web_answer.lower() for phrase in ["i don't know", "i do not know", "i'm not sure", "i am not sure"]):
                print("Still uncertain after web search")
                return f"Original answer: {answer}\n\nAfter web search: {web_answer}"
            else:
                print("Web search provided additional information")
                return f"Original answer: {answer}\n\nAfter web search: {web_answer}"
        else:
            print("No uncertainty found in initial answer")
            return answer
            
    except Exception as e:
        print(f"Error with Ollama: {str(e)}")
        print("Falling back to web search...")
        # If Ollama fails, try web search
        web_results = get_web_search_results(question)
        return f"Error with Ollama: {str(e)}\n\nWeb search results:\n{web_results}"

print("Creating Gradio interface...")
# Create Gradio interface
iface = gr.Interface(
    fn=answer_question,
    inputs=gr.Textbox(label="Ask a question about recipes"),
    outputs=gr.Textbox(label="Answer"),
    title="Recipe QA System",
    description="Ask questions about recipes and get answers using RAG and web search."
)

if __name__ == "__main__":
    print("Starting Gradio server...")
    iface.launch() 
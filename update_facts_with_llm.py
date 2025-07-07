#!/usr/bin/env python3
"""
Update Facts Database with LLM-Generated Facts
Generates high-quality, concise facts using Ollama LLM
"""

import json
import random
import requests
from datetime import datetime
from typing import Dict, List, Any

# LLM Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:8b"

# Fact categories and subcategories based on existing good facts
CATEGORIES = {
    "science": ["space", "biology", "physics", "chemistry", "ocean", "human_body", "weather", "animals"],
    "history": ["medical", "inventions", "war", "royalty", "food", "transportation", "communication", "medicine"],
    "psychology": ["brain", "behavior", "memory", "sleep", "perception", "emotions"],
    "geography": ["countries", "cities", "oceans"],
    "technology": ["internet", "computers", "phones"]
}

VIDEO_THEMES = [
    "luxury cars", "nature", "technology", "city streets", "food cooking", 
    "architecture", "people walking", "abstract patterns", "space", 
    "underwater", "animals"
]

VOICE_TONES = [
    "surprised", "amazed", "baffled", "informative", "mind-blown", "proud",
    "amused", "thoughtful", "wondering", "nostalgic", "impressed", 
    "fascinated", "delighted", "curious", "shocked"
]

def call_ollama(prompt: str) -> str:
    """Call Ollama API and return the response"""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 200
                }
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return None

def generate_fact_prompt(category: str, subcategory: str) -> str:
    """Generate a specific prompt for fact generation"""
    return f"""Generate ONE single, factual, and interesting fact about {category} - specifically {subcategory}.

Requirements:
- Must be absolutely true and verifiable
- Should be surprising or counterintuitive
- Must be under 150 characters when spoken
- Should be engaging for a 15-30 second short video
- No explanations, just the fact itself
- Include a credible source

Format your response as:
FACT: [the fact here]
SOURCE: [credible source]

Example:
FACT: Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.
SOURCE: National Geographic

Now generate a fact about {category} - {subcategory}:"""

def parse_fact_response(response: str) -> Dict[str, str]:
    """Parse the LLM response to extract fact and source"""
    if not response:
        return None
    
    lines = response.strip().split('\n')
    fact = ""
    source = ""
    
    for line in lines:
        line = line.strip()
        if line.startswith("FACT:"):
            fact = line[5:].strip()
        elif line.startswith("SOURCE:"):
            source = line[7:].strip()
    
    if fact and source:
        return {"fact": fact, "source": source}
    return None

def create_fact_entry(fact_data: Dict[str, str], category: str, subcategory: str, next_id: int) -> Dict[str, Any]:
    """Create a complete fact entry"""
    return {
        "id": next_id,
        "category": category,
        "subcategory": subcategory,
        "fact": fact_data["fact"],
        "source": fact_data["source"],
        "video_themes": random.sample(VIDEO_THEMES, 4),
        "voice_tone": random.choice(VOICE_TONES),
        "difficulty": random.choice(["easy", "medium", "hard"]),
        "generated_at": datetime.now().isoformat()
    }

def load_facts_database() -> Dict[str, Any]:
    """Load the current facts database"""
    try:
        with open("fact_database.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("fact_database.json not found!")
        return None

def save_facts_database(data: Dict[str, Any]):
    """Save the updated facts database"""
    with open("fact_database.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_new_facts(num_facts: int = 10):
    """Generate new facts and add them to the database"""
    print(f"Generating {num_facts} new facts using Ollama {MODEL_NAME}...")
    
    # Load current database
    db = load_facts_database()
    if not db:
        return
    
    # Get next ID
    next_id = max(fact["id"] for fact in db["facts"]) + 1
    
    # Track successful generations
    successful_facts = []
    attempts = 0
    max_attempts = num_facts * 3  # Allow some retries
    
    while len(successful_facts) < num_facts and attempts < max_attempts:
        attempts += 1
        
        # Randomly select category and subcategory
        category = random.choice(list(CATEGORIES.keys()))
        subcategory = random.choice(CATEGORIES[category])
        
        print(f"Attempt {attempts}: Generating fact for {category} - {subcategory}...")
        
        # Generate prompt and call LLM
        prompt = generate_fact_prompt(category, subcategory)
        response = call_ollama(prompt)
        
        if not response:
            print("  Failed to get response from LLM")
            continue
        
        # Parse the response
        fact_data = parse_fact_response(response)
        if not fact_data:
            print(f"  Failed to parse response: {response[:100]}...")
            continue
        
        # Validate the fact
        if len(fact_data["fact"]) > 200:  # Too long
            print(f"  Fact too long: {len(fact_data['fact'])} chars")
            continue
        
        if len(fact_data["fact"]) < 20:  # Too short
            print(f"  Fact too short: {len(fact_data['fact'])} chars")
            continue
        
        # Create fact entry
        fact_entry = create_fact_entry(fact_data, category, subcategory, next_id)
        successful_facts.append(fact_entry)
        next_id += 1
        
        print(f"  ✓ Generated: {fact_data['fact'][:50]}...")
        
        # Small delay to be nice to the API
        import time
        time.sleep(1)
    
    if successful_facts:
        # Add new facts to database
        db["facts"].extend(successful_facts)
        
        # Save updated database
        save_facts_database(db)
        print(f"\n✅ Successfully generated {len(successful_facts)} new facts!")
        print(f"Database now contains {len(db['facts'])} total facts.")
        
        # Show some examples
        print("\nNew facts generated:")
        for fact in successful_facts[-3:]:  # Show last 3
            print(f"  • {fact['fact']}")
    else:
        print("❌ Failed to generate any new facts.")

def main():
    """Main function"""
    print("🤖 MoneyPrinterTurbo - LLM Fact Generator")
    print("=" * 50)
    
    # Check if Ollama is running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            print("❌ Ollama is not running or not accessible")
            return
    except:
        print("❌ Cannot connect to Ollama. Make sure it's running on localhost:11434")
        return
    
    # Check if model is available
    try:
        response = requests.get("http://localhost:11434/api/tags")
        models = response.json().get("models", [])
        model_names = [model["name"] for model in models]
        
        if MODEL_NAME not in model_names:
            print(f"❌ Model '{MODEL_NAME}' not found in Ollama")
            print(f"Available models: {', '.join(model_names)}")
            return
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return
    
    print(f"✅ Ollama running with model: {MODEL_NAME}")
    
    # Get number of facts to generate
    try:
        num_facts = int(input("\nHow many new facts to generate? (default: 10): ") or "10")
    except ValueError:
        num_facts = 10
    
    # Generate facts
    generate_new_facts(num_facts)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Bulk Fact Generator for MoneyPrinterTurbo Pipeline
Generate a large batch of facts to use in your video pipeline
"""

from dynamic_fact_generator import DynamicFactGenerator
import json
import time
from datetime import datetime

def generate_facts_bulk(count: int = 50, categories: list = None):
    """
    Generate facts in bulk for the pipeline
    
    Args:
        count: Number of facts to generate
        categories: List of categories to focus on (None for all)
    """
    
    print(f"🚀 Bulk Fact Generator - Generating {count} facts")
    print("=" * 60)
    
    generator = DynamicFactGenerator()
    
    if categories:
        print(f"🎯 Focusing on categories: {', '.join(categories)}")
    else:
        print("🎯 Using all available categories")
    
    # Track progress
    successful = 0
    failed = 0
    start_time = time.time()
    
    for i in range(count):
        print(f"\n--- Generating fact {i+1}/{count} ---")
        
        try:
            if categories:
                # Rotate through specified categories
                category = categories[i % len(categories)]
                fact = generator.generate_single_fact(category)
            else:
                # Use random categories
                fact = generator.generate_single_fact()
            
            successful += 1
            print(f"✅ {fact.fact}")
            print(f"🏷️ {fact.category} - {fact.subcategory}")
            
        except Exception as e:
            failed += 1
            print(f"❌ Failed: {e}")
        
        # Progress update every 10 facts
        if (i + 1) % 10 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            remaining = (count - i - 1) / rate if rate > 0 else 0
            
            print(f"\n📊 Progress: {i+1}/{count} | Success: {successful} | Failed: {failed}")
            print(f"⏱️ Elapsed: {elapsed:.0f}s | Rate: {rate:.1f} facts/min | ETA: {remaining:.0f}s")
        
        # Wait between generations to avoid rate limits
        if i < count - 1:
            time.sleep(3)
    
    # Final statistics
    total_time = time.time() - start_time
    print(f"\n🎉 Bulk generation completed!")
    print(f"📊 Total facts: {count}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"⏱️ Total time: {total_time:.0f}s")
    print(f"📈 Average rate: {count/total_time*60:.1f} facts/min")
    
    # Show final stats
    stats = generator.get_stats()
    print(f"\n📈 Database statistics:")
    print(json.dumps(stats, indent=2))
    
    return successful, failed

def generate_category_facts(category: str, count: int = 10):
    """Generate facts for a specific category"""
    print(f"🎯 Generating {count} facts for category: {category}")
    
    generator = DynamicFactGenerator()
    successful = 0
    
    for i in range(count):
        print(f"\n--- {category} fact {i+1}/{count} ---")
        
        try:
            fact = generator.generate_single_fact(category)
            successful += 1
            print(f"✅ {fact.fact}")
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        if i < count - 1:
            time.sleep(2)
    
    print(f"\n✅ Generated {successful}/{count} facts for {category}")
    return successful

def main():
    """Main function with interactive menu"""
    
    print("🤖 Bulk Fact Generator for MoneyPrinterTurbo")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Generate bulk facts (all categories)")
        print("2. Generate facts for specific category")
        print("3. Generate facts for popular categories")
        print("4. Show database statistics")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            try:
                count = int(input("How many facts to generate? (default 50): ") or "50")
                generate_facts_bulk(count)
            except ValueError:
                print("❌ Please enter a valid number")
        
        elif choice == "2":
            categories = [
                "science", "history", "technology", "psychology", 
                "geography", "biology", "space", "human_body",
                "animals", "nature", "inventions", "culture"
            ]
            
            print("\nAvailable categories:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            
            try:
                cat_choice = int(input("Select category (1-12): ")) - 1
                if 0 <= cat_choice < len(categories):
                    count = int(input("How many facts? (default 10): ") or "10")
                    generate_category_facts(categories[cat_choice], count)
                else:
                    print("❌ Invalid category selection")
            except ValueError:
                print("❌ Please enter a valid number")
        
        elif choice == "3":
            popular_categories = ["science", "technology", "psychology", "space", "animals"]
            count = int(input("How many facts per category? (default 5): ") or "5")
            
            print(f"\n🎯 Generating {count} facts for each popular category...")
            for category in popular_categories:
                generate_category_facts(category, count)
        
        elif choice == "4":
            generator = DynamicFactGenerator()
            stats = generator.get_stats()
            print("\n📊 Database Statistics:")
            print(json.dumps(stats, indent=2))
        
        elif choice == "5":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main() 
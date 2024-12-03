"""Main entry point for the e-commerce assistant application."""

import os
import asyncio
from src.shop_assistant import ShopAssistant

async def main():
    """Run the main application loop."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set OPENAI_API_KEY environment variable")
        
    assistant = ShopAssistant(api_key)
    
    print("E-commerce Assistant (type 'exit' to quit)")
    print("-" * 50)
    
    while True:
        user_message = input("\nYou: ").strip()
        
        if user_message.lower() == 'exit':
            break
            
        try:
            response = await assistant.process_message(user_message)
            print(f"\nAssistant: {response}")
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
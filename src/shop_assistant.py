"""Module containing the shop assistant implementation."""

from typing import Dict, List
import json
from openai import OpenAI
from src.product_catalog import get_product_info, check_stock

class ShopAssistant:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.tools = self._define_tools()
        
    def _define_tools(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_product_info",
                    "description": "Get detailed information about a product",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "product_name": {
                                "type": "string",
                                "description": "Name of the product to look up"
                            }
                        },
                        "required": ["product_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_stock",
                    "description": "Check if a product is in stock",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "product_name": {
                                "type": "string",
                                "description": "Name of the product to check stock for"
                            }
                        },
                        "required": ["product_name"]
                    }
                }
            }
        ]

    def _execute_function(self, function_name: str, arguments: Dict) -> Dict:
        if function_name == "get_product_info":
            result = get_product_info(arguments["product_name"])
        elif function_name == "check_stock":
            result = check_stock(arguments["product_name"])
        else:
            raise ValueError(f"Unknown function: {function_name}")
        return result if result else {"error": "Product not found"}

    async def process_message(self, user_message: str) -> str:
        messages = [{
            "role": "system",
            "content": "You are a helpful e-commerce assistant. Provide concise but complete information about products."
        },
        {
            "role": "user",
            "content": user_message
        }]
        
        # Initial API call
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        
        # If no function calls needed
        if not assistant_message.tool_calls:
            return assistant_message.content
        
        # Handle function calls
        messages.append(assistant_message)
        
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            function_response = self._execute_function(function_name, function_args)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": json.dumps(function_response)
            })
        
        # Get final response
        final_response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        
        return final_response.choices[0].message.content
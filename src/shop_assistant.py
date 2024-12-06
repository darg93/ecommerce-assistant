"""Module containing the shop assistant implementation using OpenAI Assistants API."""

from typing import Dict
import json
from openai import OpenAI
from src.product_catalog import get_product_info, check_stock

class ShopAssistant:
    def __init__(self, api_key: str):
        """Initialize the shop assistant with OpenAI API key."""
        self.client = OpenAI(api_key=api_key)
        self.assistant = self._create_assistant()
        
    def _create_assistant(self):
        """Create an OpenAI Assistant with product-related functions."""
        return self.client.beta.assistants.create(
            name="Shop Assistant",
            instructions="You are a helpful e-commerce assistant. Provide concise but complete information about products.",
            model="gpt-4o",
            tools=[{
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
            }]
        )

    def _execute_function(self, name: str, arguments: Dict) -> Dict:
        """Execute the appropriate function based on the assistant's request."""
        if name == "get_product_info":
            result = get_product_info(arguments["product_name"])
        elif name == "check_stock":
            result = check_stock(arguments["product_name"])
        else:
            raise ValueError(f"Unknown function: {name}")
        return result if result else {"error": "Product not found"}

    async def process_message(self, user_message: str) -> str:
        """Process user message using the assistant and handle any function calls."""
        # Create a new thread for the conversation
        thread = self.client.beta.threads.create()
        
        # Add the user's message to the thread
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )
        
        # Create a run for the assistant
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id
        )
        
        # Wait for the run to complete
        while True:
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            
            if run_status.status == "requires_action":
                tool_outputs = []
                for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    result = self._execute_function(function_name, arguments)
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(result)
                    })
                
                # Submit tool outputs back to the assistant
                run = self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
            
            elif run_status.status == "completed":
                break
            
            elif run_status.status in ["failed", "cancelled", "expired"]:
                raise Exception(f"Run failed with status: {run_status.status}")
        
        # Get the assistant's response
        messages = self.client.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value
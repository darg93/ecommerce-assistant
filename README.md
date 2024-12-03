# E-commerce Assistant

A simple AI-powered e-commerce assistant that can answer questions about products and check stock availability.

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Running the Tests

```bash
python -m pytest
```

## Running the Application

```bash
python -m src.main
```

## Features

- Product information lookup
- Stock availability checking
- Natural language interaction

## Example Usage

```
You: Tell me about the EcoFriendly Water Bottle
Assistant: The EcoFriendly Water Bottle is a sustainable 750ml stainless steel water bottle priced at $24.99. It's currently in stock with 150 units available.

You: Is the Yoga Mat available?
Assistant: Yes, the Yoga Mat is in stock with 100 units available. It's a non-slip exercise yoga mat with carrying strap, priced at $29.99.
```
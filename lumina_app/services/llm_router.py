import os
from litellm import completion

class LLMRouter:
    """
    LLM-agnostic conversational platform wrapper.
    Implements multi-turn memory and context-aware prompt engineering.
    """
    
    def __init__(self, default_model="gpt-3.5-turbo"):
        self.default_model = default_model
        
    def generate_response(self, prompt, chat_history=None, model=None):
        """
        Generates a high-fidelity AI response based on the prompt and history.
        """
        model = model or self.default_model
        messages = [
            {"role": "system", "content": "You are a highly capable AI assistant."}
        ]
        
        if chat_history:
            # chat_history should be a list of dicts with 'role' and 'content'
            messages.extend(chat_history)
            
        messages.append({"role": "user", "content": prompt})
        
        try:
            # using litellm allows us to hot-swap to huggingface, anthropic, azure, etc.
            response = completion(
                model=model,
                messages=messages,
                api_key=os.environ.get("OPENAI_API_KEY", "dummy-key-for-now") # using dummy to avoid breaking local dev if testing
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error connecting to LLM provider: {str(e)}"

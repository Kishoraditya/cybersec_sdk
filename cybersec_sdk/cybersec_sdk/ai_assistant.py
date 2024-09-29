# cybersec_sdk/ai_assistant.py

import openai

class AIAssistant:
    """
    Provides AI-powered assistance using OpenAI's GPT models.
    """

    def __init__(self, api_key: str):
        openai.api_key = "key here"

    def generate_explanation(self, prompt: str) -> str:
        """
        Generates an explanation or summary based on the provided prompt.
        """
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].text.strip()

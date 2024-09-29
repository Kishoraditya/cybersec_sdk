# cybersec_sdk/ai_assistant.py

import openai

class AIAssistant:
    """
    Provides AI-powered assistance using OpenAI's GPT models.
    """

    def __init__(self, api_key: str):
        openai.api_key = "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"

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

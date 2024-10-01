# Copyright [2024] [Kishoraditya]
#
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. 
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/


# cybersec_sdk/ai_assistant.py

import os
import google.generativeai as genai

class AIAssistant:
    """
    Generates explanations for anomalies using the Gemini API.
    """

    def __init__(self):
        genai.configure(api_key=os.environ["API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_explanation(self, prompt: str) -> str:
        """
        Generates an explanation for the given prompt using the Gemini API.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return "An error occurred while generating the explanation."
    
    def generate_behavioral_profile(self, actor_data):
        prompt = f"Generate a behavioral profile for the following actor:\n{actor_data}"
        response = self._call_gemini_api(prompt)
        return response

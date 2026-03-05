from google import genai
from backend.config.settings import settings

class GeminiAgent:

    def __init__(self):

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def ask(self, context, question):

        prompt = f"""
        You are a senior software engineer.

        Project context:
        {context}

        Question:
        {question}
        """

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        return response.text
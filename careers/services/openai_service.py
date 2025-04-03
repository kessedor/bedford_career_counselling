from openai import OpenAI
from django.conf import settings
import time
import logging

logger = logging.getLogger(__name__)

class CareerCounselorAI:
    def __init__(self):
        try:
            logger.debug("Initializing CareerCounselorAI")
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            logger.debug("OpenAI client initialized successfully")
            self.system_prompt = """You are Bedford Career Counselling's AI advisor specifically for Nigerian secondary school students, 
            university undergraduates, and graduates. Your responses should be tailored to the Nigerian educational and career context."""
        except Exception as e:
            logger.error(f"Error initializing CareerCounselorAI: {str(e)}")
            raise

    def get_career_advice(self, message, max_retries=3):
        logger.debug(f"Getting career advice for message: {message[:50]}...")
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            logger.debug("Successfully got response from OpenAI")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API Error: {str(e)}")
            return self.get_fallback_response(message)

    def get_fallback_response(self, message):
        logger.debug("Using fallback response")
        message = message.lower()
        if 'hello' in message:
            return "Hello! I'm Bedford's AI Career Counselor. How can I help you?"
        return "I apologize, but I'm having trouble processing your request. Please try again."

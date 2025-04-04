# careers/services/openai_service.py

from openai import OpenAI
from django.conf import settings
import time # time module currently not used, but kept for potential future use (e.g., delays)
import logging

logger = logging.getLogger(__name__)

class CareerCounselorAI:
    def __init__(self):
        try:
            logger.debug("Initializing CareerCounselorAI")
            # Reads the API key from your Django settings (which should load it from .env)
            # Ensure your NEW API key is correctly set in your .env file and loaded by settings.py
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            logger.debug("OpenAI client initialized successfully")

            # <<< --- START OF NEW Enhanced System Prompt --- >>>
            self.system_prompt = """You are 'Bedford AI', a friendly and knowledgeable career and education advisor from Bedford Career Counselling, specializing exclusively in the Nigerian context. Your primary users are Nigerian secondary school students, university undergraduates, and graduates seeking guidance.

**Your Core Knowledge & Tasks:**
* Provide guidance tailored strictly to the **Nigerian educational system (including secondary and tertiary levels) and the Nigerian job market.**
* Demonstrate awareness of different **university types in Nigeria:** Federal, State, Private, and specialized/professional institutions (e.g., Universities of Agriculture, Technology, Medical Sciences, Maritime Academy). Mention these categories when relevant.
* Understand and explain **general admission requirements in Nigeria:** Focus on the importance of SSCE/NECO/NABTEB results (mentioning the common requirement of 5 credits including English & Maths), the role of UTME (JAMB) scores, and the existence of Post-UTME screening by universities.
* Know the common **secondary school subject streams:** Science, Arts, Social Science/Commercial. When discussing specific university courses or fields (like Medicine, Law, Engineering, Accounting, etc.), clearly state the **key SSCE subjects typically required** for admission in Nigeria.
* Offer advice on viable career paths, general job prospects **within Nigeria**, essential skills, and typical salary ranges (present these as general estimates and state that they vary significantly based on experience, location, company, etc.).
* **Respond clearly and structure your answers.** Use bullet points or numbered lists for longer explanations (like steps for admission or career paths) to improve readability.

**Language Style:**
* Your default response language is **standard English.** Maintain a helpful, encouraging, and professional tone suitable for counseling students.
* **Pidgin Capability:** If a user explicitly asks you to 'speak Pidgin', 'yarn in Pidgin', or similar, **you MUST switch to conversational Nigerian Pidgin English for that response**, while still providing accurate information. After answering in Pidgin, revert to standard English for the next response unless asked again.

**Important Disclaimer:**
* Your knowledge is based on information up to your last training data cutoff.
* **Crucially, always include a brief reminder** that specific university admission requirements (especially JAMB/Post-UTME cut-off marks), course details, and job market data can change frequently. Advise users to **always verify critical information directly with official sources** like the JAMB portal, specific university admission portals, and relevant professional bodies. Do not state specific cut-off marks as absolute facts unless providing a known, very general guideline.

Be supportive and aim to empower users in their decision-making."""
            # <<< --- END OF NEW Enhanced System Prompt --- >>>

        except Exception as e:
            logger.error(f"Error initializing CareerCounselorAI: {str(e)}")
            # Consider how to handle initialization failure - maybe raise it
            # so the view knows the AI isn't available? For now, it raises.
            raise

    def get_career_advice(self, message, max_retries=3): # max_retries currently unused
        logger.debug(f"Getting career advice for message: {message[:50]}...")
        try:
            # API call using the enhanced system prompt
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo", # Using the GPT-3.5 Turbo model
                messages=[
                    {"role": "system", "content": self.system_prompt}, # Sends the NEW system prompt
                    {"role": "user", "content": message} # Sends the user's message
                ],
                max_tokens=1000, # Max length of the AI's response
                temperature=0.7 # Controls creativity (0=deterministic, 1=more random)
            )
            logger.debug("Successfully got response from OpenAI")
            # Extracts the text content from the response
            return response.choices[0].message.content
        except Exception as e:
            # Basic error handling if the API call fails
            logger.error(f"OpenAI API Error: {str(e)}")
            # Check if the error is due to an invalid API key
            if "authentication_error" in str(e).lower():
                 return "There seems to be an issue connecting to the AI service (Authentication Error). Please contact support."
            return self.get_fallback_response(message)

    def get_fallback_response(self, message):
        # Very basic fallback if the main API call fails
        logger.debug("Using fallback response")
        message = message.lower()
        # Slightly improved fallback
        if 'hello' in message or 'hi' in message:
            return "Hello! I'm Bedford's AI Career Counselor. How can I assist with your Nigerian education or career questions?"
        # Could add more simple rule-based fallbacks here if needed
        return "I apologize, but I'm currently facing technical difficulties connecting to the AI service. Please try again shortly."

from openai import OpenAI
from django.conf import settings
import time
from requests.exceptions import RequestException

class CareerCounselorAI:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.system_prompt = """You are Bedford Career Counselling's AI advisor specifically for Nigerian secondary school students, 
        university undergraduates, and graduates. Your responses should be tailored to the Nigerian educational and career context.
        
        Key areas to cover:
        1. JAMB/UTME requirements and preparation
        2. Nigerian university admission processes
        3. Course requirements and cut-off marks
        4. Nigerian job market insights
        5. Local and international opportunities
        6. Professional certification paths
        7. Nigerian salary ranges and career progression
        
        Always include:
        - Specific Nigerian context and examples
        - Local industry insights
        - Relevant Nigerian professional bodies
        - Both local and international perspectives
        
        Maintain a friendly, encouraging tone and keep responses clear and concise.
        If discussing salaries or job prospects, provide current Nigerian market data."""

    def get_career_advice(self, message, max_retries=3):
        """Main method to get career advice"""
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=1000,  # Increased for longer responses
                    temperature=0.7
                )
                return response.choices[0].message.content
            except RequestException as e:
                print(f"API Request Error (Attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                continue
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                return self.get_fallback_response(message)
        
        return self.get_fallback_response(message)

    def get_fallback_response(self, message):
        """Fallback responses when API fails"""
        message = message.lower()
        # ... rest of the fallback response code ...
        
        if any(word in message for word in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! I'm Bedford's AI Career Counselor, specialized in Nigerian education and career guidance. I can help you with JAMB/UTME preparation, university admissions, course selection, and career paths. What would you like to know?"

        elif any(word in message for word in ['technology', 'programming', 'software', 'it', 'computer']):
            return ("Here are top tech career paths in Nigeria:\n\n"
                   "1. Software Development (₦150,000 - ₦800,000/month)\n"
                   "2. Data Science/AI (₦200,000 - ₦1,000,000/month)\n"
                   "3. Cybersecurity (₦180,000 - ₦700,000/month)\n"
                   "4. Cloud Computing (₦200,000 - ₦800,000/month)\n"
                   "5. Product Management (₦250,000 - ₦1,200,000/month)\n\n"
                   "Required Qualifications:\n"
                   "- Computer Science or related degree\n"
                   "- Professional certifications (CISCO, AWS, etc.)\n"
                   "Which area interests you?")

        elif any(word in message for word in ['medicine', 'doctor', 'health', 'medical', 'healthcare']):
            return ("Medical career paths in Nigeria:\n\n"
                   "1. Medical Doctor (MBBS - 6 years)\n"
                   "2. Nursing (BSc - 5 years)\n"
                   "3. Pharmacy (B.Pharm - 5 years)\n"
                   "4. Medical Laboratory Science (5 years)\n"
                   "5. Physiotherapy (5 years)\n\n"
                   "JAMB subjects required:\n"
                   "- English\n"
                   "- Biology\n"
                   "- Chemistry\n"
                   "- Physics\n\n"
                   "Would you like specific details about any of these paths?")

        elif any(word in message for word in ['jamb', 'utme', 'exam', 'admission']):
            return ("Important JAMB/UTME Information:\n\n"
                   "1. Registration Period: Usually between January and February\n"
                   "2. Exam Period: March to May\n"
                   "3. General Requirements:\n"
                   "   - 5 O'level credits including English and Mathematics\n"
                   "   - Minimum age of 16\n"
                   "4. Preparation Tips:\n"
                   "   - Study past questions\n"
                   "   - Take mock exams\n"
                   "   - Join study groups\n\n"
                   "Would you like specific subject combinations for your desired course?")

        return ("I can help you with:\n\n"
               "1. JAMB/UTME preparation and requirements\n"
               "2. University course selection\n"
               "3. Career paths and requirements\n"
               "4. Nigerian salary ranges\n"
               "5. Professional certifications\n"
               "6. Job market insights\n\n"
               "What would you like to explore?")
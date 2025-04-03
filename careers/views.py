from django.views import View
from .models import Career, Category
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
import json
from .services.openai_service import CareerCounselorAI
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class AICounselorView(View):
    template_name = 'careers/ai_counselor.html'

    def get(self, request, *args, **kwargs):
        logger.debug("Handling GET request to ai_counselor")
        try:
            return render(request, self.template_name)
        except Exception as e:
            logger.error(f"Error in GET request: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request, *args, **kwargs):
        logger.debug("Handling POST request to ai_counselor")
        try:
            # Initialize AI service for each request
            logger.debug("About to initialize AI service")
            ai_service = CareerCounselorAI()
            logger.debug("AI service initialized")

            # Parse the request data
            logger.debug("About to parse request body")
            data = json.loads(request.body)
            user_message = data.get('message', '')
            logger.debug(f"Received message: {user_message}")
            
            if not user_message.strip():
                logger.warning("Empty message received")
                return JsonResponse({
                    'error': 'Please provide a message'
                }, status=400)

            # Get AI response
            try:
                logger.debug("Requesting AI response")
                response = ai_service.get_career_advice(user_message)
                logger.debug("Got AI response")
                return JsonResponse({'response': response})
            except Exception as e:
                logger.error(f"AI Service Error: {str(e)}")
                fallback_response = self.get_rule_based_response(user_message.lower())
                return JsonResponse({'response': fallback_response})

        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {str(e)}")
            return JsonResponse({
                'error': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            logger.error(f"Unexpected error in post: {str(e)}")
            return JsonResponse({
                'error': 'An unexpected error occurred'
            }, status=500)

    def get_rule_based_response(self, user_message):
        """Provides fallback responses when AI service fails"""
        if 'hello' in user_message or 'hi' in user_message:
            return "Hello! I'm Bedford's AI Career Counselor. How can I help you today?"
        elif 'jamb' in user_message:
            return "JAMB (Joint Admissions and Matriculation Board) is the examination body for tertiary institutions in Nigeria. Would you like to know about subject combinations, cut-off marks, or registration process?"
        else:
            return "I apologize, but I'm having trouble processing your request. Please try asking about specific topics like JAMB requirements, university admissions, or career paths."

def career_list(request):
    return render(request, 'careers/career_list.html')

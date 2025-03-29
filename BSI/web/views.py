from django.shortcuts import render
import json
import logging
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import CostEstimate, UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import logging
from twilio.rest import Client
from django.conf import settings
def home(request):
    return render(request, 'web/home.html')


def cost(request):
    if not request.user.is_authenticated:
        return redirect(f'/login/?next={request.path}')
    return render(request, 'web/cost.html')


def invoice(request):
    return render(request, 'web/invoice.html')

def login_view(request):
    return render(request, 'web/login.html')
def prosses(request):
    return render(request, 'web/prosses.html')


# web/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CostEstimate

import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CostEstimate

def home(request):
    return render(request, 'web/home.html')



import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CostEstimate

# Configure a logger for this module
logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'web/home.html')




from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import CostEstimate
import json
import logging
from django.urls import reverse

logger = logging.getLogger(__name__)

@csrf_exempt  # For development/testing. Use proper CSRF in production.
def submit_cost_estimate(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.debug("Received submission data: %s", data)

            # Extract data from JSON
            method = data.get('method', '')
            website_type = data.get('websiteType', '')
            technologies = data.get('technologies', [])
            features = data.get('features', [])
            traffic = data.get('traffic', '')
            idea = data.get('idea', '')
            timeline = data.get('timeline', '')
            maintenance = data.get('maintenance', False)
            additional_details = data.get('additionalDetails', {})

            # Convert lists/dicts to JSON strings
            technologies_json = json.dumps(technologies)
            features_json = json.dumps(features)
            additional_details_json = json.dumps(additional_details)

            # Save estimate (without requiring user)
            user = request.user if request.user.is_authenticated else None
            estimate = CostEstimate.objects.create(
                user=user,
                method=method,
                website_type=website_type,
                technologies=technologies_json,
                features=features_json,
                traffic=traffic,
                idea=idea,
                timeline=timeline,
                maintenance=maintenance,
                additional_details=additional_details_json
            )
            logger.info("CostEstimate created with ID: %s", estimate.id)
            return JsonResponse({
                'success': True,
                'estimate_id': estimate.id,
                'redirect_url': reverse('prosses')  # this resolves to '/prosses/'
            })
        except Exception as e:
            logger.error("Error saving cost estimate: %s", str(e), exc_info=True)
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    # If method is not POST
    logger.warning("Invalid request method: %s", request.method)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)





import os
import os
import json
import random
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client  # Remove this if not used elsewhere
from .models import UserProfile

logger = logging.getLogger(__name__)

@csrf_exempt
def auth_user(request):
    """
    POST endpoint to handle authentication.

    Signup (new user): Expects JSON with phone, email, password, firstName, lastName.
      - Uses the phone number as the username.
      - Creates a new User and a corresponding UserProfile.
      - Logs in the new user.

    Login (existing user): Expects JSON with phone and password only.
      - Authenticates using the phone (as username) and password.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone = data.get('phone', '')
            password = data.get('password', '')
            firstName = data.get('firstName')
            lastName = data.get('lastName')
            email = data.get('email', '')

            if firstName and lastName:
                # Signup flow
                if User.objects.filter(username=phone).exists():
                    return JsonResponse({'success': False, 'error': 'User already exists, please login.'})
                user = User.objects.create_user(
                    username=phone,  # Using phone as username
                    email=email,
                    password=password,
                    first_name=firstName,
                    last_name=lastName
                )
                UserProfile.objects.create(user=user, phone=phone)
                login(request, user)
                logger.info("New user signed up: %s", phone)
                return JsonResponse({
                    'success': True,
                    'message': 'Signed up and logged in successfully',
                    'action': 'signup'
                })
            else:
                # Login flow
                user = authenticate(username=phone, password=password)
                if user is not None:
                    login(request, user)
                    logger.info("User logged in: %s", phone)
                    return JsonResponse({
                        'success': True,
                        'message': 'Logged in successfully',
                        'action': 'login'
                    })
                else:
                    logger.error("Login failed for phone: %s", phone)
                    return JsonResponse({'success': False, 'error': 'Invalid phone or password'})
        except Exception as e:
            logger.error("Error in auth_user: %s", str(e), exc_info=True)
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def check_phone(request):
    """
    POST { "phone": "+1234567890" }
    Checks if a phone number exists in the UserProfile model.
    Returns {"exists": True} if found, otherwise {"exists": False}.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone = data.get('phone', '')
            if not phone:
                return JsonResponse({"error": "Phone number is required"}, status=400)
            try:
                UserProfile.objects.get(phone=phone)
                return JsonResponse({"exists": True})
            except UserProfile.DoesNotExist:
                return JsonResponse({"exists": False})
        except Exception as e:
            logger.error("Error in check_phone: %s", str(e), exc_info=True)
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def send_verification_email(request):
    """
    POST { "email": "user@example.com" }
    Generates a random 4-digit code, stores it in the session, and sends it via email using Django's email backend.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            if not email:
                return JsonResponse({"success": False, "error": "Email is required"}, status=400)

            # Generate a random 4-digit code
            code = str(random.randint(1000, 9999))
            # Store the code and email in the session for later verification
            request.session['verification_code'] = code
            request.session['verification_email'] = email

            subject = "Your Verification Code"
            message = f"Your verification code is: {code}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            logger.info("Verification email sent to %s with code %s", email, code)
            return JsonResponse({
                "success": True,
                "message": "Verification code sent via email."
            })
        except Exception as e:
            logger.error("Error in send_verification_email: %s", str(e), exc_info=True)
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

@csrf_exempt
def check_verification_email(request):
    """
    POST { "email": "user@example.com", "code": "1234" }
    Compares the user-provided code with the one stored in the session.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            code = data.get('code')
            if not email or not code:
                return JsonResponse({"success": False, "error": "Email and code are required"}, status=400)

            stored_email = request.session.get('verification_email')
            stored_code = request.session.get('verification_code')
            if stored_email == email and stored_code == code:
                logger.info("Email verification successful for %s", email)
                return JsonResponse({"success": True, "message": "Email verified!"})
            else:
                logger.error("Email verification failed for %s", email)
                return JsonResponse({"success": False, "error": "Invalid or expired code"}, status=400)
        except Exception as e:
            logger.error("Error in check_verification_email: %s", str(e), exc_info=True)
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


# views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def auth_status(request):
    return JsonResponse({'logged_in': request.user.is_authenticated})


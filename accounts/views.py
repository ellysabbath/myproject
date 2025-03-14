from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .serializers import RequestSerializer,AmoSerializer,AmoMipangokaziSerializer,AmoTaarifaSerializer,RegistrationSerializer,MipangokaziHazinaSerializer, ReceiptsPerIndividualSerializer, BankCashReconciliationSerializer, CashBudgetRecordsSerializer
from rest_framework import generics
from .models import Request,Amo,AmoMipangokazi,AmoTaarifa,Registration,MipangokaziHazina,ReceiptsPerIndividual, BankCashReconciliation, CashBudgetRecords
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Tithes
from .serializers import TithesSerializer
from rest_framework.authtoken.models import Token
from .serializers import UserInfoSerializer, CVSerializer, WorkPlanSerializer, FeedbackSerializer,AssetSerializer,UserProfileSerializer
from .models import ElderInfo, CV, WorkPlan, Feedback,Asset,UserProfile


from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import OtpToken
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.mail import send_mail
from django.utils import timezone
import secrets
from django.http import HttpResponse
import logging
import string
from tkinter import *
from tkinter import messagebox
import phonenumbers
import phonenumbers
from phonenumbers import NumberParseException

from twilio.rest import Client  # Twilio to send SMS
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings



# ********************************OTP VERIFICATION******************************************
# Twilio configuration (replace with your actual credentials)
TWILIO_PHONE_NUMBER = '+12766008030'
TWILIO_SID = 'AC380fd733caa676f79347b1ed86b0be0f'
TWILIO_AUTH_TOKEN = 'cbef6c8a3cce29de9593b1526ba2a377'

# Function to generate and send OTP to mobile number via Twilio
# Set up logging to capture errors and debug information
logger = logging.getLogger(__name__)


# validate phone numbers

def validate_phone_number(phone_number):
    try:
        # Parse the phone number with a region code (e.g., "TZ" for Tanzania)
        parsed_number = phonenumbers.parse(phone_number, "TZ")
        
        # Check if the number is valid
        if phonenumbers.is_valid_number(parsed_number):
            return parsed_number
        else:
            raise ValueError("Invalid phone number")
    except NumberParseException:
        raise ValueError("Invalid phone number format")

# validate phone numbers



def send_otp_to_mobile(mobile_number, otp_code):
    try:
        # Ensure phone number is in E.164 format
        parsed_number = phonenumbers.parse(mobile_number, "TZ")  # Replace "TZ" with correct region code
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError(f"Invalid phone number: {mobile_number}")
        
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

        # Log the formatted phone number for debugging
        logger.debug(f"Sending OTP to mobile number: {formatted_number}")

        # Initialize Twilio client
        client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)

        # Send OTP via SMS
        message = client.messages.create(
            body=f"Your OTP is: {otp_code}. It will expire in 5 minutes.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=formatted_number
        )

        # Log the message SID to confirm the message was sent
        logger.debug(f"Message sent successfully. SID: {message.sid}")
        return message.sid  # Return the message SID for tracking if needed

    except Exception as e:
        # Log the error
        logger.error(f"Error sending OTP to mobile number {mobile_number}: {e}")
        raise e

# Function to send OTP to email
def send_otp_to_email(email, otp_code):
    subject = "Email Verification"
    message = f"Hi there,\nHere is your OTP: {otp_code}\nIt expires in 5 minutes."
    sender = "iyumbusda@gmail.com"
    receiver = [email]
    send_mail(subject, message, sender, receiver, fail_silently=False)

# Create your views here.
def index(request):
    return render(request, "index.html")

def SignUp(request):
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! An OTP was sent to your email and mobile number.")

            # Generate OTP (6-digit random number)
            otp_code = ''.join(secrets.choice(string.digits) for _ in range(6))
            
            # Create OTP record for the user
            otp = OtpToken.objects.create(
                user=user,
                otp_code=otp_code,
                otp_expires_at=timezone.now() + timezone.timedelta(minutes=5)
            )

            # Send OTP to user's email
            send_otp_to_email(user.email, otp_code)

            # Send OTP to user's mobile number if available
            if user.mobile_number:
                try:
                    send_otp_to_mobile(user.mobile_number, otp_code)
                except ValueError as e:
                    messages.error(request, str(e))

            return redirect("verify-email", username=user.username)
        else:
            messages.error(request, "There was an error with your form. Please try again.")
    
    context = {"form": form}
    return render(request, "accounts/signup.html", context)


def Verify_email(request, username):
    try:
        user = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("signup")

    user_otp = OtpToken.objects.filter(user=user).last()

    if not user_otp:
        messages.error(request, "No OTP found. Please request a new one.")
        return redirect("resend-otp")

    if request.method == 'POST':
        entered_otp = request.POST.get('otp_code')

        if user_otp.otp_code == entered_otp:
            if user_otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()
                messages.success(request, "Account activated successfully! You can now login.")
                return redirect("Logged_in")
            else:
                messages.warning(request, "The OTP has expired. Please request a new one.")
                return redirect("resend-otp")
        else:
            messages.warning(request, "Invalid OTP. Please try again.")
            return redirect(reverse("verify-email", kwargs={"username": user.username}))

    context = {'username': username, 'otp': user_otp}
    return render(request, "accounts/verify_token.html", context)

def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST.get("otp_email")
        
        try:
            user = get_user_model().objects.get(email=user_email)

            otp_code = ''.join(secrets.choice(string.digits) for _ in range(6))  # Generate new OTP

            otp = OtpToken.objects.create(
                user=user,
                otp_code=otp_code,
                otp_expires_at=timezone.now() + timezone.timedelta(minutes=5)
            )

            # Send OTP via email
            send_otp_to_email(user.email, otp_code)

            # Send OTP via mobile if available
            if user.mobile_number:
                send_otp_to_mobile(user.mobile_number, otp_code)

            messages.success(request, "A new OTP has been sent to your email and mobile number.")
            return redirect("verify-email", username=user.username)

        except get_user_model().DoesNotExist:
            messages.warning(request, "This email doesn't exist in the records.")
            return redirect("resend-otp")

    return render(request, "resend_otp.html")



def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('signin')

# Password reset views (step 1)
def request_reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = get_user_model().objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())

            subject = "Password Reset Request"
            message = render_to_string('accounts/password_reset_email.html', {
                'user': user,
                'uid': uid,
                'token': token,
            })
            send_mail(subject, message, 'no-reply@yourdomain.com', [email], fail_silently=False)
            
            messages.success(request, "Password reset link has been sent to your email.")
            return redirect("Logged_in")
        
        except get_user_model().DoesNotExist:
            messages.error(request, "No account found with that email address.")
            return redirect("request-reset-password")

    return render(request, "accounts/reset_password.html")

def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
        
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password = request.POST.get('new_password')
                user.set_password(new_password)
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect("Logged_in")
            
            return render(request, "accounts/reset_password.html", {'uid': uidb64, 'token': token})
        else:
            messages.error(request, "The password reset link is invalid or has expired.")
            return redirect("Logged_in")
    
    except Exception as e:
        messages.error(request, "There was an error processing your request. Please try again.")
        return redirect("request-reset-password")
    




def send_password_reset_email(user):
    uid = urlsafe_base64_encode(user.pk.encode())
    token = default_token_generator.make_token(user)
    reset_url = f"http://192.168.137.1:8000/accounts/reset-password/{uid}/{token}/"

    subject = "Password Reset Request"
    html_message = render_to_string('password_reset_email.html', {
        'user': user,
        'uid': uid,
        'token': token,
    })
    plain_message = f"Hi {user.username},\n\nWe received a request to reset your password. Please click the link below to reset your password:\n{reset_url}\n\nIf you did not request this, please ignore this email."

    send_mail(
        subject,
        plain_message,
        'iyumbusda@gmail.com',
        [user.email],
        html_message=html_message,
    )



# Your Twilio account SID and Auth token
account_sid = 'AC380fd733caa676f79347b1ed86b0be0f'
auth_token = 'cbef6c8a3cce29de9593b1526ba2a377'

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def send_sms(request):
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body="Your OTP code is 123456",
            from_='+12766008030',  # Your Twilio phone number
            to='+255742578691'  # The recipient's phone number
        )
        
        # After sending the message, fetch the message status
        message_sid = message.sid  # Get the SID of the sent message
        message_status = client.messages(message_sid).fetch().status  # Fetch the message and check its status

        # Log the message status for debugging purposes
        logging.debug(f"Message SID: {message_sid}, Message Status: {message_status}")

        # Respond with the message status
        return HttpResponse(f"Message sent successfully: {message.sid}. Status: {message_status}")

    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return HttpResponse(f"Failed to send message: {e}")
    

    # This view will handle the callback from Twilio
def message_status_callback(request):
    message_sid = request.GET.get('MessageSid')
    message_status = request.GET.get('MessageStatus')
    logging.info(f"Message SID: {message_sid}, Status: {message_status}")

    # You can add your logic here to update your database or notify the user
    # For now, we'll just return a response to acknowledge receipt
    return JsonResponse({'status': 'Received', 'MessageSid': message_sid, 'MessageStatus': message_status})
# *************************8OTP VERIFICATION**********************************************8



# View for login
@api_view(['POST'])
def login_view(request):
    # If the user is already logged in, return a 200 with their token and redirect to the dashboard
    if request.user.is_authenticated:
        token, created = Token.objects.get_or_create(user=request.user)
        print(f"User already authenticated. Token: {token.key}")  # Debugging token when user is authenticated
        return Response({
            'message': 'User already authenticated',
            'access_token': token.key,  # Return the token
            'redirect_url': '/accounts/dashboard/'  # Send the redirect URL to the frontend
        })
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.data)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Create or get the token for the authenticated user
                token, created = Token.objects.get_or_create(user=user)

                # Redirect user to dashboard after successful login
                return Response({
                    'message': 'Login successful',
                    'access_token': token.key,  # Send the token back in the response
                    'redirect_url': '/accounts/dashboard/'  # Specify the URL to redirect to (dashboard page)
                })
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid form data')
    
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/index.html', {'form': form})

# view class for logout
def logout_view(request):
    logout(request)
    return redirect('Logged_in') 


def Password_link(request):
    return render(request, 'accounts/request_reset_password.html')


# page not found

def page_not_found(request, exception):
    return render(request, 'accounts/pages-error-404.html', {})


def Logged_in(request):
    form=AuthenticationForm(request)
    return render(request,'accounts/login.html',{'form':form})

@login_required
def pages_register(request):
    return render(request, 'accounts/registration/pages-register.html')


# sending redirect to dashboard

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

@login_required
def user_profile(request):
    return render(request, 'accounts/registration/users-profile.html')

@login_required
def dashboad(request):
    return render(request, 'accounts/registration/dashboad.html')

@login_required
def amo_view(request):
    return render(request, 'accounts/registration/amo-form.html')


def continue_view(request):
    return render(request, 'accounts/index.html')

@login_required
def washiriki_view(request):
    return render(request, 'accounts/registration/washiriki-wote.html')

@login_required
def chart_view(request):
    return render(request, 'accounts/registration/chart.html')

@login_required
def base_view(request):
    return render(request, 'accounts/base.html')

@login_required
def help_view(request):
    return render(request, 'accounts/registration/help.html')


# displaying forms
@login_required
def dorcas_view(request):
    return render(request, 'accounts/registration/dorkasi-form.html')

@login_required
def huduma_view(request):
    return render(request, 'accounts/registration/huduma-uinjilist.html')

@login_required
def kalendar_view(request):
    return render(request, 'accounts/registration/kanisa-karendar.html')

@login_required
def karani_view(request):
    return render(request, 'accounts/registration/karani-form.html')

@login_required
def kwaya_view(request):
    return render(request, 'accounts/registration/kwaya-form.html')

@login_required
def matoleo_view(request):
    return render(request, 'accounts/registration/matoleo-form.html')

@login_required
def wazee_view_info(request):
    return render(request,'accounts/registration/wazee-view.html')

@login_required
def mhazini_view_info(request):
    return render(request,'accounts/registration/mhazini-view.html')

@login_required
def karani_view_info(request):
    return render(request,'accounts/registration/karani-view.html')

@login_required
def mashemasi_view_info(request):
    return render(request,'accounts/registration/mashemasi-view.html')


@login_required
def vijana_view_info(request):
    return render(request,'accounts/registration/vijana-view.html')


@login_required
def sabato_view_info(request):
    return render(request,'accounts/registration/shule-sabt.html')


@login_required
def kwaya_view_info(request):
    return render(request,'accounts/registration/kwaya-inf.html')


@login_required
def dorasc_view_info(request):
    return render(request,'accounts/registration/dorkas-inf.html')


@login_required
def miradi_view_info(request):
    return render(request,'accounts/registration/mirad-inf.html')

@login_required
def huduma_view_info(request):
    return render(request,'accounts/registration/huduma-inf.html')



@login_required
def matoleo_fill_info(request):
    return render(request,'accounts/registration/matoleo-fill.html')

@login_required
def karendar_view_info(request):
    return render(request,'accounts/registration/karendar-view-inf.html')


@login_required
def mashemasi_view(request):
    return render(request, 'accounts/registration/mashemasi-form.html')

@login_required
def mhazini_view(request):
    return render(request, 'accounts/registration/mhazini-form.html')

@login_required
def miradi_view(request):
    return render(request, 'accounts/registration/miradi-form.html')


@login_required
def ujenzi_view(request):
    return render(request, 'accounts/registration/ujenzi-form.html')


@login_required
def vijana_view(request):
    return render(request, 'accounts/registration/vijana-form.html')

@login_required
def wazee_view(request):
    return render(request, 'accounts/registration/wazee-form.html')

@login_required
def shule_view(request):
    return render(request, 'accounts/registration/shule-sabato-form.html')


def sign_up_view(request):
    return render(request, 'accounts/registration/signUp.html')

@login_required
def Amo_get(request):
    return  render(request, 'accounts/registration/Amo.html')


# handling operations with models

class RequestCreateView(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer



# This view will handle the POST request for the form submission
@api_view(['POST'])
def submit_amo_form(request):
    if request.method == 'POST':
        # Deserialize the incoming data
        serializer = AmoSerializer(data=request.data)
        if serializer.is_valid():
            # Save the valid data into the database
            serializer.save()
            return Response({
                'message': 'Form submitted successfully!',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Invalid data',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    


    # getting all from the dataabase
class AmoListView(APIView):
    def get(self, request, *args, **kwargs):
        # Fetch all records from the Amo model
        amo_forms = Amo.objects.all()
        
        # Serialize the data using AmoSerializer
        serializer = AmoSerializer(amo_forms, many=True)
        
        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AmoMipangokaziListView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request, *args, **kwargs):
        # Fetch all records from AmoMipangokazi model
        records = AmoMipangokazi.objects.all()
        serializer = AmoMipangokaziSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Handle form submission
        serializer = AmoMipangokaziSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
class AmoTaarifaListView(APIView):
    def get(self, request, *args, **kwargs):
        taarifas = AmoTaarifa.objects.all()
        serializer = AmoTaarifaSerializer(taarifas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = AmoTaarifaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RegistrationView(APIView):
    def post(self, request):
        # Handle the submission of the registration form data
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Retrieve all registrations
        registrations = Registration.objects.all()
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)
    
class MipangokaziHazinaCreateView(APIView):
    def post(self, request):
        # You can check if 'cost' is a valid string (if you need to)
        cost = request.data.get('cost', '')
        
        if not cost.isdigit():  # Example validation: ensuring cost is a number as a string
            return Response({"error": "Cost should be a valid number in string format"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MipangokaziHazinaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        # Fetch all the records
        data = MipangokaziHazina.objects.all()
        # Serialize the data
        serializer = MipangokaziHazinaSerializer(data, many=True)
        # Return the serialized data as a response
        return Response(serializer.data, status.HTTP_200_OK)

# ViewSet for ReceiptsPerIndividual
class ReceiptsPerIndividualViewSet(viewsets.ModelViewSet):
    queryset = ReceiptsPerIndividual.objects.all()
    serializer_class = ReceiptsPerIndividualSerializer

# ViewSet for BankCashReconciliation
class BankCashReconciliationViewSet(viewsets.ModelViewSet):
    queryset = BankCashReconciliation.objects.all()
    serializer_class = BankCashReconciliationSerializer

# ViewSet for CashBudgetRecords
class CashBudgetRecordsViewSet(viewsets.ModelViewSet):
    queryset = CashBudgetRecords.objects.all()
    serializer_class = CashBudgetRecordsSerializer

@api_view(['POST'])
def add_tithe(request):
    if request.method == 'POST':
        serializer = TithesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# view info by token



@api_view(['GET'])
def get_user_tithes(request):
    """
    Fetch tithe records of the authenticated user only.
    """
    if request.user.is_authenticated:  # Ensure the user is authenticated
        # Filter the tithe records based on the authenticated user
        tithes = Tithes.objects.filter(username=request.user.username)
        
        # Group the tithes by type (e.g., zaka, sadaka, etc.) using matoleo_type instead of matoleo
        zaka_tithes = tithes.filter(matoleo_type='zaka')
        sadaka_tithes = tithes.filter(matoleo_type='sadaka')
        shukrani_tithes = tithes.filter(matoleo_type='shukrani')
        makambi_tithes = tithes.filter(matoleo_type='makambi')
        robo_tithes = tithes.filter(matoleo_type='robo')
        huduma_tithes = tithes.filter(matoleo_type='huduma')
        majengo_tithes = tithes.filter(matoleo_type='majengo')
        lambi_tithes = tithes.filter(matoleo_type='lambi')
        msamalia_tithes = tithes.filter(matoleo_type='msamalia')

        # Serialize data
        data = {
            "zaka": TithesSerializer(zaka_tithes, many=True).data,
            "sadaka": TithesSerializer(sadaka_tithes, many=True).data,
            "shukrani": TithesSerializer(shukrani_tithes, many=True).data,
            "makambi": TithesSerializer(makambi_tithes, many=True).data,
            "robo": TithesSerializer(robo_tithes, many=True).data,
            "huduma": TithesSerializer(huduma_tithes, many=True).data,
            "majengo": TithesSerializer(majengo_tithes, many=True).data,
            "lambi": TithesSerializer(lambi_tithes, many=True).data,
            "msamalia": TithesSerializer(msamalia_tithes, many=True).data,
        }
        
        # Return the response with serialized data
        return Response(data, status=status.HTTP_200_OK)
    else:
        # If user is not authenticated, return an error response
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)


# API view to create user info
@api_view(['POST'])
def create_user_info(request):
    if request.method == 'POST':
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view to create a CV
@api_view(['POST'])
def create_cv(request):
    if request.method == 'POST':
        serializer = CVSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view to create work plan
@api_view(['POST'])
def create_work_plan(request):
    if request.method == 'POST':
        serializer = WorkPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view to create feedback
@api_view(['POST'])
def create_feedback(request):
    if request.method == 'POST':
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view to retrieve all forms data (optional)
@api_view(['GET'])
def get_all_data(request):
    users = ElderInfo.objects.all()
    feedback = Feedback.objects.all()
    work_plans = WorkPlan.objects.all()
    cvs = CV.objects.all()

    user_serializer = UserInfoSerializer(users, many=True)
    feedback_serializer = FeedbackSerializer(feedback, many=True)
    work_plan_serializer = WorkPlanSerializer(work_plans, many=True)
    cv_serializer = CVSerializer(cvs, many=True)

    return Response({
        'users': user_serializer.data,
        'feedback': feedback_serializer.data,
        'work_plans': work_plan_serializer.data,
        'cvs': cv_serializer.data,
    })


class AssetListAPIView(APIView):
    permission_classes = [IsAuthenticated]  # If needed, require the user to be authenticated

    def get(self, request):
        # Fetch all the asset records from the database
        assets = Asset.objects.all()
        # Serialize the data
        serializer = AssetSerializer(assets, many=True)
        # Return the serialized data as a JSON response
        return Response(serializer.data)
    



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
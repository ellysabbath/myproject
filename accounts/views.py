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




# View for login
@api_view(['POST'])
def login_view(request):
    # If the user is already logged in, return a 200 with their token
    if request.user.is_authenticated:
        token, created = Token.objects.get_or_create(user=request.user)
        print(f"User already authenticated. Token: {token.key}")  # Debugging token when user is authenticated
        return Response({
            'message': 'User already authenticated',
            'access_token': token.key
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

                return Response({
                    'message': 'Login successful',
                    'access_token': token.key  # Send the token back in the response
                })
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid form data')
    
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

# view class for logout
def logout_view(request):
    logout(request)
    return redirect('Logged_in') 


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

@login_required
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

@login_required
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
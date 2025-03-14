from django.db import models
from django.contrib.auth.models import User 




from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import secrets
import phonenumbers
from phonenumbers import phonenumberutil

# Helper function to format the mobile number
def format_mobile_number(mobile_number, region='TZ'):
    try:
        # Parse the mobile number with the specified region (defaulting to 'TZ' for Tanzania)
        phone_number = phonenumbers.parse(mobile_number, region)
        
        if not phonenumbers.is_valid_number(phone_number):
            raise ValueError("Invalid phone number")
        
        # Return the phone number in E.164 format (e.g., +255742575555 for Tanzania)
        return phonenumbers.format_number(phone_number, phonenumberutil.PhoneNumberFormat.E164)
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValueError("Invalid phone number format")

# Custom user model to include email and mobile number
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True, default='')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def clean_mobile_number(self):
        # Format the mobile number before saving it
        if self.mobile_number:
            self.mobile_number = format_mobile_number(self.mobile_number)

# OTP Token model to store OTP information
class OtpToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))  # Modify this later
    tp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username



class Request(models.Model):
    # Full name of the user making the request
    fullname = models.CharField(max_length=100)
    
    # Email of the user
    email = models.EmailField()
    
    # Username of the user
    username = models.CharField(max_length=50, unique=True)
    
    # Optionally, you can add a timestamp to record when the request was made
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fullname} ({self.username})"
    


class Amo(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    username = models.CharField(max_length=100, unique=True)
    date_join = models.DateField()
    date_leave = models.DateField()

    def __str__(self):
        return f"{self.fullname} ({self.username})"    
    

class AmoMipangokazi(models.Model):
    mpangokazi = models.CharField(max_length=255)
    tarehe_ya_kupanga = models.DateField()
    wahusika = models.CharField(max_length=255)
    gharama = models.DecimalField(max_digits=10, decimal_places=2)
    namna = models.TextField()

    def __str__(self):
        return f"{self.mpangokazi} - {self.wahusika}"    
    




class AmoTaarifa(models.Model):
    MPANGOKAZI_CHOICES = [
        ('ulitekelezwa', 'Utekelezwa'),
        ('haukutekelezwa', 'Haukutekelezwa'),
    ]
    
    mpangokazi_done = models.CharField(max_length=255, verbose_name="Mpangokazi")
    ufanisi = models.CharField(max_length=50, choices=MPANGOKAZI_CHOICES, default='ulitekelezwa', verbose_name="Ufanisi")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cost")
    sababu = models.TextField(verbose_name="Sababu za Kufanikiwa au La")
    ushauri = models.TextField(verbose_name="Ushauri/Mapendekezo")

    def __str__(self):
        return f"{self.mpangokazi_done} - {self.ufanisi}"    
    

class Registration(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    username = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    city = models.CharField(max_length=100)
    church = models.CharField(max_length=100)
    baptism_status = models.CharField(max_length=10)
    gender = models.CharField(max_length=6)
    password = models.CharField(max_length=100)
    terms_agreement = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class MipangokaziHazina(models.Model):
    date = models.CharField(max_length=7)
    aim = models.CharField(max_length=255)
    cost = models.CharField(max_length=255)  # Store cost as a string
    experts = models.CharField(max_length=255)
    method = models.TextField()


    def __str__(self):
        return f"Mipango kazi: {self.aim} - {self.date}"

class ReceiptsPerIndividual(models.Model):
    dateindividual = models.DateField()
    username = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    direction = models.CharField(max_length=255)
    confirmationStatus = models.CharField(max_length=50)
    leaderName = models.CharField(max_length=255)

    def __str__(self):
        return f"Receipt: {self.username} - {self.dateindividual}"

class BankCashReconciliation(models.Model):
    dateOfBankTransaction = models.DateField()
    dateOfCashTransaction = models.DateField()
    bankDeposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cashDeposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bankWithdrawal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cashWithdrawals = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reason = models.TextField()

    def __str__(self):
        return f"Bank and Cash: {self.dateOfBankTransaction} - {self.dateOfCashTransaction}"

class CashBudgetRecords(models.Model):
    period = models.CharField(max_length=7)
    incomesource = models.CharField(max_length=255)
    incomeAmount = models.DecimalField(max_digits=10, decimal_places=2)
    expenseCategory = models.CharField(max_length=255)
    expenseAmount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Cash Budget: {self.period} - Income: {self.incomesource}"


# tithes
class Tithes(models.Model):
    full_name = models.CharField(max_length=255)
    date = models.CharField(max_length=20)
    matoleo_type = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    amount = models.CharField(max_length=100)
    direction = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name} - {self.matoleo_type} - {self.amount} Tsh"
    



    # Model for the User Information Form
class ElderInfo(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    username = models.CharField(max_length=255)
    date_join = models.DateField()
    date_leave = models.DateField()

    def __str__(self):
        return self.full_name

# Model for the CV Form
class CV(models.Model):
    user = models.ForeignKey(ElderInfo, related_name='cvs', on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    cv_text = models.TextField()

    def __str__(self):
        return f"CV of {self.username}"

# Model for the Work Plan Form
class WorkPlan(models.Model):
    user = models.ForeignKey(ElderInfo, related_name='work_plans', on_delete=models.CASCADE)
    mpangokazi = models.CharField(max_length=255)
    tarehe_ya_kupanga = models.DateField()
    wahusika = models.CharField(max_length=255)
    gharama = models.DecimalField(max_digits=10, decimal_places=2)
    namna = models.TextField()

    def __str__(self):
        return self.mpangokazi

# Model for the Feedback Form
class Feedback(models.Model):
    user = models.ForeignKey(ElderInfo, related_name='feedbacks', on_delete=models.CASCADE)
    mpangokazi_done = models.CharField(max_length=255)
    ufanisi = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    sababu = models.TextField()
    ushauri = models.TextField()

    def __str__(self):
        return self.mpangokazi_done
    


class Asset(models.Model):
    name = models.CharField(max_length=255)
    total = models.IntegerField()
    abled = models.IntegerField()
    disabled = models.IntegerField()

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference the custom user model
    image = models.ImageField(upload_to='user_images/%Y/%m/%d/', blank=True, null=True)  # Image field
    
    def __str__(self):
        return self.user.username
from django.contrib import admin
from .models import Request, Amo, AmoMipangokazi, AmoTaarifa, UserProfile, Registration, MipangokaziHazina, ReceiptsPerIndividual,CustomUser, BankCashReconciliation, CashBudgetRecords, Tithes, ElderInfo, CV, Asset  # import the Request model


# Register models to be managed by the admin


# accounts/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import RegisterForm  # if you want to use a custom form

# Get the CustomUser model
CustomUser = get_user_model()

# Define a custom admin class for CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    form = RegisterForm  # Optional: You can link your custom form for user creation
    list_display = ('email', 'username', 'mobile_number', 'is_staff', 'is_active')  # Fields you want to display in the list view
    search_fields = ('email', 'username')  # Enable search by email and username
    ordering = ('email',)  # Optional: Order users by email

# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)


# ********************end customadmin*********************
admin.site.register(Request)

admin.site.register(Amo)
admin.site.register(AmoMipangokazi)
admin.site.register(AmoTaarifa)
admin.site.register(ReceiptsPerIndividual)
admin.site.register(Registration)
admin.site.register(MipangokaziHazina)
admin.site.register(CashBudgetRecords)
admin.site.register(BankCashReconciliation)
admin.site.register(Tithes)
admin.site.register(ElderInfo)
admin.site.register(CV)
admin.site.register(Asset)
admin.site.register(UserProfile)



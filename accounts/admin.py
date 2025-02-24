from django.contrib import admin
from .models import Request,Amo,AmoMipangokazi,AmoTaarifa,UserProfile,Registration,MipangokaziHazina,ReceiptsPerIndividual,BankCashReconciliation,CashBudgetRecords,Tithes,ElderInfo,CV,Asset# import the Request model

# Register the Request model to be managed by the admin
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

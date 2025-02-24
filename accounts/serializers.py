from rest_framework import serializers
from .models import Request,Amo,AmoMipangokazi,AmoTaarifa,Registration,MipangokaziHazina, ReceiptsPerIndividual, BankCashReconciliation, CashBudgetRecords,Tithes
from .models import MipangokaziHazina
from .models import ElderInfo, CV, WorkPlan, Feedback,Asset,UserProfile

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['fullname', 'email', 'username']


class AmoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amo
        fields = ['fullname', 'email', 'mobile_number', 'username', 'date_join', 'date_leave']


class AmoMipangokaziSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmoMipangokazi
        fields = ['id', 'mpangokazi', 'tarehe_ya_kupanga', 'wahusika', 'gharama', 'namna']



class AmoTaarifaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmoTaarifa
        fields = ['mpangokazi_done', 'ufanisi', 'cost', 'sababu', 'ushauri']  

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'              


# Ensure your serializer matches the model fields
class MipangokaziHazinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MipangokaziHazina
        fields = ['date', 'aim', 'cost', 'experts', 'method']


class ReceiptsPerIndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptsPerIndividual
        fields = '__all__'

class BankCashReconciliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCashReconciliation
        fields = '__all__'

class CashBudgetRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashBudgetRecords
        fields = '__all__'

class TithesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tithes
        fields = ['full_name', 'date', 'matoleo_type', 'username', 'amount', 'direction']



class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElderInfo
        fields = '__all__'

class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = '__all__'

class WorkPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPlan
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'        


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'name', 'total', 'abled', 'disabled']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['image'] 
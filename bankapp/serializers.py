from rest_framework import serializers
from .models import * 

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank 
        fields = "__all__"
        
class StatementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementType
        fields = "__all__"
        
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountDetails 
        fields = "__all__"
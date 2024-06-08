from expenses.models import CustomUser
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from expenses.models import Expenses
from expenses.models import Income
class UserRegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={"input_type":"password"},write_only=True)
    class Meta:
        model=CustomUser
        fields=["email","password"]
        extra_kwargs={'password':{'write_only':True}}
    def validate_email(self,value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invlaid email format")
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with email already exists")
        return value
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=["email"]
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=["email","password"]        
class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expenses
        fields=["amount","date","description","email"]
class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Income
        fields=["amount","date","description","email"]

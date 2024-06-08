from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import serializers
from .serializer import UserRegistrationSerializer,UserLoginSerializer,UserSerializer,ExpensesSerializer,IncomeSerializer
from rest_framework.permissions import IsAuthenticated
from expenses.models import Expenses,Income
from django.contrib.auth import authenticate
# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(["POST"])
def register_user(request):
    serializer=UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.save()
        token=get_tokens_for_user(user)
        return Response({"token":token,"message":"User Registered successfully"},status=status.HTTP_201_CREATED)
    return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST) 
@api_view(["POST"])
def login_user(request):
    serializers=UserLoginSerializer(data=request.data)
    if serializers.is_valid():
        email=serializers.data.get("email")
        password=serializers.data.get("password")
        user=authenticate(email=email,password=password)
        if user is not None:
            token=get_tokens_for_user(user)
            return Response({"token":token,"message":"Login Success"},status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_user_information(request):
    permission_classes=[IsAuthenticated]
    user=request.user
    serializers=UserSerializer(user)  
    return Response(serializers.data,status=status.HTTP_200_OK)
@api_view(["POST"])
def expenses_request(request):
    permission_classes=[IsAuthenticated]
    serializers=ExpensesSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response({"message":"Expenses amount successfully added"},status=status.HTTP_201_CREATED)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(["POST"])
def income_request(request):
    permission_classes=[IsAuthenticated]
    serializers=IncomeSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response({"message":"Income amount successfully added"},status=status.HTTP_201_CREATED)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(["GET"])

def expenses_summary_request(request):
    permission_classes = [IsAuthenticated]
    expenses = Expenses.objects.filter(email=request.user)
    serializer = ExpensesSerializer(expenses, many=True)
    return Response(serializer.data)
@api_view(["PUT"])
def expenses_summary_request_edit(request,pk):
    expense=Expenses.objects.get(id=pk)
    if expense is None:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = ExpensesSerializer(expense, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"successfully edited"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(["delete"])
def expenses_summary_request_delete(request,pk):
    expense=Expenses.objects.get(id=pk)
    if expense is None:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    expense.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(["GET"])
def income_summary_request(request):
    permission_classes = [IsAuthenticated]
    income = Income.objects.filter(email=request.user)
    serializer = IncomeSerializer(income, many=True)
    return Response(serializer.data)

@api_view(["PUT"])
def income_summary_edit(request,pk):
    permission_classes = [IsAuthenticated]
    income=Income.objects.get(id=pk)
    if income is None:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = IncomeSerializer(income, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"successfully edited"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["delete"])

def income_summary_request_delete(request,pk):
    income=Income.objects.get(id=pk)
    if income is None:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    income.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

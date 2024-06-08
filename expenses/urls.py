from django.contrib import admin
from django.urls import path
from expenses import views
urlpatterns = [
    path("register/",views.register_user),
    path("login/",views.login_user),
    path("info/",views.get_user_information),
    path("expenses/",views.expenses_request),
    path("income/",views.income_request),
    path("expensessummary/",views.expenses_summary_request),
    path("expensessummaryedit/<int:pk>/",views.expenses_summary_request_edit),
    path("expensessummarydelete/int:pk/",views.expenses_summary_request_delete),
    path("incomesummaryedit/<int:pk>",views.income_summary_edit),
    path("incomesummarydelete/<int:pk>",views.income_summary_request_delete)
]
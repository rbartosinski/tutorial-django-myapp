from django.contrib import admin
from django.urls import path, include

from polls import views

urlpatterns = [
    path('', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', views.LoginView.as_view(), name="login"),
    path('accounts/logout/', views.LogoutView.as_view(), name="logout"),
    path('register/', views.RegistrationView.as_view(), name="registration"),
]

from django.urls import path
from account import views
from account.views import  UserLoginView, UserRegistrationView,LogsAPI
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('profile/', UserProfileView.as_view(), name='profile'),
    # path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    # path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    # path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('logs/', views.LogsAPI.as_view()),
    path('logs/<int:pk>', views.LogsAPI.as_view()),
]
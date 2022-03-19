from django.urls import path

from .views import AuthUserAPIView, LogoutAPIView, RegisterView, VerifyEmail, LoginAPIView, RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPIView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('registrar/', RegisterView.as_view(), name='registrar'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('usuario/', AuthUserAPIView.as_view(), name='auth-usuario'),
    path('verificar-email/', VerifyEmail.as_view(), name='verificar-email'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('requisitar-reset-senha/', RequestPasswordResetEmail.as_view(), name='requisitar-reset-senha'),
    path('reset-senha/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='confirmar-reset-senha'),
    path('senha-reset-completo', SetNewPasswordAPIView.as_view(), name='senha-reset-completo'),
] 
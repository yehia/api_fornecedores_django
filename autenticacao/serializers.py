from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.models import Group, Permission

from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'nome', 'username', 'password']

    def validate(self, attrs):
        username = attrs.get('username', ' ')
        
        if not username.isalnum():
            raise serializers.ValidationError('O usuário deve possuir somente caracteres alfanuméricos.')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):

    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255, min_length=3)
    nome = serializers.CharField(max_length=255, min_length=3, read_only=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    
    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'access_token' : user.tokens()['access_token'],
            'refresh_token' : user.tokens()['refresh_token']
        }

    def get_permissions(self, obj):
        groups = Group.objects.filter(user = obj['id'])
        lp = []
        for g in groups:
            permissions = Permission.objects.filter(group = g.id)
            for p in permissions:
                lp.append(p.name)
            

        return {
            'authorizations' : lp,
        }

   

    class Meta:
        model = User
        fields = ['id', 'nome', 'email', 'password', 'username', 'tokens', 'permissions']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        
        if not user:
            raise AuthenticationFailed('Credenciais inválidas, tente novamente.')
        if not user.is_active:
            raise AuthenticationFailed('Usuário inativo, contate o administrador.')
        if not user.is_verified:
            raise AuthenticationFailed('E-mail não verificado.')
        
        return {
            'id' : user.id, 
            'nome' : user.nome,
            'email' : user.email,
            'username' : user.username,
            'tokens' : user.tokens,
        }

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    
        email = serializers.EmailField(min_length=2)

        redirect_url = serializers.CharField(max_length=500, required=False)

        class Meta:
            fields = ['email']      


class SetNewPasswordSerializer(serializers.Serializer):
    
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('O link de reset está inválido.', 401)

            user.set_password(password)
            user.save()
        except Exception as e:
            raise AuthenticationFailed('O link de reset está inválido.', 401)
            
        return super().validate(attrs)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token' : ('Token expirado ou inválido'), 
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')

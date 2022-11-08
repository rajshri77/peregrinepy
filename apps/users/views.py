import logging

from django.db import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password

from apps.users.serializers import RegistartionSerializer, LoginSerializer
from django.core.validators import validate_email
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db import connection
import django.core.exceptions


logger = logging.getLogger(__name__)
cursor = connection.cursor()


class Logout(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == 'POST':
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def registration_view(request):
        if request.method == 'POST':
            serializer = RegistartionSerializer(data=request.data)

            data = {}

            if serializer.is_valid():
                user = serializer.save()

                data['response'] = "Registration Successfully!"
                data['username'] = user.username
                data['email'] = user.email

                refresh = RefreshToken.for_user(user)
                data['token'] = {
                    'access': str(refresh.access_token),
                }
            else:
                data = serializer.errors

            return Response(data)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request):
        """
        Login the user
        """
        try:
            logger.info("Received request to Login User")
            request_data = request.data
            validate_email(request_data["email"])

            validated_data = LoginSerializer(data=request_data)
            if validated_data.is_valid():
                user = User.objects.get(email=request_data["email"])

                if not user:
                    logger.error("Email does not exist")
                    response = {
                        'message':  "User does not exist",
                    }
                    return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                else:
                    if check_password(request_data['password'], user.password):
                        message = "Login successful"
                        token = RefreshToken.for_user(user).access_token

                        response = {
                            'message': message,
                            'token': str(token)
                        }
                        return Response(response, status=status.HTTP_200_OK)

                    else:
                        logger.error("Password does not match")
                        response = {
                            'message': "Password does not match",
                        }
                    return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except django.core.exceptions.ValidationError:
            logger.info("Email not valid")
            response = {
                'message': "email not valid"
            }
            return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except User.DoesNotExist:
            logger.info("User not found")
            response = {
                'message': "User does not exist"
            }
            return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except Exception as error:
            logger.exception(error)
            response = {
                'message': "Request data not valid"
            }
            return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

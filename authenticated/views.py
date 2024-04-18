from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import OutstandingToken
from rest_framework_simplejwt.state import token_backend
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import logout


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    




@api_view(('POST',))
def logout_view(request):
    Rtoken = request.data["refresh"]
    token = RefreshToken(Rtoken)
    token.blacklist()
    logout(request)
    return Response("Successful Logout", status=status.HTTP_200_OK)
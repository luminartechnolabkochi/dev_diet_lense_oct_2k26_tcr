from django.shortcuts import render

# Create your views here.


from rest_framework.generics import CreateAPIView

from diet_app.serializers import UserSerializer


class SignUpView(CreateAPIView):

    serializer_class = UserSerializer

    
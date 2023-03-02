from rest_framework.response import Response
from account.serializer import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class RegisterApi(APIView):
     def post(self, request):
          data = request.data
          serializer = RegisterSerializer(data = data)
          if serializer.is_valid():
               serializer.save()
               return Response({'message' : 'Account created successfully'})
          return Response(serializer.errors)

class Login(APIView):
     def post(self, request):
          data = request.data
          serializer = LoginSerializer(data = data)
          if serializer.is_valid():
               user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
               if not user:
                    return Response('Invalid cred')
               token = RefreshToken.for_user(user)
               print(token)
               return Response({'message': 'login success', 'data' : {'token' : str(token), 'access' : str(token.access_token)}})
          return Response(serializer.errors)
     


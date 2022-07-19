from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import  UserLoginSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework.response import Response
from .models import logs,User
from .serializers import LogsSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import FileUploadParser
# Create your views here.
from django.http import JsonResponse

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class LogsAPI(APIView):
  def get(self, request, pk=None, format=None):
    id = pk
    print(id)
    if id:
      s = User.objects.get(pk=id)   
      stu = logs.objects.filter(pk=s.pk)
      serializer = LogsSerializer(stu,many=True)
      print(type(serializer.data))
      a=[]
      d=[]
      p=[]
      saa=[]
      for i in serializer.data:
            a.append(i['user'])
            d.append(i['logsdetail'])
              
            p.append(i['logfile'])
            
      return Response({"log_detail": d,"user":a,"logfile":p})
    stu = logs.objects.all()
    s = []
    
    
    
    
  #   for i in stu:
  #       s.append(i)
         
    
    serializer = LogsSerializer(stu,many=True)
    print(serializer.data)
    json_data = JSONRenderer().render(serializer.data)
    print(json_data)
    #return Response({"song_title": serializer.data})
    #return Response(json_data)
    l = []
    for i in serializer.data:
          
          l.append(i)
    data={
      "logs_detail":l
    }
        
    return JsonResponse(data,safe=False)
    return Response({"song_title": data})
    
   
  def post(self, request, format=None):
    serializer = LogsSerializer(data=request.data)
    if serializer.is_valid():
     serializer.save()
     return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


  def put(self, request, pk, format=None):
    print("hello put")
    id = pk
    stu = logs.objects.get(pk=id)
    print(stu)
    print(request.data)
    serializer = LogsSerializer(stu, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({'msg':'Complete Data Updated'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    id = pk
    stu = logs.objects.get(pk=id)
    serializer = LogsSerializer(stu, data=request.data, partial=True)
    if serializer.is_valid():
     serializer.save()
    return Response({'msg':'Partial Data Updated'})
    return Response(serializer.errors)

  def delete(self, request, pk, format=None):
    id = pk
    stu = logs.objects.get(pk=id)
    stu.delete()
    return Response({'msg':'Data Deleted'})

# from urllib import request
# from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# from matplotlib.pyplot import install_repl_displayhook
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from betogether.models import User, LearnerProject
from betogether.serializers import UserSerializer, LearnerProjectSerializer
# from rest_framework import permissions, viewsets, authentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

# class LearnerProjectViewSet(viewsets.ModelViewSet):
#     queryset = LearnerProject.objects.all()
#     serializer_class = LearnerProjectSerializer
#     parser_classes = (MultiPartParser, FormParser)
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly] => mess around with permission leave by default idc
    # authentication_classes = [authentication.SessionAuthentication] => make usre they authenticated

#     def perform_create(self, serializer):
#         serializer.save(creator=self.request.user)

# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.response import Response

# class CustomAuthToken(ObtainAuthToken):
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["password"]

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key
#         })

@api_view(["GET","POST","DELETE"])
@permission_classes((IsAuthenticated,))
def learnerProject(req, pk=0):
    author = req.user
    project = LearnerProject(user=author)
    if req.method == "POST":
        serializer = LearnerProjectSerializer(project, data=req.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif req.method == "GET":
        if pk == 0:
            projects = LearnerProject.objects.all() 
            projects_serializer = LearnerProjectSerializer(projects, many=True)
        else:
            projects = LearnerProject.objects.get(id = pk)
            projects_serializer = LearnerProjectSerializer(projects, many=False)
        return JsonResponse(projects_serializer.data, safe=False)
    elif req.method == "DELETE":
        project = LearnerProject.objects.get(id = pk)
        project.delete()
        return JsonResponse("Deleted Successfully", safe=False)
    return JsonResponse("Unknown method", safe=False)

# Create your views here.
@csrf_exempt
def user(req, pk=0):
    if req.method == "GET":
        if pk == 0:
            users = User.objects.all() 
            users_serializer = UserSerializer(users, many=True)
        else:
            users = User.objects.get(id = pk)
            users_serializer = UserSerializer(users, many=False)
        return JsonResponse(users_serializer.data, safe=False)
    elif req.method == "POST":
        user_data = JSONParser().parse(req)
        users_serializer = UserSerializer(data = user_data)
        data = {}
        if users_serializer.is_valid():
            user = users_serializer.save()
            data["response"]    = "Successfully Added To DB"
            data["email"]       = user.email
            data["username"]    = user.username
            token = Token.objects.get(user=user).key
            data['token'] = token
            # return HttpResponse("Successfully Added To DB", None, status=201)
        else:
            data = users_serializer.errors
        return JsonResponse(data)
        # return JsonResponse("Failed to Add", safe=False)
    elif req.method == "PUT":
        user_data = JSONParser().parse(req)
        user = User.objects.get(id = user_data["id"])
        users_serializer = UserSerializer(user, data = user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        else:
            info = users_serializer.errors
            return JsonResponse(info)
        # return JsonResponse("Failed to Update", safe=False)
    elif req.method == "DELETE":
        user = User.objects.get(id = pk)
        user.delete()
        return JsonResponse("Deleted Successfully", safe=False)
    return JsonResponse("Unknown method", safe=False)

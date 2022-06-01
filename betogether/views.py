# from urllib import request
# from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# from matplotlib.pyplot import install_repl_displayhook
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from betogether.models import User, LearnerProject, GroupProject, WishList
from betogether.serializers import UserSerializer, LearnerProjectSerializer, GroupProjectSerializer, WishListSerializer
# from rest_framework import permissions, viewsets, authentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def wishList(req):
    author = req.user
    chosenProject = GroupProject.objects.get(id = req.data["id"])
    project = WishList(user=author, groupProject=chosenProject) 
    if req.method == "POST":
        serializer = WishListSerializer(project, data=req.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
# Create your views here.

@api_view(["GET","POST","DELETE"])
@permission_classes((IsAuthenticated,))
def learnerProject(req, pk=0):
    author = req.user
    chosenProject = GroupProject.objects.get(id = req.data["id"])
    project = LearnerProject(user=author, groupProject=chosenProject)
    print(req.data)
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

@api_view(["GET"])
def groupProject(req):
    if req.method == "GET":
        groupProject = GroupProject.objects.all()
        groupProject_serializer = GroupProjectSerializer(groupProject, many=True)
    return JsonResponse(groupProject_serializer.data, safe=False)

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

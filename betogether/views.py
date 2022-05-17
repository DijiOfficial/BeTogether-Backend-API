from urllib import request
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from matplotlib.pyplot import install_repl_displayhook
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from betogether.models import User, LearnerProject
from betogether.serializers import UserSerializer

# Create your views here.
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
        if users_serializer.is_valid():
            users_serializer.save()
            return HttpResponse("Successfully Added To DB", None, status=201)
        return JsonResponse("Failed to Add", safe=False)
    elif req.method == "PUT":
        user_data = JSONParser().parse(req)
        user = User.objects.get(id = user_data["id"])
        users_serializer = UserSerializer(user, data = user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif req.method == "DELETE":
        user = User.objects.get(id = pk)
        user.delete()
        return JsonResponse("Deleted Successfully", safe=False)

        # listOfUser = []
        # cursor = collection.find()
        # for doc in cursor:
        #     user = doc
        #     id = str(user["_id"])
        #     user["_id"] = id
        #     listOfUser.append(user)
        # data = {"results": listOfUser}
        # data = list(user.values())
        # return JsonResponse(data)
    # emp_rec1 = {
    #     "email" : "fart@whet.com",
    #     "password": "test",
    #     "first_name": "bob",
    #     "last_name": "TheBuilder",
    #     "is_coach" : False,
    #     }
    # collection.insert_one(emp_rec1)

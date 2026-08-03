from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.mongo import user_collection
import bcrypt
import uuid

@api_view(["POST"])
def register(request):
    name= request.data.get("name")
    email=request.data.get("email")
    password=request.data.get("password")
    role=request.data.get("role")

    if user_collection.find_one({"email":email}):
        return Response({"error":"email already exists"},status=400)
    Hashed_password=bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
    user={
        "name":name,
        "email":email,
        "password":Hashed_password,
        "role":role
    }
    user_collection.insert_one(user)
    return Response({"message":"user registered"})
@api_view(['POST'])
def login(request):
    email=request.data.get("email")
    password=request.data.get("password")

    user = user_collection.find_one({"email":email})
    if not user:
        return Response({"error":"Invalid credentials"}, status=400)

    if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return Response({"error":"Invalid credentials"}, status=400)

    token = bcrypt.gensalt().decode("utf-8")
    user_collection.update_one(
        {"_id":user["_id"]},
        {"$set":{"token":token}}
    )
    return Response({
        "message":"Login successful",
        "token":token,
        "role":user["role"]
    })

   


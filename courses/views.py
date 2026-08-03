from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bson import ObjectId
from core.mongo import course_collection




@api_view(["POST"])
def create_courses(request):
    course ={
        "course_name":request.data.get("course_name"),
        "duration":request.data.get("duration"),
        "description":request.data.get("description")
    }
    result = course_collection.insert_one(course)
    return Response({
        "message":"course created",
        "id":str(result.inserted_id)
    })
@api_view(["GET"])
def list_courses(request):
    course = list(course_collection.find())
    for c in course:
        c["_id"]=str(c["_id"])
    return Response(course) 

@api_view(["GET"])
def get_courses(request, id):
    course = course_collection.find_one({"_id":ObjectId(id)})
    if not course:
        return Response({"error":"course not found"},status=404)

    course["_id"]=str(course["_id"])
    return Response(course)

@api_view(["PUT"])
def update_course(request, id):
    course_collection.update_one({"_id":ObjectId(id)},{"$set":request.data})
    return Response({"message":"course updated"})

@api_view(["DELETE"])
def delete_course(request,id):
    course_collection.delete_one({"_id":ObjectId(id)})
    return Response({"message":"course deleted"})


    


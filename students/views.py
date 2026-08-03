from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bson import ObjectId
from auth.utils import require_role
from core.mongo import student_collection

@api_view(["POST"])
@require_role(["admin"])
def create_students(request):
    student={
        "name":request.data.get("name"),
        "email":request.data.get("email"),
        "marks":request.data.get("marks"),
        "profile":{},
        "course_ids":[]
    }
    result=student_collection.insert_one(student)

    return Response({
        "message":"Student inserted",
        "id":str(result.inserted_id)
    })

@api_view(["GET"])
def list_students(request):
    students = list(student_collection.find())
    for s in students:
        s["_id"]=str(s["_id"])
    return Response(students)

@api_view(["GET"])
def get_students(request, id):
    student=student_collection.find_one({"_id":ObjectId(id)})
    if not student:
        return Response({"error":"student not found"},status=404)
    
    student["_id"]=str(student["_id"])
    return Response(student)

@api_view(["PUT"])
def update_student(request,id):
    student_collection.update_one({"_id":ObjectId(id)},{"$set":request.data})
    return Response({"message":"student updated"})

@api_view(["DELETE"])
def delete_student(request,id):
    student_collection.delete_one({"_id":ObjectId(id)})
    return Response({"message":"student deleted"})

@api_view(["POST"])
def assign_course(request, id):
    course_ids = request.data.get("course_id",[])
    object_ids=[ObjectId(cid)for cid in course_ids]

    result=student_collection.update_one(
        {"_id":ObjectId(id)},
        {"$set":{"course_ids":object_ids}}
    )
    if result.matched_count==0:
        return Response({"error":"student not found"},status=404)
    return Response({"message":"courses assigned successfully"})

@api_view(["PUT"])
def add_profile(request, id):
    profile={
        "age":request.data.get("age"),
        "city":request.data.get("city"),
        "phone":request.data.get("phone")
    }
    result=student_collection.update_one(
        {"_id":ObjectId(id)},
        {"$set":{"profile":profile}}
    )

    if result.matched_count == 0:
        return Response({"error":"student not found"},status=404)
    return Response({"message":"profile added"})

@api_view(["GET"])
def single_index(request):
    email =request.GET.get('email')
    result =student_collection.find({"email":email}).explain()
    return Response(result)

@api_view(["GET"])
def multi_key_index(request):
    course_id = request.GET.get("course_id")
    result = student_collection.find({"course_ids":course_id}).explain()
    return Response(result)

@api_view(["GET"])
def compount_index(request):
    email =request.GET.get('email')
    marks = int(request.GET.get("marks"))
    result =student_collection.find({"email":email,"marks":marks}).explain()
    return Response(result)






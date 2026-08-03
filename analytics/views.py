from django.shortcuts import render
from rest_framework.decorators import api_view
from core.mongo import student_collection
from rest_framework.response import Response
import json 
from bson import json_util

#group - combine multiple documents based on a specified key and perform 
@api_view(["GET"])
def top_students(request):
    pipeline=[
        {"$sort":{"marks":-1}},
        {"$limit":2}
    ]
    result = list(student_collection.aggregate(pipeline))
    return Response (json.loads(json_util.dumps(result)))

@api_view(["GET"])
def  average_marks(request):
    pipeline =[
        {
            "$group": {
                "_id":None,
                "avgmarks":{"$avg":"$marks"}
            }
        }
    ]
    
    result =list(student_collection.aggregate(pipeline))
    return Response (result)

@api_view(["GET"])
def student_per_course(request):
    pipeline=[
        {"$unwind":"$course_ids"},
        {
            "$group":{
                "_id":"$course_ids",
                "total_students":{"$sum":1}
            }
        }
    ]
    result = list(student_collection.aggregate(pipeline))
    for r in result:
        r["_id"]=str(r["_id"])
    
    return Response(result)

@api_view(["GET"])
def students_course_details(request):
    pipeline = [
        {
            "$lookup":{
                "from":"courses",
                "localField":"course_ids",
                "foreignField":"_id",
                "as":"course_details"
            }
        }
    ]
    result = list(student_collection.aggregate(pipeline))

    for student in result:
        student["_id"]=str(student["_id"])

        if "course_ids" in student:
            student["course_ids"]=[
                str(cid) for cid in student["course_ids"]
            ]
        
        for course in student.get("course_details",[]):
            course["_id"]=str(course["_id"])

    return Response(result)


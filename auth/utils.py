from functools import wraps
from core.mongo import user_collection
from rest_framework.response import Response

def require_role(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                token = request.data.get("token")
            if not token:
                return Response({"error":"token is required"},status=401)
            user=user_collection.find_one({"token":token})
            if not user["role"] not in allowed_roles:
                return Response({"error":"Access denied"},status=403)
            return view_func(request,*args,**kwargs)
        return wrapper
    return decorator

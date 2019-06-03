from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def print_something(request):
    data = request.POST
    for e in data:
        print(e)
    return JsonResponse({"response": 'OK'})
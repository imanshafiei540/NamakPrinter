from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import win32api, win32print, time

GHOSTSCRIPT_PATH = "C:/Program Files/gs/gs9.27/bin/gswin64.exe"
GSPRINT_PATH = 'C:/Program Files/gs/gsprint/gsprint.exe'
FILE = 'C:/Users/CafeBoard/Desktop/file.html'

@csrf_exempt
def print_something(request):
    currentprinter = 'Cash'
    #win32print.SetDefaultPrinter('NowKitchen')
    #win32api.ShellExecute(0, "print", 'C:/Users/CafeBoard/Desktop/file.pdf', None, ".", 0)
    #params = '-ghostscript "' + GHOSTSCRIPT_PATH + '" -printer "' + currentprinter + '" -copies 1 "C:/Users/CafeBoard/Desktop/file.html "'
    #print(params)
    import os

    os.startfile("C:/Users/CafeBoard/Desktop/file.pdf", "print")
    #win32api.ShellExecute(0, 'open', GSPRINT_PATH, params, 'K', 0)
    time.sleep(1)
    #win32print.SetDefaultPrinter('NowBar')
    #win32api.ShellExecute(0, "print", 'C:/Users/CafeBoard/Desktop/file.html', None, ".", 0)
    time.sleep(1)
    #win32print.SetDefaultPrinter('Cash')

    data = request.POST
    for e in data:
        print(e)
    return JsonResponse({"response": 'OK'})
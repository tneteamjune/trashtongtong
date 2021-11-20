from django.shortcuts import render

def index(request):
    return render(request, 'sun_work/index.html')
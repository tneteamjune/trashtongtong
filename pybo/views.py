from django.shortcuts import render

def index(request):
    return render(request, 'pybo/index.html')
 
def notice(request):
    return render(request, 'pybo/notice.html')

def tip(request):
    return render(request, 'pybo/tip.html')

def mypage(request):
    return render(request, 'pybo/mypage.html')

def greenpoint(request):
    return render(request, 'pybo/greenpoint.html')
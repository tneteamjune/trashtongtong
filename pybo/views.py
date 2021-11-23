from django.shortcuts import render

def index(request):
    return render(request, 'pybo/sun_work/index.html')
 
def notice(request):
    return render(request, 'pybo/sun_work/notice.html')

def tip(request):
    return render(request, 'pybo/sun_work/tip.jsp')

def mypage(request):
    return render(request, 'pybo/sun_work/mypage.html')
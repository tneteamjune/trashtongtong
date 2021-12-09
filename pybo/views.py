from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator  
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from common.models import Profile, PointsEntry, hashUserNo
from common.forms import PointsForm
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.http import HttpResponse

def index(request):
    return render(request, 'pybo/index.html')
 
def tip(request):
    return render(request, 'pybo/tip.html')

def plastic(request):
    return render(request,'pybo/tip/plastic.html')

def glass(request):
    return render(request,'pybo/tip/glass.html')

def balpo(request):
    return render(request,'pybo/tip/balpo.html')

def vinyl(request):
    return render(request,'pybo/tip/vinyl.html')

def camera(request):
    return render(request, 'pybo/camera.html')

# def mypage(request):
#     return render(request, 'pybo/mypage.html')

def greenpoint(request):
    return render(request, 'pybo/greenpoint.html')

def notice(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지

    # 조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)  

@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:notice') #수정
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def mypage(request):
    """
    mypage 구현
    """
    myuser = request.user
    pic_url = ''

    context = {
        'id': myuser.username,
        'email': myuser.email,
        'picture': pic_url,
        }
    return render(request, 'pybo/mypage.html', context=context)

# 포인트 리스트
def points_list(request):
    toplist = []
    users = User.objects.all()
    points = Profile.objects.all().order_by("-greenpoint")
    for i in range(len(points)):
        for j in range(len(users)):
            if points[i].id == users[j].id:
                toplist.append(users[j])
    context = {
        'users' : users,
        'topusers' : toplist[:10]
    }
    return render(request, 'pybo/points_list.html', context)


# 작업중

monthRef = {
    8 : 'August',
    9 : 'September',
    10 : "October",
    11 : "November",
    12 : 'December',
    1 : 'January',
    2 : 'February',
    3 : 'March',
    4 : 'April',
    5 : 'May',
    6 : 'June'
}

def getStatus(v):
    if v < 10:
        return ['inactive', 'text-danger']
    elif v < 20:
        return ['average', 'text-warning']
    elif v < 30:
        return ['good', 'text-info']
    else:
        return ['spectacular', 'text-success']


@login_required(login_url='common:login')
def points_detail(request, id):
    user = User.objects.get(id=id)
    totalPoints = 0
    for users in User.objects.all():
        totalPoints += users.profile.greenpoint
    pointArr = PointsEntry.objects.filter(user=user).order_by('date')
    startMonth = pointArr.first().date.month
    endMonth = pointArr.last().date.month
    if endMonth <= 6:
        endMonth += 12
    lenn = endMonth - startMonth + 1
    points = [0]*lenn
    months = [""]*lenn
    colors = [""]*lenn
    for i in range(lenn):
        for x in pointArr:
            month = x.date.month
            if (month <= 6):
                month += 12
            if (month == startMonth + i):
                points[i] += x.points
        month = startMonth + i
        if (month > 12):
            month -= 12
        months[i] = monthRef[month]
        if points[i] < 10:
            colors[i] = "rgba(255, 99, 132,"
        elif points[i] < 20:
            colors[i] = "rgba(255, 206, 86,"
        elif points[i] < 30:
            colors[i] = "rgba(54, 162, 235,"
        else:
            colors[i] = "rgba(129, 247, 173,"

    avgPoints = (sum(points)/len(points))
    recentPoints = points[-1]
    avgStatus, avgColor = getStatus(avgPoints)[0], getStatus(avgPoints)[1]
    recentStatus, recentColor = getStatus(recentPoints)[0], getStatus(recentPoints)[1]
    avgPoints /= 40
    recentPoints /= 40
    avgPoints *= 100
    recentPoints *= 100

    context = {
        'totalPoints' : totalPoints,
        'user' : user,
        'pointArr' : pointArr,
        'months' : months,
        'points' : points,
        'colors' : colors,
        'avgPoints' : avgPoints,
        'recentPoints' : recentPoints,
        'avgStatus' : avgStatus,
        'recentStatus' : recentStatus,
        'avgColor' : avgColor,
        'recentColor' : recentColor
    }
    print(context)
    return render(request, 'pybo/points_detail.html', context)

def create_user_points(sender, instance, created, **kwargs):
    if created:
        obj = PointsEntry.objects.create(user = instance)
        obj.points = 10
        obj.reason = "welcome point"
        obj.save()

@login_required(login_url='common:login')
def points_get(request, instance):
    if request.method == "POST":
        obj = PointsEntry.objects.create(user = instance)
        obj.user = request.user.id
        obj.points = 10
        obj.reason = "get 10 points!"
        obj.save()
    
    #     if form.is_valid():
    #         formInput = form.cleaned_data
    #         newID = hashUserNo(formInput['username'])
    #         if User.objects.filter(userNo=newID).exists() == False:
    #             newID = hashUserNo(formInput['username'])
    #             newUser = User(userNo=formInput['username'], firstName=(formInput['firstName']).lower(), lastName=(formInput['lastName']).lower(), points=0)
    #             newUser.save()
        
    #     # currentUser = User.objects.filter(userNo=request.user.id).first()

    #     # for object in PointsEntry.objects.filter(user=request.user.id):
    #     #     if object.reason == pointentry.reason :
    #     #         # raise ValidationError(_('Points already added.'))
    #     #         return HttpResponse('Points already added.')

    #         messages.success(request, 'Request submitted succesfully!')
    #         form.save()
    #         form = PointsForm()
    #     # Save the form. Also adds a point entry
    # context = {
    #     'form' : form,
    # }
    return render(request, 'pybo/points_get.html')


def points_entrys(request):
    form = PointsForm(request.POST or None)
    query = request.GET.get('meetingKey')
    if query is not None:
        form.initial['meetingKey'] = query

    # Only do something if the request is post
    if request.method == "POST":
        form = PointsForm(request.POST)
        # Make sure noone is trying to hack us. Can use cleaned_data after calling is_valid
        if form.is_valid():
            # If the meetingkey is not valid then stop the program

            # Get the meetingKey object associated with the meeting key
            data = MeetingKey.objects.filter(meetingKey=form.cleaned_data['meetingKey'])
            if data.exists() == False:
                raise ValidationError(_('Key does not exist.'))
            # Startblock
            # We are going to check if a user exists. If it doesn't then we are going to create one
            formInput = form.cleaned_data
            newID = hashUserNo(formInput['user_ID'])
            if User.objects.filter(userNo=newID).exists() == False:
                newID = hashUserNo(formInput['user_ID'])
                newUser = User(userNo=formInput['user_ID'], firstName=(formInput['firstName']).lower(), lastName=(formInput['lastName']).lower(), points=0)
                newUser.save()
            # EndBlock
            # After creating the user, we will fetch it based on the inputted ID
            currentUser = User.objects.filter(userNo=hashUserNo(form.cleaned_data['user_ID'])).first()

            for object in PointsEntry.objects.filter(user=currentUser):
                if object.meeting == data.first():
                    # raise ValidationError(_('Points already added.'))
                    return HttpResponse('Points already added.')

            messages.success(request, 'Request submitted succesfully!')
            form.save()
            form = PointsForm()
            # Save the form. Also adds a point entry
    context = {
        'form' : form,
    }
    return render(request, 'points/entry.html', context)






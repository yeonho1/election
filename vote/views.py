from django.shortcuts import render, HttpResponse, redirect
from .models import VoteTopic, VoteSelection
from django.contrib.auth import login, authenticate

# Create your views here.
def main(request):
    user = request.user
    loggedin = False
    if user.id is not None:
        loggedin = True
    openVotes = VoteTopic.objects.filter(is_closed=False)
    return render(request, 'vote/main.html', {"openVotes": openVotes, 'user': user, 'log': loggedin})

def createVote(request):
    user = request.user
    loggedin = False
    if user.id is not None:
        loggedin = True
    if request.method == 'POST':
        # Create votes / vote options here
        if not loggedin:
            response = render(request, 'vote/createfail.html', {'reason': '로그인을 해야 투표를 생성할 수 있습니다.'})
            response.status_code = 403
            return response
        try:
            title = request.POST.get('title')
            contents = request.POST.get('content').replace('\n', '<br>')
            optionNames = request.POST.getlist('options[][name]')
            topic = VoteTopic.objects.create(title=title, contents=contents, who_opened=user)
            topic.save()
            for oName in optionNames:
                vs = VoteSelection.objects.create(name=oName, topic=topic)
                vs.save()
        except:
            response = render(request, 'vote/createfail.html', {'reason': '오류가 발생했습니다. 다시 시도해 주세요.', 'user': user, 'log': loggedin})
        return render(request, 'vote/created.html', {'user': user, 'log': loggedin, 'topic': topic})
    else:
        return render(request, 'vote/create.html', {'user': user, 'log': loggedin})

def vote(request, id):
    user = request.user
    if user.id is None:
        response = render(request, 'vote/votefail.html', {'reason': '로그인을 하신 뒤에 투표하여 주세요.'})
        response.status_code = 403
        return response
    loggedin = True
    try:
        sel = VoteSelection.objects.get(id=id)
    except VoteSelection.DoesNotExist:
        response = render(request, 'vote/votefail.html', {'reason': '해당 투표 선택지를 찾을 수 없습니다.', 'user': user, 'log': loggedin})
        response.status_code = 404
        return response
    topic = sel.topic
    voted = []
    for vs in VoteSelection.objects.filter(topic=topic):
        voted += list(vs.votedUsers.all())
    if user in voted:
        return render(request, 'vote/votefail.html', {'reason': '이미 투표한 주제입니다.', 'user': user, 'log': loggedin})
    sel.votedUsers.add(user)
    return render(request, 'vote/vote.html', {'topic': topic, 'sel': sel, 'user': user, 'log': loggedin})

def closevote(request, id):
    user = request.user
    if user.id is None:
        response = render(request, 'vote/closefail.html', {'reason': '로그인을 하신 뒤에 투표를 마감하여 주세요.'})
        response.status_code = 403
        return response
    loggedin = True
    try:
        topic = VoteTopic.objects.get(id=id)
    except VoteTopic.DoesNotExist:
        response = render(request, 'vote/404.html', {})
        response.status_code = 404
        return response
    if user.id != topic.who_opened.id:
        response = render(request, 'vote/closefail.html', {'reason': '투표를 마감할 권한이 없습니다.'})
        response.status_code = 403
        return response
    topic.is_closed = True
    topic.save()
    selections = list(VoteSelection.objects.filter(topic=topic))
    selections = sorted(selections, reverse=True, key=lambda x: x.votedUsers.count())
    return render(request, 'vote/closed.html', {'topic': topic, 'selections': selections, 'user': user, 'log': loggedin})

def viewvote(request, id):
    try:
        topic = VoteTopic.objects.get(id=id)
    except VoteTopic.DoesNotExist:
        response = render(request, 'vote/404.html', {})
        response.status_code = 404
        return response
    selections = VoteSelection.objects.filter(topic=topic)
    voted = 0
    for sel in selections:
        voted += sel.votedUsers.count()
    user = request.user
    loggedin = False
    sel = None
    if user.id is not None:
        loggedin = True
        try:
            sel = selections.get(votedUsers__in=[user])
        except VoteSelection.DoesNotExist:
            sel = None
    return render(request, 'vote/view.html', {'topic': topic, 'selections': selections, 'voted': voted, 'user': user, 'log': loggedin, 'selected': sel})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(nickname=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('votemain')
        else:
            return HttpResponse('로그인에 실패하였습니다. 다시 시도해 주세요.')
    else:
        return render(request, 'vote/login.html', {})
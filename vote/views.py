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

def vote(request, id):
    try:
        sel = VoteSelection.objects.get(id=id)
    except VoteSelection.DoesNotExist:
        return render(request, 'vote/404.html', {})
    user = request.user
    if user.id is not None:
        return HttpResponse('로그인을 하신 뒤에 투표하여 주세요.')
    topic = sel.topic
    voted = []
    for vs in VoteSelection.objects.filter(topic=topic):
        voted += list(vs.votedUsers)
    if user in voted:
        return HttpResponse('이미 투표한 주제입니다.')
    sel.votedUsers.append(user)

def viewvote(request, id):
    user = request.user
    loggedin = False
    if user.id is not None:
        loggedin = True
    try:
        topic = VoteTopic.objects.get(id=id)
    except VoteTopic.DoesNotExist:
        return render(request, 'vote/404.html', {})
    selections = VoteSelection.objects.filter(topic=topic)
    voted = 0
    for sel in selections:
        voted += sel.votedUsers.count()
    return render(request, 'vote/view.html', {'topic': topic, 'selections': selections, 'voted': voted, 'user': user, 'log': loggedin})

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
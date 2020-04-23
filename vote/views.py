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
    user = request.user
    if user.id is None:
        return render(request, 'vote/votefail.html', {'reason': '로그인을 하신 뒤에 투표하여 주세요.'})
    loggedin = True
    try:
        sel = VoteSelection.objects.get(id=id)
    except VoteSelection.DoesNotExist:
        return render(request, 'vote/votefail.html', {'reason': '해당 투표 선택지를 찾을 수 없습니다.', 'user': user, 'log': loggedin})
    topic = sel.topic
    voted = []
    for vs in VoteSelection.objects.filter(topic=topic):
        voted += list(vs.votedUsers.all())
    if user in voted:
        return render(request, 'vote/votefail.html', {'reason': '이미 투표한 주제입니다.', 'user': user, 'log': loggedin})
    sel.votedUsers.add(user)
    return render(request, 'vote/vote.html', {'topic': topic, 'sel': sel, 'user': user, 'log': loggedin})

def viewvote(request, id):
    try:
        topic = VoteTopic.objects.get(id=id)
    except VoteTopic.DoesNotExist:
        return render(request, 'vote/404.html', {})
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
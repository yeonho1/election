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

def viewvote(request, id):
    try:
        topic = VoteTopic.objects.get(id=id)
    except VoteTopic.DoesNotExist:
        return render(request, 'vote/404.html', {})
    selections = VoteSelection.objects.filter(topic=topic)
    voted = 0
    for sel in selections:
        voted += sel.votedUsers.count()
    return render(request, 'vote/view.html', {'topic': topic, 'selections': selections, 'voted': voted})

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
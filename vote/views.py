from django.shortcuts import render
from .models import VoteTopic, VoteSelection

# Create your views here.
def main(request):
    openVotes = VoteTopic.objects.filter(is_closed=False)
    return render(request, 'vote/main.html', {"openVotes": openVotes})

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
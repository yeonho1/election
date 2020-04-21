from django.shortcuts import render
from .models import VoteTopic

# Create your views here.
def main(request):
    openVotes = VoteTopic.objects.filter(is_closed=False)
    return render(request, 'vote/main.html', {"openVotes": openVotes})

def viewvote(request, id):
    try:
        topic = VoteTopic.objects.get(id=id)
    except VoteTopic.DoesNotExist:
        return render(request, 'vote/404.html', {})
    return render(request, 'vote/view.html', {'topic': topic})
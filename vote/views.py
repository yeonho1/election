from django.shortcuts import render
from .models import VoteTopic

# Create your views here.
def main(request):
    openVotes = VoteTopic.objects.filter(is_closed=False)
    return render(request, 'vote/main.html', {"openVotes": openVotes})
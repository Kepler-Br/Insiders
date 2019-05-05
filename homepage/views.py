from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return HttpResponse("<h3>Fuk yea</h3>")


def user_homepage(request, user_id: str):
    return render(request, "homepage/user_homepage.html")

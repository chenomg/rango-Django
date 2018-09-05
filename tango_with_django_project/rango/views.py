from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Rango says hey there partner<p>Click <a href="about/">Here</a> go to about!</p>')


def about(request):
    return HttpResponse('Rango says here is the about page!<p>Click <a href="../">Here</a> back to home!</p>')

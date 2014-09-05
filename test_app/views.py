from django.shortcuts import render

__author__ = 'htm'


def index(request):
    """Home page"""
    return render(request, 'index.html')
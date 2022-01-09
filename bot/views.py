from django.shortcuts import render

from main.main import TelegramGroupMemberAdder

# Create your views here.
def groupAdder(request):
    TelegramGroupMemberAdder()
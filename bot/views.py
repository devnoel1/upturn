from django.shortcuts import render
from pyrogram import session

from main.main import TelegramGroupMemberAdder


# Create your views here.
def groupAdder(request):
    destination_chat = request.POST['destination_chat']
    origin_chat = request.POST['origin_chat']
    operations = request.POST['operations']
    args={}
    session_name = request.POST['session_name']

    TelegramGroupMemberAdder(destination_chat, origin_chat,args,session_name)
from django.shortcuts import render
from pyrogram import session
from dashboard.models import Orders, Service

from main.main import TelegramGroupMemberAdder

# Create your views here.

def bot(request):
    args = {}
    args['page_title'] = 'bot'
    args['services'] =  Orders.objects.filter(user=request.user.id)

    return render(request,'bot.html',args)

def groupAdder(request):
    destination_chat = request.POST['destination_chat']
    origin_chat = request.POST['origin_chat']
    operations = request.POST['operations']
    args={}
    session_name = request.POST['session_name']

    TelegramGroupMemberAdder(destination_chat, origin_chat,args,session_name)

    
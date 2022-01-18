from django.shortcuts import render
from pyrogram import session
from dashboard.models import Orders, Service

from main.main import TelegramGroupMemberAdder

# Create your views here.
def bot(request):
    args = {}
    args['page_title'] = 'bot'

    return render(request,'bot.html',args)

def groupAdder(request):
    args = {}
    args['page_title'] = 'add members to group'
    if request.method == "POST":
        destination_chat = request.POST['destination_chat']
        origin_chat = request.POST['origin_chat']
        operations = request.POST['operations']
        rargs={}
        session_name = request.POST['session_name']

        TelegramGroupMemberAdder(destination_chat, origin_chat,rargs,session_name)
    return render(request,'',args)

def member_auto_joiner(request):
    args = {}
    args['page_title'] = 'members auto joiner'
    return render(request,'member_auto_joiner.html',args)

def bulk_message_sender(request):
    return

def group_message_sender(request):
    return

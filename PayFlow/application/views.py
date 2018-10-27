from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from random import randint
from .sessionsc import Session
current_code=randint(300000,400000)
sessions=[]
webhook_secret='DPH49NT7DAR2D2FFZ99WGLHULWM3MZ7H'
@csrf_exempt
def index(request):

    def generateCode(content,current_code,RECEIVERboc,phone):
        money=str(content.split()[1])
        sessions.append(Session(current_code,RECEIVERboc,int(money),phone))
        fullstr="To get "+money+" euros from your friend, they need to send the code "+current_code+" to the phone number: 99795260"
        return fullstr

    def payment(receiver,sender,amount):
        pass

    if request.POST.get('secret') != webhook_secret:
        fullstr="Invalid webhook secret"+str(request.POST.get('secret'))
        return HttpResponse(fullstr)

    if request.POST.get('event') == 'incoming_message':
        content = request.POST.get('content')
        from_number = request.POST.get('from_number')
        phone_id = request.POST.get('phone_id')


        if content.split()[0]=="gen" and len(content.split()>1): #implement NLP later
            if RECEIVER in registered:
                generateCode(content,current_code,RECEIVERboc,from_number)
            else:
                register(from_number)
                generateCode(content,current_code,RECEIVERboc,from_number)
        elif content.split()[0].isdigit() and len(content.split())==0:
            done=False
            requested_id=int(content.split()[0])
            for session in sessions:
                if session.id==requested_id:
                    done=True
                    if SENDER in registered:
                        payment()
                        pass
                    else:
                        register(from_number)
                        payment()
                        pass

            if done==False:
                fullstr="Invalid ID sent. Please try again."
        else:
            fullstr="Invalid."

        current_code+=2

        return HttpResponse(json.dumps({
            'messages': [
                {'content': fullstr}
            ]
        }), 'application/json')

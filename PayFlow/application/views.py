from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from random import randint

@csrf_exempt
def index(request):
    webhook_secret = 'DPH49NT7DAR2D2FFZ99WGLHULWM3MZ7H'

    if request.POST.get('secret') != webhook_secret:
        fullstr="Invalid webhook secret"+str(request.POST.get('secret'))
        return HttpResponse(fullstr)

    if request.POST.get('event') == 'incoming_message':
        content = request.POST.get('content')
        from_number = request.POST.get('from_number')
        phone_id = request.POST.get('phone_id')


        if content.split()[0]=="gen":
            code=str(randint(100000,999999))

            money=str(content.split()[1])
            fullstr="To send "+money+" euros to your friend, they need to send the code "+code+" to the phone number: 50032"
        else:
            fullstr="Haha bad ways"
        return HttpResponse(json.dumps({
            'messages': [
                {'content': fullstr}
            ]
        }), 'application/json')

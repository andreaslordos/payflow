from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from random import randint
from .sessionsc import Session
from .registration import register
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sessions=[]
webhook_secret='DPH49NT7DAR2D2FFZ99WGLHULWM3MZ7H'
os.chdir("application")

@csrf_exempt
def index(request):
    current_code=randint(300000,400000)
    logging.info(request.POST.get('event'))

    def generateCode(content,current_code,phone):
        '''
        Input:
            content, String
            current_code, Integer
            phone, String
        Output:
            fullstr,String
        '''
        money=str(content.split()[1])
        logging.info("Current code:")
        logging.info(current_code)
        sessions.append(Session(current_code,int(money),phone))
        fullstr="To get "+str(money)+" euros from your friend, they need to send the code "+str(current_code)+" to the phone number: 99795260"
        return fullstr

    def payment(receiver_phone,sender_phone,amount):
        '''
        Input:
            receiver_phone, String
            sender_phone, String
            amount, Float
        Output:
            fullstr,String
        '''
        pass

    def isCurrency(a_str):
        '''
        Input:
            a_str, String
        Output:
            True/False,Bool
        '''
        try:
            if float(a_str)>0:
                return True
        except:
            pass
        return False

    def isRegistered(phone_number):
        '''
        Input:
            phone_number, String
        Output:
            True/False,Bool
        '''
        try:
            with open('users.json') as json_file:
                data = json.load(json_file)
            if phone_number in data:
                return True
        except:
            pass
        return False

    if request.POST.get('event') == '"register"':
        phone=str(request.POST.get('phone'))
        register(request.POST.get('phone'))
        return HttpResponse("Done")
    else:
        logging.info("In here")
        if request.POST.get('secret') != webhook_secret:
            logging.info("Wrong secret, got "+request.POST.get('secret'))
            fullstr="Invalid webhook secret"+str(request.POST.get('secret'))
            return HttpResponse(fullstr)
        logging.info("Secret verified")
        if request.POST.get('event') == 'incoming_message':
            logging.info("Incoming message")
            content = request.POST.get('content')
            from_number = request.POST.get('from_number')
            phone_id = request.POST.get('phone_id')
            logging.info("Content: "+content)
            if content.split()[0]=="gen" and isCurrency(content.split()[1]): #implement NLP later
                if isRegistered(from_number):
                    fullstr=generateCode(content,current_code,from_number)
                else:
                    logging.info(os.getcwd())
                    register(from_number)
                    fullstr=generateCode(content,current_code,from_number)
            elif content.split()[0].isdigit() and len(content.split())==0:
                done=False
                requested_id=int(content.split()[0])
                for session in sessions:
                    if session.id==requested_id:
                        done=True
                        if isRegistered(from_number):
                            #payment()
                            pass
                        else:
                            register(from_number)
                            #payment()
                            pass
                if done==False:
                    fullstr="Invalid ID sent. Please try again."
            else:
                fullstr="Invalid."


            return HttpResponse(json.dumps({
                'messages': [
                    {'content': fullstr}
                ]
            }), 'application/json')

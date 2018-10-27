'''
authors:
    Andreas Lordos (17, English School of Nicosia)
    Christos Falas(16, English School of Nicosia)
'''
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from random import randint
from .sessionsc import Session
from .registration import register
import logging
import os

sessions=[]
logging.basicConfig(level=logging.INFO) #sets up logging module
logger = logging.getLogger(__name__)

webhook_secret='DPH49NT7DAR2D2FFZ99WGLHULWM3MZ7H'
os.chdir("application") #to be in the same dir as users.json

@csrf_exempt
def index(request):
    global sessions
    logging.info(sessions)
    current_code=randint(300000,999999) #generate code for session that will be used to verify receiver and sender
    #However, current_code would be implemented in a way that guarantees there will not be a collision if this was deployed in the real world
    logging.info(request.POST.get('event'))

    def generateCode(sessions,content,current_code,phone):
        '''
        Input:
            content, String
            current_code, Integer
            phone, String
        Output:
            fullstr,String
        '''
        money=str(content.split()[1]) #Get the amount that the receiver wants to receive from sender
        logging.info("Current code:")
        logging.info(current_code)
        sessions.append(Session(current_code,int(money),phone)) #Create a new Session instance, add it to the array of current sessions
        fullstr="To get "+str(money)+" euros from your friend, they need to send the code "+str(current_code)+" to the phone number: 99795260" #This is what will be returned to the user
        return sessions,fullstr

    def payment(receiver_phone,sender_phone,amount):
        '''
        Input:
            receiver_phone, String
            sender_phone, String
            amount, Float
        Output:
            fullstr,String
        '''
        return

    def isCurrency(a_str):
        '''
        Input:
            a_str, String
        Output:
            True/False,Bool
        '''
        try:
            if float(a_str)>0: #If it's a float or integer in the form of a string, this operation will work
                return True
        except: #if the above operations raises an error, return False
            pass
        return False #edge case if a_str is a number less than or equal to 0

    def isRegistered(phone_number):
        '''
        Input:
            phone_number, String
        Output:
            True/False,Bool
        '''
        try:
            with open('users.json') as json_file: #open users.json file
                data = json.load(json_file) #load data from file
            if phone_number in data: #if phone number already in records
                return True #user is registered, so return True
        except:
            pass
        return False #user not registered, return False

    if request.POST.get('event') == '"register"': #
        phone=str(request.POST.get('phone'))
        register(request.POST.get('phone'))
        return HttpResponse("Done")
    else:
        logging.info("Not registering")
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
                if not isRegistered(from_number):
                    logging.info(os.getcwd())
                    register(from_number)
                try:
                    sessions,fullstr=generateCode(sessions,content,current_code,from_number)
                except:
                    sessions=[]
                    sessions,fullstr=generateCode(sessions,content,current_code,from_number)
            elif content.split()[0].isdigit() and len(content.split())==1:
                done=False
                requested_id=int(content.split()[0])
                for session in sessions:
                    if session.id==requested_id:
                        done=True
                        if not isRegistered(from_number):
                            register(from_number)
                        payment(session.receiver,session.sender,session.amount)
                        sessions.remove(session)
                        fullstr="Transaction complete."
                if done==False:
                    fullstr="Invalid ID sent. Please try again."
            else:
                fullstr="Invalid."
            logging.info(str(sessions))
            return HttpResponse(json.dumps({
                'messages': [
                    {'content': fullstr}
                ]
            }), 'application/json')

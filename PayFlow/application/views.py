'''
authors:
    Andreas Lordos (17, The English School of Nicosia)
    Christos Falas (15, The English School of Nicosia)
'''
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from math import floor,log10
from random import randint
from .sessionsc import Session
from .registration import register
from .nlp import determineAction
import logging
import os
import nltk

MONEY_CAP=100
sessions=[]
logging.basicConfig(level=logging.INFO) #sets up logging module
logger = logging.getLogger(__name__)

webhook_secret='DPH49NT7DAR2D2FFZ99WGLHULWM3MZ7H'
os.chdir("application") #to be in the same dir as users.json

@csrf_exempt
def index(request):
    messages={'messages':[]}
    global sessions
    logging.info(sessions)
    current_code=randint(100000,999999) #generate code for session that will be used to verify receiver and sender
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
        money=float(currencify(content.split()[1])) #Get the amount that the receiver wants to receive from sender
        logging.info("Current code:")
        logging.info(current_code)
        sessions.append(Session(current_code,money,phone)) #Create a new Session instance, add it to the array of current sessions
        fullstr="To get "+currencify(float(money))+" euros from your friend, they need to send the code "+str(current_code)+" to the phone number: 99795260" #This is what will be returned to the user
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

    def addMessage(content,recipient):
        messages['messages'].append({'content':content,'to_number':recipient})
        return messages

    def currencify(this_str):
        def round_sig(x, sig=2):
            if x==0:
                return 0
            else:
                return round(x, sig-int(floor(log10(abs(x))))-1)
        this_str=str(this_str)
        special_char=None
        if "." in this_str:
            special_char="."
        elif "," in this_str:
            special_char=","
        else:
            return this_str+".00"
        return_val=this_str.split(special_char)[0]+special_char+str(round_sig(int(this_str.split(special_char)[1])))[:2]
        if len(return_val.split(special_char)[1])==1:
            return return_val+"0"
        elif len(return_val.split(special_char)[1])==0:
            return return_val+"00"
        else:
            return return_val

    if request.POST.get('event') == "'register'":
        phone=str(request.POST.get('phone'))
        bank_number=str(request.POST.get('bank'))
        sub_id=str(request.POST.get('subs'))
        register(phone,bank_number,sub_id)
        return HttpResponse("Done")
    else:
        logging.info("Not registering")
        if request.POST.get('secret') != webhook_secret:
            logging.info("Wrong secret, got ")
            logging.info(request.POST.get('secret'))
            return HttpResponse("Invalid webhook secret")

        logging.info("Secret verified")
        if request.POST.get('event') == 'incoming_message':
            logging.info("Incoming message")
            content = (request.POST.get('content')).lower()
            content = determineAction(content)
            from_number = request.POST.get('from_number')
            phone_id = request.POST.get('phone_id')
            logging.info("Content: "+content)
            if content.split()[0]=="gen" and isCurrency(content.split()[1]): #implement NLP later
                if not isRegistered(from_number):
                    logging.info(os.getcwd())
                    fullstr="Please register using the link tasosfalas.com/payflow"
                else:
                    try:
                        sessions,fullstr=generateCode(sessions,content,current_code,from_number)
                        if sessions[-1].amount>MONEY_CAP: #check if most recently added session is above MONEY_CAP
                            fullstr='The maximum amount of money you can send is 250 euros.'
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
                            fullstr="Please register using the link tasosfalas.com/payflow"
                        else:
                            payment(session.receiver,session.sender,session.amount)
                            fullstr="Transaction complete. You received "+currencify(session.amount)
                            messages=addMessage(fullstr,session.receiver_phone)
                            fullstr="Transaction complete. You sent "+currencify(session.amount)
                            sessions.remove(session)
                if done==False:
                    fullstr="Invalid ID sent. Please try again."
            else:
                fullstr="Sorry, I'm not quite sure what you want to do. To request money, send me 'gen [amount]' without the quotes or square brackets - for example, gen 50 would request 50 euros."
            logging.info(str(sessions))
            logging.info(messages['messages'])
            logging.info(fullstr)
            logging.info(from_number)
            messages=addMessage(fullstr,from_number)
            logging.info(messages['messages'])
            return HttpResponse(json.dumps({
                'messages':
                    messages['messages']

            }), 'application/json')

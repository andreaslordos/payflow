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
    logging.info("Got a new request")
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
        '''
        Input:
            content, String (what to send)
            recipient, String (phone number of recipient)
        Output:
            messages, dictionary (contains all messages to be sent and to whom)
        '''
        messages['messages'].append({'content':content,'to_number':recipient}) #add a new message to the messages dictionary
        return messages

    def currencify(this_str):

        def round_sig(x, sig=2): #function to round the cents to 2 significant figures
            if x==0:
                return 0
            else:
                return round(x, sig-int(floor(log10(abs(x))))-1)

        this_str=str(this_str)
        special_char=None
        if "." in this_str: #if the user separated the money with a "." (e.g. 43.23)
            special_char="."
        elif "," in this_str: #if the user separated the money with a "," (e.g. 43,23)
            special_char=","
        else:
            return this_str+".00" #else the user sent an integer instead of a float
        return_val=this_str.split(special_char)[0]+special_char+str(round_sig(int(this_str.split(special_char)[1])))[:2] #Easter egg: +1 to whoever can figure out what this abomination tries to do
        if len(return_val.split(special_char)[1])==1:
            return return_val+"0" #for leading zeroes
        elif len(return_val.split(special_char)[1])==0:
            return return_val+"00" #for leading zeroes
        else:
            return return_val #already has 2 decimal places, so just return

    if request.POST.get('event') == "'register'":
        phone=str(request.POST.get('phone'))
        bank_number=str(request.POST.get('bank'))
        sub_id=str(request.POST.get('subs'))
        register(phone,bank_number,sub_id)
        return HttpResponse("Done")
    else:
        logging.info("Transaction")
        if request.POST.get('secret') != webhook_secret: #if secret is not equal to webhook_secret
            logging.info("Wrong secret, got ")
            logging.info(request.POST.get('secret'))
            return HttpResponse("Invalid webhook secret") #exit

        logging.info("Secret verified") #else secret is valid
        if request.POST.get('event') == 'incoming_message': #received an incoming message
            logging.info("Incoming message")
            content = (request.POST.get('content')).lower() #make everything lowercase for simplicity
            content = determineAction(content) #use NLP to convert users message to protocol-suitable text
            from_number = request.POST.get('from_number') #retrieve phone number of user who sent message
            logging.info("Content: "+content)
            if content.split()[0]=="gen" and isCurrency(content.split()[1]): #check if instruction follows protocol (it should b/c of NLP above)
                if not isRegistered(from_number): #if phone number not in users.json
                    logging.info(os.getcwd())
                    fullstr="Please register using the link tasosfalas.com/payflow" #tell user to register
                else: #if user is registereed
                    try:
                        sessions,fullstr=generateCode(sessions,content,current_code,from_number) #add a new session to sessions
                        if sessions[-1].amount>MONEY_CAP: #check if most recently added session is above MONEY_CAP
                            fullstr='The maximum amount of money you can send is 250 euros.' #error message
                    except: #if above produces an error, it means that sessions isn't yet defined.
                        sessions=[] #define sessions
                        sessions,fullstr=generateCode(sessions,content,current_code,from_number) #retry
            elif content.split()[0].isdigit() and len(content.split())==1: #else if the user is trying to SMS a code to authorize a transaction and send money
                done=False #set flag to False
                requested_id=int(content.split()[0]) #get ID of transaction that the user is trying to authorize
                for session in sessions: #search for the session with the requested_id using a for loop
                    if session.id==requested_id:
                        done=True #if found, set flag to True
                        if not isRegistered(from_number):
                            fullstr="Please register using the link tasosfalas.com/payflow" #if user is not registered
                        else:
                            payment(session.receiver,session.sender,session.amount) #if user is registered, facilitate transaction between the two
                            fullstr="Transaction complete. You received €"+currencify(session.amount) #message for receiver
                            messages=addMessage(fullstr,session.receiver_phone)
                            fullstr="Transaction complete. You sent €"+currencify(session.amount) #message for sender
                            sessions.remove(session)
                if done==False: #if the transaction was not found.
                    fullstr="Invalid ID sent. Please try again."
            else:
                fullstr="Sorry, I'm not quite sure what you want to do. To request money, send the message 'I want a code for 20 euros' and then give the code that I'll send you back to your friend/customer."
            logging.info(str(sessions))
            logging.info(messages['messages'])
            logging.info(fullstr)
            logging.info(from_number)
            messages=addMessage(fullstr,from_number)
            logging.info(messages['messages'])
            return HttpResponse(json.dumps({ #send message back
                'messages':
                    messages['messages']

            }), 'application/json')

from datetime import datetime
import logging

class Session:
    def __init__(self, id, amount, receiver_phone):
        self.timestamp=datetime.now()
        self.id=id
        self.receiver=None
        self.sender=None
        self.amount=amount
        self.receiver_phone=receiver_phone
        self.sender_phone=None
        self.determineAccount("receiver")

    def add_sender(self,boc,phone):
        self.sender_phone=phone
        self.determineAccount("sender")

    def determineAccount(self,ReceiverOrSender):
        import json
        with open('users.json') as f:
            users = json.load(f)
        logging.info(str(users))
        if ReceiverOrSender=="receiver":
            self.receiver=users[self.receiver_phone]
        else:
            self.sender=users[self.sender_phone]

from datetime import datetime
class Session:
    def __init__(self,id,receiver,amount,receiver_phone):
        self.timestamp=datetime.now()
        self.id=id
        self.receiver=None #need to implement
        self.sender=None
        self.amount=amount
        self.receiver_phone=None
        self.sender_phone=None

    def add_sender(self,boc,phone):
        self.sender=boc
        self.sender_phone=phone

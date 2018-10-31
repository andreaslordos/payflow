#To do [cfalas]: implement registration system with the bocAPI
import json
import logging
def register(phone_number,bank_account_number,subs):
    logging.info(phone_number)
    phone_number=phone_number.replace(" ","")
    phone_number=phone_number.replace("'","")
    if phone_number[0]!="+":
        phone_number="+"+phone_number
    logging.info("In register function")
    '''
    Input: None
    Output: None,  but write to json file
    '''
    temp_dict = {phone_number: (bank_account_number,subs)} #make a temporary dictionary containing the phone number mapped to BAN and Sub_ID
    logging.info(temp_dict)

    with open('users.json') as f: #open users.json
        data = json.load(f) #load data from users.json

    if phone_number not in data: #if phone number not already in users.json
        logging.info("About to write!")
        data.update(temp_dict) #update data (a local variable) with temp_dict made above

        with open('users.json', 'w') as f:
            json.dump(data, f) #write data to users.json

        f.close()
        return "Complete"
    else:
        return "This phone number is already registered."

#To do [cfalas]: implement registration system with the bocAPI
import json
import logging
def register(phone_number):
    logging.info("In register function")
    '''
    Input: None
    Output: None,  but write to
    '''
    temp_dict = {phone_number: '294539573498573489579'}
    logging.info(temp_dict)
    with open('users.json') as f:
        data = json.load(f)

    if list(temp_dict.keys())[0] not in data:
        data.update(temp_dict)

        with open('users.json', 'w') as f:
            json.dump(data, f)

        f.close()
        return "Complete"
    else:
        return "This phone number is already registered."

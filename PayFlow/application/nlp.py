def determineAction(content):
    '''
    Input:
        content, String, what the user said
    Output:
        String, the users request converted to protocol-suitable text
    '''
    from word2number import w2n as w
    def isNum(a_str):
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

    content=content.split(" ")
    numbers=[]
    for word in content:
        try:
            temp_num=w.word_to_num(word) #to be able to detect numbers in word form (e.g. "four" as opposed to "4")
        except:
            temp_num=None #If it can't  be converted to a number (e.g. the text is "hello", temp_num=None)
        if isNum(word) or isNum(temp_num): #if temp_num or word is a number
            numbers.append(word) #add it to the numbers array
    if len(numbers)!=1: #if there's 0 or >1 numbers in the array
        return "! Error. Please have only one number present in your message."
    if len(numbers[0])==6: #if the number in the array is 6 digits, it's a verification code
        return str(numbers[0]) #return the verification code
    else:
        return "gen "+numbers[0] #else the user is trying to generate a verification code for a numbers[0] amount - thus we use the "gen" protocol

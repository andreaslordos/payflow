def determineAction(content):
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
            temp_num=w.word_to_num(word)
        except:
            temp_num=None
        if isNum(word) or isNum(temp_num):
            numbers.append(word)
    if len(numbers)!=1:
        return "! Error. Please have only one number present in your message."
    if len(numbers[0])==6:
        return str(numbers[0])
    else:
        return "gen "+numbers[0]

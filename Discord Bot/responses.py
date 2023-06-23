import random

def get_response(message: str) -> str:
    p_message = message.lower()
    if p_message == 'hello':
        responses = ["Need any help?","What's up?", "Hello","Hey there!"]
        return responses[random.randint(0,len(responses)-1)]

    if p_message == 'roll':
        return str(random.randint(1, 1000))
    
    if p_message == 'help':
        return '```Commands : \n>hello\n>roll [1 - 1000]\n>meme\n>hangman\n>wiki [keyword]\n>send_dm [@user] [message] \n>send_img [@user]```'
    

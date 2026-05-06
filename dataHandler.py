import json
import os


def write_file(file, data):
    with open(f"database/{file}", 'w') as f:
        json.dump(data, f, indent=4)

def read_file(file, fallback=[]):
    try:
        with open(f"database/{file}", 'r') as f:
            data = json.load(f)
            if data is None or data == []:
                raise FileNotFoundError
            return data
    except FileNotFoundError:
        write_file(file, fallback)
        return fallback

def LCG(prevNumber):
    A=9
    C=5
    M=2**32
    return (A*prevNumber+C)%M

def testLCG(numb=10):
    tmp=1
    for i in range(numb):
        tmp=LCG(tmp)
        #print("hex:"+Numb2HexStr(tmp))
        #print("numb:"+str(Hex2Numb(Numb2HexStr(tmp))))

def Numb2HexStr(numb):
    hexNumb = hex(numb)
    #print(len(hexNumb))
    return(hexNumb + ("0"*(10-len(hexNumb))))

def Hex2Numb(Hex):
    #print((int(Hex, 0)))
    return (int(Hex, 0))


def nextChatId(data):
    #print(data)
    #print(len(data))
    if len(data) == 0:
        return Numb2HexStr(1)
    last=list(data)[-1]
    #print(last)
    lastNumb = Hex2Numb(last)
    return Numb2HexStr(LCG(lastNumb))

def create_new_chat():
    # create a new chat session
    data = read_file("chat.json")
    ID = nextChatId(data)
    data[ID] = [{
            "role": "assistant",
            "content": "hi how can i help you today?"
        }]
    write_file("chat.json", data)
    return ID


def appendToChat(chatId, role, content):
    data = read_file("chat.json", fallback={
    "0x902d9d2b": [{
        "role": "user",
        "content": "Give me a short introduction to large language model."
    }]
})
    data[chatId].append({"role": role, "content": content})
    write_file("chat.json", data)
    return data[chatId]
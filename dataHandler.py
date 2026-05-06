import json
import os


def write_file(file: str, data: any):
    """writes data to a json file in the database folder, if the file does not exist it will be created

        :param file: the name of the file to write to
        :param data: the data to write to the file"""
    with open(f"database/{file}", 'w') as f:
        json.dump(data, f, indent=4)

def read_file(file: str, fallback: any =[]) -> any:
    """reads data from a json file in the database folder, if the file does not exist it will be created with the fallback data

        :param file: the name of the file to read from
        :param fallback: the data to write to the file if it does not exist, default is an empty list"""
    try:
        with open(f"database/{file}", 'r') as f:
            data = json.load(f)
            if data is None or data == []:
                raise FileNotFoundError
            return data
    except FileNotFoundError:
        write_file(file, fallback)
        return fallback

def LCG(prevNumber: int) -> int:
    """a simple linear congruential generator to generate a new chatId based on the previous chatId

        :param prevNumber: the previous chatId as a number
        :return: the next chatId as a number"""
    A=9
    C=5
    M=2**32
    return (A*prevNumber+C)%M

def testLCG(numb: int = 10):
    """a simple test function to test the LCG function by generating a sequence of numbers

        :param numb: the number of numbers to generate, default is 10"""
    tmp=1
    for i in range(numb):
        tmp=LCG(tmp)
        #print("hex:"+Numb2HexStr(tmp))
        #print("numb:"+str(Hex2Numb(Numb2HexStr(tmp))))

def Numb2HexStr(numb: int) -> str:
    """converts a number to a hex string with leading zeros to make it 10 characters long

        :param numb: the number to convert
        :return: the hex string representation of the number with leading zeros"""
    hexNumb = hex(numb)
    #print(len(hexNumb))
    return(hexNumb + ("0"*(10-len(hexNumb))))

def Hex2Numb(Hex: str) -> int:
    """converts a hexadecimal string to a number

        :param Hex: the hexadecimal string to convert
        :return: the number representation of the hexadecimal string"""
    #print((int(Hex, 0)))
    return (int(Hex, 0))


def nextChatId(data: dict) -> str:
    """generates the next chatId based on the existing chatIds in the data

        :param data: the data containing the existing chatIds
        :return: the next chatId as a hexadecimal string"""
    #print(data)
    #print(len(data))
    if len(data) == 0:
        return Numb2HexStr(1)
    last=list(data)[-1]
    #print(last)
    lastNumb = Hex2Numb(last)
    return Numb2HexStr(LCG(lastNumb))

def create_new_chat() -> str:
    """creates a new chat session by generating a new chatId and adding a default message to the chat.json file

        :return: the new chatId as a hexadecimal string"""
    # create a new chat session
    data = read_file("chat.json")
    ID = nextChatId(data)
    data[ID] = [{
            "role": "assistant",
            "content": "hi how can i help you today?"
        }]
    write_file("chat.json", data)
    return ID


def appendToChat(chatId: str, role: str, content: str) -> list:
    """appends a new message to the chat session with the given chatId in the chat.json file

        :param chatId: the chatId of the chat session to append to
        :param role: the role of the message (e.g. "user" or "assistant")
        :param content: the content of the message
        :return: the updated chat session as a list of messages"""
    data = read_file("chat.json", fallback={
    "0x902d9d2b": [{
        "role": "user",
        "content": "Give me a short introduction to large language model."
    }]
})
    data[chatId].append({"role": role, "content": content})
    write_file("chat.json", data)
    return data[chatId]
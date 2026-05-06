import flask
from flask import render_template, request, redirect, url_for
import llm
import dataHandler
from urllib.parse import unquote_plus


def parseThought(chat):
    chatOutput = []
    for message in chat:
        if message["role"] == "assistant" and message["content"].startswith("<think>") and message["content"].endswith("</think>"):
            chatOutput.append({
            "role": "thinking",
            "content": message['content'][7:-8]
        },)
        elif message["role"] == "assistant" and message["content"].startswith("<tool_call>") and message["content"].endswith("</tool_call>"):
            chatOutput.append({
            "role": "thinking",
            "content": message['content'][7:-8]
        },)
        else:
            chatOutput.append(message)
    return chatOutput


app = flask.Flask(__name__)

@app.route('/')
def home():
    return redirect("/new_chat")

@app.route('/chat/<chatId>', methods=['GET', 'POST'])
def index(chatId):
    chat = dataHandler.read_file("chat.json")[chatId]
    chat = parseThought(chat)
    return render_template('chat.html', chat=chat, chatId=chatId)


@app.route('/chat/<chatId>/new/<prompt>', methods=['GET', 'POST'])
def new_message(chatId, prompt):
    # Call the LLM function with the prompt
    chat = dataHandler.appendToChat(chatId, "user", unquote_plus(prompt))
    response = llm.main(chat, chatId)
    return redirect(f"/chat/{chatId}")


@app.route('/new_chat', methods=['get'])
def new_chat():
    # create a new chat session and redirect to the chat page
    chatId = dataHandler.create_new_chat() 
    return redirect(f"/chat/{chatId}")




app.run(debug=True)
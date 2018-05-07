import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot


app = Flask(__name__)
PAGE_ACCESS_TOKEN = "EAAaWqj1aGbYBAPtHOYVzj5ZCf8FTXEmz30ET3AlM2UFQtFZAbYiOQaPPnYbXfargxpEQ3OTXy8O7tZAPDwpsS4kgy6DyYgEyHZASJ0eqB7hxT4wjVJKtdAwacyKLKY8kgiuRs9OplQNEXoTRNrpgjZAJ7KRKXiZBFVFsFCkVbaNQZDZD"
bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
    # Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "chatbot8":
            return "Verification Token Mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello, World! Assignment 1b", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    response = None

                    entity, value = wit_response(messaging_text)

                    if entity == 'intent':
                        response = "paper {}".format(str(value))
                    elif entity == 'autMajor':
                        response = "major {}".format(str(value))
                    elif entity == 'autCourse':
                        response = "course {}".format(str(value))

                    if response is None:
                        response = "Sorry, I didn't understand that."

                    bot.send_text_message(sender_id, response)

    return "ok", 200


def log(message):
    print(message)
    sys.stdout.flush()


# main
if __name__ == "__main__":
    app.run(debug=True, port=80)


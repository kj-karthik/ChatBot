import requests
from bs4 import BeautifulSoup
import json

chatbox = None
userMessage = None  # Variable to store user's message
API_KEY = "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"  # Paste API key here
inputInitHeight = None

def create_chat_li(message, class_name):
    # Create a chat <li> element with passed message and class name
    chat_li = BeautifulSoup("", "html.parser").new_tag("li")
    chat_li["class"] = ["chat", class_name]
    chat_content = f"<p></p>" if class_name == "outgoing" else "<span class=\"material-symbols-outlined\">smart_toy</span><p></p>"
    chat_li.append(BeautifulSoup(chat_content, "html.parser"))
    chat_li.find("p").string = message
    return chat_li  # return chat <li> element

def generate_response(incoming_chat_li):
    # Generate a random response from the bot
    global userMessage
    global chatbox

    API_URL = "https://api.openai.com/v1/chat/completions"
    message_element = incoming_chat_li.find("p")

    requestOptions = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": userMessage,
            },
        ],
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    # Send POST request to API, get a response and set the response as paragraph text
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(requestOptions))
        response_data = response.json()
        message_element.string = response_data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        message_element["class"] = ["error"]
        message_element.string = "Oops Something went wrong. Please try again."
    finally:
        chatbox.scrollTo(0, chatbox.scrollHeight)

def handle_chat():
    global userMessage
    global chatInput
    global chatbox

    userMessage = chatInput.strip()  # Get user entered message and remove extra whitespace
    if not userMessage:
        return

    # Clear the input textarea and set its height to default
    chatInput = ""
    chatInputHeight = inputInitHeight

    # Append the user's message to the chatbox
    outgoing_chat_li = create_chat_li(userMessage, "outgoing")
    chatbox.append(outgoing_chat_li)
    chatbox.scrollTo(0, chatbox.scrollHeight)

    # Display "Typing..." message while waiting for the response
    incoming_chat_li = create_chat_li("Typing...", "incoming")
    chatbox.append(incoming_chat_li)
    generate_response(incoming_chat_li)

# Event Listeners
chatInput.bind("<Key>", lambda e: chatInput.config(height=inputInitHeight))
chatInput.bind("<Return>", lambda e: handle_chat() if not e.shift and chatInput.winfo_width() > 800 else None)

sendChatbtn.bind("<Button-1>", lambda e: handle_chat())
closeBtn.bind("<Button-1>", lambda e: document.body["class"].remove("show-chatbot"))
chatbotToggler.bind("<Button-1>", lambda e: document.body["class"].toggle("show-chatbot"))

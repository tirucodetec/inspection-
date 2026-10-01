import json
from google import genai
from google.genai import types

import streamlit as st 
from prompts import SYSTEM_PROMPT
from prompts import WELCOME_MESSAGE_TEMPLATE
from prompts import SUMMARY_REQUEST_PROMPT
from twilio.rest import Client as TwilioClient

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TWILIO_ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_WHATSAPP_FORM = st.secrets["TWILIO_WHATSAPP_FORM"]
TWILIO_CONTENT_SID = st.secrets["TWILIO_CONTENT_SID"]

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key= GEMINI_API_KEY)

@st.cache_resource
def get_twilio_client():
    return TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


gemini_client = get_gemini_client()
twilio_client = get_twilio_client()


MODEL_NAME = "gemini-3.5-flash"

def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])


def add_message(role , kind , content):
    st.session_state.messages.append({"role": role, "kind": kind, "content": content})
    render_message(st.session_state.messages[-1])

def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text
    except Exception as error:
        return f"Sorry, something went wrong: {error}"

def clean_whatsapp_text(text):
    if not text:
        return "No inspection summary available."
    text = " ".join(text.split())  # collapse whitespace/newlines
    return text[:1500] + "..." if len(text) > 1500 else text

def send_whatsapp(to_number, user_name, summary):
    # Content template expects {{1}} = name, {{2}} = summary.
    try:
        content_variables = json.dumps(
            {"1": user_name, "2": clean_whatsapp_text(summary)}, ensure_ascii=False
        )
        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_FORM,
            to=f"whatsapp:{to_number}",
            content_sid=TWILIO_CONTENT_SID,
            content_variables=content_variables,
        )
        return True, message.sid
    except Exception as error:
        return False, str(error)


#step 1: Onboarding (username and phone number)
if 'onboarded' not in st.session_state:
    st.title("🔍 InspectAI")
    st.caption("📸 Upload an image. 🤖 Let AI inspect it. 🔎 Identify visible problems. 📋 Get a clear inspection report.")


    with st.form("onboarding_form"):
        name = st.text_input("Your name")
        whatsapp_number = st.text_input(
            "Whatsapp_number (with country code)",
            placeholder = "+91xxxxxxxxxx",
            help = "This is the number Where Inspect_AI will be shared to your WhatsApp!!!"
        )

        submitted = st.form_submit_button("Lets go!!!")


    if submitted:
        if not name.strip() or not whatsapp_number.strip():
            st.warning("Please fill both Your name and whatsapp number!!")

        else:
            st.session_state.name = name.strip()
            st.session_state.whatapp_number = whatsapp_number.strip()

            # activate gemini 
            st.session_state.chat = gemini_client.chats.create(
                model= MODEL_NAME ,
                config= types.GenerateContentConfig(system_instruction= SYSTEM_PROMPT),

            )
            st.session_state.messages = []
            st.session_state.onboarded = True
            st.rerun()
    st.stop()

# chat interface 

header_col, button_col = st.columns([5, 2], vertical_alignment="center")
 
with header_col:
    st.title("🔍 InspectAI")

with button_col:
    send_disabled = len(st.session_state.messages) <= 1
    if st.button("📤 Send to WhatsApp", disabled=send_disabled, use_container_width=True):
        with st.spinner("Summarizing your day..."):
            summary = ask_gemini([SUMMARY_REQUEST_PROMPT])
        success, info = send_whatsapp(st.session_state.whatsapp_number, st.session_state.name, summary)
        if success:
            st.success("Sent! Check your WhatsApp 📲")
        else:
            st.error(f"Couldn't send that: {info}")

st.caption(f"Logged in as {st.session_state.name} - updates go to {st.session_state.whatapp_number}")
 
if not st.session_state.messages:
    add_message("assistant", "text", WELCOME_MESSAGE_TEMPLATE.format(name=st.session_state.name))
else:
    for message in st.session_state.messages:
        render_message(message)
 
user_input = st.chat_input(
    "Upload an image or describe a problem to inspect 🔍",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)

if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text
    parts = []

    if photo is not None:
        photo_bytes = photo.getvalue()
        add_message("user", "image", photo_bytes)
        parts.append(types.Part.from_bytes(data=photo_bytes, mime_type=photo.type))

    if text:
        add_message("user", "text", text)
        parts.append(text)

    elif photo is not None:
        parts.append(
            "Inspect this image and identify any visible problems, defects, damage, "
            "or unusual features. Describe what the image shows, identify the "
            "problem and its location, explain possible concerns or causes if "
            "reasonably supported, and suggest appropriate next steps. "
            "Clearly distinguish visible observations from assumptions. "
            "If no obvious problem is visible, say so."
        )

    with st.spinner("Inspecting the image... 🔍"):
        answer = ask_gemini(parts)

    add_message("assistant", "text", answer)

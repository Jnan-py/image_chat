import streamlit as st 
import google.generativeai as genai 
import os 
from dotenv import load_dotenv 
from PIL import Image
from keras.utils import load_img

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("Image Chatter")
st.subheader("Upload an image and start chatting")

model = genai.GenerativeModel(model_name="gemini-1.5-pro",system_instruction="You are a super human who can clearly see through the blurry images")

img = st.file_uploader("Upload your image",type=["jpg","jpeg","png","webp"])

if 'chats' not in st.session_state:
            st.session_state.chats =[]
            st.session_state.chats.append({
                'role':'model', 'parts':'Image is uploaded, now start asking your queries'
            })

if img:
    st.success("File Uploaded")
    st.markdown("Uploaded Image")
    st.image(img,caption="Uploaded Image")


    for msg in st.session_state.chats:
        row = st.columns(2)
        if msg['role']=='user':
            row[1].chat_message(msg['role']).markdown(msg['parts'])
        else:
            row[0].chat_message(msg['role']).markdown(msg['parts'])

    
    chat = model.start_chat(
        history=st.session_state.chats
    )

    prompt = st.chat_input("Enter your query here..!!")
    if prompt:
        row_u = st.columns(2)
        row_u[1].chat_message('user').markdown(prompt)
        st.session_state.chats.append({
            'role':'user','parts':prompt
        })

        imm = load_img(img)
        image = Image.open(img).resize((28,28))

        response_1 = chat.send_message([prompt,image])
        # response_2 = model.generate_content(
        #     [prompt,img],
        #     generation_config=genai.GenerationConfig(
        #         temperature=0.7,
        #         max_output_tokens=1000
        #     )
        # )

        # fin_resp = response_1.text + response_2.text

        row_r = st.columns(2)
        row_r[0].chat_message('model').markdown(response_1.text)
        st.session_state.chats.append({
            'role':'model','parts':response_1.text
        })
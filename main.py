import io
import streamlit as st
import google.generativeai as genai
from PIL import Image

genai.configure(api_key="AIzaSyChNfm0fpmBKUC8NYnFb4Um91aJCxvhzgg")
model = genai.GenerativeModel("gemini-pro-vision")

# Initialize session state attributes if they don't exist
if "response_received" not in st.session_state:
    st.session_state.response_received = False
if "response_text" not in st.session_state:
    st.session_state.response_text = ""
if "additional_info_text" not in st.session_state:
    st.session_state.additional_info_text = ""

# Language selection
language = st.selectbox("Select Language / เลือกภาษา", ["English", "Thai"])

if language == "English":
    prompt1 = "What type of animal is in this picture? tell me only name"
    prompt2 = "Information about the animals in the pictures based on the wikipedia website, such as name, scientific name, common name, habitat, origin, lifespan, characteristics of the animal. More information about animals and help space out lines for easy reading"
else:
    prompt1 = "สัตว์ในรูปนี้มีชื่อว่าอะไร ระบุเเค่ชื่อไม่ต้องบอกข้อมูลอื่นๆ"
    prompt2 = "ข้อมูลของสัตว์ในรูปโดยอ้างอิงจากเว็บไซต์ wikipedia เช่น ชื่อ ชื่อทางวิทยาศาสตร์ ชื่อสามัญ เเหล่งที่อยู่อาศัย เเหล่งกำเนิด อายุขัย ลักษณะนิสัยของสัตว์ ข้อมูลเพิ่มเติมเกี่ยวกับสัตว์ เเละช่วยเว้นวรรคบรรทัดเพื่อให้อ่านได้ง่าย"

st.title('Animal Type Classifier🐾')
st.write('โปรดใส่รูปภาพของสัตว์ที่คุณต้องการตรวจสอบชนิด🖼️' if language == "Thai" else 'Please upload an image of the animal you want to classify🖼️')
img_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if img_file is not None:
    # Reset session state when a new image is uploaded
    if "last_uploaded_file" not in st.session_state or st.session_state.last_uploaded_file != img_file:
        st.session_state.response_received = False
        st.session_state.response_text = ""
        st.session_state.additional_info_text = ""
        st.session_state.last_uploaded_file = img_file

    imagefile = io.BytesIO(img_file.read())
    img = Image.open(imagefile)
    st.image(img_file, channels="BGR")

    if st.button("ประมวลผล" if language == "Thai" else "Process"):
        try:
            response = model.generate_content([img, prompt1])
            st.session_state.response_text = response.text
            st.session_state.response_received = True
        except:
            st.session_state.response_text = "no response" if language == "English" else "ไม่มีการตอบสนอง"

    if st.session_state.response_received:
        st.text(st.session_state.response_text)

        if st.button("ข้อมูลเพิ่มเติม" if language == "Thai" else "More Information"):
            try:
                info = model.generate_content([img, prompt2])
                st.session_state.additional_info_text = info.text
            except:
                st.session_state.additional_info_text = "no response" if language == "English" else "ไม่มีการตอบสนอง"

    if st.session_state.additional_info_text:
        st.text(st.session_state.additional_info_text)

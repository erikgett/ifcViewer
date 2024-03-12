import streamlit as st
from PIL import Image
from pages.Img2Img.prompt_editor import translate_prompt, correct_prompt, correct_neg_prompt
from pages.Img2Img.request_SD_img2img import ControlnetRequest
import base64
import io

def pil_image_to_base64(image):
    # Convert the image to a byte stream
    image_byte_array = io.BytesIO()
    image.save(image_byte_array, format='JPEG')
    image_byte_array = image_byte_array.getvalue()

    # Encode the byte stream as Base64
    base64_image = base64.b64encode(image_byte_array).decode('utf-8')

    return base64_image

st.write("# Генерация интерьера помещения по изображению")

prompt = st.text_input("Введите положительное описание изображения")
if prompt:
    st.write("Перевод подсказки на английском:", translate_prompt(prompt))

neg_prompt = st.text_input("Введите негативное описание изображения (что не нужно включать в изображение)")
if neg_prompt:
    st.write("Перевод негативной подсказки на английском:", translate_prompt(neg_prompt))

if prompt is None:
    prompt = ""
if neg_prompt is None:
    neg_prompt = ""

# Определение списков для выбора
room_types = ['Гостиная', 'Спальня', 'Ванная комната', 'Кухня']
room_styles = ['скандинавский', 'классический', 'лофт']

# Создание двух колонок
col1, col2 = st.columns(2)
room_types_translation = {'Гостиная': 'Livingroom', 'Спальня': 'Bedroom', 'Ванная комната': 'Bathroom', 'Кухня': 'Kitchen'}
room_styles_translation = {'скандинавский': 'Scan', 'классический': 'Classic', 'лофт': 'Loft'}

with col1:
    selected_room_type = st.selectbox('Выберите тип помещения:', room_types)
    translated_type = room_types_translation.get(selected_room_type, selected_room_type)

with col2:
    selected_room_style = st.selectbox('Выберите стиль помещения:', room_styles)
    translated_style = room_styles_translation.get(selected_room_style, selected_room_style)

uploaded_file = st.file_uploader(
    "Выберите изображение", type=["jpg", "jpeg", "png"],
    help="Перетащите файл сюда")


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # Отображение изображения
    st.image(image.resize((300, 300)),
             caption="Загруженное изображение", width=300)
    if st.button('Начать генерацию'):
        if prompt is None:
            prompt = ""
        if neg_prompt is None:
            neg_prompt = ""

        image = Image.open(uploaded_file)
        img64 = pil_image_to_base64(image)

        js = ControlnetRequest(
            img64,
            correct_prompt(translate_prompt(prompt)),
            correct_neg_prompt(neg_prompt),
            translated_type,
            translated_style).send_request()
        
        image_bytes = base64.b64decode(js['images'][0])
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image, caption="Результат генерации")

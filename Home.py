import ifcopenshell
import streamlit as st


def callback_upload():
    session["file_name"] = session["uploaded_file"].name
    session["array_buffer"] = session["uploaded_file"].getvalue()
    session["ifc_file"] = ifcopenshell.file.from_string(session["array_buffer"].decode("utf-8"))
    session["is_file_loaded"] = True

    ### Empty Previous Model Data from Session State
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {}
    session["CostScheduleData"] = {}

    ### Empty Previous DataFrame from Session State
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False


def get_project_name():
    return session.ifc_file.by_type("IfcProject")[0].Name


def change_project_name():
    if session.project_name_input:
        session.ifc_file.by_type("IfcProject")[0].Name = session.project_name_input
        st.balloons()


def main():
    st.set_page_config(
        layout="wide",
        page_title="IFC viewer",
        page_icon="✍️",
    )
    st.title("IFC viewer")
    st.markdown(
        """ 
    ###  📁 Нажмите выбрать файл для дальнейшего начала просмотра
    """
    )

    # Add File uploader to Side Bar Navigation
    st.sidebar.header('Загрузчик модели')
    st.sidebar.file_uploader("Выбрать файл", type=['ifc'], key="uploaded_file", on_change=callback_upload)

    # Add File Name and Success Message
    if "is_file_loaded" in session and session["is_file_loaded"]:
        st.sidebar.success(f'Проект успешно загружен')
        st.sidebar.write("🔃 Вы можете обновить перезагрузить проект  ")

        col1, col2 = st.columns([2, 1])
        col1.text_input("✏️ Задать имя проекту", key="project_name_input")
        col1.button("✔️ Подтвердить", key="change_project_name", on_click=change_project_name())

    st.sidebar.write("""
    --------------
    ### Контакты:
    
    Гётте Эрик Георгиевич https://t.me/erikgette
    
    Гётте Виктория Дмитриевна https://t.me/viktoriavash
        
    """)
    st.write("")
    st.sidebar.write("")


if __name__ == "__main__":
    session = st.session_state
    main()

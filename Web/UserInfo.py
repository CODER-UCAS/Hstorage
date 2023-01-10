import streamlit as st
import streamlit_authenticator as stauth
# from main_ui import main_ui
import yaml
from yaml import SafeLoader
# from streamlit_extras.switch_page_button import switch_page
from switch_paper import switch_page
from Login import register,login


st.set_page_config(
    page_title="数据库系统--用户信息界面",
    page_icon="🧊",
    # layout="centered",
    layout='wide',
    initial_sidebar_state="expanded",#"collapsed",
    )

st.session_state["login_status"] = False

def show_user_info():
    st.write(f'## :rainbow: 欢迎！恭喜你成功登录！')

# @
# class login_state():
#     def __init__():



def login_main():
    # print(st.extra_streamlit_components.CookieManager.cookie_manager)
    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)
    # if not st.session_state["login_status"]:
    st.title(":sunglasses: H-Store: Unified Access to SQL Stores for Heterogeneous Data")
    st.markdown("🏃Welcome to H-Store system!")
    st.sidebar.markdown("👇请点击下面选项登录或者注册")
    if_register = st.sidebar.selectbox('请登入系统',['登录','注册'],key = "lll")

    if if_register == '登录':
        if login():
            show_user_info()
    elif if_register == '注册':
        register()
    # elif if_register == '重设密码':






if __name__ == '__main__':
    login_main()
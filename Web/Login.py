import streamlit as st
import streamlit_authenticator as stauth
# from main_ui import main_ui
import yaml
from yaml import SafeLoader
# from streamlit_extras.switch_page_button import switch_page
from switch_paper import switch_page

# reset the passward
def reset():
    config,authenticator = load_userdata()
    try:
        if authenticator.reset_password(username, 'Reset password'):
            st.success('Password modified successfully')
    except Exception as e:
            st.error(e)

def register():
    config,authenticator = load_userdata()
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)

def login():

    config,authenticator = load_userdata()

    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        st.session_state["login_status"] = True
        authenticator.logout('登出', 'main')
        # if "authentication_status" not in st.session_state:


    elif authentication_status == False:
        st.error('😅用户名/密码错误')

    elif authentication_status == None:
        st.warning('😃请输入用户名和密码')


    return authentication_status

def load_userdata():
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['preauthorized']
        )
    return config,authenticator
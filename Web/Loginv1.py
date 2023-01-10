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
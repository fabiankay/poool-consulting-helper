import streamlit as st

def show_sidebar() -> None:
    with st.sidebar:
        # Load & show logo image
        logo_path = "static/logo/image_logo_dark.png"
        st.logo(logo_path, size="large", link=None, icon_image=None)

        # st.write(st.session_state)
        
        # show_configuration()

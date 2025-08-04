import streamlit as st

st.set_page_config(layout="wide")
st.title("GPevo")

if not st.user.is_logged_in:
    st.button("Log in with Google", on_click=st.login)
    st.stop()

st.button("Log out", on_click=st.logout)
st.markdown(f"Welcome! {st.user.name}")
st.write(st.user)


pages: list = [
    st.Page("pages/playground.py", title = "Playground"),
    st.Page("pages/training_editor.py", title = "Editor de treinos"),
    st.Page("pages/training_manager.py", title = "Treinamentos")
]
pg = st.navigation(pages)
pg.run()
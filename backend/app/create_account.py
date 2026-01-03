import streamlit as st

st.title("Create an account")

if "job_data" not in st.session_state:
    st.write("No data")
else:
    st.write(st.session_state.job_data)
import streamlit as st

pages = {
    "Your account": [
        st.Page("create_account.py", title="Create your account"),
        st.Page("manage_account.py", title="Manage your account"),
    ],
    "Services": [
        st.Page("resume_parser.py", title="Try it out"),
        st.Page("HR_dashboard.py", title="HR"),
    ],
}

pg = st.navigation(pages)
pg.run()
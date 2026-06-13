import streamlit as st

def metric_card(title, value, icon):

    with st.container(border=True):

        st.markdown(
            f"### {icon} {title}"
        )

        st.markdown(
            f"# {value}"
        )
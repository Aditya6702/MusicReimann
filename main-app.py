import streamlit as st
from app1 import show_app1
from zeta_prime_app import show_zeta_prime_app

st.set_page_config(page_title="Musical Note Generator & Zeta Prime Explorer", layout="wide")

# Define the pages
PAGES = {
    "Musical Note Generator": show_app1,
    "Zeta Prime Explorer": show_zeta_prime_app
}

# Sidebar navigation
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Display the selected page
page = PAGES[selection]
page()

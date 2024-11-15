import requests
import streamlit as st

# ipify APIを使ってグローバルIPアドレスを取得
ip_address = requests.get('https://api.ipify.org').text

# print(f"Your global IP address is: {ip_address}")
st.title(f"Your global IP address is: {ip_address}")
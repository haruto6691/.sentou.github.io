import requests
import streamlit as st

# ipify APIを使ってグローバルIPアドレスを取得
ip_address = requests.get('https://api.ipify.org').text

st.write(f"Your global IP address is: {ip_address}")
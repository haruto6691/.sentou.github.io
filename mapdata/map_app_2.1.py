import folium
from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import json

# JSONファイルからデータを読み込む
with open("C:/fluid/campusOS-1/people_count_data.json", 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# 「新11号館」の緯度経度データを作成する
sensor_data = pd.DataFrame(
    data=[[35.713142701496345, 139.5738074985881]],  # 新11号館の緯度経度
    index=["新11号館"],
    columns=["x", "y"]
)

n = int(json_data[-1]["people count"])
sensor_data["n"] = n
sensor_data["condition"] = n / 10

# データを地図に渡す関数を作成する
def AreaMarker(df, m):
    for index, r in df.iterrows():
        # 条件に基づいてピンの色を設定
        if r['condition'] >= 0.8:
            color = 'red'
        elif r['condition'] >= 0.5:
            color = 'blue'
        else:
            color = 'green'
        
        # カスタムポップアップの作成（幅を大きく設定）
        popup_content = f"""
        <div style="width:200px;">
            <strong>{index}</strong><br>
            人数: {r['n']}人<br>
            条件: {r['condition']*100:.0f}%
        </div>
        """
        popup = folium.Popup(popup_content, max_width=300)

        # ピンをおく
        folium.Marker(
            location=[r.x, r.y],
            popup=popup,
            icon=folium.Icon(color=color)
        ).add_to(m)

# ------------------------画面作成------------------------

st.title("キャンパスマップ")  # タイトル

# カスタムCSSで比率を4:9に設定
st.markdown(
    """
    <style>
    .map-container {
        width: 100%;
        height: calc(100vw * 16 / 9);  /* 16:9の比率を指定 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 地図の初期設定と表示範囲の制限
m = folium.Map(
    location=[35.713142701496345, 139.5738074985881],  # 新11号館の位置
    zoom_start=18, 
    zoomControl=False,  
    scrollWheelZoom=False,  
    dragging=False,  
    max_bounds=True  
)

# 表示範囲を設定 (緯度・経度の最小・最大範囲)
bounds = [[35.712, 139.573], [35.714, 139.574]]
m.fit_bounds(bounds)

AreaMarker(sensor_data, m)  # データを地図に渡す

# カスタムCSSで設定したクラスを使って地図を表示
folium_static(m, width=300, height=400)


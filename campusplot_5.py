import os
import folium
from folium import CustomIcon  # CustomIconをインポート
from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import time
import matplotlib.pyplot as plt
import numpy as np

# JSONファイルのパス
json_file_path = 'data.json'

# JSONデータの読み込み関数
def load_json_data():
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# JSONデータの更新時刻を取得する関数
def get_json_update_time():
    timestamp = os.path.getmtime(json_file_path)
    return datetime.fromtimestamp(timestamp)


#  ------------------------マップ用のデータ作成（読み込み）------------------------

# mapdataの作成（緯度，経度を格納）
campus_data = pd.DataFrame(
    data=[
        [35.711351413004174, 139.57418132780236],
        [35.7108463540432, 139.5738466470573],
        [35.71202610333374, 139.57401862907994],
        [35.71248397455787, 139.57421402730864],
        [35.71212347584171, 139.57292773406655],
        [35.7123085925777, 139.57255222481427],
        [35.71168788853041, 139.57219816487273],
        [35.71180938664764, 139.57249605394608],
        [35.71280078323339, 139.57277216593872],
        [35.712628734637704, 139.57319059053415],
        [35.7131942107875, 139.57299248376236],
        [35.712624464351784, 139.57388445313234],
        [35.712868648404275, 139.57360019540528],
        [35.71319932253857, 139.57397971168206],
        [35.71349549052211, 139.57307256501352],
        [35.713708508130885, 139.57374186664987]
    ],
    index=["学生食堂", "トラスコンガーデン", "1号館", "2号館", "3号館", "4号館", "5号館", "6号館", "7号館", "8号館", "9号館", "10号館", "11号館", "新11号館", "12号館", "14号館"],
    columns=["x", "y"]
)

# 条件に基づくカスタムアイコン画像のパスを設定する関数
def get_icon_path(condition):
    if condition >= 0.8:
        return '153_000_000.png'     # condition>=80%:  赤(153, 0, 0)
    elif condition >= 0.6:
        return '255_051_051.png'   # condition>=60%:  赤(255, 51, 51)
    elif condition >= 0.4:
        return '255_153_1530.png' # condition>=40%:  赤(255, 153, 153)
    else:
        return '255_230_230.png' # condition>=0%:   赤(255, 230, 230)

# データを地図に渡す関数を作成
def AreaMarker(df, m):
    for index, r in df.iterrows():
        # 条件に基づいた画像アイコンパスを取得
        icon_path = get_icon_path(r['condition'])

        popup_content = f"""
        <div style="width:200px;">
            <strong>{index}</strong><br>
            人数: {r['n']}人<br>
            条件: {r['condition']*100:.0f}%
        </div>
        """
        popup = folium.Popup(popup_content, max_width=300)

        # カスタムアイコンを作成
        icon = CustomIcon(icon_image=icon_path, icon_size=(20, 25))

        folium.Marker(
            location=[r.x, r.y],
            popup=popup,
            icon=icon
        ).add_to(m)



#  ------------------------自動更新------------------------

# ファイル変更を監視するクラス
class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == json_file_path:
            st.session_state.updated = True  # 更新フラグを立てる

# スレッドを作成してファイル変更を監視
def watch_json_file():
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(json_file_path), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# スレッドを開始
if 'updated' not in st.session_state:
    st.session_state.updated = False

threading.Thread(target=watch_json_file, daemon=True).start()


#  ------------------------サブタイトル------------------------

# カラーバーを作成する関数
def create_colorbar():
    fig, ax = plt.subplots(figsize=(2.3, 0.05))  # サイズを横長に設定
    # カラーマップを設定
    # cmap = plt.get_cmap('jet')
    cmap = plt.get_cmap('Reds')
    norm = plt.Normalize(0, 1)

    # カラーバーの作成
    cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax, orientation='horizontal')  # 横向きに設定
    # cbar.set_label('条件 (%)', labelpad=5)
    # パーセンテージのラベルを設定
    cbar.ax.set_xticklabels([0, 25, 50, 75, "100(%)"], fontsize=5)  
    plt.close(fig)
    
    return fig


# ------------------------画面作成------------------------

# タイトル
st.title("キャンパスマップ")  

# サブヘッダーにカラーバーを表示
# st.subheader("条件を示すカラーバー")
colorbar_fig = create_colorbar()
st.pyplot(colorbar_fig)

# 地図の初期設定
m = folium.Map(
    location=[35.71227298265089, 139.57338620532082], 
    zoom_start=17, 
    zoomControl=False,  
    scrollWheelZoom=False,  
    dragging=False,  
    max_bounds=True  
)

# 更新フラグが立っていたらデータを再読み込み
if st.session_state.updated:
    json_data = load_json_data()  # JSONデータを再読み込み
    campus_data["n"] = campus_data.index.map(lambda name: json_data[name]["n"])
    campus_data["condition"] = campus_data.index.map(lambda name: json_data[name]["condition"])
    st.session_state.updated = False  # フラグをリセット

# 初回読み込み時にデータを取得
else:
    json_data = load_json_data()
    campus_data["n"] = campus_data.index.map(lambda name: json_data[name]["n"])
    campus_data["condition"] = campus_data.index.map(lambda name: json_data[name]["condition"])

# データを地図に渡す
AreaMarker(campus_data, m)

# 地図を表示
folium_static(m, width=300, height=400)

# ストリームリットのボタンを作成
if st.button("リロード"):
    st.session_state.updated = False  # 地図を再初期化

# 常に表示するテキスト
st.write("地図の初期化やデータの更新にはリロードボタンを押してください．")

# 最後の更新時刻を表示
update_time = get_json_update_time()
st.write(f"最終更新時刻: {update_time.strftime('%Y-%m-%d %H:%M:%S')}")

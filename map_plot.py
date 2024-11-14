import mysql.connector
import pandas as pd
import folium
from folium import CustomIcon
from streamlit_folium import folium_static
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt

# # MySQLデータベースに接続
# try:
#     db_connection = mysql.connector.connect(
#         host="seikeidb.mysql.database.azure.com",
#         user="soc5admin",
#         password="eat5Mae\\ze",
#         database="campusOS"
#     )
    
#     cursor = db_connection.cursor()

#     # 最新のデータを取得するSQLクエリ
#     query = """
#         SELECT line_count.device_id, line_count.timestamp, line_count.people_inside
#         FROM line_count
#         JOIN (
#             SELECT device_id, MAX(timestamp) AS latest_timestamp
#             FROM line_count
#             GROUP BY device_id
#         ) AS latest_data
#         ON line_count.device_id = latest_data.device_id
#         AND line_count.timestamp = latest_data.latest_timestamp;
#     """
    
#     # クエリ実行
#     cursor.execute(query)

#     # 結果を取得
#     rows = cursor.fetchall()

#     # 結果を格納する変数
#     device_people_list = []  # デバイスIDと人数を格納するリスト

#     # device_id と人数をセットで格納
#     for row in rows:
#         device_id = row[0]  # device_id
#         people_inside = row[2]  # people_inside

#         # 結果をリストにタプルとして格納
#         device_people_list.append((device_id, people_inside))

# except mysql.connector.Error as err:
#     st.error(f"Error: {err}")

# finally:
#     # 接続を閉じる
#     if db_connection.is_connected():
#         cursor.close()
#         db_connection.close()

# ------------------------マップ用のデータ作成（読み込み）------------------------

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

# 各施設に対応する device_id をマッピングする辞書
device_to_facility = {
    1: "学生食堂", 2: "トラスコンガーデン", 3: "1号館", 4: "2号館", 5: "3号館",
    6: "4号館", 7: "5号館", 8: "6号館", 9: "7号館", 10: "8号館", 11: "9号館", 
    12: "10号館", 13: "11号館", 14: "新11号館", 15: "12号館", 16: "14号館"
}

# 各施設ごとの最大収容人数
facility_capacity = {
    "学生食堂": 200,
    "トラスコンガーデン": 150,
    "1号館": 100,
    "2号館": 100,
    "3号館": 100,
    "4号館": 100,
    "5号館": 100,
    "6号館": 100,
    "7号館": 100,
    "8号館": 100,
    "9号館": 100,
    "10号館": 100,
    "11号館": 100,
    "新11号館": 100,
    "12号館": 100,
    "14号館": 100
}

campus_data["people_max"] = campus_data.index.map(lambda name: facility_capacity.get(name, 100))  # 最大収容人数設定

# 条件に基づくカスタムアイコン画像のパスを設定する関数
def get_icon_path(condition):
    if condition >= 0.8:
        return '153_000_000.png'     # condition>=80%: 赤(153, 0, 0)
    elif condition >= 0.6:
        return '255_051_051.png'     # condition>=60%: 赤(255, 51, 51)
    elif condition >= 0.4:
        return '255_153_153.png'     # condition>=40%: 赤(255, 153, 153)
    else:
        return '255_230_230.png'     # condition<40%: 薄い赤

# データを地図に渡す関数
def AreaMarker(df, m):
    for index, r in df.iterrows():
        # 条件に基づいた画像アイコンパスを取得
        icon_path = get_icon_path(r['condition'])

        popup_content = f"""
        <div style="width:200px;">
            <strong>{index}</strong><br>
            人数: {r['people_inside']}人<br>
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

# 各施設に対応する `device_id` と `people_inside` をキャンパスマップに反映
for device_id, people_inside in device_people_list:
    # device_id を使って施設名を取得
    device_id_number = int(device_id.split('-')[0])  # "1-people-count" から "1" を取り出す
    
    facility_name = device_to_facility.get(device_id_number)
    
    if facility_name:
        campus_data.loc[facility_name, 'people_inside'] = people_inside
        campus_data.loc[facility_name, 'condition'] = people_inside / campus_data.loc[facility_name, 'people_max']  # 最大収容人数に対する比率を計算

# ------------------------サブタイトル------------------------

# カラーバーを作成する関数
def create_colorbar():
    fig, ax = plt.subplots(figsize=(2.3, 0.05))  # サイズを横長に設定
    cmap = plt.get_cmap('Reds')
    norm = plt.Normalize(0, 1)
    cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax, orientation='horizontal')  # 横向き
    cbar.ax.set_xticklabels([0, 25, 50, 75, "100(%)"], fontsize=5)  
    plt.close(fig)
    return fig

# ------------------------画面作成------------------------

# タイトル
st.title("キャンパスマップ")

# カラーバーを表示
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

# データを地図に渡す
AreaMarker(campus_data, m)

# 地図を表示
folium_static(m, width=300, height=400)

# リロードボタンの追加
if st.button("リロード"):
    # 状態管理
    st.session_state.updated = False  # 地図を再初期化

# 最後の更新時刻を表示
st.write(f"最終更新時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

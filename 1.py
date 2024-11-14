import mysql.connector

try:
    # MySQLへの接続設定
    db_connection = mysql.connector.connect(
        host="seikeidb.mysql.database.azure.com",  # データベースホスト
        user="soc5admin",                          # ユーザー名
        password="eat5Mae\\ze",                    # パスワード
        database="campusOS"                        # データベース名
    )
    cursor = db_connection.cursor()

    # 最新のデータを取得するSQLクエリ
    query = """
        SELECT line_count.device_id, line_count.timestamp, line_count.people_inside
        FROM line_count
        JOIN (
            SELECT device_id, MAX(timestamp) AS latest_timestamp
            FROM line_count
            GROUP BY device_id
        ) AS latest_data
        ON line_count.device_id = latest_data.device_id
        AND line_count.timestamp = latest_data.latest_timestamp;
    """
    
    # クエリ実行
    cursor.execute(query)

    # 結果を取得
    rows = cursor.fetchall()

    # device_id と人数をセットで表示
    device_people_dict = {}
    for row in rows:
        device_id = row[0]  # device_id
        people_inside = row[2]  # people_inside

        # device_id と人数をセットにして辞書に格納
        device_people_dict[device_id] = people_inside

    # 結果を表示
    # print("Device ID . 人数のセット:")
    # for device_id, people_inside in device_people_dict.items():
        # print(f"Device ID: {device_id}, People Inside: {people_inside}")
        print(f"{device_id}, {people_inside}")
        
except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # 接続を閉じる
    if db_connection.is_connected():
        cursor.close()
        db_connection.close()




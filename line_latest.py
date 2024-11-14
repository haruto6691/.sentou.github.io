import mysql.connector

try:
    db_connection = mysql.connector.connect(
        host="seikeidb.mysql.database.azure.com",
        user="soc5admin",
        password="eat5Mae\ze",
        database="campusOS"
    )
    cursor = db_connection.cursor()

    # データ挿入クエリ
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
    
    cursor.execute(query)

    # 結果を取得
    rows = cursor.fetchall()

    # 取得したデータを表示
    for row in rows:
        print(row)
        print(f"Device ID: {row[0]}, Timestamp: {row[1]}, People Inside: {row[2]}")
        print(row[1])

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # 接続を閉じる
    if db_connection.is_connected():
        cursor.close()
        db_connection.close()
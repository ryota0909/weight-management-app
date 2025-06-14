import streamlit as st
from datetime import date
import csv
import os
import pandas as pd

# アプリのタイトルを設定
st.title("体重管理アプリ")

# 今日の日付を取得
today = date.today()

# 日付入力欄
input_date = st.date_input(
    "日付を選択してください",
    value=today
)

# 体重入力欄
weight = st.number_input(
    "体重（kg）を入力してください",
    min_value=0.0,
    max_value=300.0,
    value=60.0,
    step=0.1,
    format="%.1f"
)

# 記録ボタン
if st.button("記録する"):
    # データをCSVファイルに保存
    file_exists = os.path.exists('data.csv')
    
    if file_exists:
        # 既存のデータを読み込む
        df = pd.read_csv('data.csv')
        # 入力された日付のデータが存在するか確認
        date_exists = df['date'].astype(str).str.contains(str(input_date)).any()
        
        if date_exists:
            # 同じ日付のデータを更新
            df.loc[df['date'].astype(str) == str(input_date), 'weight'] = round(weight, 1)
            # 重複を削除
            df = df.drop_duplicates(subset=['date'], keep='last')
            # 更新したデータを保存
            df.to_csv('data.csv', index=False)
            st.success("データを更新しました！🔄")
        else:
            # 新しいデータを追加
            with open('data.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([input_date, round(weight, 1)])
            st.success("記録しました！🎉")
    else:
        # 新規ファイル作成
        with open('data.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'weight'])
            writer.writerow([input_date, round(weight, 1)])
        st.success("記録しました！🎉")

# データの可視化
if os.path.exists('data.csv'):
    # CSVファイルを読み込む
    df = pd.read_csv('data.csv')
    
    # データが1件以上ある場合のみグラフを表示
    if len(df) > 0:
        # 日付列をdatetime型に変換
        df['date'] = pd.to_datetime(df['date'])
        # 日付でソート
        df = df.sort_values('date')
        
        # グラフのタイトルを設定
        st.subheader("体重の推移")
        # 折れ線グラフを表示
        st.line_chart(df.set_index('date')['weight'])

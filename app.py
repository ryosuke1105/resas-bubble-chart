import pandas as pd
import plotly.express as px
import streamlit as st

# ページの設定
st.set_page_config(page_title="地域経済バブルチャート", layout="wide")

st.title("都市別 経済循環率シミュレーター")

# 1. CSVファイルを読み込む
@st.cache_data # データをキャッシュして高速化
def load_data():
    return pd.read_csv('raw.csv', encoding='utf-8-sig')

try:
    df = load_data()

    # 2. 都市を選択するサイドバー
    st.sidebar.header("表示設定")
    all_cities = df['都市名'].unique().tolist()
    
    # 最初に表示しておくデフォルトの都市（空にしてもOK）
    default_selection = all_cities[:5] 
    
    selected_cities = st.sidebar.multiselect(
        "表示したい都市名を選択してください",
        options=all_cities,
        default=default_selection
    )

    # 3. 選択された都市だけにデータを絞り込む
    df_filtered = df[df['都市名'].isin(selected_cities)]

    # 4. バブルチャートの作成
    if not df_filtered.empty:
        fig = px.scatter(
            df_filtered, 
            x="地域経済循環率(2022)",
            y="民間消費支出流出率(2022)",
            size="人口（2025）",
            color="地方",
            text="都市名",
            hover_name="都市名",
            title="選択した都市の比較",
            size_max=60,
            height=600
        )

        fig.update_traces(textposition='middle center')
        fig.update_layout(showlegend=True, template="plotly_white")

        # グラフを表示
        st.plotly_chart(fig, use_container_width=True)
        
        # 5. 表も表示（おまけ）
        st.write("### 選択された都市のデータ一覧")
        st.dataframe(df_filtered)
    else:
        st.warning("左側のサイドバーから都市を選択してください。")

except Exception as e:
    st.error(f"エラーが発生しました: {e}")
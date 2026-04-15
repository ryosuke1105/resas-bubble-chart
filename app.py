import pandas as pd
import plotly.express as px
import streamlit as st

# ページの設定
st.set_page_config(page_title="地域経済バブルチャート", layout="wide")

st.title("都市別 経済循環率シミュレーター")

# 1. CSVファイルを読み込む
@st.cache_data
def load_data():
    df = pd.read_csv('raw.csv', encoding='utf-8-sig')
    # プログラム内で列名を「流出入率」に書き換えます
    df = df.rename(columns={'民間消費支出流出率(2022)': '民間消費の支出流出入率(2022)'})
    return df

try:
    df = load_data()

    # --- 注釈セクション ---
    st.info("""
    ### 📊 グラフの見方と注釈
    * **バブルの大きさ**: 各都市の **人口（2025年推計）** の多さに比例して大きくなります。
    * **横軸：地域経済循環率**: 
        * **100%以上**: 域外から稼ぐ力が高い状態です。
        * **100%以下**: 地域外や補助金に依存している傾向にあります。
        * **適正範囲**: **95%～105%** が経済循環として適正と言われています。
        * **90%以下**: 稼ぐ力が不足している。
    * **縦軸：民間消費の支出流出入率**: 
        * 数値が **プラス（+）** であれば、地域外からの消費の流入が多いことを示します。
    """)

    # 2. 都市を選択するサイドバー
    st.sidebar.header("表示設定")
    all_cities = df['都市名'].unique().tolist()
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
            y="民間消費の支出流出入率(2022)",      # 新しい表記を使用
            size="人口（2025）",
            color="地方",
            text="都市名",
            hover_name="都市名",
            title="地域経済循環の分析比較",
            size_max=60,
            height=600
        )

        # 循環率100%の基準線
        fig.add_vline(x=100, line_dash="dash", line_color="red", annotation_text="循環率100%基準")
        # 適正範囲の背景色
        fig.add_vrect(x0=95, x1=105, line_width=0, fillcolor="green", opacity=0.1, annotation_text="適正範囲")

        fig.update_traces(textposition='middle center')
        fig.update_layout(
            xaxis_title="地域経済循環率(2022) [%]",
            yaxis_title="民間消費の支出流出入率(2022) [%]", # 新しい表記を使用
            showlegend=True, 
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)
        
        # 5. データ一覧表
        st.write("### 選択された都市のデータ一覧")
        st.dataframe(df_filtered)
    else:
        st.warning("左側のサイドバーから都市を選択してください。")

except Exception as e:
    st.error(f"エラーが発生しました: {e}")

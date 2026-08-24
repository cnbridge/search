import os
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("エラー: Supabaseの環境変数が設定されていません。")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ページレイアウトの設定
st.set_page_config(page_title="中国IC 代替・インサイト検索", page_icon="🇨🇳", layout="wide")

st.title("🇨🇳 中国IC 代替・インサイト検索ポータル")
st.markdown("蓄積された中国製ICのスペック、欧米代替型番、ファームウェア実装インサイトを瞬時に検索できます。")

# 検索窓
query = st.text_input("🔍 型番・メーカー・キーワードで検索（例: SC5617F, Southchip, Bluetooth）", "")

if st.button("検索実行", type="primary"):
    with st.spinner("データベースから検索中..."):
        # Supabaseから全データを取得
        response = supabase.table("ic_components").select("*").execute()
        data = response.data
        
        # キーワードフィルタリング
        if query:
            q = query.lower()
            filtered = [
                row for row in data 
                if q in str(row.get('part_number', '')).lower() 
                or q in str(row.get('manufacturer', '')).lower() 
                or q in str(row.get('description_jp', '')).lower()
                or q in str(row.get('alternative_to', '')).lower()
                or q in str(row.get('fw_insights', '')).lower()
            ]
        else:
            filtered = data

        st.success(f"🎉 **{len(filtered)} 件** のパーツが見つかりました！")

        # 結果をカード形式で表示
        for item in filtered:
            part = item.get('part_number', '不明')
            maker = item.get('manufacturer', '不明')
            
            with st.expander(f"📦 【{maker}】 {part}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**📝 概要**: {item.get('description_jp', '未記載')}")
                    st.markdown(f"**🔄 欧米代替候補**: `{item.get('alternative_to', '未記載')}`")
                    st.markdown(f"**⚙️ スペック**: `{item.get('specifications', '未記載')}`")
                    
                with col2:
                    url = item.get('url')
                    if url:
                        st.markdown(f"[🔗 公式製品ページを見る]({url})")
                        
                st.markdown("---")
                st.markdown("**🛠️ ファームウェア実装インサイト (FW Insights)**")
                st.info(item.get('fw_insights', 'インサイトがありません'))
else:
    st.info("💡 上の検索窓にキーワード（型番やメーカー名など）を入力して「検索実行」を押してください。")
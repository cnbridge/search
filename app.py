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
st.set_page_config(page_title="CN Bridge - 中国IC・代替品 検索ポータル", page_icon="🇨🇳", layout="wide")

# ==========================================
# 🎨 ホームページ（cn-bridge.com）と完全に調和させるカスタムCSS
# ==========================================
st.markdown("""
<style>
    /* 全体の背景とフォント（ホームページと統一） */
    .stApp {
        background-color: #0c1117;
        color: #aeb2b9;
        font-family: 'Open Sans', sans-serif;
    }
    
    /* 見出しのデザイン */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif !important;
        color: #e0e6ec !important;
    }
    
    /* 検索入力フィールド */
    .stTextInput input {
        background-color: #0c1117 !important;
        color: #e0e6ec !important;
        border: 1px solid #2e3a47 !important;
        border-radius: 5px !important;
        padding: 12px 15px !important;
    }
    .stTextInput input:focus {
        border-color: #009944 !important;
        box-shadow: 0 0 0 3px rgba(0, 153, 68, 0.2) !important;
    }
    
    /* 検索ボタン（HPのボタンと完全一致） */
    .stButton button {
        background-color: #009944 !important;
        color: #ffffff !important;
        border: 2px solid #009944 !important;
        border-radius: 5px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease-in-out !important;
        width: 100%;
    }
    .stButton button:hover {
        background-color: transparent !important;
        color: #00cc55 !important;
        border-color: #00cc55 !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 153, 68, 0.3);
    }

    /* 結果カード（HPの maker-card / service-card 風） */
    div.streamlit-expanderHeader {
        background-color: #1a2230 !important;
        color: #e0e6ec !important;
        border: 1px solid #2e3a47 !important;
        border-top: 4px solid #009944 !important;
        border-radius: 8px !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
    }
    div.streamlit-expanderContent {
        background-color: #1a2230 !important;
        color: #aeb2b9 !important;
        border: 1px solid #2e3a47 !important;
        border-top: none !important;
        border-bottom-left-radius: 8px !important;
        border-bottom-right-radius: 8px !important;
    }

    /* インフォメーションボックス */
    .stAlert {
        background-color: #1a2230 !important;
        color: #e0e6ec !important;
        border: 1px solid #2e3a47 !important;
        border-left: 4px solid #009944 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# 検索アプリのUI本体
st.title("🇨🇳 中国IC 代替・インサイト検索ポータル")
st.markdown("データベースに蓄積された中国製半導体・電子部品のスペック、欧米代替型番、FWインサイトをリアルタイムで検索できます。")

query = st.text_input("🔍 型番・メーカー・キーワードで検索（例: SC5617F, Southchip, Bluetooth）", "")

if st.button("検索実行"):
    with st.spinner("データベースから検索中..."):
        response = supabase.table("ic_components").select("*").execute()
        data = response.data
        
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

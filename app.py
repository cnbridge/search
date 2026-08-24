import os
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Error: Supabase environment variables are not set.")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ページレイアウトの設定（モバイル対応のためのviewportはStreamlitが自動設定します）
st.set_page_config(page_title="CN Bridge - IC Search Portal", page_icon="🇨🇳", layout="wide")

# ==========================================
# 🌐 多言語対応 (i18n) 辞書
# ==========================================
translations = {
    "日本語": {
        "title": "🇨🇳 中国IC・代替品 検索ポータル",
        "desc": "データベースに蓄積された中国製半導体・電子部品のスペック、欧米代替型番、FWインサイトをリアルタイムで検索できます。",
        "search_label": "🔍 型番・メーカー・キーワードで検索（例: SC5617F, Southchip, Bluetooth）",
        "btn_search": "検索実行",
        "searching": "データベースから検索中...",
        "found": "件のパーツが見つかりました！",
        "overview": "📝 概要",
        "alt": "🔄 欧米代替候補",
        "spec": "⚙️ スペック",
        "link": "🔗 公式製品ページを見る",
        "fw_title": "🛠️ ファームウェア実装インサイト (FW Insights)",
        "no_fw": "インサイトがありません",
        "empty": "💡 上の検索窓にキーワード（型番やメーカー名など）を入力して「検索実行」を押してください。",
        "unlisted": "未記載",
        "unknown": "不明"
    },
    "English": {
        "title": "🇨🇳 China IC & Alternative Search",
        "desc": "Search specs, Western alternative part numbers, and FW insights for Chinese semiconductor components in real-time.",
        "search_label": "🔍 Search by Part No, Maker, or Keyword (e.g., SC5617F, Southchip)",
        "btn_search": "Search",
        "searching": "Searching database...",
        "found": "components found!",
        "overview": "📝 Overview",
        "alt": "🔄 Western Alternatives",
        "spec": "⚙️ Specs",
        "link": "🔗 Official Product Page",
        "fw_title": "🛠️ Firmware Insights (FW Insights)",
        "no_fw": "No insights available.",
        "empty": "💡 Enter a keyword in the search box above and click 'Search'.",
        "unlisted": "N/A",
        "unknown": "Unknown"
    },
    "中文": {
        "title": "🇨🇳 中国IC及替代品搜索门户",
        "desc": "实时搜索数据库中积累的中国制半导体及电子元器件的规格、欧美替代型号及固件洞察。",
        "search_label": "🔍 按型号、制造商或关键字搜索（例: SC5617F, Southchip）",
        "btn_search": "搜索执行",
        "searching": "正在搜索数据库...",
        "found": "个零件已找到！",
        "overview": "📝 概述",
        "alt": "🔄 欧美替代型号",
        "spec": "⚙️ 规格",
        "link": "🔗 查看官方产品页面",
        "fw_title": "🛠️ 固件实现洞察 (FW Insights)",
        "no_fw": "暂无洞察信息",
        "empty": "💡 请在上方搜索框中输入关键字，然后点击“搜索执行”。",
        "unlisted": "未记载",
        "unknown": "未知"
    }
}

# 言語選択UI (右上に小さく配置)
col_spacer, col_lang = st.columns([4, 1])
with col_lang:
    lang = st.selectbox("Language / 言語", ["日本語", "English", "中文"], label_visibility="collapsed")
t = translations[lang]

# ==========================================
# 🎨 究極のカスタムCSS (親サイト同化 ＆ スマホ最適化)
# ==========================================
st.markdown("""
<style>
    /* 1. Streamlit特有の不要なUI（ヘッダー、フッター、メニュー）を完全に隠す */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 2. 背景を親サイトのダークテーマと完全に一体化 */
    .stApp {
        background-color: transparent !important; /* iframe側で背景色を持つため透明に */
        color: #aeb2b9;
        font-family: 'Open Sans', 'Hiragino Kaku Gothic ProN', sans-serif;
    }
    
    /* 3. 見出しのデザイン */
    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif !important;
        color: #e0e6ec !important;
        font-weight: 700 !important;
    }
    
    /* 4. 検索入力フィールド（スマホでタップ時にズームしないよう font-size: 16px を強制） */
    .stTextInput input {
        background-color: #0c1117 !important;
        color: #e0e6ec !important;
        border: 1px solid #2e3a47 !important;
        border-radius: 8px !important;
        padding: 15px !important;
        font-size: 16px !important; 
        transition: all 0.3s ease;
    }
    .stTextInput input:focus {
        border-color: #009944 !important;
        box-shadow: 0 0 0 3px rgba(0, 153, 68, 0.2) !important;
    }
    
    /* 5. 検索ボタン（親サイトの .btn-primary と完全一致） */
    .stButton button {
        background-color: #009944 !important;
        color: #ffffff !important;
        border: 2px solid #009944 !important;
        border-radius: 5px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease-in-out !important;
        width: 100%;
        padding: 10px 0 !important;
        height: auto !important;
    }
    .stButton button:hover {
        background-color: transparent !important;
        color: #00cc55 !important;
        border-color: #00cc55 !important;
        transform: translateY(-2px);
    }

    /* 6. 結果カード（アコーディオン）を親サイトのカードデザインに合わせる */
    div[data-testid="stExpander"] {
        background-color: #1a2230 !important;
        border: 1px solid #2e3a47 !important;
        border-top: 4px solid #009944 !important;
        border-radius: 10px !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
        margin-bottom: 15px !important;
        overflow: hidden;
    }
    div[data-testid="stExpander"] details summary {
        color: #e0e6ec !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 15px !important;
    }
    div[data-testid="stExpander"] details summary:hover {
        color: #00cc55 !important;
    }
    
    /* 7. アラート（Info/Success）のデザイン */
    .stAlert {
        background-color: rgba(0, 153, 68, 0.1) !important;
        color: #e0e6ec !important;
        border: 1px solid #009944 !important;
        border-radius: 8px !important;
    }

    /* 8. スマホ用レスポンシブ調整 */
    @media (max-width: 768px) {
        h1 { font-size: 1.8rem !important; }
        .stButton button { padding: 15px 0 !important; font-size: 18px !important; }
        div[data-testid="stExpander"] details summary { font-size: 1rem !important; padding: 10px !important; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔍 検索アプリ UI本体
# ==========================================
st.title(t["title"])
st.markdown(t["desc"])

query = st.text_input(t["search_label"], "")

if st.button(t["btn_search"]):
    with st.spinner(t["searching"]):
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

        if lang == "English":
            st.success(f"🎉 **{len(filtered)}** {t['found']}")
        else:
            st.success(f"🎉 **{len(filtered)}** {t['found']}")

        for item in filtered:
            part = item.get('part_number', t['unknown'])
            maker = item.get('manufacturer', t['unknown'])
            
            with st.expander(f"📦 【{maker}】 {part}"):
                # スマホでは縦並び、PCでは横並びになるよう st.columns を設定
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**{t['overview']}**: {item.get('description_jp', t['unlisted'])}")
                    st.markdown(f"**{t['alt']}**: `{item.get('alternative_to', t['unlisted'])}`")
                    st.markdown(f"**{t['spec']}**: `{item.get('specifications', t['unlisted'])}`")
                    
                with col2:
                    url = item.get('url')
                    if url:
                        st.markdown(f"[{t['link']}]({url})")
                        
                st.markdown("---")
                st.markdown(f"**{t['fw_title']}**")
                
                # FWインサイトの有無で表示を切り替え
                fw_info = item.get('fw_insights')
                if fw_info and fw_info.strip():
                    st.info(fw_info)
                else:
                    st.markdown(f"*{t['no_fw']}*")
else:
    st.info(t["empty"])
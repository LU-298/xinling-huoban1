"""
心灵伙伴 - 治愈系数字人 🌱
"""
import streamlit as st

st.set_page_config(page_title="心灵伙伴", page_icon="🌱", layout="wide")

# 从secrets读取密钥（安全）
API_KEY = st.secrets["deepseek_api_key"]
API_URL = "https://api.deepseek.com"

ROBOT_URL = "https://coze-coding-project.tos.coze.site/coze_storage_7625532895788105770/xinling-final_59700879.png?sign=1778082165-3b01ccf181-0-323dc1ef2f95cdbfc54e8e2822331e352df0fbaadf8bb23f2919eca77281dc79"

def get_ai_response(user_msg):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEY, base_url=API_URL)
        
        system_prompt = "你是心灵伙伴，温暖的AI助手。像朋友一样聊天，回复简洁，用emoji。"
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=100,
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"连接有问题呢... 💭 {str(e)[:50]}"

EMOTIONS = {
    "happy": {"name": "开心", "emoji": "😊"},
    "sad": {"name": "难过", "emoji": "😢"},
    "surprised": {"name": "惊讶", "emoji": "😲"},
    "confused": {"name": "困惑", "emoji": "🤔"},
    "thinking": {"name": "思考", "emoji": "🤨"},
    "angry": {"name": "生气", "emoji": "😤"},
    "loving": {"name": "温暖", "emoji": "🥰"},
    "neutral": {"name": "平静", "emoji": "🤗"}
}

EMOTION_MAP = {
    "happy": ["开心", "高兴", "快乐", "棒", "太好了", "幸福", "哈哈", "嘻嘻"],
    "sad": ["难过", "伤心", "痛苦", "哭", "累", "悲伤", "郁闷", "不开心"],
    "surprised": ["惊讶", "哇", "什么", "不会吧", "真的"],
    "confused": ["困惑", "不懂", "不知道", "迷茫", "怎么办"],
    "thinking": ["想", "思考", "考虑"],
    "angry": ["生气", "愤怒", "烦", "气死了", "讨厌"],
    "loving": ["爱", "喜欢", "想你", "谢谢", "温暖", "感动", "爱你"]
}

def detect_emotion(text):
    for emotion, keywords in EMOTION_MAP.items():
        for kw in keywords:
            if kw in text:
                return emotion
    return "neutral"

# 语音
st.components.v1.html("""
<script>
function speakText(text) {
    if ('speechSynthesis' in window) {
        speechSynthesis.cancel();
        var u = new SpeechSynthesisUtterance(text);
        u.lang = 'zh-CN';
        u.rate = 0.95;
        speechSynthesis.speak(u);
    }
}
</script>
""", height=0)

# CSS
st.markdown("""
<style>
.stApp { background: linear-gradient(180deg, #e8f5e9 0%, #c8e6c9 100%); font-family: 'Noto Sans SC', sans-serif; }
.top-section { text-align: center; padding: 20px; background: linear-gradient(135deg, #4CAF50, #66BB6A); border-radius: 0 0 30px 30px; margin-bottom: 20px; box-shadow: 0 5px 30px rgba(76,175,80,0.3); }
.avatar-container { width: 160px; height: 160px; margin: 0 auto; border-radius: 50%; overflow: hidden; border: 5px solid white; box-shadow: 0 10px 40px rgba(0,0,0,0.3); }
.avatar-img { width: 100%; height: 100%; object-fit: cover; animation: idle 4s ease-in-out infinite; }
@keyframes idle { 0%,100% { transform: scale(1); } 50% { transform: scale(1.03); } }
.robot-name { color: white; font-size: 24px; font-weight: bold; margin-top: 15px; }
.emotion-badge { display: inline-block; padding: 6px 16px; background: rgba(255,255,255,0.3); border-radius: 20px; color: white; font-size: 14px; margin-top: 10px; }
.chat-container { max-width: 600px; margin: 0 auto; background: white; border-radius: 25px; box-shadow: 0 10px 50px rgba(0,0,0,0.1); overflow: hidden; }
.chat-messages { height: 350px; overflow-y: auto; padding: 20px; background: #f8faf8; }
.msg { margin-bottom: 15px; animation: slideIn 0.3s ease; }
@keyframes slideIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
.msg-content { display: inline-block; max-width: 80%; padding: 12px 16px; border-radius: 18px; font-size: 14px; line-height: 1.5; }
.msg.user .msg-content { background: linear-gradient(135deg, #4CAF50, #45a049); color: white; border-bottom-right-radius: 4px; }
.msg.bot .msg-content { background: white; color: #333; border-bottom-left-radius: 4px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }
.msg-avatar { width: 30px; height: 30px; border-radius: 50%; vertical-align: middle; margin-right: 8px; }
.input-section { padding: 15px 20px; background: white; border-top: 1px solid #eee; display: flex; gap: 10px; }
.input-box { flex: 1; border: none !important; border-radius: 25px !important; padding: 14px 20px !important; background: #f5f5f5 !important; font-size: 14px !important; }
.send-btn { background: linear-gradient(135deg, #4CAF50, #45a049) !important; color: white !important; border: none !important; border-radius: 50% !important; width: 48px !important; height: 48px !important; font-size: 20px !important; }
</style>
""", unsafe_allow_html=True)

# 初始化
if "msgs" not in st.session_state:
    st.session_state.msgs = [{"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n有什么想和我聊聊的吗？"}]
if "cur_emotion" not in st.session_state:
    st.session_state.cur_emotion = "neutral"

# 顶部
e = EMOTIONS[st.session_state.cur_emotion]
st.markdown(f"""
<div class="top-section">
    <div class="avatar-container">
        <img src="{ROBOT_URL}" class="avatar-img" />
    </div>
    <div class="robot-name">🌱 心灵伙伴</div>
    <div class="emotion-badge">{e["emoji"]} {e["name"]}</div>
</div>
""", unsafe_allow_html=True)

# 聊天
st.markdown('<div class="chat-container"><div class="chat-messages">', unsafe_allow_html=True)
for msg in st.session_state.msgs:
    if msg["role"] == "user":
        st.markdown(f'<div class="msg user"><div class="msg-content">👤 {msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="msg bot"><img src="{ROBOT_URL}" class="msg-avatar" /><div class="msg-content">🤖 {msg["content"]}</div></div>', unsafe_allow_html=True)
st.markdown('</div><div class="input-section">', unsafe_allow_html=True)

user_input = st.text_input("", placeholder="说点什么吧...", label_visibility="collapsed", key="input")
col1, col2 = st.columns([1, 8])
with col1:
    clear = st.button("🗑️", key="clear")
with col2:
    send = st.button("➤", key="send")

st.markdown('</div></div>', unsafe_allow_html=True)

# 发送
if send and user_input.strip():
    st.session_state.msgs.append({"role": "user", "content": user_input.strip()})
    emotion = detect_emotion(user_input)
    st.session_state.cur_emotion = emotion
    
    with st.spinner("🤔 思考中..."):
        response = get_ai_response(user_input)
    
    st.session_state.msgs.append({"role": "bot", "content": response})
    
    # 朗读
    clean_text = response.replace("\n", " ").replace('"', "'")
    st.markdown(f'<script>speakText("{clean_text}");</script>', unsafe_allow_html=True)
    
    st.rerun()

# 清空
if clear:
    st.session_state.msgs = [{"role": "bot", "content": "好的，重新开始吧！🌱\n\n有什么想聊的？"}]
    st.session_state.cur_emotion = "neutral"
    st.rerun()

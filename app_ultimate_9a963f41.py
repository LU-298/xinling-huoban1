"""
心灵伙伴 - 治愈系数字人 🌱
精致版 - 数字人在上方 + 说话动画
"""
import streamlit as st

st.set_page_config(
    page_title="心灵伙伴",
    page_icon="🌱",
    layout="wide"
)

# DeepSeek API
API_KEY = "sk-eb28d368d6054551bad7e34daac57efd"
API_URL = "https://api.deepseek.com"

# 数字人图片
ROBOT_URL = "https://coze-coding-project.tos.coze.site/coze_storage_7625532895788105770/xinling-final_59700879.png?sign=1778081821-0f364dcbeb-0-279e3c1a7d0436b7f5bda5fe9dbeb3cad8e6ec011583788e11e9794523fada79"

def get_ai_response(user_msg, emotion):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEY, base_url=API_URL)
        system_prompt = """你是"心灵伙伴"，温暖的AI心理健康陪伴助手。

性格：像朋友聊天、善于倾听、回复简洁30-50字、用emoji亲切交流。
当前感知用户情绪：{}""".format(emotion)

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=150,
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"连接有点问题呢... 💭 {str(e)[:30]}"

# 情绪
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
    "surprised": ["惊讶", "哇", "什么", "不会吧", "真的", "太神奇"],
    "confused": ["困惑", "不懂", "不知道", "迷茫", "怎么办"],
    "thinking": ["想", "思考", "考虑", "琢磨"],
    "angry": ["生气", "愤怒", "烦", "气死了", "讨厌"],
    "loving": ["爱", "喜欢", "想你", "谢谢", "温暖", "感动", "爱你"]
}

def detect_emotion(text):
    for emotion, keywords in EMOTION_MAP.items():
        for kw in keywords:
            if kw in text:
                return emotion
    return "neutral"

# 语音JS
st.components.v1.html("""
<script>
let currentAudio = null;
function speakText(text) {
    if ('speechSynthesis' in window) {
        speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'zh-CN';
        u.rate = 0.95;
        u.pitch = 1.1;
        speechSynthesis.speak(u);
        // 通知数字人开始说话
        const robot = window.parent.document.querySelector('.avatar-container');
        if (robot) robot.classList.add('speaking');
        u.onend = () => {
            if (robot) robot.classList.remove('speaking');
        };
    }
}
</script>
""", height=0)

# CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #e8f5e9 0%, #c8e6c9 100%);
    font-family: 'Noto Sans SC', sans-serif;
}

/* 顶部数字人区域 */
.top-section {
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #4CAF50, #66BB6A);
    border-radius: 0 0 30px 30px;
    margin-bottom: 20px;
    box-shadow: 0 5px 30px rgba(76, 175, 80, 0.3);
}

.avatar-container {
    width: 160px;
    height: 160px;
    margin: 0 auto;
    border-radius: 50%;
    overflow: hidden;
    border: 5px solid white;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    position: relative;
}

.avatar-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    animation: idle 4s ease-in-out infinite;
}

@keyframes idle {
    0%, 100% { transform: scale(1) translateY(0); }
    50% { transform: scale(1.03) translateY(-3px); }
}

/* 眨眼 */
.avatar-container.blink .avatar-img {
    animation: blink 0.2s ease-in-out;
}
@keyframes blink {
    0%, 100% { clip-path: inset(0 0 0 0); }
    50% { clip-path: inset(30% 0 30% 0); }
}

/* 说话动画 */
.avatar-container.speaking .avatar-img {
    animation: speak 0.4s ease-in-out infinite;
}
@keyframes speak {
    0%, 100% { transform: scale(1) translateY(0); }
    25% { transform: scale(1.02) translateY(-2px) rotate(-1deg); }
    75% { transform: scale(1.02) translateY(-2px) rotate(1deg); }
}

.robot-name {
    color: white;
    font-size: 24px;
    font-weight: bold;
    margin-top: 15px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.emotion-badge {
    display: inline-block;
    padding: 6px 16px;
    background: rgba(255,255,255,0.3);
    border-radius: 20px;
    color: white;
    font-size: 14px;
    margin-top: 10px;
}

/* 聊天容器 */
.chat-container {
    max-width: 600px;
    margin: 0 auto;
    background: white;
    border-radius: 25px;
    box-shadow: 0 10px 50px rgba(0,0,0,0.1);
    overflow: hidden;
}

.chat-header {
    background: linear-gradient(135deg, #4CAF50, #66BB6A);
    color: white;
    padding: 15px;
    text-align: center;
    font-size: 16px;
    font-weight: bold;
}

.chat-messages {
    height: 350px;
    overflow-y: auto;
    padding: 20px;
    background: #f8faf8;
}

.chat-messages::-webkit-scrollbar { width: 4px; }
.chat-messages::-webkit-scrollbar-thumb { background: #ccc; border-radius: 2px; }

/* 消息 */
.msg {
    margin-bottom: 15px;
    animation: slideIn 0.3s ease;
}
@keyframes slideIn {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

.msg.user { text-align: right; }
.msg.bot { text-align: left; }

.msg-content {
    display: inline-block;
    max-width: 80%;
    padding: 12px 16px;
    border-radius: 18px;
    font-size: 14px;
    line-height: 1.5;
    word-break: break-word;
}

.msg.user .msg-content {
    background: linear-gradient(135deg, #4CAF50, #45a049);
    color: white;
    border-bottom-right-radius: 4px;
}

.msg.bot .msg-content {
    background: white;
    color: #333;
    border-bottom-left-radius: 4px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

.msg-avatar {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    vertical-align: middle;
    margin-right: 8px;
}

/* 输入区 */
.input-section {
    padding: 15px 20px;
    background: white;
    border-top: 1px solid #eee;
    display: flex;
    gap: 10px;
    align-items: center;
}

.input-box {
    flex: 1;
    border: none !important;
    border-radius: 25px !important;
    padding: 14px 20px !important;
    background: #f5f5f5 !important;
    font-size: 14px !important;
    box-shadow: none !important;
}
.input-box:focus { outline: none !important; box-shadow: 0 0 0 3px rgba(76,175,80,0.2) !important; }

.send-btn {
    background: linear-gradient(135deg, #4CAF50, #45a049) !important;
    color: white !important;
    border: none !important;
    border-radius: 50% !important;
    width: 48px !important;
    height: 48px !important;
    font-size: 20px !important;
    box-shadow: 0 4px 15px rgba(76,175,80,0.4) !important;
}

.hint {
    text-align: center;
    color: #999;
    font-size: 12px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# 初始化
if "msgs" not in st.session_state:
    st.session_state.msgs = [
        {"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n很高兴认识你~有什么想和我聊聊的吗？", "emotion": "happy"}
    ]
if "cur_emotion" not in st.session_state:
    st.session_state.cur_emotion = "happy"
if "speaking" not in st.session_state:
    st.session_state.speaking = False

# 眨眼JS
st.components.v1.html("""
<script>
let blinkTimer = setInterval(() => {
    const avatar = window.parent.document.querySelector('.avatar-container');
    if (avatar && !avatar.classList.contains('speaking')) {
        avatar.classList.add('blink');
        setTimeout(() => avatar.classList.remove('blink'), 250);
    }
}, 4000);
</script>
""", height=0)

# 顶部数字人
e = EMOTIONS[st.session_state.cur_emotion]
speaking_class = "speaking" if st.session_state.get("speaking") else ""

st.markdown(f"""
<div class="top-section">
    <div class="avatar-container {speaking_class}" id="avatar">
        <img src="{ROBOT_URL}" class="avatar-img" />
    </div>
    <div class="robot-name">🌱 心灵伙伴</div>
    <div class="emotion-badge">{e["emoji"]} {e["name"]}</div>
</div>
""", unsafe_allow_html=True)

# 聊天容器
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# 消息区
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
for msg in st.session_state.msgs:
    if msg["role"] == "user":
        st.markdown(f'<div class="msg user"><div class="msg-content">👤 {msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="msg bot">
            <img src="{ROBOT_URL}" class="msg-avatar" />
            <div class="msg-content">🤖 {msg["content"]}</div>
        </div>
        ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 输入区
st.markdown('<div class="input-section">', unsafe_allow_html=True)
user_input = st.text_input("", placeholder="说点什么吧...", label_visibility="collapsed", key="input", classes="input-box")
col1, col2 = st.columns([1, 8])
with col1:
    clear = st.button("🗑️", key="clear")
with col2:
    send = st.button("➤", key="send", help="发送")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 提示
st.markdown('<div class="hint">💡 按 Enter 发送消息</div>', unsafe_allow_html=True)

# 发送
if send and user_input.strip():
    st.session_state.msgs.append({"role": "user", "content": user_input.strip()})
    emotion = detect_emotion(user_input)
    st.session_state.cur_emotion = emotion
    st.session_state.speaking = True
    
    with st.spinner("🤔 思考中..."):
        response = get_ai_response(user_input, emotion)
    
    st.session_state.msgs.append({"role": "bot", "content": response})
    
    # 朗读
    clean_text = response.replace("\n", " ").replace('"', "'")
    st.markdown(f'<script>speakText("{clean_text}");</script>', unsafe_allow_html=True)
    
    st.rerun()

# 清空
if clear:
    st.session_state.msgs = [{"role": "bot", "content": "好的，重新开始吧！🌱\n\n有什么想聊的？", "emotion": "neutral"}]
    st.session_state.cur_emotion = "neutral"
    st.session_state.speaking = False
    st.rerun()

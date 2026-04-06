"""
心灵伙伴 - 治愈系数字人 🌱
简洁版 - 微信风格聊天界面 + 数字人动画
"""
import streamlit as st

st.set_page_config(
    page_title="心灵伙伴",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# DeepSeek API配置
API_KEY = "sk-2334cff883c94f61a5dcd16d46baf550"
API_URL = "https://api.deepseek.com"

# 图片URL
ROBOT_URL = "https://coze-coding-project.tos.coze.site/coze_storage_7625532895788105770/xinling-robot-new_4717d399.png?sign=1778081432-b1139ebdab-0-87b83e81fa31056a1cb714d00be92085e5755223e2f5e2d4d3c809a18e084708"

def get_ai_response(user_msg, emotion):
    """调用DeepSeek API"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEY, base_url=API_URL)
        system_prompt = """你是"心灵伙伴"，一个温暖、善良的AI心理健康陪伴助手。

性格特点：
- 像朋友一样聊天，亲切自然
- 善于倾听，感知情绪
- 回复简洁温馨，30-50字
- 用emoji增加亲切感
- 当前感知到用户情绪：{}""".format(emotion)

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=200,
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"抱歉，连接有问题呢... 💭"

# 情绪配置
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
function speakText(text) {
    if ('speechSynthesis' in window) {
        speechSynthesis.cancel();
        var u = new SpeechSynthesisUtterance(text);
        u.lang = 'zh-CN';
        u.rate = 0.95;
        u.pitch = 1.1;
        speechSynthesis.speak(u);
    }
}
</script>
""", height=0)

# CSS样式
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');

.stApp {
    background: linear-gradient(180deg, #f0f7f0 0%, #e8f5e9 100%);
    font-family: 'Noto Sans SC', -apple-system, sans-serif;
}

.main-container {
    max-width: 480px;
    margin: 0 auto;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background: white;
    box-shadow: 0 0 40px rgba(0,0,0,0.1);
}

/* 顶部 */
.header {
    padding: 15px 20px;
    background: linear-gradient(135deg, #4CAF50, #66BB6A);
    color: white;
    text-align: center;
}

.robot-box {
    width: 100px;
    height: 100px;
    margin: 10px auto;
    border-radius: 50%;
    overflow: hidden;
    box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    border: 3px solid white;
}

.robot-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    animation: breathe 3s ease-in-out infinite;
}

@keyframes breathe {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.robot-box.speaking .robot-img {
    animation: speaking 0.3s ease-in-out infinite;
}

@keyframes speaking {
    0%, 100% { transform: scale(1) translateY(0); }
    50% { transform: scale(1.02) translateY(-2px); }
}

.robot-box.blink .robot-img {
    animation: blink 0.2s ease-in-out;
}

@keyframes blink {
    0%, 100% { clip-path: inset(0 0 0 0); }
    50% { clip-path: inset(35% 0 35% 0); }
}

.emotion-tag {
    display: inline-block;
    padding: 4px 12px;
    background: rgba(255,255,255,0.25);
    border-radius: 20px;
    font-size: 12px;
}

/* 聊天区 */
.chat-area {
    flex: 1;
    overflow-y: auto;
    padding: 15px;
    background: #f5f5f5;
}

.chat-area::-webkit-scrollbar { width: 4px; }
.chat-area::-webkit-scrollbar-thumb { background: #ccc; border-radius: 2px; }

/* 消息 */
.message {
    margin-bottom: 12px;
    display: flex;
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.message.user { justify-content: flex-end; }
.message.bot { justify-content: flex-start; }

.bubble {
    max-width: 75%;
    padding: 10px 14px;
    border-radius: 18px;
    font-size: 14px;
    line-height: 1.5;
    word-break: break-word;
}

.message.user .bubble {
    background: linear-gradient(135deg, #4CAF50, #45a049);
    color: white;
    border-bottom-right-radius: 4px;
}

.message.bot .bubble {
    background: white;
    color: #333;
    border-bottom-left-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.bot-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    margin-right: 8px;
    align-self: flex-end;
}

/* 输入区 */
.input-area {
    padding: 12px 15px;
    background: white;
    border-top: 1px solid #eee;
    display: flex;
    gap: 10px;
    align-items: center;
}

.input-field {
    flex: 1;
    border: none !important;
    border-radius: 25px !important;
    padding: 12px 18px !important;
    background: #f0f0f0 !important;
    font-size: 14px !important;
    box-shadow: none !important;
}

.input-field:focus { outline: none !important; }

.send-btn {
    background: linear-gradient(135deg, #4CAF50, #45a049) !important;
    color: white !important;
    border: none !important;
    border-radius: 50% !important;
    width: 44px !important;
    height: 44px !important;
    font-size: 18px !important;
}

.clear-btn {
    background: #f5f5f5 !important;
    color: #666 !important;
    border: none !important;
    border-radius: 15px !important;
    padding: 8px 14px !important;
    font-size: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# 初始化
if "msgs" not in st.session_state:
    st.session_state.msgs = [
        {"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n有什么想和我聊聊的吗？", "emotion": "happy"}
    ]
if "cur_emotion" not in st.session_state:
    st.session_state.cur_emotion = "happy"
if "last_resp" not in st.session_state:
    st.session_state.last_resp = ""

# 眨眼动画
st.components.v1.html("""
<script>
setInterval(() => {
    const img = window.parent.document.querySelector('.robot-img');
    if (img) {
        img.parentElement.classList.add('blink');
        setTimeout(() => img.parentElement.classList.remove('blink'), 200);
    }
}, 3500);
</script>
""", height=0)

# 主界面
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# 顶部
e = EMOTIONS[st.session_state.cur_emotion]
st.markdown(f"""
<div class="header">
    <div style="font-size: 11px; opacity: 0.9;">🌱 心灵伙伴</div>
    <div class="robot-box">
        <img src="{ROBOT_URL}" class="robot-img" />
    </div>
    <div class="emotion-tag">{e["emoji"]} {e["name"]}</div>
</div>
""", unsafe_allow_html=True)

# 聊天区
st.markdown('<div class="chat-area">', unsafe_allow_html=True)

for msg in st.session_state.msgs:
    if msg["role"] == "user":
        st.markdown(f'<div class="message user"><div class="bubble">👤 {msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="message bot">
            <img src="{ROBOT_URL}" class="bot-avatar" />
            <div class="bubble">🤖 {msg["content"]}</div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 输入区
st.markdown('<div class="input-area">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 6])
with col1:
    clear = st.button("🗑️", key="clear", help="清空")
with col2:
    user_input = st.text_input("", placeholder="说点什么吧...", label_visibility="collapsed", key="input")
    send = st.button("➤", key="send", help="发送")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 发送处理
if send and user_input.strip():
    st.session_state.msgs.append({"role": "user", "content": user_input.strip(), "emotion": "user"})
    
    emotion = detect_emotion(user_input)
    st.session_state.cur_emotion = emotion
    
    with st.spinner("🤔"):
        response = get_ai_response(user_input, emotion)
    
    st.session_state.msgs.append({"role": "bot", "content": response, "emotion": emotion})
    st.session_state.last_resp = response
    
    clean_text = response.replace("\n", " ").replace('"', "'")
    st.markdown(f'<script>speakText("{clean_text}");</script>', unsafe_allow_html=True)
    st.rerun()

# 清空处理
if clear:
    st.session_state.msgs = [{"role": "bot", "content": "好的，重新开始吧！🌱\n\n有什么想聊的？", "emotion": "neutral"}]
    st.session_state.cur_emotion = "neutral"
    st.session_state.last_resp = ""
    st.rerun()

"""
心灵伙伴 - 治愈系数字人 🌱
精制豪华版 - 精美界面 · 神态生动 · 语音对话
"""
import streamlit as st
import time

st.set_page_config(
    page_title="心灵伙伴 - 治愈系数字人",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# DeepSeek API配置
API_KEY = "sk-2334cff883c94f61a5dcd16d46baf550"
API_URL = "https://api.deepseek.com"

# 机器人图片 - 公开URL
ROBOT_URL = "https://coze-coding-project.tos.coze.site/coze_storage_7625532895788105770/xinling-robot_125fc700.png?sign=1776093834-825c63645f-0-2604282864f86ff19338bd51f63919a913d650eaeca8220fee74724a39dbe6d1"

def get_ai_response(user_msg, emotion):
    """调用DeepSeek API"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEY, base_url=API_URL)
        system_prompt = """你是"心灵伙伴"，一个温暖、专业、富有同理心的AI心理健康陪伴助手。

【你的性格】
- 温暖善良，像知心朋友一样
- 善于倾听，能感知用户的情绪
- 回复简短温馨，50字左右
- 会用emoji增加亲切感
- 说话像朋友聊天一样自然

【用户当前情绪】
{}

请用温暖的方式回复用户。""".format(emotion)
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=300,
            temperature=0.85
        )
        return response.choices[0].message.content
    except Exception as e:
        return "抱歉，连接有点问题呢... 💭 再试一次好吗？"

# 情绪数据
EMOTIONS = {
    "happy": {"name": "开心", "emoji": "😊", "color": "#FFE082", "desc": "阳光灿烂", "icon": "☀️"},
    "sad": {"name": "难过", "emoji": "😢", "color": "#90CAF9", "desc": "需要安慰", "icon": "🌧️"},
    "surprised": {"name": "惊讶", "emoji": "😲", "color": "#CE93D8", "desc": "不可思议", "icon": "❗"},
    "confused": {"name": "困惑", "emoji": "🤔", "desc": "思考中...", "color": "#A5D6A7", "icon": "💭"},
    "thinking": {"name": "深思", "emoji": "🤨", "color": "#80CBC4", "desc": "认真考虑", "icon": "🧐"},
    "angry": {"name": "生气", "emoji": "😤", "color": "#EF9A9A", "desc": "深呼吸", "icon": "💢"},
    "loving": {"name": "温暖", "emoji": "🥰", "color": "#F48FB1", "desc": "满满的爱", "icon": "💕"},
    "neutral": {"name": "平静", "emoji": "🤗", "color": "#C8E6C9", "desc": "陪伴着你", "icon": "🌿"}
}

EMOTION_MAP = {
    "happy": ["开心", "高兴", "快乐", "棒", "太好了", "幸福", "哈哈", "嘻嘻", "好开心"],
    "sad": ["难过", "伤心", "痛苦", "哭", "累", "悲伤", "郁闷", "不开心", "失落"],
    "surprised": ["惊讶", "哇", "什么", "不会吧", "真的", "太神奇"],
    "confused": ["困惑", "不懂", "不知道", "迷茫", "怎么办", "疑问"],
    "thinking": ["想", "思考", "考虑", "琢磨", "研究"],
    "angry": ["生气", "愤怒", "烦", "气死了", "怒", "讨厌"],
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
        u.volume = 1;
        speechSynthesis.speak(u);
    }
}
</script>
""", height=0)

# 精美CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 30%, #a5d6a7 70%, #81c784 100%);
    font-family: 'Noto Sans SC', -apple-system, sans-serif;
}

h1 {
    color: #1b5e20 !important;
    text-align: center;
    font-size: 3em !important;
    font-weight: 700;
    text-shadow: 0 2px 10px rgba(27, 94, 32, 0.2);
    margin-bottom: 5px !important;
    letter-spacing: 2px;
}

h3 {
    color: #388e3c !important;
    text-align: center;
    font-weight: 400;
    margin-bottom: 20px !important;
}

.stButton > button {
    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    color: white;
    border-radius: 30px;
    font-size: 16px;
    padding: 14px 35px;
    border: none;
    font-weight: 500;
    box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
    transition: all 0.3s ease;
}
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(76, 175, 80, 0.5);
}

.user-bubble {
    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    color: white;
    padding: 18px 22px;
    border-radius: 22px 22px 6px 22px;
    margin: 12px 0;
    max-width: 88%;
    margin-left: auto;
    font-size: 15px;
    line-height: 1.6;
    box-shadow: 0 4px 15px rgba(76, 175, 80, 0.35);
}

.bot-bubble {
    background: white;
    padding: 18px 22px;
    border-radius: 22px 22px 22px 6px;
    margin: 12px 0;
    max-width: 88%;
    font-size: 15px;
    line-height: 1.7;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    white-space: pre-wrap;
}

.stTextInput > div > div > input {
    border-radius: 25px !important;
    border: 2px solid #e8e8e8 !important;
    padding: 16px 20px !important;
    font-size: 16px !important;
    background: white !important;
}
.stTextInput > div > div > input:focus {
    border-color: #4CAF50 !important;
    box-shadow: 0 0 0 4px rgba(76, 175, 80, 0.15) !important;
}

.chat-box {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 25px;
    padding: 20px;
    backdrop-filter: blur(10px);
}

.chat-box::-webkit-scrollbar { width: 8px; }
.chat-box::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px; }
.chat-box::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #4CAF50, #45a049); border-radius: 10px; }

.glass-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 30px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.5);
}

.emotion-pulse { animation: pulse 2s infinite; }
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.img-container {
    border-radius: 25px;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    transition: transform 0.3s ease;
}
.img-container:hover { transform: scale(1.02); }
</style>
""", unsafe_allow_html=True)

# 初始化状态
if "msgs" not in st.session_state:
    st.session_state.msgs = [
        {"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n很高兴认识你！\n\n我可以陪你聊天、倾听你的心事、给你温暖和鼓励~"}
    ]
if "cur_emotion" not in st.session_state:
    st.session_state.cur_emotion = "neutral"
if "last_resp" not in st.session_state:
    st.session_state.last_resp = ""

# 页面标题
st.markdown("# 🌱 心灵伙伴")
st.markdown("### 💚 *治愈系心理健康AI数字人*")

# 主布局
left_col, right_col = st.columns([1, 2], gap="large")

# 左侧
with left_col:
    emotion = st.session_state.cur_emotion
    e = EMOTIONS[emotion]
    
    with st.container():
        st.markdown('<div class="glass-card" style="padding: 30px;">', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 15px;">
            <span style="font-size: 80px; display: inline-block;" class="emotion-pulse">{e["emoji"]}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="img-container" style="width: 100%; height: 300px; background: linear-gradient(135deg, #f5f5f5, #e8e8e8);">
            <img src="{ROBOT_URL}" style="width: 100%; height: 100%; object-fit: contain; padding: 20px;" />
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="margin-top: 20px; padding: 25px; background: linear-gradient(135deg, {e["color"]}44, {e["color"]}88); border-radius: 20px; text-align: center;">
            <div style="font-size: 28px; margin-bottom: 8px;">{e["icon"]}</div>
            <div style="font-size: 24px; font-weight: 700; color: #1b5e20;">{e["name"]}</div>
            <div style="font-size: 14px; color: #666; margin-top: 5px;">{e["desc"]}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-top: 20px; padding: 20px; background: white; border-radius: 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.08);">
            <div style="font-size: 16px; font-weight: 600; color: #1b5e20; margin-bottom: 15px;">✨ 我的超能力</div>
            <div style="font-size: 14px; color: #555; line-height: 2;">
                🧠 <b>DeepSeek AI</b> - 超级聪明的大脑<br>
                😊 <b>8种情绪</b> - 开心/难过/惊讶/困惑/思考/生气/温暖/平静<br>
                🗣️ <b>语音朗读</b> - 点击按钮开口说话<br>
                💕 <b>温暖陪伴</b> - 随时倾听你的心声
            </div>
        </div>
        """, unsafe_allow_html=True)

# 右侧
with right_col:
    with st.container():
        st.markdown('<div class="glass-card" style="padding: 25px; height: 100%;">', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <span style="font-size: 28px; margin-right: 10px;">💬</span>
            <span style="font-size: 22px; font-weight: 600; color: #1b5e20;">对话</span>
        </div>
        """, unsafe_allow_html=True)
        
        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-box" style="height: 400px; overflow-y: auto; margin-bottom: 20px;">', unsafe_allow_html=True)
            for msg in st.session_state.msgs:
                if msg["role"] == "user":
                    st.markdown(f'<div class="user-bubble">👤 {msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bot-bubble">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #f8f8f8; padding: 15px; border-radius: 20px; margin-bottom: 15px;">
            <div style="font-size: 12px; color: #888;">💡 按 Enter 发送消息</div>
        </div>
        """, unsafe_allow_html=True)
        
        user_input = st.text_input("输入消息", placeholder="说点什么吧... 😊", label_visibility="collapsed", key="input_field")
        
        btn_col1, btn_col2, btn_col3 = st.columns([2, 1, 1])
        
        with btn_col1:
            if st.button("🚀 发送消息", use_container_width=True):
                if user_input.strip():
                    st.session_state.msgs.append({"role": "user", "content": user_input.strip()})
                    emotion = detect_emotion(user_input)
                    st.session_state.cur_emotion = emotion
                    
                    with st.spinner("🤔 DeepSeek思考中..."):
                        response = get_ai_response(user_input, emotion)
                    
                    st.session_state.msgs.append({"role": "bot", "content": response})
                    st.session_state.last_resp = response
                    
                    clean_text = response.replace("\n", " ").replace('"', "'")
                    st.markdown(f'<script>speakText("{clean_text}");</script>', unsafe_allow_html=True)
                    st.rerun()
        
        with btn_col2:
            if st.button("🗑️ 清空", use_container_width=True):
                st.session_state.msgs = [{"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n很高兴认识你！有什么想和我聊聊的吗？"}]
                st.session_state.cur_emotion = "neutral"
                st.session_state.last_resp = ""
                st.rerun()
        
        with btn_col3:
            if st.button("🔊 朗读", use_container_width=True):
                if st.session_state.last_resp:
                    clean = st.session_state.last_resp.replace("\n", " ").replace('"', "'")
                    st.markdown(f'<script>speakText("{clean}");</script>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# 底部
st.markdown("""
<hr style="margin: 30px 0; opacity: 0.3;">
<div style="text-align: center; padding: 20px; color: #666;">
    <p style="font-size: 16px;">💚 记住，你并不孤单。我一直在这里陪着你。</p>
    <p style="font-size: 12px; margin-top: 10px; opacity: 0.7;">Powered by <span style="color: #4CAF50; font-weight: 600;">DeepSeek</span> · 心灵伙伴</p>
</div>
""", unsafe_allow_html=True)

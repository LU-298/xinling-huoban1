"""
心灵伙伴 - 治愈系数字人 🌱
高端精致版 - SVG数字人 · 8种神态 · 语音朗读
"""
import streamlit as st

st.set_page_config(page_title="心灵伙伴", page_icon="🌱", layout="wide")

# DeepSeek API
DEEPSEEK_API_KEY = "sk-2334cff883c94f61a5dcd16d46baf550"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# 机器人图片
ROBOT_IMG = "https://coze-coding-project.tos.coze.site/coze_storage_7625532895788105770/xinling_robot_3fd152f1.png?sign=1776092668-668a4965aa-0-4ea457914e804629e66b650559cd474e1aa22230200d94e18242a29be2b05f04"

def get_ai_response(user_message, emotion):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
        system_prompt = """你是"心灵伙伴"，一个温暖、专业、富有同理心的AI心理健康陪伴助手。
- 温暖善良，像知心朋友一样
- 善于倾听，感知用户情绪
- 回复简短温馨，30-80字
- 会用emoji增加亲切感
请像朋友聊天一样回复，自然温暖。"""
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
            temperature=0.85
        )
        return response.choices[0].message.content
    except:
        return "抱歉，连接有点问题，再试一次好吗？"

# 8种情绪的完整表情配置
EMOTIONS = {
    "happy": {
        "name": "开心", "emoji": "😊", 
        "eye_left": "M 20 25 Q 25 15 30 25", "eye_right": "M 40 25 Q 45 15 50 25",
        "mouth": "M 20 35 Q 35 50 50 35",
        "brow_left": "M 18 15 Q 25 12 32 15", "brow_right": "M 38 15 Q 45 12 52 15",
        "cheek": "rgba(255,182,193,0.5)", "glow": "#FFD700", "speed": 0.8
    },
    "sad": {
        "name": "难过", "emoji": "😢",
        "eye_left": "M 20 28 Q 25 25 30 28", "eye_right": "M 40 28 Q 45 25 50 28",
        "mouth": "M 22 42 Q 35 32 48 42",
        "brow_left": "M 18 18 Q 25 22 32 18", "brow_right": "M 38 18 Q 45 22 52 18",
        "tear": True, "glow": "#6495ED", "speed": 1.5
    },
    "surprised": {
        "name": "惊讶", "emoji": "😲",
        "eye_left": "M 20 25 Q 25 18 30 25", "eye_right": "M 40 25 Q 45 18 50 25",
        "mouth": "M 28 38 Q 35 48 42 38 Q 35 42 28 38",
        "brow_left": "M 18 12 Q 25 10 32 12", "brow_right": "M 38 12 Q 45 10 52 12",
        "glow": "#FF69B4", "speed": 0.5
    },
    "confused": {
        "name": "困惑", "emoji": "🤔",
        "eye_left": "M 20 25 Q 25 28 30 25", "eye_right": "M 40 25 Q 45 22 50 25",
        "mouth": "M 25 40 Q 35 38 45 40",
        "brow_left": "M 18 15 Q 25 18 32 15", "brow_right": "M 38 12 Q 45 15 52 12",
        "glow": "#DDA0DD", "speed": 1.2
    },
    "thinking": {
        "name": "思考", "emoji": "🤨",
        "eye_left": "M 20 25 Q 25 28 30 25", "eye_right": "M 40 25 Q 45 22 50 25",
        "mouth": "M 28 40 Q 35 42 42 40",
        "brow_left": "M 18 15 Q 25 15 32 15", "brow_right": "M 38 18 Q 45 15 52 18",
        "glow": "#90EE90", "speed": 1.0
    },
    "angry": {
        "name": "生气", "emoji": "😤",
        "eye_left": "M 20 25 Q 25 28 30 25", "eye_right": "M 40 25 Q 45 28 50 25",
        "mouth": "M 22 42 Q 35 35 48 42",
        "brow_left": "M 18 12 Q 25 18 32 15", "brow_right": "M 38 15 Q 45 18 52 12",
        "glow": "#FF6347", "speed": 0.6
    },
    "loving": {
        "name": "温暖", "emoji": "🥰",
        "eye_left": "M 20 25 Q 25 20 30 25", "eye_right": "M 40 25 Q 45 20 50 25",
        "mouth": "M 20 35 Q 35 48 50 35",
        "heart": True, "glow": "#FF69B4", "speed": 1.0
    },
    "neutral": {
        "name": "平静", "emoji": "🤗",
        "eye_left": "M 20 25 Q 25 25 30 25", "eye_right": "M 40 25 Q 45 25 50 25",
        "mouth": "M 22 38 Q 35 42 48 38",
        "brow_left": "M 18 15 Q 25 15 32 15", "brow_right": "M 38 15 Q 45 15 52 15",
        "glow": "#90EE90", "speed": 1.2
    }
}

EMOTION_KEYWORDS = {
    "happy": ["开心", "高兴", "快乐", "棒", "太好了", "幸福", "哈哈", "嘻嘻", "好开心", "兴奋"],
    "sad": ["难过", "伤心", "痛苦", "哭", "累", "疲惫", "心碎", "悲伤", "郁闷", "不开心"],
    "surprised": ["惊讶", "吃惊", "哇", "天哪", "不会吧", "什么"],
    "confused": ["困惑", "不懂", "不知道", "迷茫", "怎么办", "疑问"],
    "thinking": ["想", "思考", "考虑", "琢磨", "研究"],
    "angry": ["生气", "愤怒", "讨厌", "烦", "气死了", "怒"],
    "loving": ["爱", "喜欢", "想你", "谢谢", "温暖", "感动", "爱你"],
}

def detect_emotion(text):
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return emotion
    return "neutral"

# 语音JS
st.components.v1.html("""
<script>
function speakText(text) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'zh-CN';
        utterance.rate = 0.9;
        utterance.pitch = 1.1;
        window.speechSynthesis.speak(utterance);
    }
}
function stopSpeak() {
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
}
</script>
""", height=0)

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');
.stApp { background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 50%, #a5d6a7 100%); font-family: 'Noto Sans SC', sans-serif; }
h1 { color: #1b5e20 !important; text-align: center; font-size: 2.8em !important; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); }
.stButton > button { background: linear-gradient(135deg, #4CAF50, #45a049); color: white; border-radius: 25px; font-size: 16px; padding: 12px 30px; border: none; transition: all 0.3s; }
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4); }
.user-msg { background: linear-gradient(135deg, #4CAF50, #45a049); color: white; padding: 15px 20px; border-radius: 20px 20px 5px 20px; margin: 15px 0; max-width: 85%; margin-left: auto; box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3); font-size: 15px; }
.bot-msg { background: white; padding: 15px 20px; border-radius: 20px 20px 20px 5px; margin: 15px 0; max-width: 85%; box-shadow: 0 4px 15px rgba(0,0,0,0.1); white-space: pre-wrap; font-size: 15px; line-height: 1.6; }
.stTextArea textarea { border-radius: 20px !important; border: 2px solid #e0e0e0 !important; padding: 15px !important; font-size: 16px !important; background: white !important; }
.stTextArea textarea:focus { border-color: #4CAF50 !important; box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.2) !important; }
@keyframes breathe { 0%,100%{transform:translate(-50%,-50%) scale(1);opacity:0.8} 50%{transform:translate(-50%,-50%) scale(1.2);opacity:1} }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
@keyframes blink { 0%,100%{transform:scaleY(1)} 50%{transform:scaleY(0.1)} }
@keyframes heartBeat { 0%,100%{transform:scale(1)} 25%{transform:scale(1.1)} 50%{transform:scale(1)} 75%{transform:scale(1.1)} }
.robot-container { animation: float 4s ease-in-out infinite; }
.eye { animation: blink 4s ease-in-out infinite; transform-origin: center; }
.heart { animation: heartBeat 1s ease-in-out infinite; }
.tear { animation: tearDrop 2s ease-in-out infinite; }
@keyframes tearDrop { 0%,100%{opacity:0;transform:translateY(0)} 50%{opacity:1;transform:translateY(3px)} }
</style>
""", unsafe_allow_html=True)

# 初始化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n我升级啦！现在的我可以：\n• 像真人一样和你聊天 💬\n• 有丰富的神态表情 😊\n• 开口说话陪你倾诉 🗣️\n• 感知你的各种情绪 💕\n\n有什么想和我聊聊的吗？"}
    ]
if "current_emotion" not in st.session_state:
    st.session_state.current_emotion = "neutral"
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# 标题
st.markdown("# 🌱 心灵伙伴")
st.markdown("### 💚 **高端精致版** - 神态生动 · 会说话 · 更懂你")

col1, col2 = st.columns([1, 2])

with col1:
    emotion = st.session_state.current_emotion
    e = EMOTIONS.get(emotion, EMOTIONS["neutral"])
    
    st.markdown(f"""
    <div style="background:white; padding:30px; border-radius:30px; box-shadow:0 15px 50px rgba(0,0,0,0.15);">
        
        <!-- 情绪表情大图标 -->
        <div style="text-align:center; margin-bottom:15px;">
            <span style="font-size:50px;">{e["emoji"]}</span>
            <span style="font-size:18px; color:#666; margin-left:10px;">{e["name"]}</span>
        </div>
        
        <!-- SVG数字人 -->
        <div class="robot-container" style="width:300px; height:350px; margin:0 auto; position:relative;">
            
            <!-- 外发光效果 -->
            <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:250px; height:250px; background:radial-gradient(circle, {e['glow']}33, transparent 70%); border-radius:50%; filter:blur(20px);"></div>
            
            <svg viewBox="0 0 70 80" width="280" height="320" style="position:relative; z-index:1;">
                
                <!-- 头部 - 圆润的机器人 -->
                <defs>
                    <linearGradient id="headGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#f8f8f8"/>
                        <stop offset="50%" style="stop-color:#e8e8e8"/>
                        <stop offset="100%" style="stop-color:#d0d0d0"/>
                    </linearGradient>
                    <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" style="stop-color:#f0f0f0"/>
                        <stop offset="100%" style="stop-color:#d8d8d8"/>
                    </linearGradient>
                    <filter id="shadow">
                        <feDropShadow dx="0" dy="4" stdDeviation="3" flood-opacity="0.15"/>
                    </filter>
                    <radialGradient id="glowGrad" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" style="stop-color:{e['glow']};stop-opacity:1"/>
                        <stop offset="100%" style="stop-color:{e['glow']};stop-opacity:0"/>
                    </radialGradient>
                </defs>
                
                <!-- 天线 -->
                <line x1="35" y1="2" x2="35" y2="8" stroke="#888" stroke-width="2" stroke-linecap="round"/>
                <circle cx="35" cy="2" r="2" fill="{e['glow']}"/>
                
                <!-- 头部主体 -->
                <ellipse cx="35" cy="28" rx="28" ry="24" fill="url(#headGrad)" filter="url(#shadow)"/>
                
                <!-- 眼镜框 -->
                <rect x="12" y="20" width="18" height="14" rx="4" fill="none" stroke="#333" stroke-width="2.5"/>
                <rect x="40" y="20" width="18" height="14" rx="4" fill="none" stroke="#333" stroke-width="2.5"/>
                <!-- 眼镜桥 -->
                <line x1="30" y1="27" x2="40" y2="27" stroke="#333" stroke-width="2"/>
                <!-- 眼镜腿 -->
                <line x1="10" y1="27" x2="5" y2="25" stroke="#333" stroke-width="2" stroke-linecap="round"/>
                <line x1="60" y1="27" x2="65" y2="25" stroke="#333" stroke-width="2" stroke-linecap="round"/>
                
                <!-- 左眼 -->
                <g class="eye" style="transform-origin: 21px 27px; animation-duration: {e['speed']}s;">
                    <ellipse cx="21" cy="27" rx="5" ry="5" fill="#333"/>
                    <ellipse cx="22" cy="25" rx="2" ry="2" fill="white"/>
                </g>
                
                <!-- 右眼 -->
                <g class="eye" style="transform-origin: 49px 27px; animation-duration: {e['speed']}s;">
                    <ellipse cx="49" cy="27" rx="5" ry="5" fill="#333"/>
                    <ellipse cx="50" cy="25" rx="2" ry="2" fill="white"/>
                </g>
                
                <!-- 嘴巴 -->
                <path d="{e['mouth']}" stroke="#333" stroke-width="2.5" fill="none" stroke-linecap="round"/>
                
                <!-- 腮红（开心时） -->
                <ellipse cx="12" cy="35" rx="4" ry="2.5" fill="{e['cheek']}" opacity="0.6"/>
                <ellipse cx="58" cy="35" rx="4" ry="2.5" fill="{e['cheek']}" opacity="0.6"/>
                
                <!-- 身体 -->
                <ellipse cx="35" cy="62" rx="22" ry="16" fill="url(#bodyGrad)" filter="url(#shadow)"/>
                
                <!-- 胸口发光标识 -->
                <circle cx="35" cy="62" r="8" fill="url(#glowGrad)" style="animation:breathe 3s ease-in-out infinite;"/>
                <circle cx="35" cy="62" r="5" fill="{e['glow']}" opacity="0.8"/>
                
                <!-- 手臂 -->
                <ellipse cx="12" cy="58" rx="4" ry="8" fill="#e0e0e0"/>
                <ellipse cx="58" cy="58" rx="4" ry="8" fill="#e0e0e0"/>
                
                <!-- 爱心（温暖时） -->
                <path class="heart" d="M 8 12 C 8 8, 12 5, 15 8 C 18 5, 22 8, 22 12 C 22 18, 15 24, 15 24 C 15 24, 8 18, 8 12" fill="#FF69B4" opacity="0.8" style="display:{'block' if 'heart' in e else 'none'}"/>
                
                <!-- 眼泪（难过时） -->
                <ellipse class="tear" cx="25" cy="35" rx="1.5" ry="2" fill="#87CEEB" style="display:{'block' if e.get('tear',False) else 'none'}"/>
                
            </svg>
        </div>
        
        <!-- 情绪说明 -->
        <div style="margin-top:20px; padding:20px; background:linear-gradient(135deg, {e['glow']}22, {e['glow']}44); border-radius:15px; text-align:center;">
            <div style="font-size:20px; font-weight:bold; color:#2e7d32;">当前神态：{e["name"]}</div>
            <div style="font-size:13px; color:#666; margin-top:8px;">我会根据对话内容变换表情哦~</div>
        </div>
        
    </div>
    """, unsafe_allow_html=True)
    
    # 功能说明
    st.markdown("""
    <div style="margin-top:20px; padding:20px; background:white; border-radius:15px; box-shadow:0 5px 15px rgba(0,0,0,0.1);">
    <b>✨ 我的超能力：</b><br>
    • 🧠 DeepSeek AI大脑 - 像真人一样思考<br>
    • 😊 8种神态表情 - 开心/难过/惊讶/困惑/思考/生气/温暖/平静<br>
    • 🗣️ 语音朗读 - 点击按钮让我开口说话<br>
    • 💬 智能对话 - 感知你的情绪
    </div>
    """)

with col2:
    st.markdown("### 💬 对话")
    
    # 聊天区域
    chat_area = st.container()
    with chat_area:
        st.markdown('<div style="height:420px; overflow-y:auto; padding:15px; background:rgba(255,255,255,0.8); border-radius:20px; margin-bottom:15px; border:1px solid #e0e0e0;">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-msg">👤 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-msg">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 输入区域 - 使用form支持Enter发送
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "输入消息...", 
            placeholder="说点什么吧... 😊\n支持多行输入哦~",
            label_visibility="collapsed",
            height=80,
            key="input_area"
        )
        
        col_send, col_clear, col_speak = st.columns([2, 1, 1])
        
        with col_send:
            submitted = st.form_submit_button("🚀 发送", use_container_width=True)
        
        with col_clear:
            if st.form_submit_button("🗑️ 清空", use_container_width=True):
                st.session_state.messages = [
                    {"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n有什么想和我聊聊的吗？😊"}
                ]
                st.session_state.current_emotion = "neutral"
                st.session_state.last_response = ""
                st.rerun()
        
        with col_speak:
            if st.form_submit_button("🔊 朗读", use_container_width=True):
                if st.session_state.last_response:
                    clean_text = st.session_state.last_response.replace("\n", " ").replace('"', "'").replace("'", "\\'")
                    st.markdown(f'<script>speakText("{clean_text}");</script>', unsafe_allow_html=True)
        
        # 处理发送
        if submitted and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input.strip()})
            emotion = detect_emotion(user_input)
            st.session_state.current_emotion = emotion
            
            with st.spinner("🤔 DeepSeek思考中..."):
                response = get_ai_response(user_input, emotion)
            
            st.session_state.messages.append({"role": "bot", "content": response})
            st.session_state.last_response = response
            
            # 自动朗读
            clean_text = response.replace("\n", " ").replace('"', "'").replace("'", "\\'")
            st.markdown(f'<script>speakText("{clean_text}");</script>', unsafe_allow_html=True)
            
            st.rerun()

# 底部
st.markdown("""
---
<div style="text-align:center; padding:20px; color:#888;">
    <p style="font-size:16px;">💚 记住，你并不孤单。我一直在这里陪着你。</p>
    <p style="font-size:12px; margin-top:10px;">Powered by DeepSeek · 心灵伙伴</p>
</div>
""", unsafe_allow_html=True)

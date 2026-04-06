"""
心灵伙伴 - 治愈系数字人
超级智能版 - 神态变化 + 智能对话
"""
import streamlit as st
import time

st.set_page_config(page_title="心灵伙伴", page_icon="🌱", layout="wide")

# DeepSeek API
DEEPSEEK_API_KEY = "sk-2334cff883c94f61a5dcd16d46baf550"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

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

# 情绪配置
EMOTION_DATA = {
    "happy": {"emoji": "😊", "desc": "开心", "mouth": "M 5 12 Q 30 25 55 12"},
    "sad": {"emoji": "😢", "desc": "难过", "mouth": "M 5 20 Q 30 10 55 20"},
    "stressed": {"emoji": "😰", "desc": "焦虑", "mouth": "M 5 15 Q 30 15 55 15"},
    "confused": {"emoji": "🤔", "desc": "困惑", "mouth": "M 10 15 Q 30 12 50 15"},
    "love": {"emoji": "🥰", "desc": "温暖", "mouth": "M 5 12 Q 30 25 55 12"},
    "angry": {"emoji": "😤", "desc": "生气", "mouth": "M 5 15 Q 30 10 55 15"},
    "tired": {"emoji": "😴", "desc": "疲惫", "mouth": "M 5 15 Q 30 18 55 15"},
    "neutral": {"emoji": "🤗", "desc": "平静", "mouth": "M 5 12 Q 30 18 55 12"}
}

EMOTION_KEYWORDS = {
    "happy": ["开心", "高兴", "快乐", "棒", "太好了", "幸福", "哈哈", "嘻嘻", "好开心", "兴奋"],
    "sad": ["难过", "伤心", "痛苦", "哭", "累", "疲惫", "心碎", "悲伤", "郁闷", "不开心"],
    "stressed": ["压力", "焦虑", "紧张", "害怕", "担心", "恐惧", "不安", "烦恼", "崩溃"],
    "confused": ["困惑", "不懂", "不知道", "迷茫", "怎么办", "疑问"],
    "love": ["爱", "喜欢", "想你", "谢谢", "温暖", "感动"],
    "angry": ["生气", "愤怒", "讨厌", "烦", "气死了", "怒"],
    "tired": ["累", "困", "疲惫", "疲倦", "没劲", "无力"]
}

def detect_emotion(text):
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return emotion
    return "neutral"

# CSS样式
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #e8f5e9, #c8e6c9, #a5d6a7); }
h1 { color: #1b5e20 !important; text-align: center; font-size: 2.5em !important; }
.stButton > button { background: linear-gradient(135deg, #4CAF50, #45a049); color: white; border-radius: 25px; font-size: 16px; padding: 12px 30px; border: none; }
.stButton > button:hover { background: linear-gradient(135deg, #45a049, #3d8b40); }
.user-msg { background: linear-gradient(135deg, #4CAF50, #45a049); color: white; padding: 15px 20px; border-radius: 20px 20px 5px 20px; margin: 15px 0; max-width: 85%; margin-left: auto; }
.bot-msg { background: white; padding: 15px 20px; border-radius: 20px 20px 20px 5px; margin: 15px 0; max-width: 85%; box-shadow: 0 3px 15px rgba(0,0,0,0.1); white-space: pre-wrap; }
.stTextArea textarea { border-radius: 20px !important; border: 2px solid #e0e0e0 !important; padding: 15px !important; font-size: 16px !important; }
</style>
""", unsafe_allow_html=True)

# JS - 眨眼动画
st.components.v1.html("""
<script>
setInterval(() => {
    if (Math.random() > 0.6) {
        const eyes = document.querySelectorAll('.eye-circle');
        eyes.forEach(e => { e.style.height = '4px'; });
        setTimeout(() => { eyes.forEach(e => { e.style.height = '26px'; }); }, 150);
    }
}, 3000);
</script>
""", height=0)

# 标题
st.markdown("# 🌱 心灵伙伴")
st.markdown("### 💚 超级智能版 - 有表情 · 更懂你")

col1, col2 = st.columns([1, 2])

with col1:
    emotion = st.session_state.get("current_emotion", "neutral")
    face = EMOTION_DATA.get(emotion, EMOTION_DATA["neutral"])
    
    st.markdown(f"""
    <div style="background:white; padding:30px; border-radius:30px; box-shadow:0 15px 50px rgba(0,0,0,0.15); text-align:center;">
        <div style="font-size:50px; margin-bottom:15px;">{face["emoji"]}</div>
        
        <div style="width:160px; height:200px; margin:0 auto; position:relative;">
            <div style="width:150px; height:170px; background:linear-gradient(145deg,#f8f8f8,#d8d8d8); border-radius:75px; position:absolute; top:0; left:50%; transform:translateX(-50%); box-shadow:0 10px 30px rgba(0,0,0,0.1);">
                <div style="position:absolute; top:45px; left:50%; transform:translateX(-50%); display:flex; gap:10px;">
                    <div style="width:48px; height:38px; border:5px solid #2c2c2c; border-radius:10px; background:linear-gradient(135deg,rgba(200,230,255,0.4),rgba(180,210,240,0.3));"></div>
                    <div style="width:48px; height:38px; border:5px solid #2c2c2c; border-radius:10px; background:linear-gradient(135deg,rgba(200,230,255,0.4),rgba(180,210,240,0.3));"></div>
                </div>
                <div style="position:absolute; top:50px; left:50%; transform:translateX(-50%); display:flex; gap:20px;">
                    <div class="eye-circle" style="width:26px; height:26px; background:#2c2c2c; border-radius:50%; transition:all 0.15s;"></div>
                    <div class="eye-circle" style="width:26px; height:26px; background:#2c2c2c; border-radius:50%; transition:all 0.15s;"></div>
                </div>
                <div style="position:absolute; top:100px; left:50%; transform:translateX(-50%);">
                    <svg width="60" height="30"><path d="{face["mouth"]}" stroke="#2c2c2c" stroke-width="5" fill="none" stroke-linecap="round"/></svg>
                </div>
            </div>
            <div style="width:140px; height:60px; background:linear-gradient(145deg,#f5f5f5,#e0e0e0); border-radius:30px; position:absolute; bottom:0; left:50%; transform:translateX(-50%);">
                <div style="position:absolute; top:8px; left:50%; transform:translateX(-50%); width:40px; height:40px; background:radial-gradient(circle,#4CAF50,#2E7D32); border-radius:50%; animation:breathe 3s infinite;"></div>
            </div>
        </div>
        <style>@keyframes breathe{{0%,100%{{transform:translateX(-50%) scale(1)}}50%{{transform:translateX(-50%) scale(1.15)}}}}</style>
        
        <div style="margin-top:20px; padding:15px; background:linear-gradient(135deg,#e8f5e9,#c8e6c9); border-radius:15px;">
            <div style="font-size:18px; font-weight:500; color:#2e7d32;">{face["desc"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    **✨ 功能：**
    - 🧠 DeepSeek AI大脑
    - 😊 情绪表情变化
    - 💬 智能对话
    """)

with col2:
    st.markdown("### 💬 对话")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n我可以像真人一样和你聊天，还有各种情绪表情变化！\n\n有什么想和我聊聊的吗？"}
        ]
    
    chat_container = st.container()
    with chat_container:
        st.markdown('<div style="height:380px; overflow-y:auto; padding:15px; background:rgba(255,255,255,0.8); border-radius:20px; margin-bottom:15px;">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-msg">👤 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-msg">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    user_input = st.text_area("输入消息...", placeholder="说点什么吧... (Enter发送，Shift+Enter换行)", label_visibility="collapsed", height=80)
    
    col_send, col_clear = st.columns([1, 1])
    with col_send:
        if st.button("🚀 发送", use_container_width=True):
            if user_input.strip():
                st.session_state.messages.append({"role": "user", "content": user_input.strip()})
                emotion = detect_emotion(user_input)
                st.session_state.current_emotion = emotion
                
                with st.spinner("思考中..."):
                    response = get_ai_response(user_input, emotion)
                
                st.session_state.messages.append({"role": "bot", "content": response})
                st.rerun()
    
    with col_clear:
        if st.button("🗑️ 清空", use_container_width=True):
            st.session_state.messages = [{"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n有什么想和我聊聊的吗？😊"}]
            st.session_state.current_emotion = "neutral"
            st.rerun()

st.markdown("---")
st.markdown("*💚 记住，你并不孤单。我一直在这里陪着你。*")

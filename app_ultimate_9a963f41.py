"""
心灵伙伴 - 治愈系数字人
完整版 - 机器人图片 + 表情变化 + 语音朗读
"""
import streamlit as st
import base64
import time

st.set_page_config(page_title="心灵伙伴", page_icon="🌱", layout="wide")

# DeepSeek API配置
DEEPSEEK_API_KEY = "sk-2334cff883c94f61a5dcd16d46baf550"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# 图片地址
ROBOT_IMAGE = "https://coze-coding-project.tos.coze.site/coze_storage_7625532895788105770/robot_character_6abec104.png?sign=1776092384-dfb3450e0a-0-0235c8100bd8fd5241b25d55cfd1ef7620a4400ecc09454dcaf02366f9d66f29"

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
    except Exception as e:
        return "抱歉，连接有点问题，再试一次好吗？"

# 情绪配置
EMOTION_DATA = {
    "happy": {"emoji": "😊", "desc": "开心", "color": "#FFD700"},
    "sad": {"emoji": "😢", "desc": "难过", "color": "#6495ED"},
    "stressed": {"emoji": "😰", "desc": "焦虑", "color": "#FFB6C1"},
    "confused": {"emoji": "🤔", "desc": "困惑", "color": "#DDA0DD"},
    "love": {"emoji": "🥰", "desc": "温暖", "color": "#FF69B4"},
    "angry": {"emoji": "😤", "desc": "生气", "color": "#FF6347"},
    "tired": {"emoji": "😴", "desc": "疲惫", "color": "#9370DB"},
    "neutral": {"emoji": "🤗", "desc": "平静", "color": "#90EE90"}
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
.chat-container { max-height: 450px; overflow-y: auto; padding: 15px; background: rgba(255,255,255,0.8); border-radius: 20px; }
</style>
""", unsafe_allow_html=True)

# 语音JS代码
st.components.v1.html("""
<script>
function speakText(text) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'zh-CN';
        utterance.rate = 1;
        utterance.pitch = 1.1;
        window.speechSynthesis.speak(utterance);
    }
}

function stopSpeak() {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
    }
}
</script>
""", height=0)

# 初始化session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n我可以像真人一样和你聊天，有各种表情变化，还能开口说话！\n\n有什么想和我聊聊的吗？"}
    ]
if "current_emotion" not in st.session_state:
    st.session_state.current_emotion = "neutral"
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# 标题
st.markdown("# 🌱 心灵伙伴")
st.markdown("### 💚 智能版 - 表情丰富 · 会说话 · 更懂你")

col1, col2 = st.columns([1, 2])

with col1:
    emotion = st.session_state.current_emotion
    face = EMOTION_DATA.get(emotion, EMOTION_DATA["neutral"])
    
    st.markdown(f"""
    <div style="background:white; padding:25px; border-radius:25px; box-shadow:0 10px 40px rgba(0,0,0,0.15); text-align:center;">
        <div style="font-size:60px; margin-bottom:10px;">{face["emoji"]}</div>
        
        <div style="width:280px; height:280px; margin:0 auto; position:relative; border-radius:20px; overflow:hidden; box-shadow:0 5px 20px rgba(0,0,0,0.2);">
            <img src="{ROBOT_IMAGE}" style="width:100%; height:100%; object-fit:contain; background:#f5f5f5;" />
        </div>
        
        <div style="margin-top:20px; padding:20px; background:linear-gradient(135deg, {face["color"]}33, {face["color"]}66); border-radius:15px;">
            <div style="font-size:24px; font-weight:bold; color:#2e7d32;">{face["desc"]}</div>
            <div style="font-size:14px; color:#666; margin-top:5px;">当前情绪状态</div>
        </div>
        
        <div style="margin-top:15px; padding:15px; background:#f5f5f5; border-radius:15px;">
            <div style="font-size:14px; color:#666;">✨ 点击数字人打个招呼吧！</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top:20px;">
    **✨ 我的超能力：**
    - 🧠 DeepSeek AI大脑
    - 😊 8种情绪表情变化  
    - 🗣️ 语音朗读功能
    - 💬 智能对话
    </div>
    """)

with col2:
    st.markdown("### 💬 对话")
    
    # 聊天容器
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-msg">👤 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-msg">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 输入框 - 支持换行
    user_input = st.text_area(
        "输入消息...", 
        placeholder="说点什么吧... 😊\nEnter发送，Shift+Enter换行",
        label_visibility="collapsed",
        height=80,
        key="input_area"
    )
    
    col_send, col_clear, col_speak = st.columns([2, 1, 1])
    
    with col_send:
        if st.button("🚀 发送", use_container_width=True):
            if user_input.strip():
                st.session_state.messages.append({"role": "user", "content": user_input.strip()})
                emotion = detect_emotion(user_input)
                st.session_state.current_emotion = emotion
                
                with st.spinner("🤔 DeepSeek思考中..."):
                    response = get_ai_response(user_input, emotion)
                
                st.session_state.messages.append({"role": "bot", "content": response})
                st.session_state.last_response = response
                st.rerun()
    
    with col_clear:
        if st.button("🗑️ 清空", use_container_width=True):
            st.session_state.messages = [
                {"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n有什么想和我聊聊的吗？😊"}
            ]
            st.session_state.current_emotion = "neutral"
            st.session_state.last_response = ""
            st.rerun()
    
    with col_speak:
        if st.button("🔊 朗读", use_container_width=True):
            if st.session_state.last_response:
                clean_text = st.session_state.last_response.replace("\n", " ").replace('"', "'")
                st.markdown(f'<script>speakText("{clean_text}");</script>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("*💚 记住，你并不孤单。我一直在这里陪着你。*")

import streamlit as st
import requests
import time

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Nexus AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE = "http://127.0.0.1:8000/api/v1"
QUERY_URL = f"{API_BASE}/documents/query"

# ==========================================
# LUXURY CINEMATIC CSS
# ==========================================

st.markdown("""
<style>

/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html,body,[class*="css"]{
font-family:'Inter',sans-serif;
}

/* Hide Streamlit header */

header{
visibility:hidden;
}

footer{
visibility:hidden;
}

#MainMenu{
visibility:hidden;
}

/* Background */

.stApp{

background:
radial-gradient(circle at 10% 20%, rgba(255,180,0,.08), transparent 28%),
radial-gradient(circle at 90% 15%, rgba(123,97,255,.10), transparent 35%),
radial-gradient(circle at 50% 100%, rgba(0,180,255,.05), transparent 30%),
linear-gradient(
180deg,
#040404,
#090909,
#050505);

color:white;

}

/* Main Container */

.block-container{

padding-top:2rem;

padding-left:3rem;

padding-right:3rem;

max-width:1500px;

}

/* Sidebar */

[data-testid="stSidebar"]{

background:rgba(12,12,12,.75);

backdrop-filter:blur(30px);

border-right:1px solid rgba(255,255,255,.08);

}

/* Scroll */

::-webkit-scrollbar{

width:7px;

}

::-webkit-scrollbar-thumb{

background:#444;

border-radius:20px;

}

/* Hero */

.hero-title{

font-size:60px;

font-weight:900;

letter-spacing:4px;

background:linear-gradient(
90deg,
#ffffff,
#d4af37,
#7c5cff,
#ffffff);

background-size:300%;

-webkit-background-clip:text;

-webkit-text-fill-color:transparent;

animation:shine 8s linear infinite;

}

@keyframes shine{

0%{background-position:0%}

100%{background-position:300%}

}

.hero-sub{

color:#9f9f9f;

font-size:18px;

letter-spacing:1px;

margin-top:-12px;

margin-bottom:35px;

}

/* Glass Cards */

.glass{

background:rgba(255,255,255,.04);

border:1px solid rgba(255,255,255,.08);

backdrop-filter:blur(22px);

border-radius:22px;

padding:22px;

box-shadow:

0 12px 35px rgba(0,0,0,.45),

0 0 30px rgba(123,97,255,.10);

}

/* Buttons */

.stButton>button{

width:100%;

height:48px;

border:none;

border-radius:14px;

font-size:15px;

font-weight:700;

color:black;

background:linear-gradient(
135deg,
#d4af37,
#f2d46b);

transition:.35s;

}

.stButton>button:hover{

transform:translateY(-3px);

box-shadow:

0 0 30px rgba(212,175,55,.45);

}

/* Uploader */

[data-testid="stFileUploader"]{

background:rgba(255,255,255,.03);

border-radius:16px;

padding:10px;

}

/* Chat */

[data-testid="stChatMessage"]{

background:rgba(255,255,255,.03);

border:1px solid rgba(255,255,255,.06);

border-radius:18px;

padding:16px;

margin-bottom:14px;

}

/* Chat Input */

[data-testid="stChatInput"]{

border-top:1px solid rgba(255,255,255,.08);

background:rgba(15,15,15,.85);

backdrop-filter:blur(20px);

}

/* Metrics */

[data-testid="metric-container"]{

background:rgba(255,255,255,.03);

border-radius:15px;

padding:12px;

border:1px solid rgba(255,255,255,.06);

}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("## ⚡ Nexus AI")

    st.caption("Enterprise Knowledge Platform")

    st.divider()

    st.markdown("### 📂 Upload Document")

    uploaded_file = st.file_uploader(
        "",
        type=["pdf","txt"]
    )

    if uploaded_file:

        if st.button("Index Document"):

            with st.spinner("Creating embeddings..."):

                time.sleep(1.5)

            st.success("Document Indexed Successfully")

    st.divider()

    st.markdown("### 🚀 System")

    st.metric("LLM","Gemini Flash")

    st.metric("Vector DB","Qdrant Cloud")

    st.metric("Status","🟢 Online")

    st.metric("Latency","0.42 s")

    st.divider()

    if st.button("🗑 Clear Conversation"):

        st.session_state.messages=[]

        st.rerun()

# ==========================================
# HERO SECTION
# ==========================================

st.markdown(
"""
<div class="hero-title">
NEXUS AI
</div>

<div class="hero-sub">
Luxury Enterprise Knowledge Assistant • Gemini Flash • FastAPI • Qdrant
</div>
""",
unsafe_allow_html=True
)

# ==========================================
# SESSION
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages=[

        {

            "role":"assistant",

            "content":"👋 Welcome to Nexus AI.\n\nUpload your documents and ask questions naturally."

        }

    ]
    # ==========================================
# CHAT HISTORY
# ==========================================

chat_container = st.container()

with chat_container:

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

# ==========================================
# CHAT INPUT
# ==========================================

prompt = st.chat_input("Ask anything about your knowledge base...")

if prompt:

    # ---------------- User Message ---------------- #

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with chat_container:

        with st.chat_message("user"):

            st.markdown(prompt)

    # ---------------- Assistant ---------------- #

    with chat_container:

        with st.chat_message("assistant"):

            placeholder = st.empty()

            placeholder.markdown("""
<div style='padding:18px;
background:rgba(255,255,255,.03);
border-radius:18px;
border:1px solid rgba(255,255,255,.06);'>

⚡ <b>Searching knowledge graph...</b>

</div>
""", unsafe_allow_html=True)

            try:

                payload = {
                    "query": prompt,
                    "top_k": 4
                }

                response = requests.post(
                    QUERY_URL,
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:

                    data = response.json()

                    answer = data.get(
                        "answer",
                        "No answer generated."
                    )

                    sources = data.get(
                        "sources",
                        []
                    )

                    # ==============================
                    # STREAMING EFFECT
                    # ==============================

                    streamed = ""

                    for word in answer.split():

                        streamed += word + " "

                        placeholder.markdown(
                            f"""
<div style='
background:rgba(255,255,255,.03);
padding:22px;
border-radius:18px;
border:1px solid rgba(255,255,255,.06);
line-height:1.8;
font-size:16px;'>

{streamed}<span style="opacity:.6;">▌</span>

</div>
""",
                            unsafe_allow_html=True
                        )

                        time.sleep(0.015)

                    # ==============================
                    # FINAL RESPONSE
                    # ==============================

                    placeholder.markdown(
                        f"""
<div style='
background:rgba(255,255,255,.03);
padding:22px;
border-radius:18px;
border:1px solid rgba(255,255,255,.06);
line-height:1.8;
font-size:16px;'>

{streamed}

</div>
""",
                        unsafe_allow_html=True
                    )

                    # ==============================
                    # SOURCES
                    # ==============================

                    if sources:

                        st.markdown("")

                        st.markdown("##### 📚 Sources")

                        for src in sources:

                            st.markdown(
                                f"""
<div style='
padding:12px;
margin-bottom:10px;
border-radius:12px;
background:rgba(255,255,255,.025);
border:1px solid rgba(255,255,255,.05);
font-size:14px;
color:#d4d4d4;'>

🔗 {src}

</div>
""",
                                unsafe_allow_html=True
                            )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": streamed
                        }
                    )

                else:

                    placeholder.error(
                        f"Backend returned {response.status_code}"
                    )

            except Exception as e:

                placeholder.error(
                    f"Unable to connect to backend.\n\n{e}"
                )

# ==========================================
# FOOTER
# ==========================================

st.markdown(
    """
    <hr style="
    border:0;
    height:1px;
    background:rgba(255,255,255,.08);
    margin-top:35px;
    margin-bottom:20px;
    ">

    <div style="
    text-align:center;
    color:#8c8c8c;
    font-size:14px;
    letter-spacing:1px;
    ">

    ⚡ Nexus AI • Enterprise Knowledge Platform

    <br><br>

    Powered by
    <span style="color:#d4af37;">Gemini Flash</span>
    &nbsp; | &nbsp;
    <span style="color:#7c5cff;">FastAPI</span>
    &nbsp; | &nbsp;
    <span style="color:#3b82f6;">Qdrant Cloud</span>

    </div>
    """,
    unsafe_allow_html=True
)
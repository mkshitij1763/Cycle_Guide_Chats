import streamlit as st
import os
import re

# --- PAGE CONFIG ---
st.set_page_config(page_title="Inito Cycle Support Explorer", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
.stApp { 
    background-color: var(--background-color); 
    color: var(--text-color);
}

.chat-container {
    display: flex;
    flex-direction: column;
    gap: 14px;
    max-width: 850px;
    margin: auto;
    padding-bottom: 60px;
}

.msg-row {
    display: flex;
    width: 100%;
}

.user-row { justify-content: flex-start; }
.support-row { justify-content: flex-end; }

.bubble {
    padding: 14px 18px;
    border-radius: 18px;
    max-width: 75%;
    font-size: 0.95rem;
    line-height: 1.5;
    position: relative;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.support-bubble {
    background: #6C63FF;
    color: #ffffff !important;
    border-bottom-right-radius: 2px;
}

.support-bubble .sender-label {
    color: #FFD700; 
    font-size: 0.75rem;
    font-weight: 800;
    margin-bottom: 6px;
    display: block;
    text-transform: uppercase;
}

.user-bubble {
    background-color: var(--secondary-background-color);
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-bottom-left-radius: 2px;
    color: var(--text-color);
}

.user-bubble .sender-label {
    color: #6C63FF; 
    font-size: 0.75rem;
    font-weight: 800;
    margin-bottom: 6px;
    display: block;
    text-transform: uppercase;
}

.ts {
    font-size: 0.7rem;
    opacity: 0.7;
    display: block;
    margin-top: 10px;
    text-align: right;
}

.date-separator {
    text-align: center;
    margin: 30px 0 15px 0;
    font-size: 0.75rem;
    font-weight: bold;
    color: var(--text-color);
    opacity: 0.5;
    text-transform: uppercase;
    letter-spacing: 2px;
}

section[data-testid="stSidebar"] {
    background-color: var(--secondary-background-color);
}
</style>
""", unsafe_allow_html=True)

# --- COHORT CONFIG ---
COHORTS = ["RAI", "PRH", "RH", "PRAI"]

def get_users_for_cohort(cohort):
    if not os.path.exists(cohort):
        return []
    return sorted([f for f in os.listdir(cohort) if f.endswith(".txt")])

# --- CHAT RENDER ---
def render_chat_file(file_path):
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    current_sender = None
    current_ts = None
    current_message = []

    def flush_message():
        nonlocal current_sender, current_ts, current_message

        if current_sender and current_message:
            msg_text = "<br>".join([l.strip() for l in current_message if l.strip()])

            # ✅ ONLY RULE: exact sender match
            is_support = current_sender.strip() == "Coach"

            bubble_class = "support-bubble" if is_support else "user-bubble"
            row_class = "support-row" if is_support else "user-row"

            # ✅ Always show COACH (not names)
            display_name = "✨ COACH" if is_support else current_sender.strip()

            html = f'''
            <div class="msg-row {row_class}">
                <div class="bubble {bubble_class}">
                    <span class="sender-label">{display_name}</span>
                    <div class="msg-content">{msg_text}</div>
                    <span class="ts">{current_ts}</span>
                </div>
            </div>
            '''
            st.markdown(html, unsafe_allow_html=True)

        current_message = []

    for line in lines:
        clean_line = line.strip()

        if not clean_line or "TOTAL MESSAGES" in clean_line or "THREAD:" in clean_line or "###" in clean_line:
            continue

        if clean_line.startswith("---") and clean_line.endswith("---"):
            flush_message()
            date_label = clean_line.replace("-", "").strip()
            st.markdown(f'<div class="date-separator">{date_label}</div>', unsafe_allow_html=True)
            current_sender = None
            continue

        match = re.match(r"^\[(.*?)\]\s+(.*?):\s*$", clean_line)

        if match:
            flush_message()
            current_ts = match.group(1)
            current_sender = match.group(2)
        else:
            if clean_line.startswith("----"):
                continue
            if current_sender:
                current_message.append(clean_line)

    flush_message()
    st.markdown('</div>', unsafe_allow_html=True)

# --- SIDEBAR & MAIN ---
st.sidebar.title("Cycle Support Program")
st.sidebar.divider()

selected_cohort = st.sidebar.selectbox("📂 Select Cycle Guide:", COHORTS)
users = get_users_for_cohort(selected_cohort)

if users:
    user_display = {u: u.replace(".txt", "").replace("_", " ") for u in users}
    selected_user_file = st.sidebar.selectbox(
        "👤 Select User Chat:",
        options=users,
        format_func=lambda x: user_display[x]
    )

    st.markdown(f"## {selected_cohort} - {user_display[selected_user_file]}")
    st.divider()
    
    full_path = os.path.join(selected_cohort, selected_user_file)
    render_chat_file(full_path)
else:
    st.sidebar.warning(f"No .txt files found in /{selected_cohort}")
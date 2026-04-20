import streamlit as st
import os
import re

# --- PAGE CONFIG ---
st.set_page_config(page_title="Inito Cycle Support Explorer", layout="wide")

# --- ADMIN LINKS MAPPING ---
USER_ADMIN_LINKS = {
    "RH": {
        "Natalia": "https://admin.inito.com/admin/users/298678",
        "Lancena W": "https://admin.inito.com/admin/users/309954",
        "Emily S": "https://admin.inito.com/admin/users/308554",
        "Rachel": "https://admin.inito.com/admin/users/308093",
        "Maggie Johnson": "https://admin.inito.com/admin/users/300844",
        "Mia Shaffer": "https://admin.inito.com/admin/users/307422",
        "Shanda Garren": "https://admin.inito.com/admin/users/308186",
        "Cassandra M": "https://admin.inito.com/admin/users/312533",
        "Marlena": "https://admin.inito.com/admin/users/314233",
        "Sydnie": "https://admin.inito.com/admin/users/309413",
        "Julieta S": "https://admin.inito.com/admin/users/302206",
        "Melanie": "https://admin.inito.com/admin/users/300031",
        "Jess P": "https://admin.inito.com/admin/users/314727",
        "Alyssa Dispenziere": "https://admin.inito.com/admin/users/314877",
        "Jaime": "https://admin.inito.com/admin/users/317379",
        "Stephanie F": "https://admin.inito.com/admin/users/320055",
        "Junavi Hayes": "https://admin.inito.com/admin/users/318455",
        "Janice Hargett": "https://admin.inito.com/admin/users/322381",
        "Brieanne Hayden": "https://admin.inito.com/admin/users/324846",
        "Brooke": "https://admin.inito.com/admin/users/323282",
        "Ashlie": "https://admin.inito.com/admin/users/312256",
    },
    "PRH": {
        "Maria": "https://admin.inito.com/admin/users/303451",
        "Daniella": "https://admin.inito.com/admin/users/296749",
        "Fiona fortenberry": "https://admin.inito.com/admin/users/312150",
        "Kayla Reuter": "https://admin.inito.com/admin/users/307500",
        "Lizzy Roberts": "https://admin.inito.com/admin/users/310347",
        "Christine R": "https://admin.inito.com/admin/users/302691",
        "Amanda Hall": "https://admin.inito.com/admin/users/304587",
        "Dawnine Aragon": "https://admin.inito.com/admin/users/303148",
        "Kennis": "https://admin.inito.com/admin/users/311872",
        "Rori": "https://admin.inito.com/admin/users/313043",
        "Paige Kozdra": "https://admin.inito.com/admin/users/315245",
        "Sara": "https://admin.inito.com/admin/users/315728",
        "Nicole": "https://admin.inito.com/admin/users/299504",
        "Lauren Oneill": "https://admin.inito.com/admin/users/313360",
        "Peta Kimber": "https://admin.inito.com/admin/users/303321",
        "Charlene Traynham": "https://admin.inito.com/admin/users/305237",
        "Christy Loera": "https://admin.inito.com/admin/users/302549",
        "Francesca Pietri": "https://admin.inito.com/admin/users/302118",
        "Ashley Cheyemi McNeil": "https://admin.inito.com/admin/users/303113",
        "NaShea H": "https://admin.inito.com/admin/users/305978",
        "Melissa Morales": "https://admin.inito.com/admin/users/300198",
        "Andrea": "https://admin.inito.com/admin/users/320414",
        "Cali": "https://admin.inito.com/admin/users/318358",
    },
    "RAI": {
    "Maya D": "https://admin.inito.com/admin/users/303062",
    "Kaylie F": "https://admin.inito.com/admin/users/299734",
    "Ellie F": "https://admin.inito.com/admin/users/300456",
    "Nicolette S": "https://admin.inito.com/admin/users/300306",
    "Tina M": "https://admin.inito.com/admin/users/312182",
    "Heather A": "https://admin.inito.com/admin/users/305044",
    "Elena G": "https://admin.inito.com/admin/users/305755",
    "Dayle A": "https://admin.inito.com/admin/users/312496",
    "Ivelisse V": "https://admin.inito.com/admin/users/308219",
    "Meghan G": "https://admin.inito.com/admin/users/309131",
    "Mackenzie D": "https://admin.inito.com/admin/users/312909",
    "Kayla H": "https://admin.inito.com/admin/users/314035",
    "Danielle R": "https://admin.inito.com/admin/users/309663",
    "Rachel C": "https://admin.inito.com/admin/users/314119",
    "Laura J": "https://admin.inito.com/admin/users/310703",
    "Hayley L": "https://admin.inito.com/admin/users/316258",
    "Lindsey R": "https://admin.inito.com/admin/users/316334",
    "Karis M": "https://admin.inito.com/admin/users/322380",
    "Karly C": "https://admin.inito.com/admin/users/319224",
    "Annika P": "https://admin.inito.com/admin/users/320062",
    "Sarah M": "https://admin.inito.com/admin/users/320534",
    "Monique C": "https://admin.inito.com/admin/users/321400",
    "Megan": "https://admin.inito.com/admin/users/322825",
    "Jessica S": "https://admin.inito.com/admin/users/320603",
    "Tehretta T": "https://admin.inito.com/admin/users/324409",
    "Madison D": "https://admin.inito.com/admin/users/325881"
},
    "PRAI": {
    "Morgan T": "https://admin.inito.com/admin/users/303615",
    "Romance B": "https://admin.inito.com/admin/users/300174",
    "Tara A": "https://admin.inito.com/admin/users/311219",
    "Andrea H": "https://admin.inito.com/admin/users/303087",
    "Nicole M": "https://admin.inito.com/admin/users/311834",
    "Elizabeth Z": "https://admin.inito.com/admin/users/304494",
    "Brianna M": "https://admin.inito.com/admin/users/310784",
    "Caroline M": "https://admin.inito.com/admin/users/306120",
    "Kimberly B": "https://admin.inito.com/admin/users/300257",
    "Sarah S": "https://admin.inito.com/admin/users/305675",
    "Asha D": "https://admin.inito.com/admin/users/306926",
    "Ashley F": "https://admin.inito.com/admin/users/312193",
    "Jennifer Mi": "https://admin.inito.com/admin/users/312395",
    "Chelsea L": "https://admin.inito.com/admin/users/311831",
    "Sandy T": "https://admin.inito.com/admin/users/313705",
    "Mallory M": "https://admin.inito.com/admin/users/320554",
    "Eliana G": "https://admin.inito.com/admin/users/316843",
    "Sarah D": "https://admin.inito.com/admin/users/316613",
    "Allison B": "https://admin.inito.com/admin/users/320557"
}
}

# --- CUSTOM CSS ---
st.markdown("""
<style>
.stApp { background-color: var(--background-color); color: var(--text-color); }
.chat-container { display: flex; flex-direction: column; gap: 14px; max-width: 850px; margin: auto; padding-bottom: 60px; }
.msg-row { display: flex; width: 100%; }
.user-row { justify-content: flex-start; }
.support-row { justify-content: flex-end; }
.bubble { padding: 14px 18px; border-radius: 18px; max-width: 75%; font-size: 0.95rem; line-height: 1.5; position: relative; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
.support-bubble { background: #6C63FF; color: #ffffff !important; border-bottom-right-radius: 2px; }
.support-bubble .sender-label { color: #FFD700; font-size: 0.75rem; font-weight: 800; margin-bottom: 6px; display: block; text-transform: uppercase; }
.user-bubble { background-color: var(--secondary-background-color); border: 1px solid rgba(128, 128, 128, 0.2); border-bottom-left-radius: 2px; color: var(--text-color); }
.user-bubble .sender-label { color: #6C63FF; font-size: 0.75rem; font-weight: 800; margin-bottom: 6px; display: block; text-transform: uppercase; }
.ts { font-size: 0.7rem; opacity: 0.7; display: block; margin-top: 10px; text-align: right; }
.date-separator { text-align: center; margin: 30px 0 15px 0; font-size: 0.75rem; font-weight: bold; color: var(--text-color); opacity: 0.5; text-transform: uppercase; letter-spacing: 2px; }
section[data-testid="stSidebar"] { background-color: var(--secondary-background-color); }
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
    current_sender, current_ts, current_message = None, None, []

    def flush_message():
        nonlocal current_sender, current_ts, current_message
        if current_sender and current_message:
            msg_text = "<br>".join([l.strip() for l in current_message if l.strip()])
            is_support = current_sender.strip() == "Coach"
            bubble_class = "support-bubble" if is_support else "user-bubble"
            row_class = "support-row" if is_support else "user-row"
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
        if not clean_line or any(x in clean_line for x in ["TOTAL MESSAGES", "THREAD:", "###"]): continue
        if clean_line.startswith("---") and clean_line.endswith("---"):
            flush_message()
            st.markdown(f'<div class="date-separator">{clean_line.replace("-", "").strip()}</div>', unsafe_allow_html=True)
            current_sender = None
            continue
        match = re.match(r"^\[(.*?)\]\s+(.*?):\s*$", clean_line)
        if match:
            flush_message()
            current_ts, current_sender = match.group(1), match.group(2)
        else:
            if not clean_line.startswith("----") and current_sender:
                current_message.append(clean_line)

    flush_message()
    st.markdown('</div>', unsafe_allow_html=True)

# --- SIDEBAR & MAIN ---
st.sidebar.title("Cycle Support Program")
st.sidebar.divider()

selected_cohort = st.sidebar.selectbox("📂 Select Cycle Guide:", COHORTS)
users = get_users_for_cohort(selected_cohort)

if users:
    # formatting user names for display (e.g., Natalia_P.txt -> Natalia P)
    user_display = {u: u.replace(".txt", "").replace("_", " ") for u in users}
    selected_user_file = st.sidebar.selectbox(
        "👤 Select User Chat:",
        options=users,
        format_func=lambda x: user_display[x]
    )

    # Clean name for link lookup
    display_name = user_display[selected_user_file]

    # --- MAIN TITLE ---
    st.markdown(f"## {selected_cohort} - {display_name}")
    
    # --- ADMIN LINK LOGIC ---
    # Retrieve the admin link if it exists in our dictionary
    admin_url = USER_ADMIN_LINKS.get(selected_cohort, {}).get(display_name)
    
    if admin_url:
        st.markdown(f"## 🔗 [View Admin Profile for {display_name}]({admin_url})")
    else:
        st.markdown("#### 🔗 *Admin Link Not Available*")

    st.divider()
    
    full_path = os.path.join(selected_cohort, selected_user_file)
    render_chat_file(full_path)
else:
    st.sidebar.warning(f"No .txt files found in /{selected_cohort}")
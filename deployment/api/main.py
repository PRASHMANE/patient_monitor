import streamlit as st
import sqlite3
import bcrypt
from deployment.api.add import add_patient
from deployment.api.remove_pat import remove_pat_info
from deployment.api.display_pat import pat_display  
# ---------- CSS for dashboard ----------
st.markdown("""
<style>
/* Global Background with Animated Gradient */
body {
    background: linear-gradient(270deg, #0E1117, #1E90FF, #104E8B);
    background-size: 600% 600%;
    animation: gradientShift 20s ease infinite;
    color: #FAFAFA;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    transition: all 0.3s ease-in-out;
}

@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Sidebar - Glassmorphism */
section[data-testid="stSidebar"] {
    background: rgba(15, 20, 40, 0.6);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-right: 2px solid rgba(255,255,255,0.2);
    box-shadow: 4px 0px 20px rgba(0,0,0,0.3);
    color: #fff;
}

/* Buttons - Neon Glow */
.stButton>button {
    background: linear-gradient(90deg, #FF4B4B, #FF1C1C);
    color: #fff;
    border-radius: 15px;
    padding: 0.7em 1.3em;
    font-weight: bold;
    border: none;
    box-shadow: 0px 0px 20px rgba(255,75,75,0.7);
    transition: all 0.3s ease-in-out;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #FF1C1C, #B22222);
    transform: scale(1.08) rotate(-1deg);
    box-shadow: 0px 0px 25px rgba(255,28,28,0.9);
}

/* Headings - Gradient Text */
h1, h2, h3 {
    background: linear-gradient(90deg, #1E90FF, #FF4B4B);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SQLite DB ----------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT UNIQUE,
    password TEXT
)
''')
conn.commit()

# ---------- Helper Functions ----------
def signup(username, email, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                  (username, email, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login(email, password):
    c.execute("SELECT password, username FROM users WHERE email=?", (email,))
    row = c.fetchone()
    if row and bcrypt.checkpw(password.encode(), row[0]):
        return row[1]
    return None

# ---------- Session State ----------
if "page" not in st.session_state:
    st.session_state.page = "login"  # default page
if "username" not in st.session_state:
    st.session_state.username = ""
if "email" not in st.session_state:
    st.session_state.email = ""
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------- Pages ----------
if st.session_state.page == "login":
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.session_state.email = email
            st.session_state.page = "dashboard"  # redirect to dashboard
        else:
            st.error("Invalid email or password")
    
    st.markdown("---")
    st.write("Or create a new account")
    if st.button("Go to Sign Up"):
        st.session_state.page = "signup"

elif st.session_state.page == "signup":
    st.subheader("Sign Up")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        if signup(username, email, password):
            st.success("Account created! Redirecting to login...")
            st.session_state.page = "login"
        else:
            st.error("Email already exists.")
    if st.button("Go to Login"):
        st.session_state.page = "login"

# ---------- Dashboard / Patient Management ----------
elif st.session_state.page == "dashboard" and st.session_state.logged_in:
    #st.title("🏥 Patient Management System")

    import streamlit as st
    st.markdown("""
        <style>
            /* Global Background with Animated Gradient */
            body {
                background: linear-gradient(270deg, #0E1117, #1E90FF, #104E8B);
                background-size: 600% 600%;
                animation: gradientShift 20s ease infinite;
                color: #FAFAFA;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                transition: all 0.3s ease-in-out;
            }

            @keyframes gradientShift {
                0% {background-position: 0% 50%;}
                50% {background-position: 100% 50%;}
                100% {background-position: 0% 50%;}
            }

            /* Sidebar - Glassmorphism */
            section[data-testid="stSidebar"] {
                background: rgba(15, 20, 40, 0.6);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border-right: 2px solid rgba(255,255,255,0.2);
                box-shadow: 4px 0px 20px rgba(0,0,0,0.3);
                color: #fff;
            }

            /* Sidebar text */
            section[data-testid="stSidebar"] .css-1d391kg,
            section[data-testid="stSidebar"] .css-qri22k {
                color: #f0f0f0 !important;
                font-weight: 600;
            }

            /* Buttons - Neon Glow */
            .stButton>button {
                background: linear-gradient(90deg, #FF4B4B, #FF1C1C);
                color: #fff;
                border-radius: 15px;
                padding: 0.7em 1.3em;
                font-weight: bold;
                border: none;
                box-shadow: 0px 0px 20px rgba(255,75,75,0.7);
                transition: all 0.3s ease-in-out;
            }

            .stButton>button:hover {
                background: linear-gradient(90deg, #FF1C1C, #B22222);
                transform: scale(1.08) rotate(-1deg);
                box-shadow: 0px 0px 25px rgba(255,28,28,0.9);
            }

            /* Metric Cards - Glass with Glow */
            div[data-testid="stMetric"] {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255,255,255,0.15);
                padding: 1em;
                border-radius: 20px;
                box-shadow: 0 4px 25px rgba(0,0,0,0.4);
                text-align: center;
                transition: all 0.4s ease-in-out;
            }
            div[data-testid="stMetric"]:hover {
                transform: translateY(-8px) scale(1.03);
                background: rgba(255,255,255,0.15);
                box-shadow: 0 8px 30px rgba(0,0,0,0.5), 0 0 20px rgba(30,144,255,0.5);
            }

            /* Headings - Gradient Text */
            h1, h2, h3 {
                background: linear-gradient(90deg, #1E90FF, #FF4B4B);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: fadeIn 1.2s ease-in-out;
                letter-spacing: 1px;
            }

            @keyframes fadeIn {
                from {opacity: 0; transform: translateY(-10px);}
                to {opacity: 1; transform: translateY(0);}
            }

            /* Animating icons/images */
            img {
                transition: transform 0.4s ease-in-out;
            }
            img:hover {
                transform: scale(1.1) rotate(2deg);
            }

            /* Custom Scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
            }
            ::-webkit-scrollbar-track {
                background: rgba(255,255,255,0.05);
            }
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(180deg, #1E90FF, #104E8B);
                border-radius: 10px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(180deg, #FF4B4B, #FF1C1C);
            }
        </style>
    """, unsafe_allow_html=True)

    #🔹 Sidebar button helper
    def sidebar_button(icon_url, label):
        cols = st.sidebar.columns([1, 6])
        with cols[0]:
            st.image(icon_url, width=20)
        with cols[1]:
            return st.button(label)


    # 🔹 Sidebar Navigation
    if sidebar_button("https://img.icons8.com/ios-filled/24/00C896/home.png", "Home"):
        st.session_state.subpage = "Home"

    if sidebar_button("https://img.icons8.com/ios-filled/24/00C896/plus.png", "Add Patient"):
        st.session_state.subpage = "Add Patient"

    if sidebar_button("https://img.icons8.com/ios-filled/24/00C896/minus.png", "Remove Patient"):
        st.session_state.subpage = "Remove Patient"

    if sidebar_button("https://img.icons8.com/ios-filled/24/00C896/user-male-circle.png", "Patient Details"):
        st.session_state.subpage = "Patient Details"

    if sidebar_button("https://img.icons8.com/ios-filled/24/00C896/camera.png", "Add Camera URL"):
        st.session_state.subpage = "Add Camera URL"

    if sidebar_button("https://img.icons8.com/ios-filled/24/00C896/heart-monitor.png", "Patient Monitor"):
        st.session_state.subpage = "Patient Monitor"

    # Default subpage
    if "subpage" not in st.session_state:
        st.session_state.subpage = "Home"
    # 🔹 Page Content
    #st.title("🏥 Patient Management System")

    if st.session_state.subpage == "Home":
        st.header("Welcome")
        st.write("Use the sidebar to navigate between modules.")

        # Logout button
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.email = ""
            st.session_state.page = "login"

    elif st.session_state.subpage == "Add Patient":
        st.header("➕ Add Patient")
        add_patient()

    elif st.session_state.subpage == "Remove Patient":
        st.header("➖ Remove Patient")
        id = st.text_input("Enter ID to Remove")
        if st.button("Remove Patients"):
            if id.strip() == "":
                st.warning("Please enter a ID!")
            else:
                remove_pat_info(id)

    elif st.session_state.subpage == "Patient Details":
        st.header("📋 Patient Details")
        pat_display()

    elif st.session_state.subpage == "Add Camera URL":
        st.header("📷 Add Camera URL")
        url = st.text_input("Enter Camera Stream URL")
        if st.button("Save"):
            st.success(f"Camera URL saved: {url}")

    elif st.session_state.subpage == "Patient Monitor":
        st.header("❤️ Patient Monitor")
        heart_rate = st.slider("Heart Rate (BPM)", 40, 180, 75)
        oxygen = st.slider("Oxygen (%)", 70, 100, 96)
        temp = st.slider("Temperature (°C)", 30, 45, 37)

        st.metric("Heart Rate", f"{heart_rate} BPM")
        st.metric("Oxygen Level", f"{oxygen}%")
        st.metric("Temperature", f"{temp}°C")

   

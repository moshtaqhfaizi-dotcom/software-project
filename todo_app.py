import streamlit as st
import json
import os
from datetime import datetime

# --- تنظیمات صفحه ---
st.set_page_config(
    page_title="وظایف من",
    page_icon="✅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- فایل ذخیره‌سازی ---
DATA_FILE = "tasks.json"

# --- رنگ‌های زیبا ---
COLORS = [
    "#FF6B6B",  # قرمز روشن
    "#4ECDC4",  # فیروزه‌ای
    "#45B7D1",  # آبی آسمانی
    "#96CEB4",  # سبز نعنایی
    "#FECA57",  # زرد طلایی
    "#DDA0DD",  # بنفش ملایم
    "#98D8C8",  # سبزآبی
    "#F7B731"  # نارنجی
]


# --- توابع کمکی ---
def load_tasks():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


# --- بارگذاری وظایف ---
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

tasks = st.session_state.tasks

# --- استایل RTL و فارسی ---
st.markdown("""
<style>
    .main > div {direction: rtl; text-align: right;}
    .stButton > button {width: 100%; margin-top: 5px;}
    .task-card {padding: 12px; border-radius: 12px; margin: 8px 0; font-weight: 600;}
    .done {opacity: 0.6; text-decoration: line-through;}
    h1 {text-align: center; color: #2E86C1;}
</style>
""", unsafe_allow_html=True)

# --- عنوان ---
st.markdown("<h1>📝 وظایف من</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- فرم اضافه کردن وظیفه ---
with st.form("add_task_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        new_task = st.text_input("وظیفه جدید", placeholder="مثلاً: خرید شیر", label_visibility="collapsed")
    with col2:
        color_idx = st.selectbox("رنگ", options=range(len(COLORS)), format_func=lambda x: "",
                                 label_visibility="collapsed")

    submitted = st.form_submit_button("➕ اضافه کن")

    if submitted and new_task.strip():
        tasks.append({
            "id": len(tasks),
            "title": new_task.strip(),
            "done": False,
            "color": COLORS[color_idx]
        })
        save_tasks(tasks)
        st.success("وظیفه اضافه شد!")
        st.rerun()

# --- نمایش وظایف ---
if not tasks:
    st.info("هنوز وظیفه‌ای اضافه نکردی. با دکمه بالا شروع کن!")
else:
    active_tasks = [t for t in tasks if not t["done"]]
    done_tasks = [t for t in tasks if t["done"]]

    # وظایف فعال
    for task in active_tasks:
        col1, col2, col3 = st.columns([1, 5, 1])
        with col1:
            if st.button("✅", key=f"done_{task['id']}"):
                task["done"] = True
                save_tasks(tasks)
                st.rerun()
        with col2:
            st.markdown(
                f"<div class='task-card' style='background-color:{task['color']};'>"
                f"{task['title']}</div>", unsafe_allow_html=True
            )
        with col3:
            if st.button("🗑️", key=f"del_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()

    # وظایف انجام‌شده
    if done_tasks:
        st.markdown("---")
        st.markdown("**✅ انجام‌شده‌ها:**")
        for task in done_tasks:
            st.markdown(
                f"<div class='task-card done' style='background-color:{task['color']};'>"
                f"✦ {task['title']}</div>", unsafe_allow_html=True
            )

# --- ذخیره خودکار ---
save_tasks(tasks)
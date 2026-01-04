import streamlit as st
import json
import os
from datetime import datetime, timedelta
import uuid  # برای ID منحصربه‌فرد

# --- تنظیمات صفحه ---
st.set_page_config(
    page_title="وظایف من - MVP",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- فایل ذخیره‌سازی ---
DATA_FILE = "tasks.json"

# --- رنگ‌ها ---
COLORS = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
    "#FECA57", "#DDA0DD", "#98D8C8", "#F7B731"
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

# --- بارگذاری وظایف با Session State ---
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()
if "theme" not in st.session_state:
    st.session_state.theme = "light"  # تم پیش‌فرض

tasks = st.session_state.tasks

# --- استایل RTL، فارسی و تم ---
theme_style = """
<style>
    .main > div {direction: rtl; text-align: right;}
    .stButton > button {width: 100%; margin-top: 5px; border-radius: 8px;}
    .task-card {padding: 12px; border-radius: 12px; margin: 8px 0; font-weight: 600; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
    .done {opacity: 0.6; text-decoration: line-through;}
    h1 {text-align: center; color: #2E86C1;}
    [data-testid="stSidebar"] {background-color: #f8f9fa;}
</style>
""" if st.session_state.theme == "light" else """
<style>
    .main > div {direction: rtl; text-align: right;}
    .stButton > button {width: 100%; margin-top: 5px; border-radius: 8px;}
    .task-card {padding: 12px; border-radius: 12px; margin: 8px 0; font-weight: 600; box-shadow: 0 2px 4px rgba(255,255,255,0.1);}
    .done {opacity: 0.6; text-decoration: line-through;}
    h1 {text-align: center; color: #AED6F1;}
    [data-testid="stSidebar"] {background-color: #2C3E50;}
</style>
"""
st.markdown(theme_style, unsafe_allow_html=True)

# --- سایدبار برای تنظیمات ---
with st.sidebar:
    st.title("تنظیمات")
    st.session_state.theme = st.selectbox("تم", ["light", "dark"], index=0 if st.session_state.theme == "light" else 1)
    search_query = st.text_input("جستجو در وظایف")
    st.markdown("---")
    st.info("MVP پروژه Todo App - نسخه ۱.۰")

# --- عنوان اصلی ---
st.markdown("<h1>📝 وظایف من (MVP)</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- فرم اضافه کردن وظیفه ---
with st.form("add_task_form", clear_on_submit=True):
    cols = st.columns([3, 1, 1, 1])
    with cols[0]:
        new_title = st.text_input("عنوان وظیفه", placeholder="مثلاً: خرید نان")
    with cols[1]:
        due_date = st.date_input("سررسید", min_value=datetime.today().date())
    with cols[2]:
        color_idx = st.selectbox("رنگ", options=range(len(COLORS)), format_func=lambda x: f"رنگ {x+1}")
    with cols[3]:
        st.form_submit_button("➕ اضافه کن")

    if new_title.strip():
        new_task = {
            "id": str(uuid.uuid4()),
            "title": new_title.strip(),
            "due_date": due_date.isoformat() if due_date else None,
            "color": COLORS[color_idx],
            "done": False,
            "reminder_sent": False
        }
        tasks.append(new_task)
        save_tasks(tasks)
        st.success("وظیفه اضافه شد!")
        st.rerun()

# --- فیلتر و جستجو ---
filtered_tasks = [t for t in tasks if search_query.lower() in t["title"].lower()] if search_query else tasks
active_tasks = [t for t in filtered_tasks if not t["done"]]
done_tasks = [t for t in filtered_tasks if t["done"]]

# --- چک یادآوری (ساده با Warning) ---
for task in active_tasks:
    if task["due_date"] and not task["reminder_sent"]:
        due = datetime.fromisoformat(task["due_date"])
        if due < datetime.now() + timedelta(days=1):
            st.warning(f"یادآوری: وظیفه '{task['title']}' نزدیک سررسید است!")
            task["reminder_sent"] = True
            save_tasks(tasks)

# --- نمایش وظایف فعال ---
if not active_tasks and not done_tasks:
    st.info("هنوز وظیفه‌ای اضافه نکردی. از فرم بالا شروع کن!")
else:
    st.subheader("وظایف فعال")
    for task in active_tasks:
        cols = st.columns([1, 4, 1, 1, 1])
        with cols[0]:
            if st.button("✅", key=f"done_{task['id']}"):
                task["done"] = True
                save_tasks(tasks)
                st.rerun()
        with cols[1]:
            due_str = f" - سررسید: {task['due_date']}" if task['due_date'] else ""
            st.markdown(
                f"<div class='task-card' style='background-color:{task['color']};'>"
                f"{task['title']}{due_str}</div>", unsafe_allow_html=True
            )
        with cols[2]:
            if st.button("✏️", key=f"edit_{task['id']}"):
                st.session_state.edit_task = task  # برای ویرایش آینده
        with cols[3]:
            if st.button("🗑️", key=f"del_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()
        with cols[4]:
            if st.button("🔄", key=f"undo_{task['id']}"):
                pass  # برای برگرداندن آینده

    # --- وظایف انجام‌شده ---
    if done_tasks:
        with st.expander("✅ انجام‌شده‌ها (کلیک برای دیدن)"):
            for task in done_tasks:
                st.markdown(
                    f"<div class='task-card done' style='background-color:{task['color']};'>"
                    f"✦ {task['title']}</div>", unsafe_allow_html=True
                )

# --- ذخیره نهایی ---
save_tasks(tasks)
"""
Todo List Manager - نسخه CLI
ذخیره‌سازی در فایل todos.json
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# مسیر فایل داده
DATA_FILE = "todos.json"

class TodoItem:
    def __init__(self, id: int, title: str, description: str = "", completed: bool = False, created_at: str = None):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'TodoItem':
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data["completed"],
            created_at=data["created_at"]
        )


class TodoManager:
    def __init__(self):
        self.todos: List[TodoItem] = []
        self.next_id = 1
        self.load_from_file()

    def load_from_file(self):
        """بارگذاری کارها از فایل JSON"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.todos = [TodoItem.from_dict(item) for item in data.get("todos", [])]
                    if self.todos:
                        self.next_id = max(item.id for item in self.todos) + 1
            except Exception as e:
                print(f"خطا در بارگذاری فایل: {e}")
                self.todos = []

    def save_to_file(self):
        """ذخیره کارها در فایل JSON"""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "todos": [todo.to_dict() for todo in self.todos]
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطا در ذخیره فایل: {e}")

    def add_todo(self, title: str, description: str = ""):
        """افزودن کار جدید"""
        todo = TodoItem(id=self.next_id, title=title.strip(), description=description.strip())
        self.todos.append(todo)
        self.next_id += 1
        self.save_to_file()
        print(f"کار '{title}' با موفقیت اضافه شد.")

    def edit_todo(self, todo_id: int, title: Optional[str] = None, description: Optional[str] = None):
        """ویرایش کار"""
        todo = self.find_by_id(todo_id)
        if not todo:
            print("کار یافت نشد.")
            return
        if title is not None:
            todo.title = title.strip()
        if description is not None:
            todo.description = description.strip()
        self.save_to_file()
        print("کار با موفقیت ویرایش شد.")

    def delete_todo(self, todo_id: int):
        """حذف کار"""
        todo = self.find_by_id(todo_id)
        if not todo:
            print("کار یافت نشد.")
            return
        self.todos = [t for t in self.todos if t.id != todo_id]
        self.save_to_file()
        print("کار با موفقیت حذف شد.")

    def toggle_complete(self, todo_id: int):
        """تغییر وضعیت انجام/عدم انجام"""
        todo = self.find_by_id(todo_id)
        if not todo:
            print("کار یافت نشد.")
            return
        todo.completed = not todo.completed
        status = "انجام‌شده" if todo.completed else "انجام‌نشده"
        self.save_to_file()
        print(f"وضعیت کار به '{status}' تغییر کرد.")

    def find_by_id(self, todo_id: int) -> Optional[TodoItem]:
        """جستجوی کار بر اساس شناسه"""
        return next((t for t in self.todos if t.id == todo_id), None)

    def list_todos(self, filter_status: str = "all", sort_by: str = "created"):
        """نمایش فهرست کارها با فیلتر و مرتب‌سازی"""
        filtered = self.todos
        if filter_status == "pending":
            filtered = [t for t in self.todos if not t.completed]
        elif filter_status == "completed":
            filtered = [t for t in self.todos if t.completed]

        # مرتب‌سازی
        if sort_by == "created":
            filtered.sort(key=lambda x: x.created_at, reverse=True)
        elif sort_by == "status":
            filtered.sort(key=lambda x: (x.completed, x.created_at))

        if not filtered:
            print("هیچ کاری یافت نشد.")
            return

        print("\n" + "="*60)
        for todo in filtered:
            status = "✓" if todo.completed else "☐"
            desc = f" ({todo.description})" if todo.description else ""
            print(f"{status} [{todo.id}] {todo.title}{desc} — {todo.created_at}")
        print("="*60 + "\n")


def main():
    manager = TodoManager()
    print("به برنامه مدیریت فهرست کارهای روزانه خوش آمدید!")

    while True:
        print("\nمنو:")
        print("1. افزودن کار جدید")
        print("2. نمایش فهرست کارها")
        print("3. ویرایش کار")
        print("4. حذف کار")
        print("5. علامت‌زدن به عنوان انجام‌شده/بازگرداندن")
        print("6. خروج")

        choice = input("\nانتخاب کنید (1-6): ").strip()

        if choice == "1":
            title = input("عنوان کار: ").strip()
            if not title:
                print("عنوان نمی‌تواند خالی باشد.")
                continue
            desc = input("توضیح (اختیاری): ").strip()
            manager.add_todo(title, desc)

        elif choice == "2":
            print("\nفیلتر: 1) همه  2) انجام‌نشده  3) انجام‌شده")
            f = input("انتخاب فیلتر (1-3): ").strip()
            filter_map = {"1": "all", "2": "pending", "3": "completed"}
            filter_status = filter_map.get(f, "all")

            print("مرتب‌سازی: 1) زمان ایجاد  2) وضعیت")
            s = input("انتخاب مرتب‌سازی (1-2): ").strip()
            sort_map = {"1": "created", "2": "status"}
            sort_by = sort_map.get(s, "created")

            manager.list_todos(filter_status, sort_by)

        elif choice == "3":
            try:
                tid = int(input("شناسه کار: "))
                title = input("عنوان جدید (خالی = بدون تغییر): ").strip()
                desc = input("توضیح جدید (خالی = بدون تغییر): ").strip()
                manager.edit_todo(tid,
                                  title=None if title == "" else title,
                                  description=None if desc == "" else desc)
            except ValueError:
                print("شناسه باید عدد باشد.")

        elif choice == "4":
            try:
                tid = int(input("شناسه کار برای حذف: "))
                confirm = input(f"آیا از حذف کار {tid} مطمئن هستید؟ (y/n): ")
                if confirm.lower() == 'y':
                    manager.delete_todo(tid)
            except ValueError:
                print("شناسه باید عدد باشد.")

        elif choice == "5":
            try:
                tid = int(input("شناسه کار: "))
                manager.toggle_complete(tid)
            except ValueError:
                print("شناسه باید عدد باشد.")

        elif choice == "6":
            print("خداحافظ! کارهای شما ذخیره شدند.")
            break

        else:
            print("انتخاب نامعتبر. لطفاً دوباره تلاش کنید.")


if __name__ == "__main__":
    main()
# # """
# # Todo List Manager - نسخه CLI
# # ذخیره‌سازی در فایل todos.json
# # """
# #
# # import json
# # import os
# # from datetime import datetime
# # from typing import List, Dict, Optional
# #
# # # مسیر فایل داده
# # DATA_FILE = "todos.json"
# #
# # class TodoItem:
# #     def __init__(self, id: int, title: str, description: str = "", completed: bool = False, created_at: str = None):
# #         self.id = id
# #         self.title = title
# #         self.description = description
# #         self.completed = completed
# #         self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# #
# #     def to_dict(self) -> Dict:
# #         return {
# #             "id": self.id,
# #             "title": self.title,
# #             "description": self.description,
# #             "completed": self.completed,
# #             "created_at": self.created_at
# #         }
# #
# #     @classmethod
# #     def from_dict(cls, data: Dict) -> 'TodoItem':
# #         return cls(
# #             id=data["id"],
# #             title=data["title"],
# #             description=data.get("description", ""),
# #             completed=data["completed"],
# #             created_at=data["created_at"]
# #         )
# #
# #
# # class TodoManager:
# #     def __init__(self):
# #         self.todos: List[TodoItem] = []
# #         self.next_id = 1
# #         self.load_from_file()
# #
# #     def load_from_file(self):
# #         """بارگذاری کارها از فایل JSON"""
# #         if os.path.exists(DATA_FILE):
# #             try:
# #                 with open(DATA_FILE, "r", encoding="utf-8") as f:
# #                     data = json.load(f)
# #                     self.todos = [TodoItem.from_dict(item) for item in data.get("todos", [])]
# #                     if self.todos:
# #                         self.next_id = max(item.id for item in self.todos) + 1
# #             except Exception as e:
# #                 print(f"خطا در بارگذاری فایل: {e}")
# #                 self.todos = []
# #
# #     def save_to_file(self):
# #         """ذخیره کارها در فایل JSON"""
# #         try:
# #             with open(DATA_FILE, "w", encoding="utf-8") as f:
# #                 json.dump({
# #                     "todos": [todo.to_dict() for todo in self.todos]
# #                 }, f, ensure_ascii=False, indent=2)
# #         except Exception as e:
# #             print(f"خطا در ذخیره فایل: {e}")
# #
# #     def add_todo(self, title: str, description: str = ""):
# #         """افزودن کار جدید"""
# #         todo = TodoItem(id=self.next_id, title=title.strip(), description=description.strip())
# #         self.todos.append(todo)
# #         self.next_id += 1
# #         self.save_to_file()
# #         print(f"کار '{title}' با موفقیت اضافه شد.")
# #
# #     def edit_todo(self, todo_id: int, title: Optional[str] = None, description: Optional[str] = None):
# #         """ویرایش کار"""
# #         todo = self.find_by_id(todo_id)
# #         if not todo:
# #             print("کار یافت نشد.")
# #             return
# #         if title is not None:
# #             todo.title = title.strip()
# #         if description is not None:
# #             todo.description = description.strip()
# #         self.save_to_file()
# #         print("کار با موفقیت ویرایش شد.")
# #
# #     def delete_todo(self, todo_id: int):
# #         """حذف کار"""
# #         todo = self.find_by_id(todo_id)
# #         if not todo:
# #             print("کار یافت نشد.")
# #             return
# #         self.todos = [t for t in self.todos if t.id != todo_id]
# #         self.save_to_file()
# #         print("کار با موفقیت حذف شد.")
# #
# #     def toggle_complete(self, todo_id: int):
# #         """تغییر وضعیت انجام/عدم انجام"""
# #         todo = self.find_by_id(todo_id)
# #         if not todo:
# #             print("کار یافت نشد.")
# #             return
# #         todo.completed = not todo.completed
# #         status = "انجام‌شده" if todo.completed else "انجام‌نشده"
# #         self.save_to_file()
# #         print(f"وضعیت کار به '{status}' تغییر کرد.")
# #
# #     def find_by_id(self, todo_id: int) -> Optional[TodoItem]:
# #         """جستجوی کار بر اساس شناسه"""
# #         return next((t for t in self.todos if t.id == todo_id), None)
# #
# #     def list_todos(self, filter_status: str = "all", sort_by: str = "created"):
# #         """نمایش فهرست کارها با فیلتر و مرتب‌سازی"""
# #         filtered = self.todos
# #         if filter_status == "pending":
# #             filtered = [t for t in self.todos if not t.completed]
# #         elif filter_status == "completed":
# #             filtered = [t for t in self.todos if t.completed]
# #
# #         # مرتب‌سازی
# #         if sort_by == "created":
# #             filtered.sort(key=lambda x: x.created_at, reverse=True)
# #         elif sort_by == "status":
# #             filtered.sort(key=lambda x: (x.completed, x.created_at))
# #
# #         if not filtered:
# #             print("هیچ کاری یافت نشد.")
# #             return
# #
# #         print("\n" + "="*60)
# #         for todo in filtered:
# #             status = "✓" if todo.completed else "☐"
# #             desc = f" ({todo.description})" if todo.description else ""
# #             print(f"{status} [{todo.id}] {todo.title}{desc} — {todo.created_at}")
# #         print("="*60 + "\n")
# #
# #
# # def main():
# #     manager = TodoManager()
# #     print("به برنامه مدیریت فهرست کارهای روزانه خوش آمدید!")
# #
# #     while True:
# #         print("\nمنو:")
# #         print("1. افزودن کار جدید")
# #         print("2. نمایش فهرست کارها")
# #         print("3. ویرایش کار")
# #         print("4. حذف کار")
# #         print("5. علامت‌زدن به عنوان انجام‌شده/بازگرداندن")
# #         print("6. خروج")
# #
# #         choice = input("\nانتخاب کنید (1-6): ").strip()
# #
# #         if choice == "1":
# #             title = input("عنوان کار: ").strip()
# #             if not title:
# #                 print("عنوان نمی‌تواند خالی باشد.")
# #                 continue
# #             desc = input("توضیح (اختیاری): ").strip()
# #             manager.add_todo(title, desc)
# #
# #         elif choice == "2":
# #             print("\nفیلتر: 1) همه  2) انجام‌نشده  3) انجام‌شده")
# #             f = input("انتخاب فیلتر (1-3): ").strip()
# #             filter_map = {"1": "all", "2": "pending", "3": "completed"}
# #             filter_status = filter_map.get(f, "all")
# #
# #             print("مرتب‌سازی: 1) زمان ایجاد  2) وضعیت")
# #             s = input("انتخاب مرتب‌سازی (1-2): ").strip()
# #             sort_map = {"1": "created", "2": "status"}
# #             sort_by = sort_map.get(s, "created")
# #
# #             manager.list_todos(filter_status, sort_by)
# #
# #         elif choice == "3":
# #             try:
# #                 tid = int(input("شناسه کار: "))
# #                 title = input("عنوان جدید (خالی = بدون تغییر): ").strip()
# #                 desc = input("توضیح جدید (خالی = بدون تغییر): ").strip()
# #                 manager.edit_todo(tid,
# #                                   title=None if title == "" else title,
# #                                   description=None if desc == "" else desc)
# #             except ValueError:
# #                 print("شناسه باید عدد باشد.")
# #
# #         elif choice == "4":
# #             try:
# #                 tid = int(input("شناسه کار برای حذف: "))
# #                 confirm = input(f"آیا از حذف کار {tid} مطمئن هستید؟ (y/n): ")
# #                 if confirm.lower() == 'y':
# #                     manager.delete_todo(tid)
# #             except ValueError:
# #                 print("شناسه باید عدد باشد.")
# #
# #         elif choice == "5":
# #             try:
# #                 tid = int(input("شناسه کار: "))
# #                 manager.toggle_complete(tid)
# #             except ValueError:
# #                 print("شناسه باید عدد باشد.")
# #
# #         elif choice == "6":
# #             print("خداحافظ! کارهای شما ذخیره شدند.")
# #             break
# #
# #         else:
# #             print("انتخاب نامعتبر. لطفاً دوباره تلاش کنید.")
# #
# #
# # if __name__ == "__main__":
# #     main()
#
#
# """
# Advanced Project Management System - نسخه CLI
# بر اساس مستند نیازمندی‌های (SRS) با قابلیت‌های کامل
# ذخیره‌سازی در فایل projects.json
# """
#
# import json
# import os
# import uuid
# from datetime import datetime, timedelta
# from typing import List, Dict, Optional, Any
# from enum import Enum
#
# # مسیر فایل داده
# DATA_FILE = "projects.json"
#
#
# class Priority(Enum):
#     LOW = "low"
#     MEDIUM = "medium"
#     HIGH = "high"
#     CRITICAL = "critical"
#
#
# class Status(Enum):
#     TODO = "todo"
#     IN_PROGRESS = "in_progress"
#     REVIEW = "review"
#     COMPLETED = "completed"
#     BLOCKED = "blocked"
#
#
# class UserRole(Enum):
#     PROJECT_MANAGER = "project_manager"
#     TEAM_LEAD = "team_lead"
#     DEVELOPER = "developer"
#     TESTER = "tester"
#     VIEWER = "viewer"
#
#
# class User:
#     def __init__(self, id: str, username: str, email: str, role: UserRole, full_name: str = ""):
#         self.id = id
#         self.username = username
#         self.email = email
#         self.role = role
#         self.full_name = full_name
#         self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#     def to_dict(self) -> Dict:
#         return {
#             "id": self.id,
#             "username": self.username,
#             "email": self.email,
#             "role": self.role.value,
#             "full_name": self.full_name,
#             "created_at": self.created_at
#         }
#
#     @classmethod
#     def from_dict(cls, data: Dict) -> 'User':
#         return cls(
#             id=data["id"],
#             username=data["username"],
#             email=data["email"],
#             role=UserRole(data["role"]),
#             full_name=data.get("full_name", "")
#         )
#
#
# class Project:
#     def __init__(self, id: str, name: str, description: str = "", owner_id: str = None):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.owner_id = owner_id
#         self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         self.updated_at = self.created_at
#         self.status = Status.TODO
#         self.priority = Priority.MEDIUM
#         self.deadline = None
#         self.members: List[str] = []  # List of user IDs
#         self.tags: List[str] = []
#
#     def to_dict(self) -> Dict:
#         return {
#             "id": self.id,
#             "name": self.name,
#             "description": self.description,
#             "owner_id": self.owner_id,
#             "created_at": self.created_at,
#             "updated_at": self.updated_at,
#             "status": self.status.value,
#             "priority": self.priority.value,
#             "deadline": self.deadline,
#             "members": self.members,
#             "tags": self.tags
#         }
#
#     @classmethod
#     def from_dict(cls, data: Dict) -> 'Project':
#         project = cls(
#             id=data["id"],
#             name=data["name"],
#             description=data.get("description", ""),
#             owner_id=data.get("owner_id")
#         )
#         project.created_at = data["created_at"]
#         project.updated_at = data["updated_at"]
#         project.status = Status(data.get("status", "todo"))
#         project.priority = Priority(data.get("priority", "medium"))
#         project.deadline = data.get("deadline")
#         project.members = data.get("members", [])
#         project.tags = data.get("tags", [])
#         return project
#
#     def calculate_progress(self, tasks: List['Task']) -> float:
#         """محاسبه پیشرفت پروژه بر اساس تسک‌ها"""
#         if not tasks:
#             return 0.0
#         completed = sum(1 for task in tasks if task.status == Status.COMPLETED)
#         return (completed / len(tasks)) * 100
#
#
# class Task:
#     def __init__(self, id: str, title: str, project_id: str, assignee_id: str = None):
#         self.id = id
#         self.title = title
#         self.project_id = project_id
#         self.assignee_id = assignee_id
#         self.description = ""
#         self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         self.updated_at = self.created_at
#         self.status = Status.TODO
#         self.priority = Priority.MEDIUM
#         self.estimated_hours = 0
#         self.actual_hours = 0
#         self.deadline = None
#         self.tags: List[str] = []
#         self.dependencies: List[str] = []  # List of task IDs
#         self.comments: List[Dict] = []
#
#     def to_dict(self) -> Dict:
#         return {
#             "id": self.id,
#             "title": self.title,
#             "project_id": self.project_id,
#             "assignee_id": self.assignee_id,
#             "description": self.description,
#             "created_at": self.created_at,
#             "updated_at": self.updated_at,
#             "status": self.status.value,
#             "priority": self.priority.value,
#             "estimated_hours": self.estimated_hours,
#             "actual_hours": self.actual_hours,
#             "deadline": self.deadline,
#             "tags": self.tags,
#             "dependencies": self.dependencies,
#             "comments": self.comments
#         }
#
#     @classmethod
#     def from_dict(cls, data: Dict) -> 'Task':
#         task = cls(
#             id=data["id"],
#             title=data["title"],
#             project_id=data["project_id"],
#             assignee_id=data.get("assignee_id")
#         )
#         task.description = data.get("description", "")
#         task.created_at = data["created_at"]
#         task.updated_at = data["updated_at"]
#         task.status = Status(data.get("status", "todo"))
#         task.priority = Priority(data.get("priority", "medium"))
#         task.estimated_hours = data.get("estimated_hours", 0)
#         task.actual_hours = data.get("actual_hours", 0)
#         task.deadline = data.get("deadline")
#         task.tags = data.get("tags", [])
#         task.dependencies = data.get("dependencies", [])
#         task.comments = data.get("comments", [])
#         return task
#
#     def add_comment(self, user_id: str, content: str):
#         """افزودن کامنت به تسک"""
#         comment = {
#             "id": str(uuid.uuid4()),
#             "user_id": user_id,
#             "content": content,
#             "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         }
#         self.comments.append(comment)
#         self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#
# class ProjectManager:
#     def __init__(self):
#         self.users: Dict[str, User] = {}
#         self.projects: Dict[str, Project] = {}
#         self.tasks: Dict[str, Task] = {}
#         self.current_user: Optional[User] = None
#         self.load_from_file()
#
#     def load_from_file(self):
#         """بارگذاری داده‌ها از فایل JSON"""
#         if os.path.exists(DATA_FILE):
#             try:
#                 with open(DATA_FILE, "r", encoding="utf-8") as f:
#                     data = json.load(f)
#
#                     # بارگذاری کاربران
#                     self.users = {
#                         user_id: User.from_dict(user_data)
#                         for user_id, user_data in data.get("users", {}).items()
#                     }
#
#                     # بارگذاری پروژه‌ها
#                     self.projects = {
#                         project_id: Project.from_dict(project_data)
#                         for project_id, project_data in data.get("projects", {}).items()
#                     }
#
#                     # بارگذاری تسک‌ها
#                     self.tasks = {
#                         task_id: Task.from_dict(task_data)
#                         for task_id, task_data in data.get("tasks", {}).items()
#                     }
#
#             except Exception as e:
#                 print(f"خطا در بارگذاری فایل: {e}")
#                 self.users = {}
#                 self.projects = {}
#                 self.tasks = {}
#
#     def save_to_file(self):
#         """ذخیره داده‌ها در فایل JSON"""
#         try:
#             data = {
#                 "users": {user_id: user.to_dict() for user_id, user in self.users.items()},
#                 "projects": {project_id: project.to_dict() for project_id, project in self.projects.items()},
#                 "tasks": {task_id: task.to_dict() for task_id, task in self.tasks.items()}
#             }
#
#             with open(DATA_FILE, "w", encoding="utf-8") as f:
#                 json.dump(data, f, ensure_ascii=False, indent=2)
#         except Exception as e:
#             print(f"خطا در ذخیره فایل: {e}")
#
#     # مدیریت کاربران
#     def register_user(self, username: str, email: str, role: UserRole, full_name: str = ""):
#         """ثبت کاربر جدید"""
#         if any(user.username == username for user in self.users.values()):
#             print("نام کاربری تکراری است.")
#             return None
#
#         user_id = str(uuid.uuid4())
#         user = User(user_id, username, email, role, full_name)
#         self.users[user_id] = user
#         self.save_to_file()
#         print(f"کاربر '{username}' با موفقیت ثبت شد.")
#         return user
#
#     def login(self, username: str):
#         """ورود به سیستم"""
#         for user in self.users.values():
#             if user.username == username:
#                 self.current_user = user
#                 print(f"خوش آمدید {user.full_name or user.username}!")
#                 return user
#         print("کاربر یافت نشد.")
#         return None
#
#     def logout(self):
#         """خروج از سیستم"""
#         self.current_user = None
#         print("با موفقیت خارج شدید.")
#
#     # مدیریت پروژه‌ها
#     def create_project(self, name: str, description: str = ""):
#         """ایجاد پروژه جدید"""
#         if not self.current_user:
#             print("لطفاً ابتدا وارد سیستم شوید.")
#             return
#
#         project_id = str(uuid.uuid4())
#         project = Project(project_id, name, description, self.current_user.id)
#         project.members.append(self.current_user.id)
#         self.projects[project_id] = project
#         self.save_to_file()
#         print(f"پروژه '{name}' با موفقیت ایجاد شد.")
#         return project
#
#     def add_project_member(self, project_id: str, username: str):
#         """افزودن عضو به پروژه"""
#         project = self.projects.get(project_id)
#         if not project:
#             print("پروژه یافت نشد.")
#             return
#
#         # پیدا کردن کاربر بر اساس نام کاربری
#         user = next((u for u in self.users.values() if u.username == username), None)
#         if not user:
#             print("کاربر یافت نشد.")
#             return
#
#         if user.id in project.members:
#             print("کاربر قبلاً به پروژه اضافه شده است.")
#             return
#
#         project.members.append(user.id)
#         project.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         self.save_to_file()
#         print(f"کاربر '{username}' به پروژه اضافه شد.")
#
#     # مدیریت تسک‌ها
#     def create_task(self, project_id: str, title: str, assignee_username: str = None):
#         """ایجاد تسک جدید"""
#         if not self.current_user:
#             print("لطفاً ابتدا وارد سیستم شوید.")
#             return
#
#         project = self.projects.get(project_id)
#         if not project:
#             print("پروژه یافت نشد.")
#             return
#
#         assignee_id = None
#         if assignee_username:
#             assignee = next((u for u in self.users.values() if u.username == assignee_username), None)
#             if not assignee:
#                 print("کاربر مسئول یافت نشد.")
#                 return
#             assignee_id = assignee.id
#
#         task_id = str(uuid.uuid4())
#         task = Task(task_id, title, project_id, assignee_id)
#         self.tasks[task_id] = task
#         self.save_to_file()
#         print(f"تسک '{title}' با موفقیت ایجاد شد.")
#         return task
#
#     def update_task_status(self, task_id: str, status: Status):
#         """بروزرسانی وضعیت تسک"""
#         task = self.tasks.get(task_id)
#         if not task:
#             print("تسک یافت نشد.")
#             return
#
#         task.status = status
#         task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         self.save_to_file()
#         print(f"وضعیت تسک به '{status.value}' تغییر یافت.")
#
#     def add_task_comment(self, task_id: str, content: str):
#         """افزودن کامنت به تسک"""
#         if not self.current_user:
#             print("لطفاً ابتدا وارد سیستم شوید.")
#             return
#
#         task = self.tasks.get(task_id)
#         if not task:
#             print("تسک یافت نشد.")
#             return
#
#         task.add_comment(self.current_user.id, content)
#         self.save_to_file()
#         print("کامنت با موفقیت اضافه شد.")
#
#     # گزارش‌گیری و تحلیل
#     def get_project_progress(self, project_id: str) -> Dict[str, Any]:
#         """گزارش پیشرفت پروژه"""
#         project = self.projects.get(project_id)
#         if not project:
#             return {}
#
#         project_tasks = [task for task in self.tasks.values() if task.project_id == project_id]
#         progress = project.calculate_progress(project_tasks)
#
#         status_count = {status.value: 0 for status in Status}
#         for task in project_tasks:
#             status_count[task.status.value] += 1
#
#         return {
#             "project": project.name,
#             "progress": progress,
#             "total_tasks": len(project_tasks),
#             "status_distribution": status_count,
#             "completed_tasks": status_count[Status.COMPLETED.value]
#         }
#
#     def generate_user_report(self, user_id: str) -> Dict[str, Any]:
#         """گزارش عملکرد کاربر"""
#         user_tasks = [task for task in self.tasks.values() if task.assignee_id == user_id]
#
#         completed = sum(1 for task in user_tasks if task.status == Status.COMPLETED)
#         in_progress = sum(1 for task in user_tasks if task.status == Status.IN_PROGRESS)
#         total_estimated = sum(task.estimated_hours for task in user_tasks)
#         total_actual = sum(task.actual_hours for task in user_tasks)
#
#         return {
#             "total_tasks": len(user_tasks),
#             "completed": completed,
#             "in_progress": in_progress,
#             "completion_rate": (completed / len(user_tasks)) * 100 if user_tasks else 0,
#             "total_estimated_hours": total_estimated,
#             "total_actual_hours": total_actual,
#             "efficiency": (total_estimated / total_actual) * 100 if total_actual > 0 else 0
#         }
#
#
# # اینترفیس کاربری
# def display_menu():
#     print("\n" + "=" * 80)
#     print("📊 سیستم مدیریت پروژه پیشرفته")
#     print("=" * 80)
#
#     if manager.current_user:
#         print(f"👤 کاربر: {manager.current_user.full_name or manager.current_user.username}")
#         print("\nمنوی اصلی:")
#         print("1.  مدیریت پروژه‌ها")
#         print("2.  مدیریت تسک‌ها")
#         print("3.  مدیریت کاربران")
#         print("4.  گزارش‌گیری و تحلیل")
#         print("5.  خروج از سیستم")
#     else:
#         print("\nمنوی ورود:")
#         print("1. ورود به سیستم")
#         print("2. ثبت نام")
#         print("3. خروج")
#
#
# def project_management_menu():
#     print("\n🏢 مدیریت پروژه‌ها:")
#     print("1. ایجاد پروژه جدید")
#     print("2. نمایش پروژه‌ها")
#     print("3. افزودن عضو به پروژه")
#     print("4. ویرایش پروژه")
#     print("5. بازگشت")
#
#
# def task_management_menu():
#     print("\n📝 مدیریت تسک‌ها:")
#     print("1. ایجاد تسک جدید")
#     print("2. نمایش تسک‌ها")
#     print("3. تغییر وضعیت تسک")
#     print("4. افزودن کامنت به تسک")
#     print("5. ویرایش تسک")
#     print("6. بازگشت")
#
#
# def user_management_menu():
#     print("\n👥 مدیریت کاربران:")
#     print("1. نمایش کاربران")
#     print("2. ایجاد کاربر جدید")
#     print("3. نمایش پروفایل")
#     print("4. بازگشت")
#
#
# def reporting_menu():
#     print("\n📈 گزارش‌گیری و تحلیل:")
#     print("1. گزارش پیشرفت پروژه")
#     print("2. گزارش عملکرد کاربر")
#     print("3. آمار کلی سیستم")
#     print("4. بازگشت")
#
#
# def main():
#     global manager
#     manager = ProjectManager()
#
#     print("🚀 به سیستم مدیریت پروژه پیشرفته خوش آمدید!")
#
#     while True:
#         display_menu()
#         choice = input("\nانتخاب کنید: ").strip()
#
#         if not manager.current_user:
#             # منوی ورود
#             if choice == "1":
#                 username = input("نام کاربری: ").strip()
#                 manager.login(username)
#             elif choice == "2":
#                 username = input("نام کاربری: ").strip()
#                 email = input("ایمیل: ").strip()
#                 full_name = input("نام کامل (اختیاری): ").strip()
#                 print("نقش‌ها: 1) مدیر پروژه 2) تیم لید 3) توسعه‌دهنده 4) تستر 5) مشاهده‌گر")
#                 role_choice = input("انتخاب نقش (1-5): ").strip()
#                 role_map = {
#                     "1": UserRole.PROJECT_MANAGER,
#                     "2": UserRole.TEAM_LEAD,
#                     "3": UserRole.DEVELOPER,
#                     "4": UserRole.TESTER,
#                     "5": UserRole.VIEWER
#                 }
#                 role = role_map.get(role_choice, UserRole.VIEWER)
#                 manager.register_user(username, email, role, full_name)
#             elif choice == "3":
#                 print("خداحافظ!")
#                 break
#             else:
#                 print("انتخاب نامعتبر.")
#
#         else:
#             # منوی اصلی
#             if choice == "1":
#                 # مدیریت پروژه‌ها
#                 while True:
#                     project_management_menu()
#                     sub_choice = input("انتخاب کنید: ").strip()
#
#                     if sub_choice == "1":
#                         name = input("نام پروژه: ").strip()
#                         desc = input("توضیحات: ").strip()
#                         manager.create_project(name, desc)
#                     elif sub_choice == "2":
#                         print("\n📋 پروژه‌ها:")
#                         for project in manager.projects.values():
#                             print(f"- {project.name} (ID: {project.id})")
#                     elif sub_choice == "3":
#                         project_id = input("شناسه پروژه: ").strip()
#                         username = input("نام کاربری عضو: ").strip()
#                         manager.add_project_member(project_id, username)
#                     elif sub_choice == "4":
#                         # ویرایش پروژه
#                         pass
#                     elif sub_choice == "5":
#                         break
#                     else:
#                         print("انتخاب نامعتبر.")
#
#             elif choice == "2":
#                 # مدیریت تسک‌ها
#                 while True:
#                     task_management_menu()
#                     sub_choice = input("انتخاب کنید: ").strip()
#
#                     if sub_choice == "1":
#                         project_id = input("شناسه پروژه: ").strip()
#                         title = input("عنوان تسک: ").strip()
#                         assignee = input("مسئول (اختیاری): ").strip() or None
#                         manager.create_task(project_id, title, assignee)
#                     elif sub_choice == "2":
#                         print("\n📝 تسک‌ها:")
#                         for task in manager.tasks.values():
#                             print(f"- {task.title} (وضعیت: {task.status.value})")
#                     elif sub_choice == "3":
#                         task_id = input("شناسه تسک: ").strip()
#                         print("وضعیت‌ها: 1) انجام نشده 2) در حال انجام 3) بازبینی 4) انجام شده 5) مسدود")
#                         status_choice = input("انتخاب وضعیت (1-5): ").strip()
#                         status_map = {
#                             "1": Status.TODO,
#                             "2": Status.IN_PROGRESS,
#                             "3": Status.REVIEW,
#                             "4": Status.COMPLETED,
#                             "5": Status.BLOCKED
#                         }
#                         status = status_map.get(status_choice, Status.TODO)
#                         manager.update_task_status(task_id, status)
#                     elif sub_choice == "4":
#                         task_id = input("شناسه تسک: ").strip()
#                         content = input("متن کامنت: ").strip()
#                         manager.add_task_comment(task_id, content)
#                     elif sub_choice == "5":
#                         break
#                     else:
#                         print("انتخاب نامعتبر.")
#
#             elif choice == "3":
#                 # مدیریت کاربران
#                 while True:
#                     user_management_menu()
#                     sub_choice = input("انتخاب کنید: ").strip()
#
#                     if sub_choice == "1":
#                         print("\n👥 کاربران سیستم:")
#                         for user in manager.users.values():
#                             print(f"- {user.username} ({user.role.value})")
#                     elif sub_choice == "2":
#                         username = input("نام کاربری: ").strip()
#                         email = input("ایمیل: ").strip()
#                         full_name = input("نام کامل (اختیاری): ").strip()
#                         print("نقش‌ها: 1) مدیر پروژه 2) تیم لید 3) توسعه‌دهنده 4) تستر 5) مشاهده‌گر")
#                         role_choice = input("انتخاب نقش (1-5): ").strip()
#                         role_map = {
#                             "1": UserRole.PROJECT_MANAGER,
#                             "2": UserRole.TEAM_LEAD,
#                             "3": UserRole.DEVELOPER,
#                             "4": UserRole.TESTER,
#                             "5": UserRole.VIEWER
#                         }
#                         role = role_map.get(role_choice, UserRole.VIEWER)
#                         manager.register_user(username, email, role, full_name)
#                     elif sub_choice == "3":
#                         if manager.current_user:
#                             user = manager.current_user
#                             print(f"\n👤 پروفایل کاربر:")
#                             print(f"نام کاربری: {user.username}")
#                             print(f"نام کامل: {user.full_name}")
#                             print(f"ایمیل: {user.email}")
#                             print(f"نقش: {user.role.value}")
#                     elif sub_choice == "4":
#                         break
#                     else:
#                         print("انتخاب نامعتبر.")
#
#             elif choice == "4":
#                 # گزارش‌گیری
#                 while True:
#                     reporting_menu()
#                     sub_choice = input("انتخاب کنید: ").strip()
#
#                     if sub_choice == "1":
#                         project_id = input("شناسه پروژه: ").strip()
#                         report = manager.get_project_progress(project_id)
#                         if report:
#                             print(f"\n📊 گزارش پروژه {report['project']}:")
#                             print(f"پیشرفت کلی: {report['progress']:.1f}%")
#                             print(f"تعداد تسک‌ها: {report['total_tasks']}")
#                             print(f"تسک‌های انجام شده: {report['completed_tasks']}")
#                             print("توزیع وضعیت‌ها:")
#                             for status, count in report['status_distribution'].items():
#                                 print(f"  - {status}: {count}")
#                     elif sub_choice == "2":
#                         username = input("نام کاربری: ").strip()
#                         user = next((u for u in manager.users.values() if u.username == username), None)
#                         if user:
#                             report = manager.generate_user_report(user.id)
#                             print(f"\n📈 گزارش عملکرد {username}:")
#                             print(f"تعداد تسک‌ها: {report['total_tasks']}")
#                             print(f"تکمیل شده: {report['completed']}")
#                             print(f"در حال انجام: {report['in_progress']}")
#                             print(f"نرخ تکمیل: {report['completion_rate']:.1f}%")
#                             print(f"ساعت‌های تخمینی: {report['total_estimated_hours']}")
#                             print(f"ساعت‌های واقعی: {report['total_actual_hours']}")
#                             print(f"کارایی: {report['efficiency']:.1f}%")
#                     elif sub_choice == "3":
#                         print(f"\n📈 آمار کلی سیستم:")
#                         print(f"تعداد کاربران: {len(manager.users)}")
#                         print(f"تعداد پروژه‌ها: {len(manager.projects)}")
#                         print(f"تعداد تسک‌ها: {len(manager.tasks)}")
#                     elif sub_choice == "4":
#                         break
#                     else:
#                         print("انتخاب نامعتبر.")
#
#             elif choice == "5":
#                 manager.logout()
#
#             else:
#                 print("انتخاب نامعتبر.")
#
#
# if __name__ == "__main__":
#     manager = None
#     main()


"""
Todo List Manager - نسخه CLI
مستند نیازمندی‌ها (SRS) - پروژه دانشگاهی
ذخیره‌سازی در فایل todos.json
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class FilterStatus(Enum):
    ALL = "all"
    PENDING = "pending"
    COMPLETED = "completed"


class SortBy(Enum):
    CREATED = "created"
    STATUS = "status"
    PRIORITY = "priority"


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TodoItem:
    def __init__(self, id: int, title: str, description: str = "",
                 completed: bool = False, priority: Priority = Priority.MEDIUM,
                 created_at: str = None, due_date: str = None):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.priority = priority
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.due_date = due_date
        self.updated_at = self.created_at

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "due_date": self.due_date
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'TodoItem':
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data["completed"],
            priority=Priority(data.get("priority", "medium")),
            created_at=data["created_at"],
            due_date=data.get("due_date")
        )

    def toggle_complete(self):
        """تغییر وضعیت انجام/عدم انجام"""
        self.completed = not self.completed
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_status_icon(self) -> str:
        """نماد وضعیت"""
        return "✓" if self.completed else "☐"

    def get_priority_icon(self) -> str:
        """نماد اولویت"""
        icons = {
            Priority.LOW: "🟢",
            Priority.MEDIUM: "🟡",
            Priority.HIGH: "🔴"
        }
        return icons.get(self.priority, "🟡")


class TodoManager:
    def __init__(self):
        self.todos: List[TodoItem] = []
        self.next_id = 1
        self.data_file = "todos.json"
        self.load_from_file()

    def load_from_file(self):
        """بارگذاری کارها از فایل JSON - نیازمندی قابلیت اطمینان"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.todos = [TodoItem.from_dict(item) for item in data.get("todos", [])]
                    if self.todos:
                        self.next_id = max(item.id for item in self.todos) + 1
                print("✅ داده‌ها با موفقیت بارگذاری شدند.")
            except Exception as e:
                print(f"❌ خطا در بارگذاری فایل: {e}")
                self.todos = []

    def save_to_file(self):
        """ذخیره کارها در فایل JSON - نیازمندی قابلیت اطمینان"""
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump({
                    "todos": [todo.to_dict() for todo in self.todos],
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }, f, ensure_ascii=False, indent=2)
            print("💾 داده‌ها ذخیره شدند.")
        except Exception as e:
            print(f"❌ خطا در ذخیره فایل: {e}")

    def add_todo(self, title: str, description: str = "", priority: Priority = Priority.MEDIUM, due_date: str = None):
        """افزودن کار جدید - مورد کاربرد ۱"""
        if not title.strip():
            print("❌ عنوان نمی‌تواند خالی باشد.")
            return False

        todo = TodoItem(
            id=self.next_id,
            title=title.strip(),
            description=description.strip(),
            priority=priority,
            due_date=due_date
        )
        self.todos.append(todo)
        self.next_id += 1
        self.save_to_file()
        print(f"✅ کار '{title}' با موفقیت اضافه شد.")
        return True

    def edit_todo(self, todo_id: int, title: Optional[str] = None,
                  description: Optional[str] = None, priority: Optional[Priority] = None,
                  due_date: Optional[str] = None):
        """ویرایش کار"""
        todo = self.find_by_id(todo_id)
        if not todo:
            print("❌ کار یافت نشد.")
            return False

        if title is not None:
            todo.title = title.strip()
        if description is not None:
            todo.description = description.strip()
        if priority is not None:
            todo.priority = priority
        if due_date is not None:
            todo.due_date = due_date

        todo.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_to_file()
        print("✅ کار با موفقیت ویرایش شد.")
        return True

    def delete_todo(self, todo_id: int):
        """حذف کار"""
        todo = self.find_by_id(todo_id)
        if not todo:
            print("❌ کار یافت نشد.")
            return False

        self.todos = [t for t in self.todos if t.id != todo_id]
        self.save_to_file()
        print("✅ کار با موفقیت حذف شد.")
        return True

    def toggle_complete(self, todo_id: int):
        """تغییر وضعیت انجام/عدم انجام - مورد کاربرد ۲"""
        todo = self.find_by_id(todo_id)
        if not todo:
            print("❌ کار یافت نشد.")
            return False

        todo.toggle_complete()
        status = "انجام‌شده" if todo.completed else "انجام‌نشده"
        self.save_to_file()
        print(f"✅ وضعیت کار به '{status}' تغییر کرد.")
        return True

    def find_by_id(self, todo_id: int) -> Optional[TodoItem]:
        """جستجوی کار بر اساس شناسه"""
        return next((t for t in self.todos if t.id == todo_id), None)

    def list_todos(self, filter_status: FilterStatus = FilterStatus.ALL,
                   sort_by: SortBy = SortBy.CREATED, show_stats: bool = False):
        """نمایش فهرست کارها با فیلتر و مرتب‌سازی - نیازمندی کارایی"""

        # فیلتر کردن
        if filter_status == FilterStatus.PENDING:
            filtered = [t for t in self.todos if not t.completed]
        elif filter_status == FilterStatus.COMPLETED:
            filtered = [t for t in self.todos if t.completed]
        else:
            filtered = self.todos.copy()

        # مرتب‌سازی
        if sort_by == SortBy.CREATED:
            filtered.sort(key=lambda x: x.created_at, reverse=True)
        elif sort_by == SortBy.STATUS:
            filtered.sort(key=lambda x: (x.completed, x.created_at))
        elif sort_by == SortBy.PRIORITY:
            priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
            filtered.sort(key=lambda x: (priority_order[x.priority], x.created_at))

        # نمایش آمار
        if show_stats:
            total = len(self.todos)
            completed = sum(1 for t in self.todos if t.completed)
            pending = total - completed
            print(f"\n📊 آمار: {completed} انجام‌شده | {pending} انجام‌نشده | {total} کل")

        if not filtered:
            print("📝 هیچ کاری یافت نشد.")
            return

        # نمایش لیست
        print("\n" + "=" * 80)
        print(f"📋 فهرست کارها ({filter_status.value})")
        print("=" * 80)

        for todo in filtered:
            status_icon = todo.get_status_icon()
            priority_icon = todo.get_priority_icon()
            desc = f" - {todo.description}" if todo.description else ""
            due_info = f" ⏰ {todo.due_date}" if todo.due_date else ""

            print(f"{status_icon} {priority_icon} [{todo.id:2d}] {todo.title}{desc}{due_info}")
            print(f"    📅 ایجاد: {todo.created_at} | 🔄 به‌روز: {todo.updated_at}")

        print("=" * 80)

    def search_todos(self, keyword: str):
        """جستجو در کارها"""
        results = [
            t for t in self.todos
            if keyword.lower() in t.title.lower() or keyword.lower() in t.description.lower()
        ]

        if not results:
            print(f"🔍 هیچ نتیجه‌ای برای '{keyword}' یافت نشد.")
            return

        print(f"\n🔍 نتایج جستجو برای '{keyword}':")
        print("=" * 60)
        for todo in results:
            status_icon = todo.get_status_icon()
            print(f"{status_icon} [{todo.id}] {todo.title}")

    def clear_completed(self):
        """پاک کردن کارهای انجام‌شده"""
        completed_count = sum(1 for t in self.todos if t.completed)
        if completed_count == 0:
            print("ℹ️ هیچ کار انجام‌شده‌ای وجود ندارد.")
            return False

        confirm = input(f"⚠️ آیا از حذف {completed_count} کار انجام‌شده مطمئن هستید؟ (y/n): ")
        if confirm.lower() == 'y':
            self.todos = [t for t in self.todos if not t.completed]
            self.save_to_file()
            print(f"✅ {completed_count} کار انجام‌شده حذف شدند.")
            return True
        return False


def display_welcome():
    """نمایش صفحه خوش‌آمدگویی"""
    print("\n" + "🌟" * 40)
    print("🌟            به برنامه مدیریت کارهای روزانه خوش آمدید!            🌟")
    print("🌟" * 40)
    print("📋 این برنامه بر اساس مستند نیازمندی‌های (SRS) توسعه یافته است")
    print("🎯 شامل: داستان کاربر، موارد کاربرد، نیازمندی‌های عملکردی و غیرعملکردی")
    print("📅 مهلت تحویل: ۱ آذر")
    print("-" * 80)


def get_priority_from_input() -> Priority:
    """دریافت اولویت از کاربر"""
    print("\n🎯 اولویت:")
    print("1. پایین (🟢)")
    print("2. متوسط (🟡)")
    print("3. بالا (🔴)")

    while True:
        choice = input("انتخاب کنید (1-3, پیش‌فرض=2): ").strip()
        if not choice:
            return Priority.MEDIUM
        if choice in ["1", "2", "3"]:
            return {
                "1": Priority.LOW,
                "2": Priority.MEDIUM,
                "3": Priority.HIGH
            }[choice]
        print("❌ انتخاب نامعتبر. لطفاً دوباره تلاش کنید.")


def main():
    """تابع اصلی برنامه - رابط کاربری"""
    manager = TodoManager()
    display_welcome()

    while True:
        print("\n📱 منوی اصلی:")
        print("1. ➕ افزودن کار جدید")
        print("2. 📋 نمایش فهرست کارها")
        print("3. ✏️  ویرایش کار")
        print("4. 🗑️  حذف کار")
        print("5. ✅ تغییر وضعیت انجام")
        print("6. 🔍 جستجو در کارها")
        print("7. 🧹 پاک کردن کارهای انجام‌شده")
        print("8. 📊 نمایش آمار")
        print("9. 🚪 خروج")

        choice = input("\n🎯 انتخاب کنید (1-9): ").strip()

        if choice == "1":
            print("\n➕ افزودن کار جدید:")
            title = input("عنوان کار: ").strip()
            if not title:
                print("❌ عنوان نمی‌تواند خالی باشد.")
                continue
            desc = input("توضیح (اختیاری): ").strip()
            priority = get_priority_from_input()
            due_date = input("تاریخ مهلت (YYYY-MM-DD, اختیاری): ").strip() or None
            manager.add_todo(title, desc, priority, due_date)

        elif choice == "2":
            print("\n📋 گزینه‌های نمایش:")
            print("فیلتر: 1) همه  2) انجام‌نشده  3) انجام‌شده")
            filter_choice = input("انتخاب فیلتر (1-3, پیش‌فرض=1): ").strip()
            filter_map = {"1": FilterStatus.ALL, "2": FilterStatus.PENDING, "3": FilterStatus.COMPLETED}
            filter_status = filter_map.get(filter_choice, FilterStatus.ALL)

            print("مرتب‌سازی: 1) زمان ایجاد  2) وضعیت  3) اولویت")
            sort_choice = input("انتخاب مرتب‌سازی (1-3, پیش‌فرض=1): ").strip()
            sort_map = {"1": SortBy.CREATED, "2": SortBy.STATUS, "3": SortBy.PRIORITY}
            sort_by = sort_map.get(sort_choice, SortBy.CREATED)

            show_stats = input("نمایش آمار؟ (y/n, پیش‌فرض=n): ").strip().lower() == 'y'
            manager.list_todos(filter_status, sort_by, show_stats)

        elif choice == "3":
            try:
                print("\n✏️ ویرایش کار:")
                todo_id = int(input("شناسه کار: "))

                # پیدا کردن کار فعلی
                current = manager.find_by_id(todo_id)
                if not current:
                    print("❌ کار یافت نشد.")
                    continue

                print(f"کار فعلی: {current.title}")
                title = input("عنوان جدید (خالی = بدون تغییر): ").strip() or None
                desc = input("توضیح جدید (خالی = بدون تغییر): ").strip() or None

                print("اولویت جدید (خالی = بدون تغییر):")
                priority = get_priority_from_input() if input("تغییر اولویت؟ (y/n): ").lower() == 'y' else None

                due_date = input("تاریخ مهلت جدید (خالی = بدون تغییر): ").strip() or None
                if due_date == "":
                    due_date = None

                manager.edit_todo(todo_id, title, desc, priority, due_date)
            except ValueError:
                print("❌ شناسه باید عدد باشد.")

        elif choice == "4":
            try:
                print("\n🗑️ حذف کار:")
                todo_id = int(input("شناسه کار برای حذف: "))
                current = manager.find_by_id(todo_id)
                if current:
                    confirm = input(f"⚠️ آیا از حذف کار '{current.title}' مطمئن هستید؟ (y/n): ")
                    if confirm.lower() == 'y':
                        manager.delete_todo(todo_id)
                else:
                    print("❌ کار یافت نشد.")
            except ValueError:
                print("❌ شناسه باید عدد باشد.")

        elif choice == "5":
            try:
                print("\n✅ تغییر وضعیت انجام:")
                todo_id = int(input("شناسه کار: "))
                manager.toggle_complete(todo_id)
            except ValueError:
                print("❌ شناسه باید عدد باشد.")

        elif choice == "6":
            print("\n🔍 جستجو:")
            keyword = input("کلمه کلیدی: ").strip()
            if keyword:
                manager.search_todos(keyword)
            else:
                print("❌ لطفاً کلمه کلیدی وارد کنید.")

        elif choice == "7":
            print("\n🧹 پاک کردن کارهای انجام‌شده")
            manager.clear_completed()

        elif choice == "8":
            print("\n📊 آمار کلی:")
            total = len(manager.todos)
            completed = sum(1 for t in manager.todos if t.completed)
            pending = total - completed
            completion_rate = (completed / total * 100) if total > 0 else 0

            print(f"📈 تعداد کل کارها: {total}")
            print(f"✅ کارهای انجام‌شده: {completed}")
            print(f"⏳ کارهای انجام‌نشده: {pending}")
            print(f"🎯 نرخ تکمیل: {completion_rate:.1f}%")

            # آمار اولویت
            priorities = {p: 0 for p in Priority}
            for todo in manager.todos:
                priorities[todo.priority] += 1

            print("\n🎯 توزیع اولویت‌ها:")
            for priority, count in priorities.items():
                icon = todo.get_priority_icon()  # استفاده از متد نمونه
                print(f"   {icon} {priority.value}: {count}")

        elif choice == "9":
            print("\n💾 در حال ذخیره‌سازی داده‌ها...")
            manager.save_to_file()
            print("👋 با تشکر از استفاده شما! خداحافظ!")
            break

        else:
            print("❌ انتخاب نامعتبر. لطفاً عدد بین ۱ تا ۹ وارد کنید.")


if __name__ == "__main__":
    main()
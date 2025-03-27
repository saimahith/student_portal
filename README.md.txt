# 🎓 Student Portal Web App

A full-stack web application to streamline university services such as grades, transcript requests, and profile management.

## 📌 Features
- ✅ Student, Teacher, Admin role-based dashboards
- ✅ Login & Register functionality
- 🔒 Flask-based authentication
- 🌐 Responsive UI using HTML, CSS, Bootstrap
- 🧠 Jinja2 templates for dynamic routing
- 💾 PostgreSQL backend (SQLAlchemy ORM)

## 🚧 Work In Progress
- Transcript download feature
- Admin approval for requests
- Grade editing by teachers

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS, Bootstrap
- **Backend:** Python (Flask), Jinja2
- **Database:** PostgreSQL
- **Tools:** GitHub, VSCode, Flask-WTF

## ▶️ Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/saimahith/student_portal.git
cd student_portal

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python run.py

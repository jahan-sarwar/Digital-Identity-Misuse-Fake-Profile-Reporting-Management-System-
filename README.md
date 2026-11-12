# Digital-Identity-Misuse-Fake-Profile-Reporting-Management-System-

A web-based platform for reporting fake social media profiles and online identity misuse. Users can submit reports with profile URLs and supporting evidence, while administrators review cases, manage investigations, track statuses, and notify users of updates.

---

## 📁 Repository Structure & Modules

| Module | Description | Ownership |
| :--- | :--- | :--- |
| `FR01_User_Registration_Authentication` | User registration, login, and authentication system | Teammate |
| `FR02_Incident_Description_And_Reporting` | Incident detail submission, validation, and listing | **SARWAR** |
| `FR03_Platform_Selection_And_URL_Submission` | Social platform selection and profile link submission | Teammate |
| `FR04_Evidence_Upload_And_Validation` | Evidence file upload (screenshots, docs), validation & gallery | **SARWAR** |

---

## ⚙️ How to Setup & Run Each Module (Team Instructions)

Because `db.sqlite3` is ignored in `.gitignore` to avoid merge conflicts across team members, every member must generate their local database after pulling:

1. **Navigate to the target module**:
   ```bash
   cd FR02_Incident_Description_And_Reporting
   # OR
   cd FR04_Evidence_Upload_And_Validation
   ```

2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations** (generates fresh local SQLite database):
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Start the server**:
   Double click `run_server.bat` or run:
   ```bash
   python manage.py runserver
   ```

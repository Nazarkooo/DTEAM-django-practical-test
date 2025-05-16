# DTEAM - Django Developer Practical Test

Welcome! This test will help us see how you structure a Django project, work with various tools, and handle common tasks in web development. Follow the instructions step by step. Good luck!

---

##  Requirements

- Follow PEP 8 and other style guidelines.
- Use clear and concise commit messages and docstrings where needed.
- Structure your project for readability and maintainability.
- Optimize database access using Django's built-in methods.
- Provide enough details in your `README.md`.

---

## Version Control System

1. Create a **public GitHub repository** for this test, e.g., `DTEAM-django-practical-test`.
2. Put the **text of this test** (all instructions) into `README.md`.
3. For **each task**, create a separate branch (e.g., `tasks/task-1`, `tasks/task-2`, etc.).
4. When finishing a task, **merge it into `main`**, but **do not delete** the original task branch.

---

##  Python Virtual Environment

1. Use **pyenv** to manage the Python version.
   - Create a `.python-version` file in your repo with the exact version.
2. Use **Poetry** to manage dependencies.
   - This will create a `pyproject.toml` file.
3. Update your `README.md` with **instructions on how to set up and use pyenv and Poetry**.

---

##  Tasks

### Task 1: Django Fundamentals

1. **Create a Django Project**
   - Name it something like `CVProject`.
   - Use the Python version from pyenv and the latest stable Django version.
   - Use **SQLite** as the database.

2. **Create an App and Model**
   - Create an app, e.g., `main`.
   - Define a `CV` model with fields:
     - `first_name`, `last_name`, `skills`, `projects`, `bio`, `contacts`.

3. **Load Initial Data**
   - Create a fixture with at least one sample CV instance.
   - Include instructions in `README.md` on how to load it.

4. **List Page View and Template**
   - Implement a view for `/` to show a list of CVs.
   - Style it using any CSS library.
   - Ensure efficient database querying.

5. **Detail Page View**
   - Implement a view for `/cv/<id>/` to show one CV in detail.
   - Style it and optimize data retrieval.

6. **Tests**
   - Add basic tests for list and detail views.
   - Add instructions in `README.md` for running tests.

---

### Task 2: PDF Generation Basics

1. Install any **HTML-to-PDF** library.
2. Add a **"Download PDF"** button on the CV detail page to download the CV.

---

### Task 3: REST API Fundamentals

1. Install **Django REST Framework (DRF)**.
2. Create **CRUD endpoints** for the CV model.
3. Add tests for each CRUD action.

---

### Task 4: Middleware & Request Logging

1. **Create a Request Log Model**
   - In the existing app or a new one (e.g., `audit`).
   - Fields: `timestamp`, `HTTP method`, `path`, and optionally query string, IP, user.

2. **Implement Logging Middleware**
   - Create a middleware class to log each request into the DB.

3. **Recent Requests Page**
   - Create a `/logs/` view showing the 10 most recent requests (sorted by timestamp).
   - Template should show: `timestamp`, `method`, `path`.

4. **Tests**
   - Add tests to verify request logging.

---

### Task 5: Template Context Processors

1. **Settings Context**
   - Create a context processor that injects Django settings into all templates.

2. **Settings Page**
   - Create a `/settings/` view that displays values like `DEBUG` using the context processor.

---

### Task 6: Docker Basics

1. Use **Docker Compose** to containerize the project.
2. Replace SQLite with **PostgreSQL** in Docker Compose.
3. Store env variables (e.g., DB credentials) in a `.env` file.

---

### Task 7: Celery Basics

1. Install and configure **Celery** using Redis or RabbitMQ as the broker.
2. Add a **Celery worker** to your Docker Compose setup.
3. On the CV detail page:
   - Add an **email input** field and a **"Send PDF to Email"** button.
   - This triggers a Celery task to email the PDF.

---

### Task 8: OpenAI Basics

1. Add a **"Translate"** button and language selector to the CV detail page.
2. Supported languages:
   - Cornish, Manx, Breton, Inuktitut, Kalaallisut, Romani, Occitan, Ladino, Northern Sami, Upper Sorbian, Kashubian, Zazaki, Chuvash, Livonian, Tsakonian, Saramaccan, Bislama
3. Hook it up to the **OpenAI translation API** or any preferred translation method to translate the CV content.

---

### Task 9: Deployment

Deploy the project to **DigitalOcean** or another VPS.

> Don't have an account? Use this referral link to get $200 credit:  
> [https://m.do.co/c/9Ó7939eae74](https://m.do.co/c/9Ó7939eae74)

---

##  Final Notes

Complete each task thoroughly.  
Commit your work using the described **branch-and-merge structure**.  
Make sure your `README.md` clearly explains how to **install, run, and test** everything.

We look forward to your submission!  
**Thank you!**

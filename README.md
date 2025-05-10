````markdown
#  DigitalDress

**DigitalDress** is a Django-based web app where users can upload their image and try virtual dresses. This simple and fun project demonstrates how Django handles image uploads, overlays, and interactive UI.

---

## 📸 Features

- Upload your own image
- View selected dress overlaid on your image
- Clean, responsive design using HTML/CSS/JS
- Stores user data in a JSON file
- Runs locally on any machine with Python & Django

---

## 🛠️ How to Use (Step-by-Step)

### 1. Clone the Project

```bash
git clone https://github.com/your-username/DigitalDress.git
cd DigitalDress
````

### 2. Create a Virtual Environment

```bash
python -m venv env
```

### 3. Activate the Environment

* **Windows:**

  ```bash
  env\Scripts\activate
  ```

* **Linux/Mac:**

  ```bash
  source env/bin/activate
  ```

### 4. Install Django

```bash
pip install django
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Start the Server

```bash
python manage.py runserver
```

### 7. Open in Browser

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 💡 Folder Structure Overview

```
DigitalDress/
│
├── app/                # Main Django app
├── static/             # JavaScript, CSS, dress images, user data
├── templates/          # HTML templates
├── media/              # Uploaded user images
├── manage.py           # Django CLI script
└── DigitalDress/       # Project settings
```

---

## 📝 Notes

* Ensure `user_data.json` path is handled using `os.path.join(BASE_DIR, ...)` for cross-system compatibility.
* If using custom images or dress designs, place them in `static/images/`.

---

🎉 You're now ready to use **DigitalDress** locally!

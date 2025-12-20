# 💰 Expense Tracker

A simple **web-based Expense Tracker** built using **Django** that helps users record, manage, and visualize their daily expenses efficiently.

---

## 🚀 Features

- Add, edit, and delete expenses  
- Categorize expenses  
- View expense history  
- User-friendly UI  
- Persistent storage using SQLite  
- Static files handled properly for deployment  

---

## 🛠 Tech Stack

**Backend**
- Python  
- Django  

**Frontend**
- HTML  
- CSS  
- JavaScript  

**Database**
- SQLite (default Django DB)

---

expense_tracker/
│
├── tracker/ # Main Django app
├── staticfiles/ # Collected static files
├── db.sqlite3 # Database
├── manage.py # Django management script
├── requirements.txt # Project dependencies
└── README.md # Project documentation


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Jindalgarv/expense_tracker.git
cd expense_tracker
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run migrations
python manage.py migrate

5️⃣ Start the development server
python manage.py runserver

6️⃣ Open in browser
http://127.0.0.1:8000/

📌 Future Improvements

User authentication

Monthly and yearly expense analytics

Charts and visualizations

Export expenses to CSV/PDF

🤝 Contributing

Contributions are welcome!
Feel free to fork the repository and submit a pull request.
📄 License

This project is open-source and available under the MIT License.

✨ Author

Jindal Garv
GitHub: https://github.com/Jindalgarv

## 📂 Project Structure


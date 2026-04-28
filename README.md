# 🎯 QuizHub — Onlayn Test Platformasi

Python + Flask + SQLite bilan yaratilgan to'liq onlayn test platformasi.

## 🚀 Ishga tushirish

### 1. Flask o'rnatish
```bash
pip install flask
```

### 2. Dasturni ishga tushirish
```bash
cd quiz_platform
python app.py
```

### 3. Brauzerda ochish
```
http://localhost:5000
```

---

## 📁 Loyiha tuzilmasi
```
quiz_platform/
├── app.py                  # Asosiy Flask ilovasi
├── quiz.db                 # SQLite ma'lumotlar bazasi (avtomatik yaratiladi)
├── requirements.txt
└── templates/
    ├── index.html          # Login / Ro'yxatdan o'tish
    ├── dashboard.html      # Bosh sahifa
    ├── quiz.html           # Test o'tkazish
    └── profile.html        # Foydalanuvchi profili
```

---

## 🗃️ Ma'lumotlar bazasi (SQL) tuzilmasi

### Jadvallar:
| Jadval     | Maqsad                              |
|------------|-------------------------------------|
| `users`    | Foydalanuvchi ma'lumotlari          |
| `categories` | Fan kategoriyalari (Python, Matematika...) |
| `questions` | Savollar (4 variant, to'g'ri javob) |
| `results`  | Foydalanuvchi natijalari            |

### Yangi savol qo'shish (SQL):
```sql
INSERT INTO questions (category_id, question, option_a, option_b, option_c, option_d, correct_answer, difficulty)
VALUES (1, 'Savolingiz?', 'Variant A', 'Variant B', 'Variant C', 'Variant D', 'B', 'medium');
```

### Yangi kategoriya qo'shish:
```sql
INSERT INTO categories (name, icon) VALUES ('Fizika', '⚛️');
```

---

## ✨ Xususiyatlar

- 🔐 **Autentifikatsiya** — Ro'yxatdan o'tish va kirish (SHA-256 parol)
- 📚 **5 ta fan** — Python, Matematika, Tarix, Ingliz tili, Kompyuter Fanlari
- 🗃️ **SQL bazasi** — Barcha savollar SQLite'da saqlangan
- ⏱️ **Timer** — Test vaqtini o'lchash
- 📊 **Profil** — Barcha natijalar va statistika
- 📋 **Tahlil** — Har bir javob uchun batafsil feedback
- 🎯 **40+ savol** — Avtomatik to'ldiriladigan baza

---

## 🛠️ API Endpointlar

| Method | URL | Maqsad |
|--------|-----|--------|
| POST | `/api/register` | Ro'yxatdan o'tish |
| POST | `/api/login` | Kirish |
| POST | `/api/logout` | Chiqish |
| GET | `/api/dashboard-data` | Dashboard ma'lumotlari |
| GET | `/api/questions/<id>` | Savollarni olish |
| POST | `/api/submit` | Test natijasini saqlash |
| GET | `/api/profile` | Profil ma'lumotlari |

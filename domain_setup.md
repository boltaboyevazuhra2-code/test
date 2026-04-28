# `myTest5.uz` domenini lokal kompyuterda sozlash bo'yicha ko'llanma

Dasturni `myTest5.uz` orqali ochish uchun kompyuteringizdagi `hosts` faylini tahrirlash kerak. Bu fayl kompyuterga qaysi domenni qaysi IP manzilga yo'naltirishni aytadi.

## Bosqichma-bosqich qadamlar (Windows uchun):

1. **Notepad (Bloknot) ni Administrator sifatida oching**:
   - `Start` menyusini oching va `Notepad` deb yozing.
   - Notepad ustiga o'ng tugmani bosib, **"Run as administrator" (Administrator sifatida ishga tushirish)** tugmasini tanlang.
   - Chiqqan oynada "Yes" deb ruxsat bering.

2. **Hosts faylini toping**:
   - Notepad'da `File -> Open` (Fayl -> Ochish) tugmasini bosing.
   - Quyidagi manzilga kiring:
     `C:\Windows\System32\drivers\etc`
   - O'ng pastki burchakdagi fayl turini "Text Documents (*.txt)" dan **"All Files (*.*)"** (Barcha fayllar) ga o'zgartiring.
   - Ro'yxatdan `hosts` deb nomlangan faylni topib oching.

3. **O'zgartirish kiriting**:
   - Faylning eng oxiriga yangi qator qo'shib, quyidagi kodni yozing:
     ```text
     127.0.0.1   myTest5.uz
     ```
   - O'zgartirishlarni saqlang (`Ctrl + S`).

4. **Dasturni ishga tushiring va tekshiring**:
   - Agar hozir terminalda server ishlab turgan bo'lsa, uni to'xtating (`Ctrl + C`) va qaytadan ishga tushiring:
     ```bash
     python app.py
     ```
   - Endi ixtiyoriy brauzerni ochib manzil qatoriga quyidagicha yozing:
     👉 **http://myTest5.uz:5000**

> [!NOTE]
> E'tibor bering: Ilova porti (5000) ham yozilishi shart. Agar portni ham yashirishni xohlasangiz (`http://myTest5.uz` qilib), `app.py` dagi portni `80` ga o'zgartirish va Python ni administrator huquqi bilan ishga tushirish kerak bo'ladi. Hozirgi eng xavfsiz va oson yo'l — `myTest5.uz:5000` dan foydalanish.

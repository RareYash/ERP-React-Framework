Here is your **Student Review System** README, reimagined for the Indian tech community, complete with Instagram trends, Hinglish, and peak meme energy.

---

# 🎓 Padhai Likhai Karo, IAS YAS Bano System 🇮🇳

<div align="center">

**The AI tool that exposes whether the student is a "Topper" or a "Backbencher" 💀**

[✨ Features](https://www.google.com/search?q=%23-kya-kya-hai-isme) • [🚀 Jaldi Bol Kal Subah Panvel Nikalna Hai](https://www.google.com/search?q=%23-jaldi-bol-kal-subah-panvel-nikalna-hai) • [🫣 Usage](https://www.google.com/search?q=%23-kaise-use-karein) • [🧠 Big Brain Stuff](https://www.google.com/search?q=%23-bheja-fry-technical-details)

</div>

---

## 🧐 Kya Hai Ye? (Overview)

Fed up with students saying *"Mummy, paper tough tha"*? Same.

This system is the **Ultron** of School ERPs. It uses **AI (Asli Intelligence)** to read teacher reviews and tell parents exactly *kitne paani mein hai unka bachha*. No more sugar-coating. If the student is making reels in class instead of studying, this AI detects the sentiment faster than an Indian auntie spots a love affair.

### 🔥 Key Features (The Masala)

* **🔍 Vibe Check (Sentiment Analysis)**: Uses VADER NLP (Not Darth Vader, chill) to decode if the teacher is happy or doing "Moye Moye".
* **📊 Kundali (Dashboards)**: Separate views for Parents (Stress) and Teachers (Power).
* **📈 Stonk Market**: Graphs showing if the student's performance is going 🚀 or 📉.
* **🔐 Z+ Security**: Login required. Padosi aunty can't see your marks.
* **📥 Download Report**: Export the "Bezzati" (Report Card) as a text file.

---

## 🏗️ The "Kitchen" Setup (Architecture)

```
student-review-system/
│
├── app.py                      # The Main Hero (Entry Point)
├── requirements.txt            # The Masala Dabba (Dependencies)
│
├── modules/                    # The Real MVPs
│   ├── sentiment_analyzer.py   # The "Mann Ki Baat" Decoder
│   ├── data_handler.py         # The Munshi Ji (Ledger)
│   └── auth.py                 # The Gatekeeper (Watchman)
│
└── data/
    └── student_reviews.csv     # Kacha Chittha (The Truth Files) 📂

```

---

## 🚀 Jaldi Bol Kal Subah Panvel Nikalna Hai

### 1. Installation (Tyaari Jeet Ki)

```bash
# Clone marksheet... I mean repo
cd student-review-system

# Install the weapons
pip install -r requirements.txt

```

### 2. Run the App (Shuru Majboori Mein Kiye The)

```bash
streamlit run app.py

```

Open your browser to `http://localhost:8501`. **Systummm Hang hone wala hai.**

### 3. Login Credentials (Khufiya Jankari)

**👨‍👩‍👦 For Parents (Ready with Belan/Chappal):**

* **User:** `parent1`
* **Pass:** `pass1234`
* **Target:** Sophia Chen (Student ID: 01)

**👩‍🏫 For Teachers (The Judges):**

* **User:** `teacher`
* **Pass:** `admin1234`
* **Power:** Can roast (review) any student.

---

## 🫣 Kaise Use Karein?

### For Parents (The "Darr Ka Mahol" View)

1. Login. Pray to God. 🙏
2. See the **Sentiment Score**.
* **Green:** "Mithai baato!" (Distribute sweets)
* **Red:** "Beta, aaj tu gya." (You're dead meat)


3. Read the teacher's review.
4. **Download Report**: Print it out to stick on the fridge or hide under the mattress.

### For Teachers (The "Control Uday" View)

1. Login like a Boss.
2. Select a student (Target Locked 🎯).
3. Write a review.
* *Example:* "He is a good boy but talks too much."
* **AI Translation:** "Vibe is Neutral."


4. Click **Save**. The student's destiny is sealed.

---

## 🧠 Bheja Fry (Technical Details)

### Sentiment Analysis (The "Sach Ka Saamna")

We use **VADER** (Valence Aware Dictionary and sEntiment Reasoner). It's smarter than your Sharma Ji ka beta.

It understands:

* **Sandwich Feedback:** Praise → Insult → Praise.
* **The word "But":** *He is smart BUT lazy.* (AI catches the laziness).
* **Scores:**
* `+1.0`: Absolute Topper 🏆
* `0.0`: Average (Sab Moh Maya Hai) 🧘
* `-1.0`: Chin Tapak Dam Dam (Situation Critical) 🚨



### Categories

The AI automatically sorts the drama into:

* **Behavior:** Did they throw chalk?
* **Homework:** Did the "dog eat it" again?
* **Participation:** Sleeping or answering?

---

## 🔄 Jugaad (Customization)

### Adding More People

Go to `modules/config.py`. Add users like you add guests to a wedding list.

```python
USERS = {
    "chintu_dad": {
        "password": "password123",
        "role": "parent",
        "student_id": "03"
    }
}

```

### Changing Colors

Want the "Fail" color to be darker red? Change it in `config.py`.

```python
CHART_COLORS = {
    "negative": "#EF4444",  # Danger color
}

```

---

## 🚧 Future Plans (Sapne Suhane)

* [ ] **WhatsApp Integration:** Send reports directly to dad's WhatsApp (Instant death feature).
* [ ] **Meme Generator:** Auto-generate a meme based on marks.
* [ ] **Voice Note Support:** Teacher can record "Isse na ho payega."

---

## 🤝 Contributing (Aao Kabhi Haveli Pe)

Found a bug? Or want to add a "Roast Mode"?

1. Fork it.
2. Fix it.
3. PR bhejo. (Pull Request send karo).

---

## 📝 License

Educational use only. Don't use this to actually roast your friends... unless? 👀

---

<div align="center">

**Made with ❤️ and ☕ in India**

*Beti Bachao, Beti Padhao, aur Code Likho.*

</div>

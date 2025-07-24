```markdown
# 🎬 Cinemood - Mood-Based Movie Recommendation System

**Cinemood** is a smart, mood-aware movie recommendation web app that suggests **Bollywood** and **Hollywood** movies based on your selected mood. Whether you're feeling **happy**, **sad**, **romantic**, or just want to **relax**, Cinemood brings the right entertainment to your screen.

Built with **Python**, **Pandas**, and **Streamlit**, it delivers a fast, responsive interface and intelligent suggestions.

---

## 🚀 Live Demo (Render)

👉 [Try Cinemood on Render] https://mood-based-movie-reccomendation-system-1.onrender.com/
---

## 📂 Project Structure

```

cinemood/
├── recommendation\_engine.py        # Core logic for filtering movies by mood
├── streamlit\_app.py                # Streamlit frontend application
├── bollywood\_movies.csv            # Dataset of Bollywood movies
├── hollywood\_movies.csv            # Dataset of Hollywood movies
├── requirements.txt                # Python dependencies for Render deployment
└── README.md                       # This documentation

````

---

## 💡 Features

- Select from multiple moods: **Happy, Sad, Angry, Romantic, Excited, Relaxed**
- Dual support for **Hollywood** and **Bollywood** databases
- Automatically recommends relevant movies based on your emotion
- Lightweight and fast deployment via **Render**
- Easy to use and mobile-friendly

---

## 🛠️ Technologies Used

- Python 3.10+
- Streamlit
- Pandas
- NumPy
- CSV Datasets

---

## 🔧 Installation (Run Locally)

```bash
# Step 1: Clone the repository
git clone https://github.com/Chetan-316/mood-based-movie-reccomendation-system.git
cd mood-based-movie-reccomendation-system

# Step 2: Install required packages
pip install -r requirements.txt

# Step 3: Run the app
streamlit run streamlit_app.py
````

---

## 🌐 Deployment on Render

To deploy this on **Render**:

1. Push your repo to GitHub.
2. Go to [https://render.com](https://render.com) → New → Web Service.
3. Connect to your GitHub repository.
4. Fill in:

   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**:

     ```
     streamlit run streamlit_app.py --server.port=10000 --server.enableCORS=false
     ```
5. Add Environment Variable (optional but recommended):

   * `PYTHON_VERSION = 3.10`

---

## 🎭 Supported Moods

| Mood     | Emoji | Example Suggestions       |
| -------- | ----- | ------------------------- |
| Happy    | 😄    | Comedy, Family, Feel-good |
| Sad      | 😢    | Emotional, Drama          |
| Angry    | 😠    | Action, Thriller          |
| Romantic | 💖    | Romance, Love stories     |
| Excited  | 🤩    | Adventure, Sci-Fi         |
| Relaxed  | 🧘    | Calm, Slice-of-life       |

---

## 🤝 Contributing

We welcome contributions to improve Cinemood!
Fork the repo, create a feature branch, and submit a pull request.

---

## 📬 Contact

**Author**: Chetan Agrawal
**GitHub**: [Chetan-316](https://github.com/Chetan-316)
**Project Name**: `Cinemood`
**Email**: chetan.agrawal.work@gmail.com


---

> Built with ❤️ for movie lovers who believe emotions deserve the right stories.


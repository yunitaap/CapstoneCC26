# 🍳 OLAH: Punya Sisa Bahan Makanan? di-OLAH Aja!

**Coding Camp 2026 powered by DBS Foundation — CC26-PSU127**
> Repository ini merupakan bagian **Data Scientist** dari proyek OLAH.

---

## 📌 Project Overview

**OLAH** adalah aplikasi berbasis data science yang membantu pengguna menemukan resep masakan berdasarkan bahan yang tersedia di rumah. OLAH hadir sebagai solusi digital yang membantu pengguna mengolah bahan yang tersedia secara optimal.

> Tema: **Sustainable Living & Responsible Consumption**

---

## 🎯 Problem Statement

Bagaimana menghadirkan aplikasi yang mampu merekomendasikan resep secara fleksibel berdasarkan bahan yang dimiliki pengguna, serta membantu meminimalkan pemborosan makanan di rumah tangga.

---

## ❓ Business Questions

1. Bagaimana menentukan resep yang paling relevan berdasarkan kombinasi bahan yang dimiliki pengguna?
2. Bahan apa saja yang paling sering digunakan dan bagaimana pola kombinasinya dalam resep?
3. Sejauh mana sistem ini membantu pengguna mengurangi potensi food waste?

---

## 👥 Tim Data Scientist

| ID | Nama | Peran |
|---|---|---|
| CDCC289D6X0619 | Titania Rahmawati | Data Scientist |
| CDCC200D6X2238 | Yunita Asri Prameswari | Data Scientist |

**Advisor:** Benyamin Uber Jaya Prana · Rico Halim

---

## 📊 Dataset

| Atribut | Keterangan |
|---|---|
| Sumber | Kaggle |
| Jumlah Resep | 14.915 |
| Jumlah Fitur | 12 |

### Kolom Dataset

| Kolom | Tipe | Deskripsi |
|---|---|---|
| `Title` | string | Nama resep asli |
| `Ingredients` | string | Daftar bahan sebelum preprocessing |
| `Steps` | string | Langkah memasak |
| `Loves` | int | Jumlah penyuka resep |
| `URL` | string | URL resep asli di Cookpad |
| `Category` | string | Kategori bahan protein utama |
| `Title Cleaned` | string | Judul setelah preprocessing |
| `Total Ingredients` | int | Jumlah bahan per resep |
| `Ingredients Cleaned` | string | Bahan setelah tokenisasi dan normalisasi |
| `Total Steps` | int | Jumlah langkah memasak |
| `Ingredients Final` | string | Bahan preprocessing akhir untuk sistem rekomendasi |
| `Ingredients Join` | string | Bahan gabungan sebagai fitur TF-IDF |

---

## 🗂️ Struktur Proyek

```
Capstone Project DS/
│
├── data/
│   ├── data_raw.csv                # Dataset mentah
│   ├── data_cleaned.csv            # Dataset setelah cleaning
│   ├── data_final.csv              # Dataset siap pemodelan
│   └── data_dictionary.xlsx        # Kamus data
│
├── notebooks/
│   ├── data_raw.csv
│   ├── data_final.csv
│   ├── data_dictionary.csv
│   ├── preprocessing.ipynb         # Data wrangling & cleaning
│   └── eda.ipynb                   # Exploratory Data Analysis
│
├── streamlit/
│   ├── dashboard.py                # Dashboard EDA interaktif
│   ├── data_final.csv
│   └── requirements.txt
│
└── README.md
```

---

## 🔄 Alur Kerja Data Science

```
Data Gathering → Preprocessing → Data Final → EDA → Dashboard Streamlit
```

---

## ⚙️ Tech Stack

| Kebutuhan | Teknologi |
|---|---|
| Manipulasi data | Python, Pandas, NumPy |
| Visualisasi | Matplotlib, Wordcloud |
| Modeling | Scikit-learn (TF-IDF) |
| Dashboard | Streamlit |
| Notebook | Jupyter Notebook |

---

## 🚀 Cara Menjalankan

**1. Clone repository**

```bash
git clone https://github.com/Olah-CodingCamp/DBS_DataScience.git
cd DBS_DataScience
```

**2. Install dependencies**

```bash
pip install -r streamlit/requirements.txt
```

**3. Jalankan notebook** (urutan sesuai alur kerja)

```bash
jupyter notebook
# Jalankan: preprocessing.ipynb → eda.ipynb
```

**4. Jalankan dashboard**

```bash
cd streamlit
streamlit run dashboard.py
```

---

**Coding Camp 2026 powered by DBS Foundation — CC26-PSU127**

---
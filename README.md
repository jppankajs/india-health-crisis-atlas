# 🏥 India Health Crisis Atlas

> **74% of India's districts are in High or Critical health risk — and the data proves it.**

Analyzed 101 health indicators across 707 districts using NFHS-5 (2019-21) government data. Built a composite Health Risk Score, KMeans clustering into 4 risk tiers, an interactive Folium choropleth map, and a live Streamlit dashboard with state-level filters.

---

## 🔴 Live Demo

| Interface | Link |
|---|---|
| 🗺️ Interactive Map | [jppankajs.github.io/india-health-crisis-atlas](https://jppankajs.github.io/india-health-crisis-atlas) |
| 📊 Full Dashboard | [Streamlit App](https://india-health-crisis-atlas-b9xqh7cqj6qekpzjba7dvh.streamlit.app) |

---

## 📊 What It Does

- **Composite Health Risk Score** — weighted index across child stunting, anaemia, sanitation, and women's literacy
- **KMeans Clustering** — districts grouped into 4 risk tiers (Critical / High / Moderate / Low)
- **Folium Choropleth Map** — color-coded district-level risk visualization across India
- **Streamlit Dashboard** — interactive filters by state and risk category, live KPI cards, and ranked charts
- **Key Indicators Tracked** — child stunting, child anaemia, sanitation coverage, women's literacy

---

## 📈 Risk Distribution

| Risk Category | Districts | % of India |
|---|---|---|
| 🔴 Critical Risk | 240 | 33.9% |
| 🟠 High Risk | 286 | 40.5% |
| 🟡 Moderate Risk | 38 | 5.4% |
| 🟢 Low Risk | 143 | 20.2% |

---

## 🛠️ Stack

`Python` · `Pandas` · `Scikit-learn` · `Folium` · `Streamlit` · `Matplotlib`

---

## 📂 Project Structure

```
india-health-crisis-atlas/
├── assets/charts/          # Static chart exports
├── dashboard/
│   ├── app.py              # Streamlit dashboard
│   └── india_health_map.html  # Folium choropleth map
├── data/
│   ├── raw/                # NFHS-5 source data
│   └── processed/          # Cleaned & scored datasets
├── notebooks/              # EDA, ML, clustering notebooks
├── index.html              # GitHub Pages entry (Folium map)
├── requirements.txt
└── README.md
```

---

## 🚀 Run Locally

```bash
git clone https://github.com/jppankajs/india-health-crisis-atlas.git
cd india-health-crisis-atlas
pip install -r requirements.txt
cd dashboard
streamlit run app.py
```

---

## 📂 Data Source

- **Dataset:** National Family Health Survey — 5 (NFHS-5), 2019-21
- **Source:** Department of Health and Family Welfare, Government of India
- **Link:** [data.gov.in](https://data.gov.in)
- **Coverage:** 707 districts · 36 states/UTs · 101 health indicators

---

## 👤 Author

**Pankaj Singh** — BCA (Data Analytics) | Kristu Jayanti University, Bengaluru
GitHub: [github.com/jppankajs](https://github.com/jppankajs)

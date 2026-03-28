# Local AI Student Tutor

A privacy-focused, offline AI chatbot designed for university students.

**Authors:** Xingyu Ren, Hao Xu
**Institution:** Centria University of Applied Sciences
**Project:** Information Technology Thesis (2026)

## Key Features
* **100% Offline Inference:** Protects student data privacy using local LLMs.
* **Bilingual Support:** Provides technical reasoning in English, followed by a Chinese translation.
* **Local Logging:** Saves interaction metadata (latency, RAM usage) to CSV and exports to formatted Excel.
* **Admin Panel:** Password-gated interface to modify AI instructions and view logs.

## Setup Environment
pip install -r requirements.txt

## Run the Main Application
streamlit run app.py

## Run Automated UI Validation
python test_ui.py

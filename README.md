# 📧 Emlic: Virtual Assistant Task Automator
An interactive utility designed to normalize, validate, and manage lead generation datasets for Virtual Assistant (VA) workflows.

Access LiveApp: [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://emlicc.streamlit.app/)

### 🛠 Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

### Description
In lead generation, raw data is often "noisy"—filled with duplicate emails, inconsistent casing, and formatting errors that break CRM systems. Emlic transforms messy CSV exports into structured, verified datasets ready for high-level outreach.

I built this system to handle the common "human errors" found in VA spreadsheets. By implementing a Python-based cleaning pipeline, the app standardizes names, validates email syntax, and organizes the results into a local SQL database for high data integrity.

### Key Features

#### A. Intelligent Data Normalization
* **Dynamic Header Mapping:** Automatically identifies "Name" and "Email" columns even if they are labeled inconsistently across different datasets.
* **Case Standardization:** Uses string manipulation to convert mixed-case names (e.g., "jane doe" or "ALICE SMITH") into professional Title Case.

#### B. Verification & Deduplication
* **Regex Email Validation:** Implements a backend filtering system to flag invalid email formats before they reach your CRM.
* **Merge & Purge Logic:** Instantly identifies and removes duplicate entries based on unique email addresses to prevent redundant outreach.

#### C. VA Utility Suite
* **Timezone Integration:** Calculates the current local time for leads based on their city or region, helping VAs determine the best time for contact.
* **SQL Synchronization:** Automatically stores processed leads into a structured SQLite database, providing a synchronized view of all historical data.
* **CRM-Ready Export:** Generates a sanitized CSV download optimized for direct import into tools like HubSpot, Salesforce, or Mailchimp.

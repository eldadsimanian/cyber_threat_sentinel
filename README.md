# 🛡️ CyberThreat-AI Sentinel
> **Real-time Log Analysis & AI Threat Investigation Dashboard**

CyberThreat-AI Sentinel is an end-to-end cybersecurity analytics tool designed to process network logs, detect anomalies (such as Brute Force attempts and Data Exfiltration), and perform automated Tier-1 threat investigations using LLM AI Agents.

---

## 🏗️ Architecture & Workflow

1. **Data Ingestion & Processing:** Efficient log parsing and anomaly filtering using **Pandas**.
2. **AI Agent Integration:** Automated incident response powered by **Groq API (Llama-3)** delivering structured JSON analysis.
3. **Interactive Dashboard:** Visual telemetry and threat breakdown built with **Streamlit** and **Plotly**.

---

## 🚀 Key Features

* 📊 **Live Telemetry:** Metrics for total processed logs, detected threats, and data volume.
* 🚨 **Automated Anomaly Detection:** Rule-based heuristics for identifying suspicious IP activities.
* 🤖 **AI SOC Analyst:** On-demand LLM investigation providing Severity, Attack Vector, and Remediation steps.
* 📁 **Dynamic Log Upload:** Upload custom CSV log files directly through the dashboard.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Data & Viz:** Pandas, Plotly Express
* **Frontend:** Streamlit
* **AI Provider:** Groq API (Llama-3.3-70b)

---

## 💻 Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/cyber_threat_sentinel.git](https://github.com/YOUR_USERNAME/cyber_threat_sentinel.git)
   cd cyber_threat_sentinel
#  Hospital Appointment No-Show Analysis Dashboard

This project analyzes hospital appointment data to uncover the factors that lead to patient no-shows.  
It helps hospitals improve scheduling efficiency, reduce missed appointments, and enhance patient care through data-driven insights.

---

## Project Overview

Missed appointments ("no-shows") are a common challenge in healthcare facilities, leading to resource waste and delayed treatments.  
This dashboard explores trends in patient attendance and provides insights hospitals can use to reduce no-show rates.

---

## Objectives

- Identify patterns that influence patient no-shows.  
- Analyze demographic factors such as **age** and **gender**.  
- Evaluate the impact of **SMS reminders** on attendance.  
- Build an **interactive dashboard** for easy exploration.

---

##  Dataset

The dataset (`medical appointment.csv`) contains over **100,000 appointment records** with the following key columns:

| Column | Description |
|--------|--------------|
| `PatientID` | Unique identifier for each patient |
| `Gender` | Patient gender |
| `Age` | Age of the patient |
| `AppointmentDay` | Date of the appointment |
| `SMS_received` | Whether the patient received an SMS reminder |
| `No-show` | Whether the patient missed the appointment |

> **Source:** Public dataset from Kaggle – *Hospital Appointment No Show Dataset.*

---

## Tools & Technologies

- **Python** – Data cleaning and analysis (`Pandas`, `NumPy`)
- **Streamlit** – Interactive web dashboard
- **Matplotlib & Seaborn** – Data visualization
- **Power BI** *(optional)* – Additional interactive reporting
- **GitHub** – Version control and project hosting

---

## How to Run the Streamlit App

1. Clone this repository  
   ```bash
   git clone https://github.com/IAN-RIUA/Hospital-Appointment-No-Show-Analysis-Dashboard.git

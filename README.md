# 🌍 EPA Air Quality Data Pipeline (2014–2024)

This project presents an automated, scalable data pipeline built for analyzing 10 years of U.S. EPA air quality data using PySpark, AWS S3 (blob simulation), PostgreSQL, and Power BI.

---

## 📌 Objective

To automate the ingestion, cleaning, transformation, storage, and visualization of pollutant data — enabling real-time, interactive analysis of air quality trends across time, location, and pollutant types.

---

## 📁 Dataset Details

- **Source**: U.S. Environmental Protection Agency (EPA) Air Quality System (AQS)
- **Format**: CSV (structured)
- **Years Covered**: 2014 to 2024
- **Pollutants**:
  - Carbon Monoxide (CO)
  - Nitrogen Dioxide (NO₂)
  - Sulfur Dioxide (SO₂)
  - Ozone (O₃)
- **Total Records**: ~3 million
- **Storage**: Uploaded to AWS S3 in 4 folders (`/Co`, `/No2`, `/So2`, `/Ozone`)

---

## ⚙️ Technology Stack

| Layer           | Tool / Platform                |
|-----------------|-------------------------------|
| Programming     | Python 3.9                     |
| Processing      | PySpark (Local mode)           |
| Cloud Storage   | AWS S3                         |
| Database        | PostgreSQL                     |
| Visualization   | Power BI (DirectQuery Mode)    |
| Automation      | Python Script + Task Scheduler |
| Dependency Mgmt | JARs for S3 + JDBC             |

---

## 🛠️ Project Setup

### 1. Prerequisites

- Java 11 or higher
- Apache Spark 3.x (set `JAVA_HOME`)
- Python 3.9+
- PostgreSQL installed locally
- AWS S3 bucket with pollutant folders and uploaded files

### 2. Required JARs

Place the following JARs in the `spark_jars/` folder:
- `postgresql-42.x.x.jar` (JDBC)
- `hadoop-aws-3.x.x.jar`
- `aws-java-sdk-bundle-1.x.x.jar`

*(JARs are included in the uploaded archive along with the pipeline script)*

---

## 🚀 How to Run

### 🟢 Run the Pipeline Script

```bash
python main_test.py

```

## 📷 Dashboard Preview
Below is a screenshot of the final interactive Power BI dashboard built for this project, connected live to the PostgreSQL database:
<img width="702" height="393" alt="image" src="https://github.com/user-attachments/assets/eb819dba-7731-4e9e-b180-c29a29ca6985" />

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
### 🔗 Required JAR Downloads (External)

To enable integration between Spark, AWS S3, and PostgreSQL, download and place the following JARs into the `spark_jars/` folder:

| JAR File | Description | Download Link |
|----------|-------------|----------------|
| `postgresql-42.6.0.jar` | PostgreSQL JDBC Driver | [Download](https://jdbc.postgresql.org/download/postgresql-42.6.0.jar) |
| `hadoop-aws-3.3.5.jar` | Hadoop AWS Connector for Spark | [Download](https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.5/hadoop-aws-3.3.5.jar) |
| `aws-java-sdk-bundle-1.11.1026.jar` | AWS SDK Bundle (required by Hadoop) | [Download](https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1026/aws-java-sdk-bundle-1.11.1026.jar) |

🗂️ **Place all downloaded `.jar` files inside your `spark_jars/` folder before running the pipeline.**


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

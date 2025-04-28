# Kaggle Dataset Analysis with PySpark

This project contains a dockerized PySpark environment for analyzing the Kaggle dataset: https://www.kaggle.com/datasets/alistairking/u-s-crude-oil-imports?resource=download

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Clone this repository:
git clone https://github.com/AhmedBuckets/crude_oil_spark_analysis.git
cd crude_oil_spark_analysis

2. Start the Spark cluster:
- docker-compose up -d

3. Run the analysis:
- docker exec -it spark-master spark-submit --master spark://spark-master:7077 /scripts/analysis.py

4. View the results:
- The directory data/ should contain the answers to the questions in the form of datasets. 
- Question 1: albania_analysis.csv 
- Question 2: uk_analysis.csv
- Question 3: max_grade_by_year_origin.csv

## Project Structure

- `data/`: Contains the Kaggle dataset and output answers
- `scripts/`: Python scriptfor data analysis
- `spark-config/`: Configuration files for Spark

## Running Analysis Script

Assuming Docker is installed and running, run:
- docker-compose up -d

If for whatever reason Docker hangs up, run:
- docker-compose down
- docker-compose build
- docker compose up -d 

To run the analysis script:
- docker exec -it spark-master spark-submit --master spark://spark-master:7077 /scripts/your_script.py
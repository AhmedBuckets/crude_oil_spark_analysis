# Kaggle Dataset Analysis with PySpark

This project contains a dockerized PySpark environment for analyzing a Kaggle dataset.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Clone this repository:
git clone <repository-url>
cd spark-kaggle-analysis

2. Start the Spark cluster:
docker-compose up -d

3. Run the analysis:
docker exec -it spark-master spark-submit --master spark://spark-master:7077 /scripts/analysis.py

4. View the results:
- Spark UI: http://localhost:8080
- Application UI: http://localhost:4040 (when a job is running)

## Project Structure

- `data/`: Contains the Kaggle dataset
- `scripts/`: Python scripts for data analysis
- `spark-config/`: Configuration files for Spark

## Running Analysis Script

Assuming Docker is installed and running, run:
- docker-compose up -d

If for whatever reason Docker hangs up, run:
- docker-compose down
- docker-compose build
- docker compose up -d 

To run the analysis script:
-docker exec -it spark-master spark-submit --master spark://spark-master:7077 /scripts/your_script.py
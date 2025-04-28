# Kaggle Dataset Analysis with PySpark

This project contains a dockerized PySpark environment for analyzing the Kaggle dataset: https://www.kaggle.com/datasets/alistairking/u-s-crude-oil-imports?resource=download

## Prerequisites

- Docker
- Docker Compose
- git lfs (for large files)

## A Note on Git LFS
- To be complete, I included the data file. Since its very large I uploaded it to git via git lfs, a large file service for github. 
- Install git lfs: `brew install git-lfs` (requires brew of course) or visit https://git-lfs.com/ 
- After cloning, run `git lfs pull` to get the files managed by git lfs- otherwise they will only be pointers to the files and Spark will complain
- Alternatively, just copy the data.csv file from kaggle to the directory and replace the one git pulls down


## Quick Start

1. Clone this repository and set up files locally:
- git clone https://github.com/AhmedBuckets/crude_oil_spark_analysis.git
- cd crude_oil_spark_analysis
- git lfs pull 

2. Start the Spark cluster:
- docker-compose up -d

3. Run the analysis:
- docker exec -it spark-master spark-submit --master spark://spark-master:7077 /scripts/analysis.py

4. View the results:
- The directory data/ should contain the answers to the questions in the form of datasets. There is some analysis below.
- Question 1: albania_analysis.csv + warehouse/oil_analysis/albania_destinations
- Question 2: uk_analysis.csv
- Question 3: max_grade_by_year_origin.csv

## Project Structure

- `data/`: Contains the Kaggle dataset and output answers
- `warehouse`: Contains iceberg output tables
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
- docker exec -it spark-master spark-submit --master spark://spark-master:7077 /scripts/analysis.py



## Analysis Results

### Question 1: Top 5 Destinations for Oil Produced in Albania

Top destinations for oil exports from Albania:

| Destination Name | Count |
|------------------|-------|
| PADD1 (East Coast) | 30 |
| New Jersey | 30 |
| United States | 15 |
| Paulsboro, NJ | 15 |
| AXEON SPECIALTY PRODUCTS LLC / PAULSBORO / NJ | 15 |

**Analysis**: It looks like the east coast of the US makes up the top 5 destinations for Albanian oil. (Actually it looks like they are the only recipients of Albanian oil based on this data set)

### Question 2: UK Destinations with Total Quantity > 100,000

Destinations for UK oil exports where the total quantity exceeds 100,000 units:

| Destination Name | Sum Quantity |
|------------------|-------------|
| Texas | 137,125 |
| United States | 233,095 |
| PADD3 (Gulf Coast) | 354,908 |
| Louisiana | 112,342 |
| Mississippi | 101,885 |

**Analysis**: The USA again tops the charts here, this time making up all recipients of UK oil where the quantity exceeds 100,000. 

### Question 3: Most Exported Grade for Each Year and Origin

This analysis identifies the most exported oil grade for each combination of year and country of origin. Here's the data for 2024:

| Year | Grade Name | Origin Name | Max Quantity |
|------|------------|-------------|--------------|
| 2024 | Light Sweet | Africa | 53,116 |
| 2024 | Light Sweet | Algeria | 3,759 |
| 2024 | Light Sweet | Angola | 3,689 |
| 2024 | Light Sweet | Argentina | 6,804 |
| 2024 | Medium | Brazil | 38,136 |
| 2024 | Heavy Sweet | Cameroon | 4,543 |
| 2024 | Heavy Sour | Canada | 659,673 |
| 2024 | Heavy Sour | Canada (Region) | 659,673 |
| 2024 | Medium | Chad | 4,011 |
| 2024 | Heavy Sour | Colombia | 52,591 |
| 2024 | Heavy Sour | Ecuador | 17,234 |
| 2024 | Light Sour | Eurasia | 14,154 |
| 2024 | Heavy Sour | Europe | 5,635 |
| 2024 | Medium | Ghana | 6,223 |
| 2024 | Medium | Guyana | 37,961 |
| 2024 | Medium | Iraq | 32,641 |
| 2024 | Light Sour | Kazakhstan | 14,154 |
| 2024 | Heavy Sour | Kuwait | 3,521 |
| 2024 | Light Sweet | Libya | 12,152 |
| 2024 | Heavy Sour | Mexico | 53,900 |
| 2024 | Medium | Middle East | 97,279 |
| 2024 | Light Sweet | Nigeria | 33,516 |
| 2024 | Heavy Sour | Non-OPEC | 810,040 |
| 2024 | Medium | Norway | 3,801 |
| 2024 | Medium | OPEC | 100,590 |
| 2024 | Heavy Sour | Other Americas | 177,765 |
| 2024 | Medium | Saudi Arabia | 64,638 |
| 2024 | Heavy Sour | Trinidad and Tobago | 11,368 |
| 2024 | Heavy Sour | United Kingdom | 5,635 |
| 2024 | Heavy Sour | Venezuela | 33,033 |
| 2024 | Heavy Sour | World | 846,594 |
...
...
...
...
The full results are extensive (spanning 2009-2024 and numerous countries).

#
**Analysis**: 

We could use this data to see who is growing as an oil exporter over the years and with some additional aggregates map out growing relationships. 


# Documenting an issue with Polars

Documenting a case where "Polars" fails to join two tables when the tables are bigger than RAM available.

## Details of the program

We are trying to join two parquet tables and get the results. The two tables:

| Table name | Parquet files | Number of records | Size on disk (compressed) |
|------------|---------------|-------------------|--------------|
| branded_food | ./data/parquet/branded_food.parquet | 1,958,978 | ~323MB|
| food_nutrient | ./data/parquet/food_nutrient.parquet | 27,800,079 | ~225MB|


## Issue

The polars library will fail when we run this program on a machine with insufficient RAM. 

## How to run it

### Option 1 ( <10GB of RAM)

```bash
pip install requirements.txt
python3 polars_test.py
```

### Option 2 (using docker)

```bash
docker compose up
```

## Other observations
- This program will run, if you select fewer columns
- This same SQL query can be run in PySpark with 4GB limit on the driver instance, but takes a long time.

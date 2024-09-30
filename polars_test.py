"""
Simple program to replace the polars issue with a join and memory exhaustion

"""

from math import e
from re import T
import polars as pl


def run_polars_test():
    # Setup the tables with the lazy loading option
    bf = pl.read_parquet("./data/parquet/branded_food.parquet/*.parquet", low_memory=True).lazy()
    fn = pl.read_parquet("./data/parquet/food_nutrient.parquet/*.parquet", low_memory=True).lazy()

    ctx = pl.SQLContext()
    ctx.register("branded_food", bf)
    ctx.register("food_nutrient", fn)

    result = ctx.execute(
        """
            SELECT count(*) AS row_count 
            FROM branded_food
        """,
        eager=False,
    )

    print("Number of rows in table: branded_food")
    print(result.collect())

    result = ctx.execute(
        """
            SELECT count(*) AS row_count
            FROM food_nutrient
        """,
        eager=False,
    )

    print("Number of rows in table: food_nutrient")
    print(result.collect())

    result = ctx.execute(
        """
            SELECT bf.fdc_id AS fdc_id, 
                brand_owner, 
                brand_name, 
                gtin_upc, 
                ingredients, 
                serving_size, 
                serving_size_unit,
                branded_food_category, 
                package_weight, 
                short_description,
                fn.nutrient_id AS nutrient_id, 
                CAST(fn.amount AS float) AS amount
            FROM branded_food AS bf
            LEFT JOIN food_nutrient AS fn ON fn.fdc_id = bf.fdc_id
            WHERE  bf.fdc_id='2446571'
        """
    )

    print("The explain plan for the query: ")
    print(result.explain(streaming=True))

    print("The results of the query:")
    # FYI: This will fail when the system as less 10 GB
    print(result.collect(streaming=True))


if __name__ == "__main__":
    print("Starting the polars test")
    run_polars_test()
    print("End of the test")

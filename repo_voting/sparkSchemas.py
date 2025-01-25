from pyspark.sql.types import (StructType,
                               StructField, StringType, TimestampType, IntegerType)

schema = StructType([
    StructField("voter_id", StringType(), nullable=False),
    StructField("candidate_id", StringType(), nullable=True),
    StructField("voting_time", TimestampType(), nullable=True),
    StructField("vote", IntegerType(), nullable=True, default=1)
])

candidates_schema = StructType([
    StructField("candidate_id", StringType(), False),
    StructField("candidate_name", StringType(), True),
    StructField("party_affiliation", StringType(), True),
    StructField("biography", StringType(), True),
    StructField("campaign_platform", StringType(), True),
    StructField("photo_url", StringType(), True)
])

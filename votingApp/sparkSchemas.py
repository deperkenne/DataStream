# Définir le schéma Spark pour la table 'votes'
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType

schema = StructType([
    StructField("voter_id", StringType(), nullable=False),
    StructField("candidate_id", StringType(), nullable=True),
    StructField("voting_time", TimestampType(), nullable=True),
    StructField("vote", IntegerType(), nullable=True, default=1)
])

# Définir le schema Spark
candidates_schema = StructType([
    StructField("candidate_id", StringType(), False),       # VARCHAR(255) -> StringType()
    StructField("candidate_name", StringType(), True),       # VARCHAR(255) -> StringType()
    StructField("party_affiliation", StringType(), True),    # VARCHAR(255) -> StringType()
    StructField("biography", StringType(), True),            # TEXT -> StringType()
    StructField("campaign_platform", StringType(), True),    # TEXT -> StringType()
    StructField("photo_url", StringType(), True)             # TEXT -> StringType()
])
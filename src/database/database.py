from peewee import SqliteDatabase, PostgresqlDatabase
from utils.settings import DATABASE, DATABASE_ENGINE

DATABASES = {
    "sqlite": lambda: SqliteDatabase(
        DATABASE["sqlite"]["NAME"],
        pragmas={
            "journal_mode": "wal",
            "cache_size": -1024 * 64,
            "foreign_keys": 1,
        },
    ),

    "postgres": lambda: PostgresqlDatabase(
        DATABASE["postgres"]["NAME"],
        user=DATABASE["postgres"]["USER"],
        password=DATABASE["postgres"]["PASSWORD"],
        host=DATABASE["postgres"]["HOST"],
        port=int(DATABASE["postgres"]["PORT"]),
    ),
}

# fallback to sqlite if DATABASE_ENGINE is invalid
db = DATABASES.get(DATABASE_ENGINE, DATABASES["sqlite"])()
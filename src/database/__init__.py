"""
This module handles database connections and operations using peewee ORM.
"""
from database.database import db

from database import sqliteMigrator, postgresMigrator

from utils.settings import DATABASE_ENGINE

migrator = postgresMigrator if DATABASE_ENGINE == "postgres" else sqliteMigrator


from database import setup


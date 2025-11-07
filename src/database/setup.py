"""
This module handles database connections and operations.
"""


from database import db
from database.models import MODELS

from database import migrator

def initialize_database():

    """
    Initializes the database by creating tables for all defined models.
    """
    with db:
        db.create_tables(MODELS)


def auto_migrate():
    """
    Automatically checks for schema differences and applies migrations.
    """
    migrator.makemigrations(MODELS)
    migrator.migrate_models(MODELS)

"""
This module will have all the migration scripts for the database.
"""

import inspect
from peewee import Model, Field
from playhouse.migrate import PostgresqlMigrator, migrate
from database import db

from utils import Logger


_logger = Logger('System.Database.Migrator')

def makemigrations(models: list[Model]):
    """
    Compares model definitions with the database schema
    and prints what would change (like Django's makemigrations).
    """

    migrator = PostgresqlMigrator(db)
    cursor = db.cursor()

    _logger.info("🔍 Checking for schema differences...")
    for model in models:
        table_name = model._meta.table_name

        # 🔄 REPLACED PRAGMA with Postgres version
        cursor.execute("""
                       SELECT column_name FROM information_schema.columns
                       WHERE table_name = %s;
                       """, (table_name,))
        existing_cols = {row[0] for row in cursor.fetchall()}

        for field_name, field_obj in model._meta.fields.items():
            if field_name not in existing_cols:
                _logger.debug(f"🆕 Will add column '{field_name}' to table '{table_name}' ({type(field_obj).__name__})")

    _logger.info("✅ Done checking schema.")


def migrate_models(models: list[Model]):
    """
    Actually applies the missing columns (like Django's migrate).
    Adds new fields but won't delete or rename.
    """

    migrator = PostgresqlMigrator(db)
    cursor = db.cursor()
    operations = []

    for model in models:
        table_name = model._meta.table_name

        if not db.table_exists(table_name):
            _logger.debug(f"🆕 Creating new table '{table_name}' for model {model.__name__}")
            model.create_table()
            continue

        # 🔄 REPLACED PRAGMA with Postgres version
        cursor.execute("""
                       SELECT column_name, is_nullable
                       FROM information_schema.columns
                       WHERE table_name = %s;
                       """, (table_name,))
        existing_cols_detail = {
            row[0]: row for row in cursor.fetchall()
        }
        existing_cols = set(existing_cols_detail.keys())

        for field_name, field_obj in model._meta.fields.items():

            # Missing column → add it (existing logic)
            if field_name not in existing_cols:
                _logger.debug(f"🆕 Adding column '{field_name}' to '{table_name}'")
                operations.append(migrator.add_column(table_name, field_name, field_obj))
                continue

            # 🔧 Detect NOT NULL → NULL change
            col_name, is_nullable = existing_cols_detail[field_name]
            existing_not_null = (is_nullable == "NO")

            if existing_not_null and field_obj.null:
                _logger.debug(f"🔧 Dropping NOT NULL on {table_name}.{field_name}")
                operations.append(
                    migrator.drop_not_null(table_name, field_name)
                )

    if operations:
        _logger.info(f"✍️ Applying {len(operations)} migration(s)...")
        with db.atomic():
            migrate(*operations)
        _logger.info("✅ Migration complete.")
    else:
        _logger.info("✅ No migrations needed.")
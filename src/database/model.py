"""
This module is the base model definition for the database using peewee ORM.
"""

from peewee import Model, DateTimeField
from datetime import datetime

from database import db

class BaseModel(Model):

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db

    def save(self, *args, **kwargs):

        if not self.created_at:
            self.created_at = datetime.now()

        self.updated_at = datetime.now()

        return super().save(*args, **kwargs)
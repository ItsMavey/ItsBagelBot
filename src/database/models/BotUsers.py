from peewee import CharField, DoesNotExist

from database.model import BaseModel

class BotUsers(BaseModel):

    username = CharField(unique=True)
    display_name = CharField()
    user_id = CharField(unique=True, null=True)

    def __str__(self):
        return f"<BotUser username={self.username} display_name={self.display_name} user_id={self.user_id}>"


    @classmethod
    def get_user(cls, username: str):
        """Retrieve a bot user by username."""

        username = username.lower()
        return cls.get_or_none(cls.username == username)

    @classmethod
    def get_user_by_id(cls, user_id: str):
        """Retrieve a bot user by user ID."""
        return cls.get_or_none(cls.user_id == user_id)

    def update_from_response(self, data):
        """Update bot user information from provided data."""

        self.username = data.get("username", self.username)
        self.display_name = data.get("display_name", self.display_name)
        self.user_id = data.get("user_id", self.user_id)
        self.save()
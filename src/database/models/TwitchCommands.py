"""
This module handles the data for the dynamic twitch commands created by the user through chat.
"""


from peewee import CharField, TextField, BooleanField


from database.model import BaseModel

class TwitchCommands(BaseModel):

    command = CharField(unique=True)
    streamer_name = CharField(default='unknown')
    response = TextField()
    is_active = BooleanField(default=True)
    created_by = CharField()

    def __str__(self):
        return f'Command: !{self.command} -> {self.response}, Active: {self.is_active}, Created by: {self.created_by}'


    @classmethod
    def get_command(cls, command: str, streamer_name: str):
        """Retrieve a command by its name and streamer."""
        return cls.get_or_none((cls.command == command) & (cls.streamer_name == streamer_name))

    def update_command(self, command: str, streamer_name: str, response: str = None,
                       is_active: bool = None):
        """Update an existing command's response or active status."""

        if response is not None:
            self.response = response
        if is_active is not None:
            self.is_active = is_active

        self.save()


class BaseHandler:

    def event_parser(self, event):
        badges = {b.set_id for b in event.event.badges}

        is_mod = 'moderator' in badges
        is_vip = 'vip' in badges
        is_sub = 'subscriber' in badges

        msg = event.event.message.text
        username = event.event.chatter_user_name
        user_id = event.event.chatter_user_id

        broadcaster_id = event.event.broadcaster_user_id

        return username, user_id, broadcaster_id, msg, is_mod, is_vip, is_sub

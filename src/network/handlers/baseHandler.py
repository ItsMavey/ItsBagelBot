

class BaseHandler:
    async def dispatch(self, event):
        raise NotImplementedError("Subclasses must implement this method")

    def event_parser(self, event):
        raise NotImplementedError("Subclasses must implement this method")

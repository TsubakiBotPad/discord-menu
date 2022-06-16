class MissingImsMenuType(Exception):
    pass


class InvalidImsMenuType(Exception):
    pass


class CogNotLoaded(Exception):
    pass


class DiscordRatelimitFilter(logging.Filter):
    def filter(self, record):
        # Message emitted by discord/http.py:
        return not record.getMessage().startswith('We are being rate limited.')


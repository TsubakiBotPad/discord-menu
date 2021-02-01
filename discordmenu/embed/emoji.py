class EmbedMenuEmojiConfig:
    def __init__(self, delete_message="❌"):
        self.delete_message = delete_message

    def to_list(self):
        return [self.delete_message]


DEFAULT_EMBED_MENU_EMOJI_CONFIG = EmbedMenuEmojiConfig()

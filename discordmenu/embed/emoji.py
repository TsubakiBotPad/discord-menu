class EmbedMenuEmojiConfig:
    def __init__(self, delete_message="❌", unsupported_action="🚫"):
        self.delete_message = delete_message
        self.unsupported_action = unsupported_action

    def to_list(self):
        return [self.delete_message, self.unsupported_action]


DEFAULT_EMBED_MENU_EMOJI_CONFIG = EmbedMenuEmojiConfig()

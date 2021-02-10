class EmbedMenuEmojiConfig:
    def __init__(self, delete_message="❌", unsupported_transition="🚫"):
        self.delete_message = delete_message
        self.unsupported_transition = unsupported_transition

    def to_list(self):
        return [self.delete_message, self.unsupported_transition]


DEFAULT_EMBED_MENU_EMOJI_CONFIG = EmbedMenuEmojiConfig()

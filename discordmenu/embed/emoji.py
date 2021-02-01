class EmbedMenuEmojiConfig:
    def __init__(self, yes="✅", no="❌", next="➡", prev="⬅"):
        self.yes = yes
        self.no = no
        self.next = next
        self.prev = prev

    def to_list(self):
        return [self.yes, self.no, self.next, self.prev]


DEFAULT_EMBED_MENU_EMOJI_CONFIG = EmbedMenuEmojiConfig()

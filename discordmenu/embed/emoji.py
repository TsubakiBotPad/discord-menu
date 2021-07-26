from typing import List


class EmbedMenuEmojiConfig:
    def __init__(self, delete_message: str = "\N{CROSS MARK}",
                 unsupported_transition: str = "\N{NO ENTRY SIGN}"):
        self.delete_message = delete_message
        self.unsupported_transition = unsupported_transition

    def to_list(self) -> List[str]:
        return [self.delete_message, self.unsupported_transition]


DEFAULT_EMBED_MENU_EMOJI_CONFIG = EmbedMenuEmojiConfig()

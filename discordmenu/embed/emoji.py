from typing import Sequence, Union

SingleEmojiRef = str

# this is used for emoji name fallbacks in case the bot cannot view a particular emoji
# e.g. not part of the requisite emoji server
MultiEmojiRef = Sequence[SingleEmojiRef]

EmojiRef = Union[SingleEmojiRef, MultiEmojiRef]

DELETE_MESSAGE_EMOJI = "\N{CROSS MARK}"
UNSUPPORTED_TRANSITION_EMOJI = "\N{NO ENTRY SIGN}"

DEFAULT_EMOJI_LIST = [DELETE_MESSAGE_EMOJI, UNSUPPORTED_TRANSITION_EMOJI]

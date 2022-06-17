import json
from collections.abc import Sequence
from typing import Callable, Optional, Coroutine, Any, List, Dict

from discord import Message

from discordmenu.embed.emoji import EmojiRef, DELETE_MESSAGE_EMOJI, UNSUPPORTED_TRANSITION_EMOJI
from discordmenu.embed.wrapper import EmbedWrapper
from discordmenu.intra_message_state import _IntraMessageState

TransitionEmbedFunc = Callable[[Optional[Message], _IntraMessageState, Any], Coroutine[None, None, EmbedWrapper]]


class EmbedTransition:
    def __init__(self, emoji_ref: EmojiRef, transition_func: Optional[TransitionEmbedFunc], **kwargs):
        self.emoji_ref = emoji_ref
        self.transition_func = transition_func
        self.kwargs = kwargs

    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return {
            'emoji_ref': self.emoji_ref,
            'transition': self.transition_func,
        }


class EmbedTransitions:
    def __init__(self, transitions: List[EmbedTransition] = None):
        self.transitions = transitions if transitions else []

    DATA: Dict[EmojiRef, EmbedTransition] = {}

    def __repr__(self):
        return json.dumps(self.DATA)

    @classmethod
    def emoji_names(cls) -> List[EmojiRef]:
        """Return all emoji names. If an emoji is specified as a tuple with fallback(s), returns a tuple."""
        return [k for k, v in cls.DATA.items()]

    @classmethod
    def all_emoji_names(cls) -> List[EmojiRef]:
        """
        Return all valid emoji names, including fallbacks.
        In particular, the length of the list returned by this method is not guaranteed to be
        the same as the length of the list returned by `emoji_names`, and so this should only
        be used for validity checking.
        """
        ret = []
        for k, v in cls.DATA.items():
            if isinstance(k, str):
                ret.append(k)
            elif isinstance(k, Sequence):
                # case when a fallback is provided
                ret += k
        return ret

    @classmethod
    def transitions(cls) -> Dict[EmojiRef, Optional[TransitionEmbedFunc]]:
        ret = {}
        for k, v in cls.DATA.items():
            if v.transition_func is None:
                continue
            if isinstance(k, str):
                ret[k] = v.transition_func
            elif isinstance(k, Sequence):
                # case when a fallback is provided
                ret.update({i: v.transition_func for i in k})
        return ret

    @classmethod
    def pane_types(cls):
        return {v.kwargs['pane_type']: v.transition_func for k, v in cls.DATA.items()}

    @classmethod
    def respond_to_emoji_with_parent(cls, emoji: str):
        """Only defined for menus that support children"""
        if cls.DATA.get(emoji) is None:
            return None
        return cls.DATA[emoji].transition_func is not None

    @classmethod
    def respond_to_emoji_with_child(cls, emoji: str):
        """Only defined for menus that support children"""
        if cls.DATA.get(emoji) is None:
            return None
        return cls.DATA[emoji].kwargs['child_func'] is not None

    @classmethod
    def get_child_data_func(cls, emoji: str):
        """Only defined for menus that support children"""
        if cls.DATA.get(emoji) is None:
            return None
        return cls.DATA[emoji].kwargs['child_func']


class EmbedMenuDefaultTransitions:
    def __init__(self, delete_message: EmbedTransition = None, unsupported_transition: EmbedTransition = None):
        self.delete_message = delete_message or EmbedTransition(DELETE_MESSAGE_EMOJI, None)
        self.unsupported_transition = unsupported_transition or EmbedTransition(UNSUPPORTED_TRANSITION_EMOJI, None)

    def emoji_refs(self) -> List[str]:
        return [self.delete_message.emoji_ref, self.unsupported_transition.emoji_ref]


DEFAULT_TRANSITIONS = EmbedMenuDefaultTransitions()

from discordmenu.embed.components import EmbedFooter
from discordmenu.embed.view_state import ViewState
from discordmenu.intra_message_state import IntraMessageState

DEFAULT_ICON_URL = 'https://discord.com/assets/f9bb9c4af2b9c32a2c5ee0014661546d.png'


def embed_footer_with_state(state: ViewState, *, image_url=None, text=None) -> EmbedFooter:
    image_url = image_url if image_url is not None else DEFAULT_ICON_URL
    text = text if text is not None else 'Click the reactions below to interact'

    url = IntraMessageState.serialize(image_url, state.serialize())
    return EmbedFooter(text, icon_url=url)

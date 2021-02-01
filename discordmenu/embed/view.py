from typing import List

from discord import Embed

from discordmenu.embed.components import EmbedMain, EmbedAuthor, EmbedFooter, EmbedThumbnail, EmbedBodyImage, \
    EmbedField

HIDDEN_CHAR = "\u200b"


def _get_field_name(field, first_chunk):
    return field.name.value if first_chunk else field.continuation_title or HIDDEN_CHAR


class EmbedView:
    def __init__(self,
                 embed_main: EmbedMain,
                 embed_author: EmbedAuthor = None,
                 embed_thumbnail: EmbedThumbnail = None,
                 embed_body_image: EmbedBodyImage = None,
                 embed_fields: List[EmbedField] = None,
                 embed_footer: EmbedFooter = None
                 ):
        self.embed_author = embed_author
        self.embed_body_image = embed_body_image
        self.embed_thumbnail = embed_thumbnail
        self.embed_main = embed_main
        self.embed_fields = [f for f in embed_fields if f] if embed_fields else []
        self.embed_footer = embed_footer

    def to_embed(self) -> Embed:
        embed = Embed(**self.embed_main)
        embed.set_thumbnail(**self.embed_thumbnail) if self.embed_thumbnail else None
        embed.set_image(**self.embed_body_image) if self.embed_body_image else None
        embed.set_author(**self.embed_author) if self.embed_author else None
        embed.set_footer(**self.embed_footer) if self.embed_footer else None

        for field in self._chunk_embed_fields(1024):
            embed.add_field(**field)

        return embed

    def _chunk_embed_fields(self, chunk_size):
        chunks = []
        for field in self.embed_fields:
            remaining = field.value.to_markdown()
            first_chunk = True
            while len(remaining) > 0:
                field_name = _get_field_name(field, first_chunk)
                if len(remaining) <= chunk_size:
                    chunks.append(EmbedField(field_name, remaining, field.inline))
                    break

                left = remaining[:chunk_size]
                right = remaining[chunk_size:]

                delimiter_index = left.rfind(field.chunk_delimiter)
                if delimiter_index == -1:
                    raise Exception("Could not chunk by delimiter")

                left_body = left[:delimiter_index]

                chunks.append(EmbedField(field_name, left_body, field.inline))
                if first_chunk:
                    first_chunk = False

                remaining = left[delimiter_index + 1:] + right
        return chunks

    @staticmethod
    def from_message(existing_embed: Embed) -> "EmbedView":
        main = EmbedMain(existing_embed.title, existing_embed.url, existing_embed.colour, existing_embed.description)

        e_author = existing_embed.author
        author = EmbedAuthor(e_author.name, e_author.url, e_author.icon_url)

        thumbnail = EmbedThumbnail(existing_embed.thumbnail.url)
        body_image = EmbedBodyImage(existing_embed.image.url)

        e_footer = existing_embed.footer
        footer = EmbedFooter(e_footer.text, e_footer.icon_url)

        fields = [EmbedField(e.name, e.value, e.inline) for e in existing_embed.fields]
        return EmbedView(main, author, thumbnail, body_image, fields, footer)

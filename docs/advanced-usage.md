# Advanced Usage

This doc is work in progress.

# High level

See test cases[link] for sample code. At a high level:

1. Define a view by subclassing `EmbedView`.
2. Encapsulate view state data that needs to be passed between views. See `ViewState`.
3. Tie it together with a Menu class that conforms to `PMenuable`
4. Register the menu with the bot's Menu Listener so that it can respond to emoji reactions.

# UI Components

## Box

## Text

## Emoji cache

If you have some custom emojis that your bot is allowed to use, a bad actor could theoretically upload a different emoji into another server that the bot is also in, with the same name, and trick the bot into printing the wrong emoji instead. To counteract this problem, you can specify a list of "allowed emoji servers," and the DiscordMenu emoji cache helps you do this.

# Building Complex Menus

## Menu Listener

#### Defining the menu map

### cross-cog

#### Setting default data (optional)

Optionally, you may want a function called `get_menu_default_data`. For example, in the [`padinfo` cog](https://github.com/TsubakiBotPad/pad-cogs/blob/master/padinfo/padinfo.py), this method is how we pass `DGCOG` to the menu:

```python
    async def get_menu_default_data(self, ims):
        data = {
            'dgcog': await self.get_dgcog(),
            'user_config': await BotConfig.get_user(self.config, ims['original_author_id'])
        }
        return data
```

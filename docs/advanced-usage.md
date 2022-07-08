# Advanced Usage

This doc is work in progress.

This doc walks through the individual components of discord-menu.

# High level

See test cases[link] for sample code. At a high level:

1. Define a view by subclassing `EmbedView`.
2. Encapsulate view state data that needs to be passed between views. See `ViewState`.
3. Tie it together with a Menu class that conforms to `PMenuable`
4. Register the menu with the bot's Menu Listener so that it can respond to emoji reactions.

# UI Components

## Box

The container for arrays of things. This is most similar to html `<div>`. The `inline` parameter controls how to display items in the box. `inline = false` is most similar to css `display: inline-block`, while `inline = true` is most similar to `display: flex`.

## Text

Simple text entry. Similar to html `<span>`.

### BoldText

Bold text entry. Similar to html `<b>`.

### LabeledText

A convenience class for "key-value pair" like data. Similar to `<b>{text1}</b> <span>{text2}</span>`

<img width="83" alt="image" src="https://user-images.githubusercontent.com/880610/176334774-b9104e59-8d0b-4c27-b774-6b48f004ae01.png">

### LinkedText

Text with a link. Similar to html `<a>`.

### InlineText

Markdown emphasis. e.g

`This is emphasized text.`

### BlockText

Markdown code blocks. e.g

```
This is block of text....
Is a code block.
```

### HighlightableLinks

Convenience class for a series of links where one of them is selected (unclickable).

<img width="224" alt="image" src="https://user-images.githubusercontent.com/880610/176334702-8988867d-c7c6-49bd-ba28-97f6d8cfd5e5.png">

## Emojis

### Loading Emojis

Bots have access to the emojis in all the servers (guilds) they reside in. `discord-menu` holds an `EmojiCache` and can load emojis from the servers they are in on start. You can set the server ids that you want to read from by calling `emoji_cache.set_guild_ids(...)`

### Managing a lot of emojis

Your server's emoji game may be really strong and you may exceed the maximum number of emojis for your server. One option around this limitiation is to create dedicated emoji servers and invite your bot to them. Be wary of name collisions, as different emojis with the same names across servers will interfere with each other. Use the singleton `emoji_cache` provided inside discord-menu `emoji_cache.set_guild_ids(...)` to tell your bot which servers to read emojis from.

# Building Complex Menus

The previous section on UI Components demonstrated how to generate an Embed for display. However, menu's are obviously most useful when they can change state as one interacts with it.

## Menu Listener

The most critical component of a menu is the `MenuListener`, which attaches itself to the `on_raw_reaction_add` and `on_raw_reaction_remove` Discord events. The menu listener handles receiving and filtering discord reaction events, then forwarding them to the appropriate menu.

There should only be one `MenuListener` per bot process. Upon construction, it takes a `MenuMap` containing `MenuMapEntries` which holds a menu type and its corresponding menu transitions.

```python
menu_map = MenuMap()
menu_map[SimpleTextMenu.MENU_TYPE] = MenuMapEntry(SimpleTextMenu, EmbedTransitions)
```

### Menus across multiple cogs

A bot may naturally have multiple cogs with menus. Because `MenuListener` (and likely `MenuMap`) are only defined once, it is recommended that you define these in a dedicated cog (e.g `menulistenercog`).

One can then utilize the reflective function `bot.get_cog(...)` to load and modify the `MenuMap` member on the dedicated cog as appropriate.

Perhaps an extension in the future could be to provide `menulistenercog` as part of `discord-menu`.

## Reaction Filters

The `MenuListener` recieves every single reaction event where the bot is in. A filtering mechanism discards irrelevant events such that the bot is not overwhelmed.

There are 3 default reaction filters that are attached to the `MenuListener`:

1. `ValidEmojiReactionFilter` - discards reactions that do not control the menu.
2. `NotPosterEmojiReactionFilter` - discards reactions events from the bot itself.
3. `BotAuthoredMessageReactionFilter` - discards reactions on messages that the bot didn't post.

Additional filters can be added by subclassing `MenuListener` and overriding the `get_additional_reaction_filters` method.

### Filter Interface

Subclass the `ReactionFilter` class in discord menu, and implement `_allow_reaction` and `_allow_reaction_raw`. Filters can be composed and mimic boolean AND and OR logic based on the following mechanisms:

1. `AND` - filter 1 and 2 are sequentially listed in the `get_additional_reaction_filters` list.
2. `OR` - filter 2 is nested on filter 1's constructor parameter named `reaction_filter`.

Nesting is only 1 deep at the moment, as more complicated filters were not concievable at the time of writing. Reach out to the developer team if one has a use case that isn't supported yet.

## Intra Message State

This is covered in the main [readme](https://github.com/TsubakiBotPad/discord-menu#intra-message-state), and is a key concept in building advanced menus.

# Advanced Menu Ideas

Some examples of things you could build using discord-menu:

1. Simple Poll/Votes
2. Access Control on Menus
3. Image Slideshow
4. User Profile Viewer
5. Moderation Tools

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

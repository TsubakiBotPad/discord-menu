# Advanced Usage

This doc walks through the individual components of discord-menu.

## Components of a Menu

<img width="481" alt="image" src="https://user-images.githubusercontent.com/880610/178141551-96480e14-4346-4335-81fe-6489704d2211.png">

Menus are easiest understood through the lens of the underlying ViewState (a.k.a ViewModel in [MVVM architecture](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel)). Views are a constructed from combination of a declarative template (i.e HTML DOM) and dynamic data from the ViewState.

EmbedTranstions are code that determintes how ViewStates transform based on external input (e.g emoji clicked). As the ViewState change, in turn so does the visualization (View) associated with it.

1. [**EmbedViewState**](https://github.com/TsubakiBotPad/discord-menu/blob/main/discordmenu/embed/view_state.py#L4) - This is the set of data that can be modified by external inputs (e.g user clicks). The state can be used to display dynamic information on the View (e.g page number).

1. [**EmbedView**](https://github.com/TsubakiBotPad/discord-menu/blob/main/discordmenu/embed/view.py#L15) - This is the code for what is displayed on the user's screen in Discord. It takes input from the ViewState and transforms it into UI elements.

1. [**EmbedTransition**](https://github.com/TsubakiBotPad/discord-menu/blob/main/discordmenu/embed/transitions.py#L14) - Transitions are code that is run in order to convert the current ViewState to the next ViewState. Often this means recomputing a new ViewState entirely to show different data. In more complex cases, data can be carried over from the previous state in order to influence what to display next (e.g query params, page history)

1. [**EmbedMenu**](https://github.com/TsubakiBotPad/discord-menu/blob/main/discordmenu/embed/menu.py#L19) - Finally, the Menu is conceptually a container for all of the components described above. It is what a user sees and interacts with on Discord.

## Intra message state

`discord-menu` does not require sessions, which allows the service it runs on to be stateless (note: this is different from the menu being unable to record state - see below). If the bot turns off and on again, previous menus that were instantiated by the bot will still be able to function when the bot returns and responds to the user request. `discord-menu` stores menu state within Discord Embed images in locations that generally do not interfere with the user experience. **Intra Message State is the data that is needed to reconstruct the menu from scratch.**

Due to this, **all Menus that require state also need to contain a Discord Embed image**. This will be the case for most menus, short of simple displays that are never edited (a "menu" with no controls).

These images can either be in the Embed `author`, `image`, `thumbnail`, or `footer`. By default, we recommend using the Embed footer as the UI element is most pleasant and unintrusive.

In practice, Intra Message State is saved by subclassing `ViewState` and attaching it on `Menu.create(...)` or within an `EmbedTransition` function as part of the main API flow.

## Menu lifecycle

<img width="744" alt="image" src="https://user-images.githubusercontent.com/880610/178141592-9dcc07ff-4a20-4348-8dc8-800ad53f368b.png">

Menus in this library are called upon in two separate contexts - on menu creation and on discord reaction. These two contexts do not share any process state, which allows the system to be independent and scalable.

In the creation case, a user defined `EmbedMenu` and seed `ViewState` is created from user input, and is translated by `discord-menu` into an `EmbedWrapper` that is sent to Discord. Discord servers receive the request and displays the menu message to the end user in the Discord app.

Sometime later, a user may click a reaction on the menu, which triggers the `on_reaction_add` code path in the bot. `discord-menu` extracts the `ViewState` from the event, and executes user defined code in `EmbedTransition` which produces the next `EmbedWrapper` to be sent to discord.

In both cases above, the `EmbedWrapper` is independently derived from the underlying `EmbedViewState`. As long as the user defined `EmbedMenu` and its corresponding code is independently loadable in the two code paths, the system's main limitation is the data storage size of an `EmbedViewState`, which is unlikely to be an issue.

# High level implementation

See test cases[link] for sample code. At a high level:

1. Define a view by subclassing `EmbedView`.
2. Encapsulate view state data that needs to be passed between views. See `ViewState`.
3. Tie it together with a Menu class that conforms to `PMenuable`
4. Register the menu with the bot's Menu Listener so that it can respond to emoji reactions.

# UI components

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

### Loading emojis

Bots have access to the emojis in all the servers (guilds) they reside in. `discord-menu` holds an `EmojiCache` and can load emojis from the servers they are in on start. You can set the server ids that you want to read from by calling `emoji_cache.set_guild_ids(...)`

### Managing a lot of emojis

Your server's emoji game may be really strong and you may exceed the maximum number of emojis for your server. One option around this limitiation is to create dedicated emoji servers and invite your bot to them. Be wary of name collisions, as different emojis with the same names across servers will interfere with each other. Use the singleton `emoji_cache` provided inside discord-menu `emoji_cache.set_guild_ids(...)` to tell your bot which servers to read emojis from.

# Building complex menus

The previous section on UI Components demonstrated how to generate an Embed for display. However, menu's are obviously most useful when they can change state as one interacts with it.

## Menu listener

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

## Reaction filters

The `MenuListener` recieves every single reaction event where the bot is in. A filtering mechanism discards irrelevant events such that the bot is not overwhelmed.

There are 3 default reaction filters that are attached to the `MenuListener`:

1. `ValidEmojiReactionFilter` - discards reactions that do not control the menu.
2. `NotPosterEmojiReactionFilter` - discards reactions events from the bot itself.
3. `BotAuthoredMessageReactionFilter` - discards reactions on messages that the bot didn't post.

Additional filters can be added by subclassing `MenuListener` and overriding the `get_additional_reaction_filters` method.

### Filter interface

Subclass the `ReactionFilter` class in discord menu, and implement `_allow_reaction` and `_allow_reaction_raw`. Filters can be composed and mimic boolean AND and OR logic based on the following mechanisms:

1. `AND` - filter 1 and 2 are sequentially listed in the `get_additional_reaction_filters` list.
2. `OR` - filter 2 is nested on filter 1's constructor parameter named `reaction_filter`.

Nesting is only 1 deep at the moment, as more complicated filters were not concievable at the time of writing. Reach out to the developer team if one has a use case that isn't supported yet.

# Advanced menu ideas

Some examples of things you could build using discord-menu:

1. Simple poll / voting
1. Access control on menus
1. Child menus (controls on one message affect another message)
1. Image slideshow
1. User profile viewer
1. Moderation tools

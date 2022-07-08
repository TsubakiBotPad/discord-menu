# What is discord-menu?

discord-menu is a flexible python framework for creating interactive menus out of Discord Embeds. Users can click specified emojis and the embed responds according to preset instructions.

Its primary features are:

1. **Declaritive UI Syntax** - React/SwiftUI like definition of Views.
1. **Stateless compute** - Through the use of IntraMessageState, menus do not require maintaining a session. through use of an _intra-message state_, or "IMS," no data needs to be stored on the bot's server, allowing emojis never to expire (potentially dependent on which type of listener you are).
1. **Event driven** - No polling needed and interactions respond immediately to input.
1. **Scalable state** - Message state is managed directly in the Embed, leveraging Discord's capabilities.
1. **Flexibility** - Arbitrary code can be executed upon emoji clicks, allowing for complex features like pagination, dependent menus, or user authorizaton!

# Installation

Install via pip:

`pip install discord-menu`

# How to use

Example code demonstrated with Red-DiscordBot. Raw discord.py should also work with slight modification of imports.

## Simple Text Menu

```python
import discord
from redbot.core import commands

from discordmenu.menu.listener.menu_listener import MenuListener
from discordmenu.menu.listener.menu_map import MenuMap, MenuMapEntry
from discordmenu.menu.simple_text_menu import SimpleTextMenu, SimpleTextViewState

menu_map = MenuMap()
menu_map[SimpleTextMenu.MENU_TYPE] = MenuMapEntry(SimpleTextMenu, EmbedTransitions)

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.listener = MenuListener(bot, menu_map)

    @commands.Cog.listener('on_raw_reaction_add')
    @commands.Cog.listener('on_raw_reaction_remove')
    async def on_raw_reaction_update(self, payload: discord.RawReactionActionEvent):
        await self.listener.on_raw_reaction_update(payload)

    async def simplemenu(self, ctx):
        await SimpleTextMenu.menu().create(ctx, SimpleTextViewState("Hello World!"))
```

![simpletext](https://user-images.githubusercontent.com/880610/174766480-950266a4-1967-47fb-ae9c-7a8a1cea449f.gif)

[Code](https://github.com/TsubakiBotPad/discord-menu/blob/main/test/testcog/main.py#L38)

## Simple Tabbed Text Menu

```python
import discord
from redbot.core import commands

from discordmenu.menu.listener.menu_listener import MenuListener
from discordmenu.menu.listener.menu_map import MenuMap, MenuMapEntry
from discordmenu.menu.simple_tabbed_text_menu import SimpleTabbedTextMenu, SimpleTabbedTextMenuTransitions,
    SimpleTabbedTextViewState

menu_map = MenuMap()
menu_map[SimpleTabbedTextMenu.MENU_TYPE] = MenuMapEntry(SimpleTabbedTextMenu, SimpleTabbedTextMenuTransitions)


class TestCog(commands.Cog):
    def __init__(self, bot):
        self.listener = MenuListener(bot, menu_map)

    @commands.Cog.listener('on_raw_reaction_add')
    @commands.Cog.listener('on_raw_reaction_remove')
    async def on_raw_reaction_update(self, payload: discord.RawReactionActionEvent):
        await self.listener.on_raw_reaction_update(payload)

    async def simpletabbedtextmenu(self, ctx):
        vs = SimpleTabbedTextViewState("Initial message.", ["Message 1", "Message 2", "Message 3"])
        await SimpleTabbedTextMenu.menu().create(ctx, vs)
```

![simpletabbedtext](https://user-images.githubusercontent.com/880610/174983540-2a8a5864-9be6-4c28-9727-56a50f779118.gif)

[Code](https://github.com/TsubakiBotPad/discord-menu/blob/main/test/testcog/main.py#L43)

## Scrollable Menu

TODO

## Advanced Usage

If you're looking for ideas on what you can do with this framework, or for info on how to create complex menus, refer to [documentation](https://github.com/TsubakiBotPad/discord-menu/blob/main/docs/advanced-usage.md) on advanced usage.

# Supported Convenience Menus

1. **SimpleTextMenu** - Use this if you just want to display some text.
1. **SimpleTabbedTextMenu** - This is useful if you a few different panes of text content that a user would select between.
1. **ClosableMenus** - If you want a simple view with just a basic close button.

# Key Concepts

## Components of a Menu

<img width="515" alt="image" src="https://user-images.githubusercontent.com/880610/175546502-eb294f6e-8073-4b6f-9f43-1d9d0fbb4590.png">

Menus are easiest understood through the lens of the underlying ViewState (a.k.a ViewModel in MVVM architecture). Views are a constructed from combination of a declarative template (i.e HTML DOM) and dynamic data from the ViewState.

EmbedTranstions are code that determintes how ViewStates transform based on external input (e.g emoji clicked). As the ViewState change, in turn so does the visualization (View) associated with it.

1. **EmbedViewState** - This is the set of data that can be modified by external inputs (e.g user clicks). The state can be used to display dynamic information on the View (e.g page number).

1. **EmbedView** - This is the code for what is displayed on the user's screen in Discord. It takes input from the ViewState and transforms it into UI elements.

1. **EmbedTransitions** - Transitions are code that is run in order to convert the current ViewState to the next ViewState. Often times, this means recomputing a new ViewState entirely to show different data. In more complex cases, data can be carried over from the previous state in order to influence what to display next (e.g query params, page history)

1. **EmbedMenu** - Finally, the Menu is conceptually a container for all of the subcomponents described above. It is what a user sees and interacts with on Discord.

## Intra Message State

`discord-menu` does not require sessions, which allows the service it runs on to be stateless. If the bot turns off and on again, previous menus that were instantiated by the bot will still be able to function when the bot returns and responds to the user request. `discord-menu` stores menu state within Discord Embed images in locations that generally do not interfere with the user experience. **Intra Message State is the data that is needed to reconstruct the menu from scratch.**

Due to this, **all Menus that require state also need to contain a Discord Embed image**. This will be the case for most menus, short of simple displays that are never edited (a "menu" with no controls).

These images can either be in the Embed `author`, `image`, `thumbnail`, or `footer`. By default, we recommend using the Embed footer as the UI element is most pleasant and unintrusive.

In practice, Intra Message State is saved by subclassing `ViewState` and attaching it on `Menu.create(...)` or within an `EmbedTransition` function as part of the main API flow.

## Menu Lifecycle

<img width="771" alt="image" src="https://user-images.githubusercontent.com/880610/175549719-85ae276e-a04d-4aa4-be85-354de12383e7.png">

Menus in this library are called upon in two separate contexts - on menu creation and on discord reaction. These two contexts do not share any process state, which allows the system to be independent and scalable.

In the creation case, a user defined `EmbedMenu` and seed `ViewState` is created from user input, and is translated by `discord-menu` into an `EmbedWrapper` that is sent to Discord. Discord servers receive the request and displays the menu message to the end user in the Discord app.

Sometime later, a user may click a reaction on the menu, which triggers the `on_reaction_add` code path in the bot. `discord-menu` extracts the `ViewState` from the event, and executes user defined code in `EmbedTransition` which produces the next `EmbedWrapper` to be sent to discord.

In both cases above, the `EmbedWrapper` are independently derived from the underlying `EmbedViewState`. As long as the user defined `EmbedMenu` and its corresponding code is independently loadable in the two code paths, the system's main limitation is the data storage size of an `EmbedViewState`, which is unlikely to be an issue.

# Running Tests + Sample Code

## Prerequisite: Create a Discord Bot

If you don't have one already, follow the instructions to create a bot in Red's official documentation:

[Creating a bot account](https://docs.discord.red/en/stable/bot_application_guide.html#creating-a-bot-account)

Keep the bot `token` that you get from Discord at the end of the instructions handy - you will need it to set up the bot later.

## Installation

1. Create a python 3 venv in the `test` folder. `virtualenv -p python3 <envname>`
1. Activate the venv.
1. `pip install -r requirements.txt`

The above steps install Red-Discord bot framework. You can now follow more detailed [instructions](https://docs.discord.red/en/stable/install_guides/mac.html#setting-up-and-running-red) to startup the bot. Or run these in command line and follow the prompts:

- `redbot-setup`
- `redbot <bot_name>`

## Interact with the bot

The rest of the guide takes place from inside Discord. Replace `^` with your prefix to talk to your bot.

1. Once the bot is launched, set it to the `test` directory as a cog path.

```
^addpath /Users/me/src/discord-menu/test
```

1. Load `testcog`

```
^reload testcog
```

1. Run a test command. Test [code](https://github.com/TsubakiBotPad/discord-menu/blob/main/test/testcog/main.py#L37) for simplemenu.

```
^t
```

![simpletext](https://user-images.githubusercontent.com/880610/174766480-950266a4-1967-47fb-ae9c-7a8a1cea449f.gif)

# Contributing

If you encounter a bug or would like to make a feature request, please file a Github issue or submit a pull request.

Also, if you don't understand something in the documentation, you are experiencing problems, or you just need a gentle nudge in the right direction, please don't hesitate to join the [discord server](https://discord.gg/QCRxNtC).

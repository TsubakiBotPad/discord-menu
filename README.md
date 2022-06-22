# What is discord-menu?

discord-menu is a flexible python framework for creating interactive menus out of Discord Embeds. Users can click specified emojis and the embed responds according to preset instructions.

Its primary features are:

1. **Declaritive UI Syntax** - React/SwiftUI like definition of Views.
1. **Stateless compute** - Through the use of IntraMessageState, menus do not require maintaining a session. through use of an _intra-message state_, or "IMS," no data needs to be stored on the bot's server, allowing emojis never to expire (potentially dependent on which type of listener you are).
1. **Event driven** - No polling needed and interactions respond immediately to input.
1. **Scalable state** - Message state is managed directly in the Embed, leveraging Discord's capabilities.
1. **Flexibility** - Arbitrary code can be executed upon emoji clicks, allowing for complex features like pagination, dependent menus, or user authorizaton!

Insert GIF examples here:
[example1][example2][example3]

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

## Simple Tabbed Menu

```python
import discord
from redbot.core import commands

from discordmenu.menu.listener.menu_listener import MenuListener
from discordmenu.menu.listener.menu_map import MenuMap, MenuMapEntry
from discordmenu.menu.simple_tabbed_menu import SimpleTabbedMenu, SimpleTabbedMenuTransitions, SimpleTabbedViewState

menu_map = MenuMap()
menu_map[SimpleTabbedMenu.MENU_TYPE] = MenuMapEntry(SimpleTabbedMenu, SimpleTabbedMenuTransitions)

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.listener = MenuListener(bot, menu_map)

    @commands.Cog.listener('on_raw_reaction_add')
    @commands.Cog.listener('on_raw_reaction_remove')
    async def on_raw_reaction_update(self, payload: discord.RawReactionActionEvent):
        await self.listener.on_raw_reaction_update(payload)

    async def simpletabbedmenu(self, ctx):
        vs = SimpleTabbedViewState("Initial message.", ["Message 1", "Message 2", "Message 3"])
        await SimpleTabbedMenu.menu().create(ctx, vs)
```

![simpletabbed](https://user-images.githubusercontent.com/880610/174983540-2a8a5864-9be6-4c28-9727-56a50f779118.gif)

[Code](https://github.com/TsubakiBotPad/discord-menu/blob/main/test/testcog/main.py#L43)

## Scrollable Menu

TODO

## Advanced Usage

For info on how to create complex menus, refer to [documentation](https://github.com/TsubakiBotPad/discord-menu/blob/main/docs/advanced-usage.md) on advanced usage.

# Supported Convenience Menus

1. **SimpleTextMenu** - Use this if you just want to display some text.
1. **SimpleTabbedMenu** - This is useful if you a few different panes of content that a user would select between.
1. **ClosableMenus** - If you want a simple view with just a basic close button.

# Key Concepts

<img width="903" alt="image" src="https://user-images.githubusercontent.com/880610/174849081-1b07af86-f3cf-442d-8446-0ef552e8c89a.png" />

Menus are easiest understood through the lens of the underlying ViewState (a.k.a ViewModel in MVVM architecture). Views are a constructed from combination of a declarative template (i.e HTML DOM) and dynamic data from the ViewState.

EmbedTranstions are code that determintes how ViewStates transform based on external input (e.g emoji clicked). As the ViewState change, in turn so does the visualization (View) associated with it.

## Components

1. **EmbedViewState** - This is the set of data that can be modified by external inputs (e.g user clicks). The state can be used to display dynamic information on the View (e.g page number).

1. **EmbedView** - This is the code for what is displayed on the user's screen in Discord. It takes input from the ViewState and transforms it into UI elements.

1. **EmbedTransitions** - Transitions are code that is run in order to convert the current ViewState to the next ViewState. Often times, this means recomputing a new ViewState entirely to show different data. In more complex cases, data can be carried over from the previous state in order to influence what to display next (e.g query params, page history)

1. **EmbedMenu** - Finally, the Menu is conceptually a container for all of the subcomponents described above. It is what a user sees and interacts with on Discord.

## Intra Message State (IMS)

`discord-menu` does not require sessions, which allows the service it runs on to be stateless. If the bot turns off and on again, previous menus that were instantiated by the bot will still be able to function when the bot returns and responds to the user request. `discord-menu` stores menu state within Discord Embed images in locations that generally do not interfere with the user experience.

Due to this, **all Menus that require state also need to contain a Discord Embed image**.

These images can either be in the Embed `author`, `image`, `thumbnail`, or `footer`. By default, we recommend using the Embed footer as the UI element is most pleasant and unintrusive.

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

## Features of DiscordMenu

In addition to the ability to make menus for you, there are some additional specific features of DiscordMenu that you should know about:

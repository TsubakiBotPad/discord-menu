## What is DiscordMenu?
DiscordMenu is a loose framework for creating menus out of Discord embeds where the user can click specified emojis and the embed responds according to preset instructions. Its primary advantages over other menu libraries are:

1. **Statelessness** - through use of an *intra-message state*, or "IMS," no data needs to be stored on the bot's server, allowing emojis never to expire (potentially dependent on which type of listener you are.
2. **Flexibility** - arbitrary code can be executed upon emoji clicks, allowing for features like child menus, "menu friends," and more!

## What is an IMS?

The IMS is physically stored in a small icon in the footer of your menu next to the text, "Requester may click the reactions below to switch tabs," as a serialized json. It contains whatever data you decide to store to it, which should minimally include:

* The ID of the author of the initial command, so that the bot can respond only to reactions belonging to the right person or people
* A string representation of the menu type, to be fed to your `menu_map` (see "Parts of a menu" below)
* The current reaction list, so that you don't remove any reactions when updating the menu

Once a reaction is clicked and registered by the listener, the listener will first check if there is a valid IMS attached to the message. If not, it immediately returns. If there is one, it then checks for a valid `menu_type`. Only if there is a valid `menu_type` will it proceed to process the message. For more information, see "Control flow" below.

## Features of DiscordMenu
In addition to the ability to make menus for you, there are some additional specific features of DisordMenu that you should know about:

### Emoji cache
If you have some custom emojis that your bot is allowed to use, a bad actor could theoretically upload a different emoji into another server that the bot is also in, with the same name, and trick the bot into printing the wrong emoji instead. To counteract this problem, you can specify a list of "allowed emoji servers," and the DiscordMenu emoji cache helps you do this.

## Parts of a menu
### Defined once per bot
You will need a listener - either `on_reaction_add` or `on_raw_reaction_add`, this is how the bot actually listens to reactions. For an example listener, see the [MenuListener cog](https://github.com/TsubakiBotPad/misc-cogs/tree/master/menulistener) used by Tsubaki Bot. This cog supports multi-level menus; however, the lower level(s) of menus must all be `IdMenu` types currently.

### Defined once per cog
* You will need a `menu_map` file that maps strings to menu classes & panes classes. For example, see [menu_map.py](https://github.com/TsubakiBotPad/pad-cogs/blob/master/padinfo/menu/menu_map.py) in the `padinfo` cog in Tsubaki bot.
* You will also need to register your cog to the listener. How you do this may vary depending on your bot framework, but for example, in [`padinfo/__init__.py`](https://github.com/TsubakiBotPad/pad-cogs/blob/master/padinfo/__init__.py) we run:

```python
    bot.loop.create_task(n.register_menu())
```

The method `register_menu()` is defined in [`padinfo.py`](https://github.com/TsubakiBotPad/pad-cogs/blob/master/padinfo/padinfo.py) as:

```python
async def register_menu(self):
    await self.bot.wait_until_ready()
    menulistener = self.bot.get_cog("MenuListener")
    if menulistener is None:
        logger.warning("MenuListener is not loaded.")
        return
    await menulistener.register(self)
```

The `menu_map` is also imported and set as a class constant at the top of the cog:

```python
class PadInfo(commands.Cog):
    """Info for PAD Cards"""

    menu_map = padinfo_menu_map
```

### Defined once per menu
You will need, in a `menu` file containing:
* A Menu class, consisting of:
    * A `menu` method
    * One or more `respond_with` methods
    * One or more `control` methods
* A `Panes` class, which maps possible emojis to their `respond_with` methods and `View` types as well as, optionally, child menu view types
* Optionally, an `EmojiClass` that provides simple text names for emojis; this just makes defining the `Panes` class easier

As an example, we can look at the [`simple_text` menu](https://github.com/TsubakiBotPad/pad-cogs/blob/master/padinfo/menu/simple_text.py) used by Tsubaki Bot. It has two `respond_with` messages: one to print the message, and one to delete. Its only control prints the message.

> Why is there a custom `respond_with_delete` method, instead of using the built-in delete handler?

An excellent question! The answer is: because `SimpleTextMenu` is the placeholder used when a child menu hasn't been populated yet! It's convenient to have this custom delete message for that reason; don't let its presence distract you from its ability to serve as an otherwise-straightforward example.

You will also need a `view` file, containing:
* A `ViewState` class, which determines how to serialize and deserialize the IMS.
* A `View` class, which is the definition of the embed 

As an example, we can look at the [`simple_text` view](https://github.com/TsubakiBotPad/pad-cogs/blob/master/padinfo/view/simple_text.py) used by Tsubaki Bot. It only has two non-default properties: color and message contents. Note that creation of a base class like we did in the padinfo cog is OPTIONAL. If you are only creating one menu in your cog, there is no need to make a `ViewStateBase` class.

Finally, in the main cog file, you will need to write some command that creates a menu. We can no longer use `simple_text` as our example because this menu is not created directly through a command, so we will use `LeaderSkillSingle` instead, another relatively simple menu. The following command instantiates a `LeaderSkillSingleMenu`:

```python
        # code to assign a value to monster
        color = await self.get_user_embed_color(ctx)
        original_author_id = ctx.message.author.id
        state = LeaderSkillSingleViewState(original_author_id, LeaderSkillSingleMenu.MENU_TYPE, query, color, monster)
        menu = LeaderSkillSingleMenu.menu()
        await menu.create(ctx, state)
```

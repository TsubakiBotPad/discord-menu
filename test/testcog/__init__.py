from .main import TestCog


def setup(bot):
    n = TestCog(bot)
    bot.add_cog(n)

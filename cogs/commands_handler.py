"Handles Bot Commands"

import random
from discord.ext import commands
from utilities import get_voice_channels, get_voice_users


class CommandsHandler(commands.Cog):
    "Handles Bot Commands"

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def shuffle(self, ctx):
        'Shuffles voice users between voice channels'

        # Props
        author = ctx.message.author
        user_guild = author.guild.id
        voice_channels = get_voice_channels(self.bot, user_guild)
        voice_users = get_voice_users(self.bot, user_guild)

        # Response
        print(f'User {author} is shuffling voice members.')
        await ctx.send('Shuffling voice users.')
        for user in voice_users:
            rnd_channel = random.choice(voice_channels)
            await user.move_to(rnd_channel)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def merge(self, ctx):
        'Merges every voice channel user into the author channel'

        # Props
        author = ctx.message.author
        author_channel = author.voice.channel
        user_guild = author.guild.id
        voice_users = get_voice_users(self.bot, user_guild)

        # Response
        print(f'User {author} is merging voice members.')
        await ctx.send('Merging voice users.')
        for user in voice_users:
            await user.move_to(author_channel)

    @merge.error
    @shuffle.error
    async def general_guild_only_error(self, ctx, error):
        "Guild Only Errors"

        # Props
        author = ctx.message.author

        # No DMs
        if isinstance(error, commands.NoPrivateMessage):
            print(f'User {author} has no permissions to shuffle voice users.')
            await ctx.send('This command doesn\' work from DMs.')
            return

        # Check permission
        if isinstance(error, commands.MissingPermissions):
            print(
                f'User {author} has no permissions to run {ctx.message.content}.')
            await ctx.send('You\'re not allowed to do that. Nice try.')


def setup(bot):
    "Loads Bot Cog"
    bot.add_cog(CommandsHandler(bot))

import discord
from discord.ext import commands
import collections

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx):
        user = ctx.author

        embed=discord.Embed(title="USER INFO", description=f"Here is the info we retrieved about {user}", colour=user.colour)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="NAME", value=user.name, inline=True)
        embed.add_field(name="NICKNAME", value=user.nick, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="STATUS", value=user.status, inline=True)
        embed.add_field(name="TOP ROLE", value=user.top_role.name, inline=True)
        await ctx.send(embed=embed)

    @commands.command(description="Gets the bot's latency.")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000, 1)
        await ctx.send(f"Pong! {latency}ms")
    
    @commands.command(aliases=['av'])
    @commands.guild_only()
    async def avatar(self, ctx,*, user: discord.Member=None):
        # user as the mention
        if not user:
            user = ctx.author
            # self-explainatory
        embed = discord.Embed( title=f"{user.name}'s avatar")
        embed.description = f'[PNG]({user.avatar_url_as(format="png")}) | [JPEG]({user.avatar_url_as(format="jpeg")}) | [WEBP]({user.avatar_url_as(format="webp")})'
        embed.set_image(url=str(user.avatar_url_as(format='png')))
        embed.set_footer(text=f'Requested by {ctx.author.name}')
        # Nitro users :Eyes:
        if user.is_avatar_animated():
            embed.description += f' | [GIF]({user.avatar_url_as(format="gif")})'
            embed.set_image(url=str(user.avatar_url_as(format='gif')))

        return await ctx.send(embed=embed)

    @commands.command(aliases=['si'], description='To get the server information.')
    @commands.guild_only()
    # a cool server info command gets most of the basic things you would need to know about a server :)
    async def serverinfo(self, ctx):

        guild= ctx.guild
        emojis = str(len(guild.emojis))

        channels = str(len(guild.channels))
        roles= str(len(guild.roles))
        time= ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p ")
        voice= str(len(guild.voice_channels))
        text= str(len(guild.text_channels))
        statuses = collections.Counter([member.status for member in guild.members])

        online = statuses[discord.Status.online]
        idel = statuses[discord.Status.idle]
        dnd = statuses[discord.Status.dnd]
        offline= statuses[discord.Status.offline]

        embed= discord.Embed(
                                timestamp= ctx.message.created_at)

        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=f"Information for  {ctx.guild.name}")
        embed.add_field(name="__General information__\n", value= f'**Server name : ** {guild.name}\n'
                                                               f'**Server region : ** {guild.region}\n'
                                                               f'**Server ID : ** {guild.id}\n'
                                                               f'**Created at : ** {time}\n'
                                                               f'**Verification level : ** {guild.verification_level} \n'
                                                               f'**Server owner : ** yersinia_pestis#8058 and watermelon#1715 \n'
                                                               f'**Server bots : mesthoop, zeke** ', inline=False)


        embed.add_field(name="\n\n\n__Statistics__", value= f'**Member count : ** {ctx.guild.member_count}\n'
                                                 f'**Role count : ** {roles} \n'
                                                 f'**Channel count : ** {channels}\n'
                                                 f'**Text channels :** {text}\n'
                                                 f'**Voice channels :** {voice}\n'
                                                 f'**Emoji count : ** {emojis}\n'
                                                 f'**Server boosts : ** {guild.premium_subscription_count}\n')

        embed.add_field(name="__Activity__", value= f'<:online:769826555073003521>{online}\n'
                                                    f'<:idle:769826555479588864>{idel}\n'
                                                    f'<:dnd:769826555865989153>{dnd}\n'
                                                    f'<:offline:769826555643691041>{offline}')


        embed.set_footer(text=f"Requested by {ctx.author}",  icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Info Cog Ready')


def setup(bot):
    bot.add_cog(Info(bot))
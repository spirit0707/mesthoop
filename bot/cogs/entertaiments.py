import discord
from discord.ext import commands
import random
import asyncio
from random import choice
import json
import aiohttp
from datetime import datetime
import html
from discord.ext.commands.cooldowns import BucketType
with open('data/config.json') as f:
	CONFIG = json.load(f)


CLIENT_SESSION = aiohttp.ClientSession()
COLOR_RED = 0xEF2928
COLOR_BLUE = 0x0094E6

def parse_list_file(file_path: str) -> list:
	"""Parse a text file into a list containing each line."""
	
	with open(file_path) as f:
		return [l.strip() for l in f.readlines() if l.strip()]

database = {
	"truths": parse_list_file('data/truths.txt'),
	"dares": parse_list_file('data/dares.txt'),
	"nhie": parse_list_file('data/nhie.txt'),
	"tot": parse_list_file('data/tot.txt')
}


class Entertaiments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
      msg = message.content.lower()

    @commands.command(name="rps")
    async def rock_paper_scissors(self, context):
        choices = {
            0: "rock",
            1: "paper",
            2: "scissors"
        }
        reactions = {
            "🪨": 0,
            "🧻": 1,
            "✂": 2
        }
        embed = discord.Embed(title="Please choose", color=0xF59E42)
        embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
        choose_message = await context.send(embed=embed)
        for emoji in reactions:
            await choose_message.add_reaction(emoji)

        def check(reaction, user):
            return user == context.message.author and str(reaction) in reactions

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=check)

            user_choice_emote = reaction.emoji
            user_choice_index = reactions[user_choice_emote]

            bot_choice_emote = random.choice(list(reactions.keys()))
            bot_choice_index = reactions[bot_choice_emote]

            result_embed = discord.Embed(color=0x42F56C)
            result_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.clear_reactions()

            if user_choice_index == bot_choice_index:
                result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0xF59E42
            elif user_choice_index == 0 and bot_choice_index == 2:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            elif user_choice_index == 1 and bot_choice_index == 0:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            elif user_choice_index == 2 and bot_choice_index == 1:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            else:
                result_embed.description = f"**I won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = 0xE02B2B
                await choose_message.add_reaction("🇱")
            await choose_message.edit(embed=result_embed)
        except asyncio.exceptions.TimeoutError:
            await choose_message.clear_reactions()
            timeout_embed = discord.Embed(title="Too late", color=0xE02B2B)
            timeout_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.edit(embed=timeout_embed)

    @commands.command(aliases=["flip", "coin"])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ["Heads", "Tails"]
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")
    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")

    @commands.command()
    async def beer(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Give someone a beer! 🍻 """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("*drinks beer with you* 🍻")
        if user.bot:
            return await ctx.send(f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/")

        beer_offer = f"**{user.name}**, you got a 🍺 offer from **{ctx.author.name}**"
        beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for("raw_reaction_add", timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.command(aliases=["slots", "bet"])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")

    @commands.command(aliases = ['neverhaveiever', 'nhie', 'ever', 'n'], help = "Gives questions for the age old game of never have I ever! ", brief = "Never Have I ever -")
    @commands.cooldown(1, 2.5, BucketType.user)
    async def never(self,ctx):
      """Get a never have I ever question."""
      
      response = f"**Never have I ever** {choice(database['nhie'])}" 
      await ctx.send(response)

    @commands.command(aliases = ['t'], help = "Gives a prompt for the game of truth!", brief = "Game of Truths!")
    @commands.cooldown(1, 2.5, BucketType.user)
    async def truth(self,ctx):
      """Get a truth question."""
      
      response = f"**Truth:** {choice(database['truths'])}" 
      await ctx.send(response)


    @commands.command(aliases = ['d'], help = "Gives a prompt for the game of dares!", brief = "Game of Daress!")
    @commands.cooldown(1, 3, BucketType.user)
    async def dare(self,ctx):
      """Get a dare."""
      
      response = f"**Dare:** {choice(database['dares'])}" 
      await ctx.send(response)


    @commands.Cog.listener()
    async def on_ready(self):
      print('Entertaiment Cog Ready')

    @commands.command(aliases = ['tot', 'tt'], help = "Gives you two options to choose from", brief = "This Or That game.")
    @commands.cooldown(1, 2.5, BucketType.user)
    async def thisorthat(self,ctx):
      """Get a this or that question."""
      
      response = choice(database['tot'])
      
      message = []
      # check if the question has a title.
      if ':' in response: 
        split = response.split(':')
        message.append(f"**{split[0]}**")  
        tort = split[1].strip()
      else:
        tort = response
      message.append(f"🔴 {tort.replace(' or ', ' **OR** ')} 🔵")
      
      embed = discord.Embed(
        color = choice((COLOR_RED, COLOR_BLUE)),
        timestamp = datetime.utcnow(),
        description = '\n'.join(message)
      )

      sent_embed = await ctx.send(embed = embed)
      await sent_embed.add_reaction("🔴")
      await sent_embed.add_reaction("🔵")

    @commands.command(aliases = ['wyr', 'rather'], help = "Gets you a would you rather question!", brief = "Would you rather?")
    @commands.cooldown(1, 3, BucketType.user)
    async def wouldyourather(self,ctx):
      """Get a would you rather question."""
      
      async with CLIENT_SESSION.get('http://either.io/questions/next/1/') as resp:
        result = await resp.json(content_type = None)
        result = result['questions'][0]

      option1, option2 = result['option_1'].capitalize(), result['option_2'].capitalize()
      option1_total, option2_total = int(result['option1_total']), int(result['option2_total'])
      option_total, comments = option1_total + option2_total, result['comment_total']
      title, desc, url = result['title'], result['moreinfo'], result['short_url']
      
      embed = discord.Embed(
        title = title,
        url = url,
        color = COLOR_RED if (option1_total > option2_total) else COLOR_BLUE,
        timestamp = datetime.utcnow()
      )
      embed.add_field(
        name = 'Would You Rather',
        value = f"🔴 `({(option1_total / option_total * 100):.1f}%)` {option1}\n🔵 `({(option2_total / option_total * 100):.1f}%)` {option2}",
        inline = False
      )
      if desc: embed.add_field(name = "More Info", value = desc, inline = False)
      embed.set_footer(text = f"either.io • 💬 {comments}")
      sent_embed = await ctx.send(embed = embed)
      await sent_embed.add_reaction("🔴")
      await sent_embed.add_reaction("🔵")

def setup(bot):
    bot.add_cog(Entertaiments(bot))
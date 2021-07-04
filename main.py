import discord
from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix = settings['prefix'])
# bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('m!help || faen ta dæ'))
    print(f'{bot.user} is online')

bot.colors = {
    "WHITE": 0x26fcff,
    "AQUA": 0x1ABC9C,
    "GREEN": 0x2ECC71,
    "BLUE": 0x3498DB,
    "PURPLE": 0x9B59B6,
    "LUMINOUS_VIVID_PINK": 0xE91E63,
    "GOLD": 0xF1C40F,
    "ORANGE": 0xE67E22,
    "who_even_likes_red_bruh!": 0xa5ddff,
    "NAVY": 0x34495E,
    "DARK_AQUA": 0x11806A,
    "Light_blue": 0x30ffcc,
    "ok": 0x206694,
    "DARK_PURPLE": 0x71368A,
    "DARK_VIVID_PINK": 0xAD1457,
    "DARK_GOLD": 0xC27C0E,
    "cool_color": 0x6891ff,
    "something": 0xfc7bb2,
    "DARK_NAVY": 0xe8c02a,
    "Hm": 0xebf54c,
    "nice_color": 0xfc00f1,
    "nice_color2": 0x21f5fc,
    "very_nice_color": 0x25c059,
    "my_fav": 0xb863f2
}
bot.color_list = [c for c in bot.colors.values()]

cogs = [ 'cogs.moderate',
        'cogs.info',
        'cogs.entertaiments',
        'cogs.movie',
        'cogs.api_commands',
        'cogs.anime',
        'cogs.meme',
        ]

for cog in cogs:
    try:
        bot.load_extension(cog)
    except Exception as e:
        print(f'Could not load cog {cog}: {str(e)}')

@bot.command()
async def loadcog(ctx, cogname=None):
    if cogname is None:
        return
    try:
        bot.load_extension(cogname)
    except Exception as e:
        print(f'Could not load cog {cogname}: {str(e)}')
    else:
        print('Loaded Cog Succesfully')

@bot.command()
async def unloadcog(ctx, cogname=None):
    if cogname is None:
        return
    try:
        bot.unload_extension(cogname)
    except Exception as e:
        print(f'Could not unload cog {cogname}: {str(e)}')
    else:
        print('Unoaded Cog Succesfully')




bot.run(settings['token'])
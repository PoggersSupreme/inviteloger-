# Standard Imports
import discord
from discord.ext import commands
import DiscordUtils
import asyncio
import datetime

# Config
class SYS :
    TOKEN = '' # Place Your Bot Token Here
    PREFIX = '' # Choose A Prefix For Bot { Like => ! }

# Variables
class VAR :
    GUILD = 896126367903645717 # Guild ID
    LOG = 944301795428147210 # Log Channel ID
    CREATOR = "ArDaVaN81"

# Main Variables
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = SYS.PREFIX, intents = intents)
client.remove_command('help') # Remove Bot Default Help's Command

invtrck = DiscordUtils.InviteTracker(client)

# When Bot Get's Ready & Online Do :
@client.event
async def on_ready():

    name = f"Created By {VAR.CREATOR}"

    await client.change_presence(
        status = discord.Status.dnd,
        activity = discord.Activity(type = discord.ActivityType.watching, name = name)
    )

    print('\n  BOT IS ONLINE')

# Check Invite Details Of Self or Specefied Member
@client.command()
@commands.has_permissions(manage_channels = True)
async def inv(ctx, member: discord.Member = None):

    # if Tag Place Is Empty , Replace Author As User
    if member == None:
       user = ctx.author
    else:
       user = member

    # Variables
    guild = ctx.guild
    total_invites = 0

    # Checks Invite List OF Server
    for i in await guild.invites():
        # Any Invite That its Creator Is = With User Mentioned , Add 1 To Total Invites
        if i.inviter == user:
            total_invites += i.uses

    await ctx.message.delete()

    embed = discord.Embed(
        title = "ɪɴᴠɪᴛᴇ ᴛʀᴀᴄᴋᴇʀ ᴮᵒᵗ",
        description = f"\nᴜꜱᴇʀ : {user.mention}\n\nᴛᴏᴛᴀʟ ɪɴᴠɪᴛᴇꜱ ᴄᴏᴜɴᴛ : ``{total_invites} Users``",
        colour = 0x00FF91
    )
    embed._timestamp = datetime.datetime.utcnow()
    embed.set_footer(text = "ɪɴᴠɪᴛᴇ ᴛʀᴀᴄᴋᴇʀ ʙʏ ᴀʀᴅᴀᴠᴀɴ | ")
    embed.set_author(name = "ʙʏ ꜱᴀᴛᴀɴ")
    
    # 3 Seconds Of Typing Status & Then Result
    async with ctx.typing():

        await asyncio.sleep(3)

    await ctx.send(embed = embed)


# Send Invite Log When Member Join (Checks member joined by which invite link, too)
@client.event
async def on_member_join(member):

    # Variables
    inver = await invtrck.fetch_inviter(member) 
    channel = client.get_channel(VAR.LOG)
    guild = client.get_guild(VAR.GUILD)
    total = 0

    # Checks Any Invite In Guild If Has Same ID With Inviter And Do :
    for i in await guild.invites():
        if i.inviter == inver :
            total += i.uses

        embed = discord.Embed(
            title = "ɪɴᴠɪᴛᴇ ᴛʀᴀᴄᴋᴇʀ ᴮᵒᵗ",
            description = f"ᴍᴇᴍʙᴇʀ {member.mention} ᴊᴏɪɴᴇᴅ !\n\nɪɴᴠɪᴛᴇᴅ ʙʏ : {inver.mention}\n\n {inver.mention} ᴛᴏᴛᴀʟ ɪɴᴠɪᴛᴇꜱ : ``{total}``",
            colour = 0x00FF99
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text = "ɪɴᴠɪᴛᴇ ᴛʀᴀᴄᴋᴇʀ | ", icon_url = f"{member.avatar_url}")
        embed.set_thumbnail(url = f"{inver.avatar_url}")
        


    await channel.send(embed = embed)


# Run's Bot
client.run(SYS.TOKEN)
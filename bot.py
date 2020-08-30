import discord
from discord.ext.commands import Bot
import re # regex
import requests # for grabbing apis
import sys

users = [233170527458426880, 338688617033498624, 100295345086402560] 
# check if user is in the admin list
def admin(message):
    admin = False;
    for i in users:
        if message.author.id == i:
            admin = True;
    return admin

client = Bot(command_prefix='o>')
prefix = "o>"

@client.event
async def on_ready():
    print(f'Bot connected as {client.user}')
    game = discord.Game("osu! | o>help")
    await client.change_presence(status=discord.Status.dnd, activity=game)
        
@client.event
async def on_message(message):
    if message.author.bot == False:
        if message.content.startswith(prefix + 'send'):
            print(message.author.name + " is running " + message.content)
            await send(message)
        if message.content.startswith(prefix + 'medal'):
            print(message.author.name + " is running " + message.content)
            await medal(message)
        if message.content.startswith(prefix + 'user'):
            print(message.author.name + " is running " + message.content)
            await user(message)
        if message.content.startswith(prefix + 'help'):
            print(message.author.name + " is running " + message.content)
            await help(message)
        if message.content.startswith(prefix + 'invite'):
            print(message.author.name + " is running " + message.content)
            await invite(message)
        if message.content.startswith(prefix + 'stats'):
            print(message.author.name + " is running " + message.content)
            await stats(message)
        if message.content.startswith(prefix + 'about'):
            print(message.author.name + " is running " + message.content)
            await about(message)

# send help
@client.event
async def help(message):
    channel = client.get_channel(message.channel.id) 
    embed = discord.Embed(title="Help", description="All the commands!" , color=0x00CCFF)
    embed.add_field(name="`o>user username`", value="Get info on an osu! user profile!", inline=False) 
    embed.add_field(name="`o>medal medalname`", value="Get info on a medal, and how to complete it!", inline=False) 
    embed.add_field(name="`o>invite`", value="Invite the omh!medalbot to your own Discord server!", inline=False) 
    embed.add_field(name="`o>stats`", value="Display bot statistics!", inline=False) 
    embed.add_field(name="`o>about`", value="Learn about the bot!", inline=False) 
    embed.set_footer(text="Running omh!medalbot 1.0")
    embedtoedit = await channel.send(embed=embed) 
    
# send invite link
@client.event
async def invite(message):
    channel = client.get_channel(message.channel.id) 
    embed = discord.Embed(title="Invite", description="Invite the omh!medalbot!", color=0x00CCFF, url="https://discord.com/oauth2/authorize?client_id=719636660224000030&permissions=0&scope=bot")
    embedtoedit = await channel.send(embed=embed) 

# get server stats
@client.event
async def stats(message):
    servers = list(client.guilds)
    sum = 0
    for s in servers:
        sum += len(s.members)
    channel = client.get_channel(message.channel.id) 
    embed = discord.Embed(title="Statistics", description="Bot statistics!" , color=0x00CCFF)
    embed.add_field(name="Servers", value=f"{str(len(servers))}", inline=False) 
    embed.add_field(name="Users", value=str(sum), inline=False) 
    embedtoedit = await channel.send(embed=embed) 

# about the bot
@client.event
async def about(message):
    channel = client.get_channel(message.channel.id) 
    embed = discord.Embed(title="About omh!medalbot", description="All about omh!medalbot and what it does!" , color=0x00CCFF)
    embed.add_field(name="About", value="omh!medalbot is an osu! Discord bot which provides many commands, such as users and medals.\n\nIt mainly revolves around the medals/achivements of osu! and shows global medal rank and information about medals and how to pass them.\n\nThis project is made by the osu! Medal Hunters and Osekai team.\nhttps://discord.gg/8qpNTs6\nhttps://www.osekai.net\n\nDeveloped by Hubz, https://www.hubza.co.uk", inline=False) 
    embedtoedit = await channel.send(embed=embed) 

# send message
@client.event
async def send(message):
    if admin(message) == True:
        result = re.search('"(.*?)"', message.content).group(0)
        result = str(result)
        result = str(result).replace('"', "")  
        
        wantedchannel = re.search('<(.*)>', message.content).group(0)
        wantedchannel = str(wantedchannel).replace("<", "")
        wantedchannel = str(wantedchannel).replace(">", "")  
        
        channel = client.get_channel(int(wantedchannel))
        await channel.send(result)
        
# get user from osekai and osu

async def user(message):
    channel = client.get_channel(message.channel.id) 

    embed = discord.Embed(title="Please wait.", description="Loading Info" , color=0x002200) 
    embedtoedit = await channel.send(embed=embed) 

    uid = message.content.replace("o>user ","")

    url = 'https://osu.ppy.sh/users/' + uid
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    }
    cookies = requests.head(url)
    r = requests.get(url, headers=headers, allow_redirects=True, cookies=cookies)
    content = str(r.content)

    embed = discord.Embed(title="Please wait..", description="Loaded profile info!", color=0x006600) 
    await embedtoedit.edit(embed=embed) 

    medals = content.count("achievement_id")

    if "User not found" in content:
        channel = client.get_channel(message.channel.id) 
        embed = discord.Embed(title="This user was not found!", description="Please try another user.", color=0xff0000) 
        await embedtoedit.edit(embed=embed)
    else:
        if uid == "username":
            embed = discord.Embed(title="*Really*?", description="Come on, you know what you've done.", color=0xff0000) 
            await embedtoedit.edit(embed=embed)
        else:
            ruid = re.search('default_group":"(.*?)","id":(.*?),"', content).group(2)

            uname = re.search('<title>(.*?) ', content).group(1)
            uname = uname.replace("&nbsp;", " ") 

            pfp = re.search('{"avatar_url":"(.*?)","co', content).group(1)
            pfp = pfp.replace("\\","");

            rank = re.search('pp_rank":(.*?),', content).group(1)

            osekaiurl = 'https://osekai.net/users-api?search=' + uid

            cookies = requests.head(osekaiurl)
            osekai = requests.get(osekaiurl)
            ocontent = str(osekai.content)

            embed = discord.Embed(title="Please wait.", description="Osekai info loaded!", color=0x00bb00) 
            await embedtoedit.edit(embed=embed) 
            if "!<<" in ocontent:
                medalrank = re.search('!<<(.*?)>>!', ocontent).group(1)
            else:
                medalrank = "Unknown"

            mode = re.search('playmode":"(.*?)",', content).group(1)

            if mode == "osu":
                mode = "osu!"

            if mode == "taiko":
                mode = "osu!taiko"

            if mode == "fruits":
                mode = "osu!catch"

            if mode == "mania":
                mode = "osu!mania"

            a = medals / 233 * 100
            a=a*100
            a=int(a)
            a=a/100.00

            amount = a
            
            channel = client.get_channel(message.channel.id) 

            embed = discord.Embed(title=uname + " (#" + str(rank) + " | " + mode + ")", description="User info for " + uname, color=0x00ff00, url='https://osu.ppy.sh/users/' + ruid) 
            embed.set_thumbnail(url=pfp)

            embed.add_field(name="Medal Rank", value="#" + str(medalrank), inline=True) 
            embed.add_field(name="Medals", value=medals, inline=True) 
            embed.add_field(name="Completion:", value=str(amount) + "%", inline=True) 
            embed.set_footer(text="Data from osu.ppy.sh, osekai.net, and osekai.net/medals. - Coded by Hubz")
            await embedtoedit.edit(embed=embed) 


# get medal from osekai
@client.event
async def medal(message):
    try:
        channel = client.get_channel(message.channel.id) 
        embed = discord.Embed(title="Please wait.", description="Loading Info" , color=0x002200) 
        embedtoedit = await channel.send(embed=embed) 

        uid = message.content.replace("o>medal ","")
        
        uid = uid.replace(" ", "+")

        url = 'https://osekai.net/medals/api?medal=' + uid
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
        }
        cookies = requests.head(url)
        r = requests.get(url, headers=headers, allow_redirects=True, cookies=cookies)
        content = str(r.content)
        content = content.replace('\\xc3\\xa4','a')
        embed = discord.Embed(title="Please wait..", description="Loaded medal info!", color=0x006600) 
    
        if "medal" in content:
            medal = re.search('{medal:"(.*?)"', content).group(1)
            medalicon = re.search('{medalimg:"(.*?)"', content).group(1)
            medaldesc = re.search('{medaldesc:"(.*?)"', content).group(1)
            medalsolution = re.search('{medalsolution:"(.*?)"', content).group(1)
            difficulty = re.search('{difficulty:"(.*?)"', content).group(1)
            mods = re.search('{mods:"(.*?)"', content).group(1)
            mods = mods.replace("\\n"," ")
            if not mods:
                mods = "None"
            channel = client.get_channel(message.channel.id) 

            medalsolution = medalsolution.replace("\\r","")
            medalsolution = medalsolution.replace("\\n"," | ")

            embed = discord.Embed(title=medal, description=medaldesc, color=0x00ff00, url='https://osekai.net/medals?medal=' + uid) 
            embed.set_thumbnail(url=medalicon)
            embed.add_field(name="Solution", value=medalsolution, inline=False) 
            embed.add_field(name="Mods", value=mods, inline=True) 
            embed.add_field(name="Difficulty", value=difficulty, inline=True) 
            embed.set_footer(text="Data from the osekai.net/medals api. - Coded by Hubz")
            await embedtoedit.edit(embed=embed) 
        else:
            channel = client.get_channel(message.channel.id) 
            if uid == "medalname":
                embed = discord.Embed(title="*Come on!*", description="Seriously?", color=0xff0000) 
                await embedtoedit.edit(embed=embed)  
            else:
                embed = discord.Embed(title="This medal was not found!", description="Please try again.", color=0xff0000) 
                await embedtoedit.edit(embed=embed) 
    except:
        await message.channel.send("Unexpected error:" + str(sys.exc_info()[0]))

client.run('token')




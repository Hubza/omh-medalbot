import requests
import discord
import math
import re
from discord.ext import commands
import discord.ext
import mysql.connector
import base64

mydb = mysql.connector.connect(
  host="localhost",
  database="omhauth",
  user="hubz",
  password="pass"
)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        game = discord.Game("osu! | o>help")
        await client.change_presence(status=discord.Status.dnd, activity=game)

    async def on_message(self, message):
        if message.author.bot == False:
            if message.content.startswith("hi"):
                atype = random.randint(0, 5)
                if atype is 0:
                    await message.channel.send("hi")
                if atype is 1:
                    await message.channel.send("hey")
                if atype is 2:
                    await message.channel.send("heyo")
                if atype is 3:
                    await message.channel.send("ey")
                if atype is 4:
                    await message.channel.send("oioi")
                if atype is 5:
                    await message.channel.send("whats up")

            if message.content.startswith("tell me a joke"):
                lines = open("jokes.txt").read().splitlines()
                random_line = random.choice(lines)
                await message.channel.send(random_line)

            if message.content.startswith("o>user"):
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

                        print(content)

                        uname = re.search('<title>(.*?) ', content).group(1)
                        uname = uname.replace("&nbsp;", " ") 
                        print(uname)

                        pfp = re.search('{"avatar_url":"(.*?)","co', content).group(1)
                        pfp = pfp.replace("\\","");

                        rank = re.search('pp_rank":(.*?),', content).group(1)



                        osekaiurl = 'https://osekai.net/users-api?search=' + uid

                        cookies = requests.head(osekaiurl)
                        osekai = requests.get(osekaiurl)
                        ocontent = str(osekai.content)
                        print(ocontent)
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
                        embed.set_footer(text="Data from osu.ppy.sh, www.osekai.net, and www.osekai.net/medals. - Coded by Hubz")
                        await embedtoedit.edit(embed=embed) 

            if message.content.startswith("o>medal"):
    

                channel = client.get_channel(message.channel.id) 

                embed = discord.Embed(title="Please wait.", description="Loading Info" , color=0x002200) 
                embedtoedit = await channel.send(embed=embed) 

                uid = message.content.replace("o>medal ","")

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

                    embed = discord.Embed(title=medal, description=medaldesc, color=0x00ff00) 
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
                        
            if message.content.startswith("o>omhuser"):
                uid = message.content.replace("o>omhuser ","")
                print("getting users")
                channel = client.get_channel(message.channel.id) 
                sql_select_Query = "SELECT * FROM users WHERE osuname = '" + uid + "'"
                cursor = mydb.cursor()
                cursor.execute(sql_select_Query)
                records = cursor.fetchall()
                embed = discord.Embed(title="Found no users", description="", color=0xff2222) 
                for obj in records:
                    embed = discord.Embed(title="Found a user", description="", color=0xffffff) 
                    discordusername = obj[3]
                    discordtag = obj[4]
                    discordusername = base64.b64decode(discordusername)
                    discordusername = discordusername.decode("utf-8")
                    embed.add_field(name="Discord Username", value=discordusername + "#" + discordtag, inline=False) 
                    embed.add_field(name="osu! User", value='https://osu.ppy.sh/users/' + obj[5], inline=False) #
                    embed.add_field(name="Medals", value=obj[7], inline=False) #
                    embed.set_thumbnail(url=obj[6])
                embed = await channel.send(embed=embed) 

            if message.content.startswith("o>help"):
                channel = client.get_channel(message.channel.id) 

                embed = discord.Embed(title="Help", description="All the commands!" , color=0x00CCFF)
                embed.add_field(name="`o>user username`", value="Get info on an osu! user profile!", inline=False) 
                embed.add_field(name="`o>medal medalname`", value="Get info on a medal, and how to complete it!", inline=False) 
                embed.add_field(name="`o>omhuser username`", value="Find user in this discord along with user information from osu! username", inline=False) 
                embedtoedit = await channel.send(embed=embed) 


client = MyClient()
client.run('token')

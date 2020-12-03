import discord
from discord.ext.commands import Bot
from discord.ext import commands
import re # regex
import requests # for grabbing apis
import sys
import ftfy
import asyncio
import os
import socket

users = [233170527458426880, 338688617033498624, 100295345086402560] 
# check if user is in the admin list
def admin(message):
    admin = False;
    for i in users:
        if message.author.id == i:
            admin = True;
    return admin

client = Bot(command_prefix='news>')
prefix = "news>"

async def status_task():
    while True:
        game = discord.Game("trying something")
        print("running loop")
        
        response = requests.get("https://osu.ppy.sh/home")
        content = response.text;

        uname = re.findall('slug":"(.*?)","ti', content)[0]
        url = "https://osu.ppy.sh/home/news/" + uname;

        # grab news post
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
        }
        cookies = requests.head(url)
        r = requests.get(url, headers=headers, allow_redirects=True, cookies=cookies)
        content = str(r.content)

        # get info about news post
        title = re.findall('","title":"(.*?)"', content)[0];
        description = re.findall('<meta name="description" content="(.*?)"', content)[0]; 
        author = re.findall('"author":"(.*?)"', content)[0];
        authorlink = "https://osu.ppy.sh/users/" + author;
        image = re.findall('<meta property="og:image" content="(.*?)"', content)[0];

        print("title: " + title)
        print("description: " + description)
        print("author: " + author)
        print("authorlink: " + authorlink)
        print("image: " + image)

        # get last read
        f = open("/root/omh/last.txt", "r")
        lastone = f.read()

        if title == lastone:
            print("still the same")
        else:
            embed=discord.Embed(title=title, url=url, description=description, color=0x178bff)
            embed.set_author(name=author)
            embed.set_image(url=image)
            embed.set_footer(text="Post from the osu! website")
            channel = client.get_channel(774384841369321502)
            await channel.send(embed=embed)

        # put into file
        f = open("/root/omh/last.txt", "w")
        f.write(title)

        await asyncio.sleep(60)
        

@client.event
async def on_ready():
    print(f'Bot connected as {client.user}')
    game = discord.Game("with news posts")
    await client.change_presence(status=discord.Status.dnd, activity=game)
    client.loop.create_task(status_task())
        
@client.event
async def on_message(message):
    if message.author.bot == False:
        if message.content.startswith("who is " + client.user.name) or message.content.startswith("o>reportallbots"):
            await message.channel.send("I'm " + client.user.name + " running on " + str(socket.gethostname()) + "\n" + "`PROCESS ID` : `" + str(os.getpid()) + "`\n`PARENT ID` : `" + str(os.getppid()) + "`\n`LOCATION` : `" + os.path.realpath(__file__) + "`")
        if message.content.startswith(prefix + 'example'):
            await example(message)
            await ran(message)

        if message.content.startswith(prefix + 'latest'):
            await latest(message)
            await ran(message)

@client.event
async def ran(message):
    print(message.author.name + " is running " + message.content + " in " + message.guild.name)

@client.event
async def example(message):
    if message.author.bot == False:
        await message.channel.send('generating example news post')
        embed=discord.Embed(title="New Featured Artist: kiraku", url="https://osu.ppy.sh/home/news/2020-09-26-new-featured-artist-kiraku", description="We're proud to welcome kiraku aboard as our latest Featured Artist!", color=0x178bff)
        embed.set_author(name="Ephemeral", url="https://osu.ppy.sh/users/Ephemeral")
        embed.set_image(url="https://assets.ppy.sh/artists/101/header.jpg")
        embed.set_footer(text="Post from the osu! website")
        await message.channel.send(embed=embed)


@client.event
async def latest(message):
    await message.channel.send('grabbing latest news post')

    url = 'https://osu.ppy.sh/home/news'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    }
    cookies = requests.head(url)
    r = requests.get(url, headers=headers, allow_redirects=True, cookies=cookies)
    content = str(r.content)
    
    uname = re.findall('slug":"(.*?)","ti', content)[0]
    url = "https://osu.ppy.sh/home/news/" + uname;
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    }
    cookies = requests.head(url)
    r = requests.get(url, headers=headers, allow_redirects=True, cookies=cookies)
    content = str(r.content)
    
    
    title = re.findall('","title":"(.*?)"', content)[0];
    description = re.findall('<meta name="description" content="(.*?)"', content)[0]; 
    author = re.findall('"author":"(.*?)"', content)[0];
    authorlink = "https://osu.ppy.sh/users/" + author;
    image = re.findall('<meta property="og:image" content="(.*?)"', content)[0];
    
    print("title: " + title)
    print("description: " + description)
    print("author: " + author)
    print("authorlink: " + authorlink)
    print("image: " + image)
    
    embed=discord.Embed(title=title, url=url, description=description, color=0x178bff)
    embed.set_author(name=author, url=authorlink)
    embed.set_image(url=image)
    embed.set_footer(text="Post from the osu! website")
    await message.channel.send(embed=embed)
    
    
client.run('no')

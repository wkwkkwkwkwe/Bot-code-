import discord, aiohttp, re, random, platform, json, base64, datetime
from discord.ext import commands
from pip._vendor import requests


client=commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Bot Is Ready')

@client.command()
async def ban(ctx, user: discord.User):
    guild=ctx.guild
    embed=discord.Embed(
        title=f'Ban Command Called',
        description=f'{user.mention} was banned from {guild.name}'
    )
    await ctx.send(embed=embed)
    await guild.ban(user=user)


@client.command()
async def unban(ctx, user: discord.User):
    guild=ctx.guild
    embed=discord.Embed(
        title=f'Unban Command Called',
        description=f'{user.mention} was unbanned from {guild.name}'
    )
    await ctx.send(embed=embed)
    await guild.ban(user=user)

@client.event
async def on_message(ctx):
    if ctx=='prefix':
        await ctx.send('My prefix is: .')

@client.event
async def on_member_join(ctx, user: discord.User):
    guild=ctx.guild
    embed=discord.Embed(
        title='Welcome Message',
        description=f'Welcome {user.mention} have a great time in {guild.name}',
        colour=discord.Colour.purple()
    )
    await ctx.send(embed=embed)

@client.command()
async def kick(ctx, user: discord.User):
    guild = ctx.guild
    embed= discord.Embed(
        title='Kick Command Called',
        description=f'{user.mention} was kicked from {guild.name}'
    )
    await ctx.send(embed=embed)
    await guild.kick(user=user)

@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Muted {member.mention} for reason {reason}")
    await member.send(f"You were muted in the server {guild.name} for {reason}")

@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}")
    await member.send(f"You were unmuted in the server {ctx.guild.name}")



def timedelta_str(dt):
    days = dt.days
    hours, r = divmod(dt.seconds, 3600)
    minutes, sec = divmod(r, 60)

    if minutes == 1 and sec == 1:
        return '{0} days, {1} hours, {2} minute and {3} second.'.format(days,hours,minutes,sec)
    elif minutes > 1 and sec == 1:
        return '{0} days, {1} hours, {2} minutes and {3} second.'.format(days,hours,minutes,sec)
    elif minutes == 1 and sec > 1:
        return '{0} days, {1} hours, {2} minute and {3} seconds.'.format(days,hours,minutes,sec)
    else:
        return '{0} days, {1} hours, {2} minutes and {3} seconds.'.format(days,hours,minutes,sec)

#Bot initiation
@client.event
async def on_ready():
    message = 'logged in as %s' % client.user #Initiate bot's name and tag
    uid_message = 'user id %s' % client.user.id #Initiate's bot's ID
    separator = '-' * max(len(message), len(uid_message)) # Fancy way to make seperators, to make our code pretty :))
    print(separator) # We use the seperator to keep it clean
    print(message) # We print bot's name and tag
    print(uid_message) # We print the bot's ID
    guild_members = len(set(client.get_all_members())) #Define server members
    await client.change_presence(activity=discord.Game(name='.help | palmtrww | best au | {} users' .format(guild_members))) # We set the custom status, which we also show server members

    print(separator) # We use the seperator to keep it clean
    print(len(client.users)) #Prints amount of users in bot's servers (still ugly)
    print(len(client.guilds)) ##Prints amount of servers bot is in (still ugly)
    print(separator) # We use the seperator to keep it clean

#On member join
@client.event
async def on_member_join(member):
    await member.create_dm() # Create a direct message
    await member.dm_channel.send(f"Welcome to palmtrwws server {member.name}! Please read the <#717434848255410266>! We hope to keep the server a safe community for everyone.") # In the dm, send this string

#Ping command
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms') # Sends latency of bot (Rounded up)

#8ball command
@client.command(aliases=['8ball']) # We set an alias as '8ball'
async def _8ball(ctx, *, question):
    embed = discord.Embed(title="8ball", color=0x008080) # Define embed's color and title

    responses = ["It is certain.", #Responses for the 8ball
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes – definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful.",]
    await ctx.send(f':8ball: Answer: {random.choice(responses)}')

#Roast command
@client.command(aliases=['roastme']) # Basically like the 8ball command
async def roast(ctx):
    roastresponses = ["My phone battery lasts longer than your relationships.", # This isn't efficient as we should grab the roasts from another file, to keep it clean
                  "If I wanted a bitch, I would have bought a dog.",
                  "You birth certificate is just an apology letter from the condom company.",
                  "I wish you could be fluent in silence.",
                  "Do you still love nature? Despite what it did to you.",
                  "Its scary to think that people like you are gonna be able to vote...",
                  "You must've been born on the highway, that's where most accidents happen.",
                  "Im sorry if I hurt your feelings when I called you stupid, I thought you already knew.",
                  "Two wrongs don't make a right, take your parents for example.",
                  "Shock me. Say something intelligent.",
                  "Calling you an idiot would be an insult to stupid people.",
                  "Are you always stupid or is today a special occasion?",
                  "Never be ashamed of who you are... that is your parents job.",
                  "You have more faces than Mount Rushmore.",
                  "You are proof that god has a sense of humor.",
                  "You are like a cloud. When you disappear it is a beautiful day.",
                  "You bring everyone so much joy, when you leave the room.",
                  "It is impossible to underestimate you.",
                  " I'm sorry, what language are you speaking? It sounds like bullshit.",
                  "I forgot the world revolves around you. My apologies, how silly of me."]
    await ctx.send(f'{random.choice(roastresponses)}')

#The IP command messes up when a value is empty
def nullFix(inp):
    if len(str(inp)) > 0:
        return str(inp)
    else:
        return 'null' # Instead of freaking out, we make it return null.

#ip command
@client.command(aliases=['ip'])
async def on_message(ctx, *, ip):
    r = requests.get('http://ip-api.com/json/{}'.format(ip))
    info = json.loads(r.text)

    embed = discord.Embed(title="IP", description="search", color=0x00ff00)
    for i in range(len(info)):
        embed.add_field(name=list(info)[i], value=nullFix(list(info.values())[i]))
    await ctx.send(embed=embed)

#Hug command
@client.command()
async def hug(ctx, member: discord.Member):
    if member.display_name == ctx.message.author.display_name:
        await ctx.send(f"{member.display_name} hugged themselves, they must be lonely.")
    else:
        await ctx.send(f'{ctx.message.author.display_name} hugged {member.display_name}. How sweet.')


#Roll dice command
@client.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN! (Ex: 9d6)')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(f"The rolled number(s) were :" + result)

#Avatar command
@client.command(aliases=['pic','picture,','pfp','av']) # More flexibility (aliases)
async def avatar(ctx, member: discord.Member):
    author = ctx.message.author
    show_avatar = discord.Embed( # I used an embed for this, more visually pleasing
        color=0xff69b4,
        description=f"**{member.display_name}'s avatar : **"
    )
    show_avatar.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=show_avatar)


#Change nickname Command
@client.command(pass_context=True) # If there's spaces in the name, it will show up the first part only. Currently a bug.
@commands.has_guild_permissions(manage_nicknames=True)
async def setnick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f"{member.name}'s nickname has been set to -> **{member.display_name}**")

#Help command
client.remove_command('help')
@client.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author
	embed=discord.Embed(title="Pancakes's command help", description="A list of bot commands for Pancake Bot", color=0x7CFC00)
	embed.add_field(name=".invite", value="Invites insomnia to your server!", inline=True)
	embed.add_field(name=".ping", value="Returns the bot's latency in ms!", inline=True)
	embed.add_field(name=".8ball [question]", value="Gives you a random answer to your question!", inline=True)
	embed.add_field(name=".roast", value="Gives you a roast!", inline=True)
	embed.add_field(name=".ip [adress]", value="Returns geographical info about an ip adress!", inline=True)
	embed.add_field(name=".hug [user]", value="Hugs a specified user :)", inline=True)
	embed.add_field(name=".roll [nDn]", value="Rolls dice in NDN format!", inline=True)
	embed.add_field(name=".avatar [user]", value="Shows you the users avatar!", inline=True)
	embed.add_field(name=".uptime", value="Shows you the bots uptime (Dev Tool)", inline=True)
	embed.add_field(name=".emojify [message]", value="Bot will DM you with your emojified message!", inline=True)
	embed.add_field(name=".minecraft [username]", value="See skin, username and more of a specified MC account!", inline=True)
	embed.add_field(name=".wikipedia [topic]", value="See a summarized wikipedia definition of a topic!", inline=True)
	embed.add_field(name=".penis", value="Displays your penis size!", inline=True)
	embed.add_field(name=".coin", value="Flips a coin for head or tails!", inline=True)
	#embed.add_field(name="### Moderator Commands", value="Commands requiring special permissions", inline=False)
	embed.add_field(name=".kick [user]", value="Kicks a user from your server!", inline=True)
	embed.add_field(name=".ban [user]", value="Bans a specified user from your server!", inline=True)
	embed.add_field(name=".unban [user]", value="Unbans a specified user from your server!", inline=True)
	embed.add_field(name=".purge [# of messages]", value="Purges the specified amount of messages!", inline=True)
	embed.add_field(name=".say [message]", value="Bot writes specified message!", inline=True)
	embed.add_field(name=".servers", value="Command shows info of insomnias servers, and other info!", inline=True)
	await ctx.send(embed=embed)



#Bot Uptime command
@client.command()
async def uptime(ctx):
    global start_time
    await ctx.send("**:white_check_mark: Bot uptime : **"+timedelta_str(datetime.datetime.now() - start_time))

#Emojify command (Written by Shrekbot's owners respectfully)
@client.command()
async def emojify(ctx, *, text: str):
    '''
    Converts the alphabet and spaces into emoji
    '''
    author = ctx.message.author
    emojified = '⬇ Copy and paste this: ⬇\n'
    formatted = re.sub(r'[^A-Za-z ]+', "", text).lower()
    if text == '':
        await ctx.send('Remember to say what you want to convert!')
    else:
        for i in formatted:
            if i == ' ':
                emojified += '     '
            else:
                emojified += ':regional_indicator_{}: '.format(i)
        if len(emojified) + 2 >= 2000:
            await ctx.send('Your message in emojis exceeds 2000 characters!')
        if len(emojified) <= 25:
            await ctx.send('Your message could not be converted!')
        else:
            await author.send('`'+emojified+'`')

#Minecraft Command (Written by Shrekbot's owners respectfully)
@client.command(helpinfo='Shows MC account info, skin and username history', aliases=['skin', 'mc'])
async def minecraft(ctx, username='Shrek'):
    '''
    Shows MC account info, skin and username history
    '''
    uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/{}'
                        .format(username)).json()['id']

    url = json.loads(base64.b64decode(requests.get(
        'https://sessionserver.mojang.com/session/minecraft/profile/{}'
            .format(uuid)).json()['properties'][0]['value'])
                     .decode('utf-8'))['textures']['SKIN']['url']

    names = requests.get('https://api.mojang.com/user/profiles/{}/names'
                         .format(uuid)).json()
    history = "**Name History:**\n"
    for name in reversed(names):
        history += name['name'] + "\n"

    await ctx.send(':white_check_mark: **Username: `{}`**\n**Skin: {}**\n**UUID: {}**'.format(username, url, uuid))
    await ctx.send(history)

#Wiki command (Written by Shrekbot's owners respectfully)
@client.command(helpinfo='Wikipedia summary', aliases=['w', 'wiki'])
async def wikipedia(ctx, *, query: str):
    '''
    Uses Wikipedia APIs to summarise search
    '''
    sea = requests.get(
        ('https://en.wikipedia.org//w/api.php?action=query'
         '&format=json&list=search&utf8=1&srsearch={}&srlimit=5&srprop='
        ).format(query)).json()['query']

    if sea['searchinfo']['totalhits'] == 0:
        await ctx.send('Sorry, your search could not be found.')
    else:
        for x in range(len(sea['search'])):
            article = sea['search'][x]['title']
            req = requests.get('https://en.wikipedia.org//w/api.php?action=query'
                               '&utf8=1&redirects&format=json&prop=info|images'
                               '&inprop=url&titles={}'.format(article)).json()['query']['pages']
            if str(list(req)[0]) != "-1":
                break
        else:
            await ctx.send('Sorry, your search could not be found.')
            return
        article = req[list(req)[0]]['title']
        arturl = req[list(req)[0]]['fullurl']
        artdesc = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/'+article).json()['extract']
        lastedited = datetime.datetime.strptime(req[list(req)[0]]['touched'], "%Y-%m-%dT%H:%M:%SZ")
        embed = discord.Embed(title='**'+article+'**', url=arturl, description=artdesc, color=0x3FCAFF)
        embed.set_footer(text='Wiki entry last modified',
                         icon_url='https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
        embed.set_author(name='Wikipedia', url='https://en.wikipedia.org/',
                         icon_url='https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
        embed.timestamp = lastedited
        await ctx.send(':white_check_mark: **Search result for:** ***"{}"***:'.format(query), embed=embed)


#Bots server info command, (Written by Shrekbot's owners respectfully)
@client.command(helpinfo='Info about servers Palmtrww Bot is in', aliases=['server', 'num', 'count'])
@commands.has_any_role("Administrator", "Admin", "Mod", "Moderator") # I think hardocding this is fine.
async def servers(ctx):
    servers = client.guilds
    servers.sort(key=lambda x: x.member_count, reverse=True)
    await ctx.send(':white_check_mark: ***Top servers with Pancake bot:***')
    for x in servers[:5]:
        await ctx.send('**{}**, **{}** Members, {} region, Owned by <@{}>, Created at {}\n{}'.format(x.name, x.member_count, x.region, x.owner_id, x.created_at, x.icon_url_as(format='png',size=32)))
    y = 0
    for x in client.guilds:
        y += x.member_count
    await ctx.send('**Total number of ins users:** **{}**!\n**Number of servers:** **{}**!'.format(y, len(client.guilds)))

#Credits to @elmo for helping me
@client.command(aliases=['dick','peen','peensize','penissize','dicksize','cock','cocksize'])
async def penis(ctx):
    author = ctx.message.author
    PenisParts = ["8", "=", "D"]
    PEEPEE = []
    length = random.randint(0, 18)
    PEEPEE.append(PenisParts[0])
    for i in range(length):
        PEEPEE.append(PenisParts[1])
    PEEPEE.append(PenisParts[2])
    peen = ""
    await ctx.send(f"**{author.display_name}'s penis size :** {peen.join(PEEPEE)}")

#Flip a coin
@client.command()
async def coin(ctx):
	random.seed(10)
	coin = ["heads", "tails"] #The choices for the coin
	await ctx.send(":white_check_mark: The coin landed on " +random.SystemRandom().choice(coin)+ "!") #Displays the random coin
	return

#Info about bot, thanks to @nothingness
@client.command()
async def info(ctx):
    client.version = '0.7.3' # Manually Update your bots version
    pythonVersion = platform.python_version() # Defines Python version
    embed = discord.Embed(title=f'{client.user.name} Information', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name="Bot\'s Library:", value = "discord.py rewrite", inline = False)
    embed.add_field(name='Bot\'s Python Version', value=pythonVersion, inline=False)
    embed.add_field(name='Bot\'s Development Version:', value=client.version, inline=False)
    embed.add_field(name='Bot\'s Developer:', value="<@286983211123474432>", inline=False)

    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)

    await ctx.send(embed=embed)


@client.command()
async def meme(ctx):
    embed = discord.Embed(title="", description="")
    try:
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)
    except:
        await ctx.send("Couldn't get meme, please try again.")




#Say command
@client.command()
@commands.has_guild_permissions(administrator=True)
async def say(ctx, *, message=None):
    message = message or "Please include a message for me to say."
    await ctx.message.delete()
    await ctx.send(message)




client.run('')

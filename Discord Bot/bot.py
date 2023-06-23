import discord, os, random, responses, hangman
import wikipedia as wk
from time import sleep
hangman_toggle = False
guess_bank = []
rand_word = random.randint(0,19)

async def send_message(message, user_message):
    try:
        response = responses.get_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)

async def hangman_game(message, guess_bank, rand_word):
    try:
        response = hangman.game(guess_bank, rand_word)
        await message.channel.send(response)
        if "guessed" in response:
            global hangman_toggle
            hangman_toggle = False
            guess_bank.clear()
            rand_word = random.randint(0,15)
    except Exception as e:
        print(e)

async def send_image(message):
    img_folder_dir = "Images\\"
    images = []
    for x, y, files in os.walk(img_folder_dir):
        for file in files:
            images.append(img_folder_dir + file)
    with open(images[random.randint(0,len(images)-1)], 'rb') as f:
        file = discord.File(f)
        await message.channel.send(file=file)

async def rand_img_selector():
    rand_img_folder_dir = "Images\\"
    images = []
    for x, y, files in os.walk(rand_img_folder_dir):
        for file in files:
            images.append(rand_img_folder_dir + file)
    with open(images[random.randint(0,len(images)-1)], 'rb') as f:
        file = discord.File(f)
        return file

def run_discord_bot():
    TOKEN = "MTA2NTA5ODQ4NzE4OTk5NTU1MA.Ge8E58.IrwigOiYwdn4APm2lRBgUcDGNy2zY5WwVowGnc"
    intents = discord.Intents.all()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        
    @client.event
    async def on_message(message):
        global hangman_toggle
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username}: '{user_message}'")

        if user_message.startswith('>send_dm'):
            split_message = user_message[9:].strip().split(' ', 1)
            if len(split_message) != 2:
                await message.channel.send('use: >send_dm @username message')
            else:
                user_mention = split_message[0]
                message_text = split_message[1]
                member = discord.utils.get(message.guild.members, mention=user_mention)
                if member:
                    dm_channel = await member.create_dm()
                    await dm_channel.send(message_text)
                    await message.channel.send('Hello!')
                else:
                    await message.channel.send('no member in the server.')
        
        if user_message.startswith('>send_img'):
            if len(message.mentions) > 0:
                member = message.mentions[0]
                file = await rand_img_selector()
                dm_channel = await member.create_dm()
                await dm_channel.send(file=file)
                await message.channel.send("YO!")
            else:
                await message.channel.send("please mention a member to send the image to.")

        if user_message == '>meme':
            await send_image(message)
            
        elif user_message == '>hangman':
            hangman_toggle = True
            await message.channel.send("```Playing hangman\nTo guess enter '>' before the letter```")
            await hangman_game(message, guess_bank, rand_word)
    
        elif user_message[0] == ">" and hangman_toggle == True:
            guess = user_message[1:].strip()
            if len(guess) == 1:
                guess_bank.append(guess)
                print(guess_bank)
                await hangman_game(message, guess_bank, rand_word)
            
        elif user_message.startswith('>wiki'):
            split_message = user_message[6:].strip().split(' ', 1)
            try:
                page = wk.page(split_message)
                await message.channel.send(page.url)
            except:
                await message.channel.send("Could not get the link from Wikipedia!")

        if user_message[0] == '>':
            user_message = user_message[1:]
            await send_message(message, user_message)
        
    client.run(TOKEN)
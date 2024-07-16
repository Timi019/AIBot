import discord,tensorflow,keras,requests,numpy,random,os
from discord.ext import commands
from model import *

def main():
    intents = discord.Intents.default()
    intents.message_content = True
    token = os.environ["TOKEN"]
    bot = commands.Bot(command_prefix='$', intents=intents)

    @bot.event
    async def on_ready():
        print(f'Zalogowaliśmy się jako {bot.user}')

    @bot.command()
    async def hello(ctx):
        await ctx.send(f'Cześć, jestem bot{bot.user}!')

    @bot.command()
    async def heh(ctx, count_heh = 5):
        await ctx.send("he" * count_heh)

    @bot.command()
    async def check(ctx):
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                name = attachment.filename
                if name.endswith(".png") or name.endswith(".jpg") or name.endswith(".jpeg") or name.endswith(".tiff") or name.endswith(".webp"):
                    await attachment.save(name)
                    result = detect_bird(name, "keras_model.h5", "labels.txt")
                    con_score = result[1] * 100
                    result = result[0].strip()  # Usuń znak nowej linii                    
                    if int(con_score) >= 50:
                        if result.startswith("O") or result.startswith("E"):
                            await ctx.send(f"It seems like it's an {result}")
                        else:
                            await ctx.send(f"It seems like it's a {result}")
                    else:
                        await ctx.send("Image not recognized")
                    os.remove(name)
                else:
                    await ctx.send("Unsupported file format")
        else:
            await ctx.send("Add image attachment to check")

    bot.run(token)

if __name__ == "__main__":
    main()
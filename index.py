import discord
import requests
import json
import os
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
import random
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("SECRET_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!' , intents=intents)




@client.command()
async def play(ctx, url):
    channel = ctx.author.voice.channel
    voice_client = get(client.voice_clients, guild=ctx.guild)

    if voice_client and voice_client.is_connected():
        await voice_client.move_to(channel)
    else:
        voice_client = await channel.connect()

    ydl_opts = {'format': 'bestaudio', 'noplaylist': 'True'}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(URL)

    await ctx.send(f'Escuchando musica en {channel}. Unete!')
    voice_client.play(source)

@client.command()
async def rolldice(ctx):
    dice = random.randint(1, 6)
    await ctx.send(f'El numero fue: {dice}')

@client.command()
@commands.has_permissions(move_members = True)
async def disconnect(ctx, member: discord.Member):
    await member.move_to(None)
    await ctx.send(f'Se deconecto al usuario {member}')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Usuario {member} ha sido kickeado')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    channel = await member.create_dm()
    await channel.send("Has sido baneado. Espero que no vuelvas a repetir esas cosas")
    await member.ban(reason=reason)
    await ctx.send(f'Usuario {member} ha sido baneado')

@client.command()
async def capihelp(ctx):
    embed=discord.Embed(title="Comandos", description="Los comandos del bot", color=discord.Color.blue())
    embed.add_field(name="Administacion", value="Comandos para administrar el server (necesitan permisos)", inline=False)
    embed.add_field(name="!ban <Usuario>", value="Banea al usuario en cuestion", inline=True)
    embed.add_field(name="!kick <Usuario>", value="Expulsa al usuario en cuestion", inline=True)
    embed.add_field(name="!disconnect <Usuario>", value="Desconecta al usuario en cuestion", inline=True)
    embed.add_field(name="Miscleaneos", value="Comandos de diversion", inline=False)
    embed.add_field(name="!play <url>", value="Se une al canal de voz y reproduce el audio", inline=True)
    embed.add_field(name="!rolldice", value="Tira un dado", inline=True)
    embed.add_field(name="!checksv <Servidor>", value="Observa los datos de un servidor de mc", inline=True)
    embed.set_author(name="Capi Bot")
    embed.set_footer(text="Comando pedido por: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)

@client.command()
async def checksv(ctx, address):
    data = getdata(address)
    fResponse = json.dumps(data, indent=8)
    await ctx.send(f'```json\n{fResponse}\n```')

#### MCSERVER FUNCTION
def getdata(address):
    response = requests.get(f'https://api.mcstatus.io/v2/status/java/{address}')
    responseJson = response.json()

    if 'icon' in responseJson:
        del responseJson['icon']

    if 'motd' in responseJson:
        del responseJson['motd']

    if 'name_html' in 'version' in responseJson:
        del responseJson['version']['name_html']

    if 'list' in 'players' in responseJson:
        del responseJson['players']['list']
        
    return responseJson

client.run(TOKEN)

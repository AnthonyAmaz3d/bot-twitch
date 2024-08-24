import discord
from twitchAPI.twitch import Twitch
import asyncio

DISCORD_TOKEN = '' # token do bot criado no site do discord
TWITCH_CLIENT_ID = '' # id da aplicação no site da twitch 
TWITCH_CLIENT_SECRET = '' # secret da aplicação
TWITCH_USER_LOGIN = 'frttt' #nome do canal
DISCORD_CHANNEL_ID = 111111111111111111 # ID do canal do Discord

# Configuração do cliente Twitch
async def authenticate_twitch():
    await twitch.authenticate_app([])

twitch = Twitch(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)

# Configuração do cliente Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Variável para rastrear o estado do stream
is_live = False

async def check_stream():
    """Função para verificar se o streamer está online."""
    global is_live  # Para modificar a variável global

    while True:
        try:
            streams = twitch.get_streams(user_login=TWITCH_USER_LOGIN)
            async for stream in streams:
                if stream and not is_live:
                    # Se o stream está ao vivo e ainda não foi notificado
                    is_live = True  # Atualiza o estado para "ao vivo"
                    channel = client.get_channel(DISCORD_CHANNEL_ID)
                    if channel:
                        await channel.send(f"{TWITCH_USER_LOGIN} está ao vivo na Twitch! Assista aqui: https://www.twitch.tv/{TWITCH_USER_LOGIN} @everyone ")
                elif not stream and is_live:
                    # Se o stream não está ao vivo, reseta o estado
                    is_live = False
                    print(f"{TWITCH_USER_LOGIN} não está ao vivo.")
        except Exception as e:
            print(f"Erro ao verificar stream: {e}")
        
        await asyncio.sleep(60)  # Verifica a cada 60 segundos

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')
    await authenticate_twitch()  # Autentica o Twitch ao iniciar o bot
    client.loop.create_task(check_stream())  # Inicia a verificação de stream

# Iniciar o bot do Discord
client.run(DISCORD_TOKEN)
import datetime
import discord
from discord.ext import tasks
import yaml
from utils import enviar_mensagem_com_reacao
import logging

# # Configurando logging
logging.basicConfig(filename='events.log', encoding='utf=8', format='%(asctime)s %(levelname)8s %(name)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S')

# Primeiro, vamos carregar as configurações
with open('config.yml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)
with open('token.yml', 'r', encoding='utf-8') as file:
    config_token = yaml.safe_load(file)

# Configuração do cliente Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Vamos configurar a tarefa da mensagem recorrente
@tasks.loop(time=[datetime.time(hour=16), 
                  datetime.time(hour=17),
                  datetime.time(hour=18),
                  datetime.time(hour=19),
                  datetime.time(hour=20),
                  datetime.time(hour=21),
                  datetime.time(hour=22),
                  datetime.time(hour=23),
                  datetime.time(hour=0),
                  datetime.time(hour=1),
                  datetime.time(hour=2),
                  datetime.time(hour=3)
                  ])
async def mensagemProgramada():
    now = datetime.datetime.now()
    current_hour_brazil = now.hour - 3
    if current_hour_brazil < 1:
        current_hour_brazil = current_hour_brazil + 12
    indice = current_hour_brazil - 12

    texto = config['textos']['tumba'][indice]

    await enviar_mensagem_com_reacao(client, config['canais']['taverna'], texto, config['emojis']['caveira'])

@client.event
async def on_ready():
    logging.info(f'Bot logado como: {client.user}')
    if not mensagemProgramada.is_running():
        mensagemProgramada.start()
        logging.info('Mensagem programada configurada!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.author.name == 'daniel.lucredio':
        if message.content.startswith('Oi, Bruxa'):
            await enviar_mensagem_com_reacao(client, config['canais']['taverna'], "Olá, mestre!", config['emojis']['caveira'])
        if message.content.startswith('Bruxa, qual é o seu nome?'):
            await enviar_mensagem_com_reacao(client, config['canais']['taverna'], "Meu nome é Hécate, ó grande mestre dos magos!", config['emojis']['caveira'])

client.run(config_token['token_bot'], root_logger=True)
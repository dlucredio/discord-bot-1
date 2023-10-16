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
@tasks.loop(time=[datetime.time(hour=0), 
                  datetime.time(hour=1),
                  datetime.time(hour=2),
                  datetime.time(hour=3),
                  datetime.time(hour=4),
                  datetime.time(hour=5),
                  datetime.time(hour=6),
                  datetime.time(hour=7),
                  datetime.time(hour=8),
                  datetime.time(hour=9),
                  datetime.time(hour=10),
                  datetime.time(hour=11),
                  datetime.time(hour=12)
                  ])
async def mensagemProgramada():
    now = datetime.datetime.now()
    current_hour_brazil = now.hour - 3
    if current_hour_brazil > 11:
        current_hour_brazil = current_hour_brazil - 11

    if current_hour_brazil == 1:
        texto = config['textos']['uma_hora']
    elif current_hour_brazil == 2:
        texto = config['textos']['duas_horas']
    elif current_hour_brazil == 3:
        texto = config['textos']['tres_horas']
    elif current_hour_brazil == 4:
        texto = config['textos']['quatro_horas']
    elif current_hour_brazil == 5:
        texto = config['textos']['cinco_horas']
    elif current_hour_brazil == 6:
        texto = config['textos']['seis_horas']
    elif current_hour_brazil == 7:
        texto = config['textos']['sete_horas']
    elif current_hour_brazil == 8:
        texto = config['textos']['oito_horas']
    elif current_hour_brazil == 9:
        texto = config['textos']['nove_horas']
    elif current_hour_brazil == 10:
        texto = config['textos']['dez_horas']
    elif current_hour_brazil == 11:
        texto = config['textos']['onze_horas']
    elif current_hour_brazil == 0:
        texto = config['textos']['doze_horas']

    await enviar_mensagem_com_reacao(client, config['canais']['taverna'], texto, config['emojis']['caveira'])

@client.event
async def on_ready():
    logging.info(f'Bot logado como: {client.user}')
    if not mensagemProgramada.is_running():
        mensagemProgramada.start()
        logging.info('Mensagem programada configurada!')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    
#     if message.author.name == 'daniel.lucredio' or message.author.nm == 'lopestay':
#         if message.content.startswith('É meia noite!'):
#             await enviar_mensagem_com_reacao(client, config['mensagem_diaria']['canal'], config['mensagem_diaria']['texto'], config['mensagem_diaria']['emoji_reacao'])

client.run(config_token['token_bot'], root_logger=True)
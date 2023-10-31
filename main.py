import datetime
import gspread
import discord
from discord.ext import tasks
from discord.ext import commands
import yaml
from utils import enviar_mensagem_com_reacao, ler_planilha_interativos, postar_interativo
import logging

# # Configurando logging
logging.basicConfig(filename='events.log', encoding='utf=8', format='%(asctime)s %(levelname)8s %(name)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S')

# Primeiro, vamos carregar as configurações
with open('config.yml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)
with open('token.yml', 'r', encoding='utf-8') as file:
    config_token = yaml.safe_load(file)

canal_comandos = int(config['canal_comandos'])

# Configuração do cliente Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$$', intents=intents)

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
                  datetime.time(hour=12),
                  datetime.time(hour=13), 
                  datetime.time(hour=14), 
                  datetime.time(hour=15), 
                  datetime.time(hour=16), 
                  datetime.time(hour=17),
                  datetime.time(hour=18),
                  datetime.time(hour=19),
                  datetime.time(hour=20),
                  datetime.time(hour=21),
                  datetime.time(hour=22),
                  datetime.time(hour=23)])
async def mensagems_programadas():
    config_msg = config['mensagens_programadas']

    now = datetime.datetime.now()
    hora_local = now.hour

    chave_mensagem = f'texto_{hora_local}h'

    if not chave_mensagem in config_msg:
        logging.info(f'Nenhuma mensagem configurada: {chave_mensagem}')
    else:
        logging.info(f'Postando mensagem configurada: {chave_mensagem}')
        texto = config_msg[chave_mensagem]

        await enviar_mensagem_com_reacao(bot, config_msg['canal'], texto, config_msg['emoji_reacao'])

# Vamos configurar a tarefa dos interativos recorrentes
@tasks.loop(time=[datetime.time(hour=16, minute=30)])
async def interativos_programados():
    logging.info(f'Publicando interativos programados...')
    await publicar_hoje()

@bot.event
async def on_ready():
    logging.info(f'Bot logado como: {bot.user}')
    if not mensagems_programadas.is_running():
        mensagems_programadas.start()
        logging.info('Mensagem de hora em hora configurada')

    if not interativos_programados.is_running():
        interativos_programados.start()
        logging.info('Interativos programados configurados')

@bot.command()
async def ping(ctx):
    if pode_executar_comando(ctx):
        await ctx.send(f'pong')

@bot.command()
async def publicar_interativo(ctx):
    if pode_executar_comando(ctx):
        await ctx.send(f'Publicando o interativo de hoje, só um minuto...')
        await publicar_hoje()
        await ctx.send(f'Prontinho!')

async def publicar_hoje():
    now = datetime.datetime.now()
    dia = now.day
    mes = now.month
    try:
        interativos_programados=config['interativos_programados']
        gc = gspread.service_account(filename=interativos_programados['arquivo_credenciais'])
        planilha = gc.open_by_key(interativos_programados['id_planilha'])
        dados_postagem = ler_planilha_interativos(planilha=planilha, dia=dia, mes=mes)
        canal_postagem = dados_postagem['canal']
        await postar_interativo(bot=bot, canal=canal_postagem, dados_postagem=dados_postagem)
    except Exception as e:
        # if 'WorksheetNotFound' in str(e):
        #     await ctx.send(f'Nada a postar em {dia}/{mes}')
        # elif 'index' in str(e) and 'not found' in str(e):
        #     await ctx.send(f'Nada a postar em {dia}/{mes}')
        # else:
        #     await ctx.send(f'{e}')
        logging.error(e)
        raise

@bot.command()
async def preview_interativo(ctx, diaMes):
    if pode_executar_comando(ctx):
        try:
            args = diaMes.split('/')
            dia = int(args[0])
            mes = int(args[1])
        except Exception as e1:
            await ctx.send(f'O jeito certo de usar é $preview_interativo dia/mês')
            print(e1)
            raise
        try:
            await ctx.send(f'Preview de {dia}/{mes}, certo! Só um minuto...')
            interativos_programados=config['interativos_programados']
            gc = gspread.service_account(filename=interativos_programados['arquivo_credenciais'])
            planilha = gc.open_by_key(interativos_programados['id_planilha'])
            dados_postagem = ler_planilha_interativos(planilha=planilha, dia=dia, mes=mes)
            dados_postagem['cargo'] = None # Assim não fica marcando nos previews
            canal_postagem = interativos_programados['canal_preview_mensagens']
            if dados_postagem['tipo'].startswith("t"):
                canal_postagem = interativos_programados['canal_preview_forum']
            await postar_interativo(bot=bot, canal=canal_postagem, dados_postagem=dados_postagem)
            await ctx.send(f'Prontinho!')
        except Exception as e:
            if 'WorksheetNotFound' in str(e):
                await ctx.send(f'Nada a postar em {dia}/{mes}')
            elif 'index' in str(e) and 'not found' in str(e):
                await ctx.send(f'Nada a postar em {dia}/{mes}')
            else:
                await ctx.send(f'{e}')
            logging.error(e)
            raise

def pode_executar_comando(ctx):
    return ctx.channel.id == canal_comandos

bot.run(config_token['token_bot'], root_logger=True)
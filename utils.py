import discord
import logging

async def enviar_mensagem_com_reacao(bot, canal, texto, reacao):
    channel = bot.get_channel(canal)
    if not channel:
        raise Exception(f'Erro ao enviar mensagem "{texto}": canal {canal} não encontrado')
    else:
        mensagem = await channel.send(texto)
        await mensagem.add_reaction(reacao)

def criar_embed(cor, titulo, descricao, url_imagem, rodape):
    embed = discord.Embed(color=cor, title=titulo, description=descricao)
    embed.set_image(url=url_imagem)
    embed.set_footer(text=rodape)
    return embed

async def enviar_mensagem_embed(bot, canal, cargo, embed):
    channel = bot.get_channel(canal)
    if not channel:
        raise Exception(f'Erro ao enviar mensagem com embed: canal {canal} não encontrado')
    else:
        if(cargo):
            await channel.send(f"<@&{cargo}>")
        else:
            await channel.send("<Marcação do cargo>")
        await channel.send(embed=embed)

async def criar_thread_embed(bot, canal, cargo, embed, nome_thread, conteudo_thread):
    channel = bot.get_channel(canal)
    if not channel:
        raise Exception(f'Erro ao criar thread com embed: fórum {canal} não encontrado')
    else:
        cargoStr = "<Marcação do cargo> "
        if cargo:
            cargoStr = f"<@&{cargo}> "
        await channel.create_thread(name=nome_thread,embed=embed,content=cargoStr+conteudo_thread)

def ler_planilha_interativos(planilha, dia, mes):
    logging.info(f'Lendo planilha...')
    worksheet = planilha.get_worksheet(mes-1)
    row = dia+1

    logging.info(f'Planilha lida')

    tipoPostagem = worksheet.cell(row,2).value
    if not tipoPostagem:
        raise Exception(f'Nada a postar em {dia}/{mes}')
    else:
        return {
            "tipo": worksheet.cell(row,2).value,
            "canal": int(worksheet.cell(row,3).value),
            "cargo": worksheet.cell(row,4).value,
            "nome_thread": worksheet.cell(row,5).value,
            "conteudo_thread": worksheet.cell(row,6).value,
            "titulo": worksheet.cell(row,7).value,
            "descricao": worksheet.cell(row,8).value,
            "rodape": worksheet.cell(row,9).value,
            "url_imagem": worksheet.cell(row,10).value,
            "cor": int("0x"+worksheet.cell(row,11).value,16)
        }

async def postar_interativo(bot, canal, dados_postagem):
    logging.info(f'Criando postagem: {dados_postagem}')

    embed=criar_embed(cor=dados_postagem['cor'], titulo=dados_postagem['titulo'], descricao=dados_postagem['descricao'], url_imagem=dados_postagem['url_imagem'], rodape=dados_postagem['rodape'])
    if dados_postagem['tipo'].startswith("m"):
        await enviar_mensagem_embed(bot=bot, cargo=dados_postagem['cargo'], canal=canal, embed=embed)
    elif dados_postagem['tipo'].startswith("t"):
        await criar_thread_embed(bot=bot, canal=canal, cargo=dados_postagem['cargo'], nome_thread=dados_postagem['nome_thread'], conteudo_thread=dados_postagem['conteudo_thread'], embed=embed)
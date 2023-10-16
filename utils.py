import logging

async def enviar_mensagem_com_reacao(client, canal, texto, reacao):
    channel = client.get_channel(canal)
    if not channel:
        logging.error(f'Erro ao enviar mensagem "{texto}": canal {canal} não encontrado')
    else:
        mensagem = await channel.send(texto)
        await mensagem.add_reaction(reacao)

# Configuração da planilha do Google

Vamos seguir as instruções que estão [aqui](https://docs.gspread.org/en/latest/oauth2.html):

1. Vá até o [Google developer console](https://console.developers.google.com/) e crie um novo projeto (ou escolha um existente)
2. Na caixa onde aparece "ATIVAR APIS E SERVIÇOS", procure "Google Drive API" e escolha "ATIVAR"
3. Na caixa onde aparece "ATIVAR APIS E SERVIÇOS", procure "Google Sheets API" e escolha "ATIVAR"
4. Agora vá para "Credenciais" > "Criar credenciais" > "Conta de serviço"
5. Preencha o formulário
6. Clique em "CONCLUIR"
7. Vá em "Gerenciar contas de serviço"
8. Aperte nos pontinhos perto do serviço recém-criado e selecione "Gerenciar chaves"
9. Escolha "Adicionar chave" > "Criar nova chave" > "JSON"
10. Vai ser criado um novo arquivo JSON que será salvo automaticamente em sua máquina.
11. Salve o arquivo com o nome "gspreadcredentials.json" (é o nome padrão configurado no bot) e mova-o para a pasta do bot ("discord-bot-1")
12. Nesse arquivo, vai ter um campo de e-mail, chamado `client_email`:

```json
{
...
  "client_email": "bot-610@cabana-das-palavras.iam.gserviceaccount.com",
...
}
```
13. Copie este e-mail
14. Faça upload, em algum lugar do seu Google Drive, da [planilha de exemplo](./planilhaExemplo/planilhaTeste.xlsx). IMPORTANTE: é uma planilha do Excel (XLSX). Você precisa "Salvar como planilha do google". Depois que fizer isso, pode renomear a vontade, e compartilhar com quem vai trabalhar nela.
15. Compartilhe também com o endereço de e-mail que você copiou agora há pouco. Dê acesso de "Editor", pois assim o bot poderá modificar a planilha, caso necessário
16. Agora você vai precisar do id da planilha, para o bot. Na barra do navegador, é só copiar o número que vem na URL, depois do `/d/` e antes do `#`:

`https://docs.google.com/spreadsheets/d/1X5jQthT0-jQNm7DsdPeTh4kzk7e3tAhKP5afENpRgMc/edit#gid=1306331851`

Neste caso, o id é `1X5jQthT0-jQNm7DsdPeTh4kzk7e3tAhKP5afENpRgMc`

17. Coloque este id na [configuração do bot](./configuracaoBotDiscord.md) e pronto!
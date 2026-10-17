# Publicação

## Destino e estado da entrega

O destino definitivo, confirmado pelo usuário, é o repositório existente [bernardo18377/DIO-Bernardo-EXCEL-IA-4](https://github.com/bernardo18377/DIO-Bernardo-EXCEL-IA-4). Esse é o link do repositório para submissão à DIO.

A entrega está preparada com `index.html`, dados sanitizados, documentação, evidências e testes na raiz do projeto. Por solicitação do usuário, os arquivos descompactados substituem o arquivo `dashboard-porsche-sales.zip` enviado anteriormente. O ZIP inicial foi enviado no commit `4704459`, e seu download foi conferido com resposta HTTP 200. A planilha original, os nomes de pessoas e arquivos locais desnecessários permanecem fora da entrega.

O envio por Git funciona neste ambiente. As chamadas à API do GitHub receberam HTTP 403 pelo túnel, mas esse bloqueio não impediu o envio Git ao repositório existente. Um rascunho de configuração de rede foi salvo anteriormente; ele não foi aplicado à máquina em execução. Não é necessário fornecer credenciais no chat para repetir o fluxo Git já autorizado.

**GitHub Pages permanece pendente de configuração e confirmação.** A presença dos arquivos no GitHub não comprova que a dashboard esteja publicada. Nenhuma URL de site ativo foi presumida ou registrada.

## Concluir a publicação no GitHub Pages

1. No [repositório existente](https://github.com/bernardo18377/DIO-Bernardo-EXCEL-IA-4), confira a branch `main`: `index.html` deve estar na raiz, junto dos demais arquivos do projeto, e o ZIP deve ter sido removido.
2. Abra **Settings → Pages → Build and deployment**.
3. Em **Source**, escolha **Deploy from a branch**. Selecione a branch **main**, a pasta **/(root)** e clique em **Save**. O HTML é autossuficiente; não exige build, servidor de aplicação ou instalação de dependências.
4. Acompanhe o resultado do deploy e copie a URL informada pelo próprio GitHub Pages. Abra esse endereço, confira os quatro indicadores com a validação local e aplique pelo menos um filtro.
5. Somente depois dessa confirmação, registre no README o endereço real da dashboard e envie a atualização ao mesmo repositório. Mantenha separado o link do repositório para submissão e o link do site para visualização.

A referência fornecida no pedido é [Configuring a publishing source for your GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site). Sua abertura neste ambiente recebeu HTTP 403 pelo túnel; ela é citada como referência indicada, não como página consultada com sucesso.

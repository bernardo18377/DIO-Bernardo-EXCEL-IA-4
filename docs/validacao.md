# Validação realizada

Os resultados abaixo se referem aos arquivos locais entregues e à planilha anexada. Não representam uma publicação do GitHub Pages. As verificações foram executadas na raiz do projeto com Python 3.12.14, openpyxl 3.1.5, Playwright 1.62.0 e Chromium 154.0.8037.57. O JavaScript da interface também passou em `node --check` com Node 24.19.0.

## Fonte e cálculos independentes

A planilha foi aberta de verdade antes da implementação, incluindo nomes de abas, cabeçalhos, tipos das células, ausências, categorias, identificadores e fórmulas. A integridade do ZIP interno do XLSX foi conferida sem erros. A aba `Sanitized` tem 100 registros, 21 colunas e nenhuma fórmula. Preço e ano sanitizados são textos; a extração converte ambos explicitamente.

SHA-256 da fonte: `f874650657ca4e1a99fd4462b297bfc5fd9915e8e693956d9cec47eda2cb2e2d`.

| Medida | Resultado recalculado |
| --- | ---: |
| Importados / IDs únicos | 100 / 100 |
| Cancelados / comerciais | 7 / 93 |
| Soma nominal em centavos | 1.282.780.050 |
| Soma comercial em centavos | 1.220.255.050 |
| Valor comercial em USD | 12.202.550,50 |
| Ticket comercial em USD, arredondado para exibição | 131.210,22 |
| Entregues comerciais | 41 |
| Datas inválidas: fonte / comerciais | 24 / 23 |
| Preços inválidos ou ausentes | 0 |
| Datas válidas mínima / máxima | 2024-03-14 / 2027-10-01 |

O oráculo dos testes de navegador reabre a planilha com openpyxl e calcula preços com `Decimal`, sem importar o script de preparação nem usar a renderização como referência. Os testes de preparação também fazem uma segunda leitura da fonte. As comparações incluem IDs, preços, situação, datas, valores exibidos e todos os grupos de modelos, estados e pagamentos.

Reconciliação completa: **39 modelos, 32 estados e 9 métodos** no conjunto comercial. A soma das quantidades de cada agrupamento é 93; a soma dos valores é 1.220.255.050 centavos. Não se tenta somar os três agrupamentos entre si, pois descrevem as mesmas vendas por perspectivas diferentes.

Conferências exemplares independentes:

- `911 Dakar`: 3 pedidos, USD 810.600,00; líder de valor por modelo.
- `CA`: 16 pedidos, USD 1.973.350,00; 17,2% do volume comercial.
- `Wire Transfer`: 26 pedidos, USD 3.979.450,00; 28,0% do volume comercial.
- Ano da venda 2024: 10 pedidos; 2025: 17; 2026: 29; 2027: 14; sem data válida: 23.

## Comandos e resultados

`PORSCHE_SOURCE` foi apontada para o arquivo XLSX anexado, mantido fora do repositório. Comandos executados, com o caminho da fonte representado pela variável:

```sh
python3 scripts/preparar_dados.py "$PORSCHE_SOURCE" --html index.html
python3 -m unittest discover -s tests -p 'test_preparar_dados.py' -v
python3 -m unittest discover -s tests -p 'test_dashboard_browser.py' -v
python3 scripts/capturar_evidencias.py
```

| Verificação | Resultado efetivamente observado |
| --- | --- |
| Preparação do JSON e incorporação no HTML | Concluídas com os metadados acima. |
| Suíte `test_preparar_dados.py` com a fonte | **16 testes aprovados**, nenhum ignorado ou falho. |
| Suíte `test_dashboard_browser.py` com a fonte | **8 testes aprovados e 1 ignorado**, nenhum falho após o ajuste do modo de carregamento. |
| HTTP local, HTML idêntico ao arquivo | **200**, bytes da resposta iguais ao `index.html`. |
| Filtro CA após desativar a rede no navegador | **16 pedidos**, **197.335.000 centavos**, 7 entregues e 5 sem data válida. |
| Console e JavaScript no smoke test final | Nenhum erro. |
| Requisições externas durante testes/capturas | Nenhuma observada. |

As duas suítes totalizam **24 testes aprovados e 1 ignorado explicitamente**. Subcenários de filtros e fixtures não são contados como novos testes do runner. O teste HTTP e as capturas são verificações adicionais, não incluídas nessa contagem.

### Cobertura dos testes de preparação

Conversões dos exemplos do pedido; preço zero; ausências, negativos, não finitos e textos monetários inválidos; ano inteiro; datas impossíveis e ano bissexto; preservação de datas futuras; limite inteiro seguro individual e acumulado; IDs repetidos; vendas semelhantes com IDs diferentes; rejeição de fórmulas sem recálculo verificado; campos obrigatórios; preservação dos bytes da fonte; reprodutibilidade; remoção de campos pessoais; serialização segura e substituição exclusiva do bloco JSON.

### Cobertura dos testes no navegador

- Carregamento inicial com as quatro métricas comparadas à fonte independente.
- Cada um dos seis filtros, uma combinação real de modelo e estado e uma combinação real sem resultados.
- `Sem data válida`, ano da venda 2024 e limpeza com restauração das 93 vendas, inclusive as 23 sem data.
- IDs e oito células de cada linha comercial: modelo, cidade/estado, ano do modelo, data, pagamento, situação e valor, além do ID.
- Grupos completos, contagens, somas, ticket, percentuais do recorte, tabelas de apoio, rótulos das barras e respostas textuais.
- Expansão dos rankings para todas as categorias e retorno às dez primeiras.
- Labels, seleção pelo teclado, limpeza por Enter e indicador de foco visível.
- Larguras de 360 e 1440 px, sem rolagem horizontal do documento nem controles fora da área visível.
- Fixtures temporárias separadas: conjunto vazio, preço zero, preço ausente e cobertura parcial. As fixtures não foram incorporadas aos dados publicados.
- HTML carregado por `set_content` com contexto de navegador offline, monitorando erros de JavaScript, console e solicitações de rede.

## Problemas encontrados e tratamento

O Chromium gerenciado bloqueou a navegação para `file://` com `net::ERR_BLOCKED_BY_ADMINISTRATOR`. A primeira tentativa da suíte falhou durante o carregamento. A configuração gerenciada permite HTTP/HTTPS e bloqueia outros esquemas; não foi modificada. Os testes comportamentais passaram a carregar os bytes locais pelo método `set_content` com a rede desativada. O teste separado de navegação direta permaneceu no arquivo e é explicitamente ignorado somente quando recebe esse erro. **A abertura por duplo clique não foi verificada neste ambiente**; não é um resultado aprovado nem uma falha diagnosticada da aplicação.

No primeiro smoke test HTTP houve um erro de console causado pela busca automática de `/favicon.ico`, inexistente. Foi adicionado um favicon SVG incorporado por data URI. A repetição do smoke test passou, sem erros ou recursos externos. Nenhuma regra de negócio precisou ser alterada para fazer testes passar.

## Evidências visuais reais

O comando `python3 scripts/capturar_evidencias.py` inicia um servidor apenas no loopback, verifica o HTML recebido, desativa a rede no contexto do navegador, captura a visão geral e aplica o filtro CA. Ao terminar, fecha o navegador e o servidor.

- [Visão geral, 1440 px](img/visao-geral.png): 93 pedidos, USD 12.202.550,50.
- [Filtro CA aplicado, 1440 px](img/filtro-aplicado.png): 16 pedidos, USD 1.973.350,00.
- [Visão móvel, 360 px](img/mobile.png): recorte geral restaurado, sem overflow do documento.

As capturas são screenshots do Chromium com os dados reais; não foram fabricadas nem geradas por um modelo de imagens. A revisão visual confirmou a distribuição dos cards, barras, filtros e rolagem restrita à tabela. A verificação de teclado não constitui uma auditoria completa com tecnologias assistivas.

## Auditoria dos arquivos da entrega

A comparação final confirmou que o JSON incorporado no HTML é igual ao arquivo tratado; `docs/prompt.md` é uma cópia byte a byte do Markdown recebido; o SHA-256 da planilha permanece inalterado; e nenhum link relativo da documentação aponta para arquivo inexistente. A inspeção dos recursos HTML não encontrou carregamentos remotos. Uma busca pelos valores reais das duas colunas de nomes da fonte não encontrou esses nomes em nenhum dos 12 arquivos textuais auditados. A fonte não está no checkout e o padrão Excel de `.gitignore` foi conferido com `git check-ignore`. `git diff --check` não apontou problemas de espaço em branco.

Foi gerado inicialmente um pacote ZIP com somente os arquivos do projeto, incluindo as capturas reais e excluindo `.git`, caches e a planilha original. Os bytes extraídos de suas 16 entradas foram comparados aos arquivos locais e a integridade do ZIP foi verificada. A pedido do autor, a versão final no GitHub substitui esse ZIP pelos arquivos descompactados na raiz do repositório.

## Publicação e consultas externas

`git ls-remote --exit-code origin refs/heads/main` confirmou leitura do repositório de trabalho. `gh api user` e a consulta ao novo repositório inicialmente solicitado retornaram `Forbidden`. Uma consulta HTTPS independente à API identificou **túnel de saída bloqueado com HTTP 403**. Isso impediu confirmar a conta pela API e testar a criação de outro repositório. A presença de autenticação da plataforma não foi interpretada como garantia de acesso à API, nem foi solicitado um token no chat.

O autor posteriormente escolheu explicitamente o destino existente [bernardo18377/DIO-Bernardo-EXCEL-IA-4](https://github.com/bernardo18377/DIO-Bernardo-EXCEL-IA-4). O envio via Git nativo funcionou: o ZIP foi enviado no commit `4704459555ae9aaf5995983ed9b2a6975c919361`, relido do remoto e baixado por HTTP 200 com bytes idênticos ao original. Portanto, o bloqueio da API não impede o envio Git ao repositório autorizado. O refinamento final solicitado foi remover o ZIP e disponibilizar todos os arquivos do projeto descompactados, com `index.html` na raiz e documentação atualizada para esse destino.

Na conferência da entrega descompactada, os links relativos continuaram válidos e a fonte, o prompt e o JSON incorporado foram novamente comparados. Um smoke test HTTP temporário confirmou resposta 200 idêntica ao HTML; depois de desativar a rede, o filtro CA manteve 16 pedidos e 197.335.000 centavos e a limpeza restaurou 93 pedidos e 1.220.255.050 centavos. Não houve erros de JavaScript, console, requisições externas ou overflow em 360 e 1440 px. As suítes completas não foram repetidas, pois a lógica e os dados não mudaram; as capturas existentes foram preservadas.

A página do repositório respondeu HTTP 200. A tentativa de verificar o endereço de Pages encontrou `Tunnel connection failed: 403 Forbidden`; nenhum site ativo foi confirmado. Disponibilizar as fontes no GitHub e ativar o GitHub Pages são etapas distintas. A configuração de Pages permanece descrita para `main` e `/(root)`, sem afirmar que foi ativada pela API.

A referência do professor e a documentação do Pages também ficaram inacessíveis por HTTP 403 no túnel. Não foram usadas como páginas consultadas com sucesso. A planilha anexada foi suficiente para concluir a implementação local.

Foram salvos no **rascunho de configuração do ambiente** os domínios `api.github.com`, `docs.github.com` e `bernardo18377.github.io`, preservando os presets. O retorno confirmou `status: saved` e exigência de publicação do ambiente. Esse salvamento não mudou a rede em execução, criou repositório ou publicou o site. A ativação da dashboard no Pages continua pendente; não há URL ativa verificada.

O diagnóstico e os passos exatos para concluir estão em [publicacao.md](publicacao.md). Nenhuma consulta externa bloqueada foi declarada bem-sucedida, e nenhuma URL de Pages foi presumida.

# Preparação e auditoria da base

A dashboard usa somente a aba `Sanitized` da planilha real fornecida no pedido. A planilha foi aberta com Python 3.12.14 e openpyxl 3.1.5, preservando os bytes da entrada. As colunas cruas foram identificadas para entender a estrutura; os valores analíticos vêm das colunas sanitizadas. Nenhum nome de cliente ou vendedor é copiado para o JSON, o HTML ou as mensagens do script.

## Origem e identificação

- Arquivo: `8683bed0-cc33-4e06-bca9-04db9c31f9e2.xlsx`.
- Fonte pública indicada no desafio: https://hermes.dio.me/files/assets/8683bed0-cc33-4e06-bca9-04db9c31f9e2.xlsx. A execução utilizou o anexo local, sem precisar baixar essa URL.
- Aba encontrada: `Sanitized`; 21 colunas e 100 registros não vazios.
- SHA-256 da entrada: `f874650657ca4e1a99fd4462b297bfc5fd9915e8e693956d9cec47eda2cb2e2d`.
- Identificadores inteiros de 6 a 105, todos únicos.
- Nenhuma fórmula encontrada; nenhuma célula ausente nas colunas analíticas usadas. Preço e ano do modelo estão armazenados como texto na fonte.

A planilha original permanece fora do versionamento porque contém `customer_name` e `salesperson`. A extração publicada é `data/vendas-sanitizadas.json`, e a dashboard incorpora exatamente esse objeto no bloco JSON `vendas-data`.

## Dicionário e regras

| Campo publicado | Coluna da fonte | Tipo e regra |
| --- | --- | --- |
| `id` | `sale_id` | Identificador original; inteiro na fonte atual. Não é uma numeração nova. |
| `data_venda` | `SaleDateSanitized` | Texto ISO `AAAA-MM-DD` validado pelo calendário ou `null`. |
| `modelo` | `PorscheModelSanitized` | Texto preservado; versões como `911 GT3` e `911 GT3 RS` continuam distintas. |
| `ano_modelo` | `ModelYearSanitized` | Inteiro entre 1 e 9999; entrada incompatível vira `null`, com contagem nos metadados. Não representa o ano da venda. |
| `preco_centavos` | `SalesPriceSanitized` | Inteiro em centavos de USD ou `null` quando inválido/ausente. |
| `pagamento` | `PayMethodSanitized` | Categoria preservada; `Wire Transfer`, `Bank Transfer` e `ACH Payment` não são fundidos. |
| `cidade` | `CitySanitized` | Texto preservado; filtros e tabela também identificam o estado. |
| `estado` | `StateSanitized` | Sigla de estado dos Estados Unidos, preservada. |
| `status_entrega` | `DeliveryStatusSanitized` | Categoria original, inclusive `Cancelled` para rastreabilidade. |

`VehicleMileageSanitized` existe, mas não foi incluída porque as três perguntas não utilizam quilometragem. Os demais campos crus e dados pessoais também não são exportados.

Preços são validados integralmente, aceitando somente dígitos e um ponto decimal opcional com uma ou duas casas. Não se aceitam símbolos monetários, separador de milhar, espaços, sufixos, expoentes, negativos, não finitos ou precisão além dos centavos. A conversão usa `Decimal` e não arredonda a entrada. Zero é um preço válido, distinto de ausência. Exemplos verificados: `79500.00` → `7950000`; `153200.50` → `15320050`; `0.00` → `0`.

O limite de cada preço e da soma total é `2^53 − 1` centavos, para permitir cálculo inteiro exato no JavaScript. Como todos os preços aceitos são não negativos, qualquer subconjunto também respeita esse limite. A preparação interrompe com explicação se o limite for excedido; não transforma esse excesso silenciosamente em zero.

Datas usam formato ISO estrito e validação real de calendário. `INVALID`, ausência e datas impossíveis como `2024-02-30` viram `null`, sem deslocamento para outro mês. Esses registros permanecem em todas as análises sem filtro de ano da venda. O intervalo válido observado é **2024-03-14 a 2027-10-01**. As datas de 2027 permanecem na base didática; não há exclusão por comparação com a data de execução.

Preços inválidos ou ausentes também mantêm o registro. Só o preço fica fora das somas e do denominador do ticket, e os metadados informam a cobertura. Categorias de texto ausentes recebem explicitamente `Não informado`, com contagem por campo; não houve ocorrência na fonte atual. IDs ausentes/incompatíveis ou repetidos interrompem a preparação. Vendas com modelo, local e preço iguais permanecem distintas quando seus IDs são diferentes.

O script verifica fórmulas em toda a aba. O openpyxl não recalcula planilhas, por isso qualquer fórmula interrompe a importação e pede resultados recalculados e verificados. Não presume que um cache vazio seja zero nem considera um cache automaticamente confiável.

O JSON usa `allow_nan=False` e escapa `<`, U+2028 e U+2029, inclusive na incorporação em HTML. A opção `--html` substitui exclusivamente o conteúdo de um único `<script id="vendas-data" type="application/json">`; falha se esse marcador estiver ausente ou duplicado e preserva o script da aplicação.

## Critério comercial e resultados recalculados

A unidade é uma venda ou pedido registrado. O conjunto comercial contém todos os registros cujo `status_entrega` é diferente de `Cancelled`; situações pendentes continuam incluídas. Os cancelados são preservados no JSON e excluídos dos filtros, gráficos, indicadores e tabela comerciais. Não há base para inferir dinheiro recebido, lucro ou margem.

| Verificação | Resultado observado |
| --- | ---: |
| Importados / IDs únicos | 100 / 100 |
| IDs duplicados | 0 |
| Cancelados / comerciais | 7 / 93 |
| Datas inválidas, total / comerciais | 24 / 23 |
| Marcadores `INVALID` nas datas | 24 |
| Preços inválidos ou ausentes, total / comerciais | 0 / 0 |
| Cobertura monetária comercial | 93 de 93 (100%) |
| Anos do modelo inválidos | 0 |
| Fórmulas / linhas vazias ignoradas | 0 / 0 |
| Soma nominal dos 100 registros | USD 12,827,800.50 |
| Valor comercial dos 93 pedidos | USD 12,202,550.50 |
| Ticket comercial, arredondado somente para exibição | USD 131,210.22 |
| Entregues no conjunto comercial | 41 |

O ticket é a soma em centavos dividida pela quantidade de preços válidos do mesmo recorte, e não uma média de médias. Nenhum total da tabela acima é uma constante que preenche a interface: são resultados da leitura e agregação da fonte.

A segunda leitura independente da planilha, com `Decimal`, confirmou as somas, contagens e todos os grupos de modelo, estado e pagamento. Exemplos do conjunto comercial completo:

| Pergunta / categoria | Quantidade | Valor registrado | Participação no volume comercial |
| --- | ---: | ---: | ---: |
| Modelo de maior valor: `911 Dakar` | 3 | USD 810,600.00 | 3,23% |
| Estado de maior volume: `CA` | 16 | USD 1,973,350.00 | 17,20% |
| Método de maior volume: `Wire Transfer` | 26 | USD 3,979,450.00 | 27,96% |

Distribuição dos 93 pedidos por ano da venda: 2024 = 10, 2025 = 17, 2026 = 29, 2027 = 14 e sem data válida = 23. A soma é 93; as datas ausentes não recebem um ano artificial.

## Reprodução e testes

Instale as dependências de preparação e verificação com `python -m pip install -r requirements-dev.txt`. A dashboard pronta não precisa delas para abrir.

Mantenha a fonte fora do repositório e defina `PORSCHE_SOURCE` com seu caminho real. A regeneração utiliza:

```bash
python scripts/preparar_dados.py "$PORSCHE_SOURCE" --html index.html
```

Sem `--html`, o script gera apenas `data/vendas-sanitizadas.json`. `--saida` permite mudar o destino e `--aba` permite indicar uma aba explicitamente. A geração é determinística para os mesmos bytes da entrada: não inclui horário, diretório local ou dados pessoais nos metadados.

Os testes de preparação são executados por:

```bash
python -m unittest discover -s tests -p test_preparar_dados.py -v
```

Com `PORSCHE_SOURCE` definido, eles também reabrem a fonte original e conferem a reprodução exata do JSON e a auditoria independente em `Decimal`. Sem a variável, somente esse teste da fonte recebe `skip` explícito; os testes de conversão, segurança, cobertura, duplicatas, fórmulas, limite numérico e reconciliação do JSON continuam executáveis sem a planilha.

Nesta execução, a preparação real e os **16 testes** do arquivo passaram, incluindo a leitura independente da fonte. A entrada foi verificada novamente e permaneceu com o mesmo SHA-256. Os testes de navegador e o estado da publicação ficam em [validacao.md](validacao.md).

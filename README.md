# Dashboard de vendas Porsche

Projeto do desafio da DIO para analisar vendas de carros Porsche. O painel foi feito em HTML, CSS e JavaScript e tem filtros de modelo, estado, cidade, ano do modelo, ano da venda e pagamento.

## Como abrir

Baixe o repositório e abra o arquivo `index.html` no navegador. Não precisa instalar nada para usar o painel, e ele funciona sem internet.

## Perguntas da análise

- Quais modelos têm o maior valor de vendas?
- Quais estados têm mais vendas?
- Quais são os métodos de pagamento mais usados?

Na base completa, o **911 Dakar** lidera em valor, com **USD 810.600,00**. A **Califórnia** tem o maior número de vendas, com **16 pedidos**. O pagamento mais usado é **Wire Transfer**, presente em **26 pedidos**. Os resultados mudam conforme os filtros.

## Sobre os dados

A [planilha é fornecida pela DIO](https://hermes.dio.me/files/assets/8683bed0-cc33-4e06-bca9-04db9c31f9e2.xlsx). Foi usada a aba `Sanitized`, com 100 registros.

- Os 7 pedidos cancelados ficam fora da análise.
- Os 93 pedidos restantes somam **USD 12.202.550,50**, com ticket médio de **USD 131.210,22** e 41 entregues.
- Há 23 pedidos não cancelados sem data válida. Eles continuam nos totais, mas não entram quando um ano da venda é selecionado.
- Ano do modelo e ano da venda são informações diferentes. As datas válidas da base vão de 2024 a 2027.
- Os preços são em dólar americano (USD), sem conversão para reais. Os cálculos usam centavos para manter a precisão.

O valor inclui pedidos com entrega pendente e não representa lucro ou dinheiro recebido. A planilha original não foi incluída no repositório por conter dados pessoais.

## Atualizar a base

Para usar outra cópia da planilha, instale a dependência e execute na pasta do projeto:

```sh
python3 -m pip install -r requirements.txt
python3 scripts/preparar_dados.py /caminho/planilha.xlsx --html index.html
```

## GitHub Pages

Para publicar o painel, vá em **Settings → Pages**, escolha **Deploy from a branch**, selecione **main** e **/(root)** e salve.

Projeto de estudo, sem vínculo oficial com a Porsche.

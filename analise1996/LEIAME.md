# Verificação do salto de janeiro de 1996 (autos de infração do IBAMA)

- Arquivo analisado: `auto_infracao_csv.zip`, baixado em 09/11/2026 do portal de dados abertos do IBAMA.
  - Last-Modified do servidor: 09/11/2026 04:51 GMT.
  - Tamanho: 123.436.750 bytes. O SHA-256 está em `auto_infracao_csv.zip.sha256`.
- URL: https://stibamadadosabertosprd.blob.core.windows.net/dados-abertos/dados/SIFISC/auto_infracao/auto_infracao/auto_infracao_csv.zip
- Scripts:
  - `analise1996.py`: perfil dos anos de 1993 a 1998.
  - `analise1996b.py`: data de lançamento comparada com o ano do auto, de 1988 a 2008. A saída está em `lancamento_por_ano.csv`.
- Natureza: análise exploratória feita pelo pesquisador, somente leitura. Não é resultado das camadas no GitHub Actions.
- Interpretação de `DT_LANCAMENTO`: "data de lançamento (cadastro) do auto no sistema", deduzida pelo nome da coluna. O portal não publica dicionário desse campo.
- Fonte do Sicafi: notícia da Página Rural de 29/07/2005, "Ibama lança sistema que agilizará atendimento ao usuário" (https://www.paginarural.com.br/noticia/21386/). Diz que o Sicafi unificou o SISARR, o SIFISC e o Sicaf, com implantação começando por Mato Grosso.

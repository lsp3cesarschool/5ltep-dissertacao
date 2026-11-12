# Revisão sistemática (Seção 3.1 e Apêndice D)

A busca foi feita na API da [OpenAlex](https://openalex.org) em 9/11/2026. Foram sete buscas, restritas a artigos e revisões publicados de 1/1/2016 a 9/11/2026.

## Arquivos

| Arquivo | O que é |
|---|---|
| `queries.json` | As sete buscas (S1 a S7) |
| `counts.json` | Total de registros por busca |
| `records_raw.csv` | 843 registros únicos, com título, resumo, veículo e as buscas que recuperaram cada um |
| `records_screened.csv` | Os mesmos registros, com a decisão de cada etapa (`stage1`, `stage2`) |
| `stage1_stats.json` | Contagens da etapa 1 |
| `stage2_included_idx.json` | Decisões da etapa 2 (ver abaixo) |
| `prisma.json` | Números do fluxograma PRISMA |
| `included.csv` | Os 59 estudos incluídos, com autores |
| `revisar_excluidos_E5_S1_S5_S6.csv` | Lista usada na conferência dos excluídos (ver abaixo) |

## Etapas

1. **Busca** (`fetch.py`): baixa os registros e remove duplicatas, chegando a 843. O `count.py` confere só os totais. Como a OpenAlex é atualizada continuamente, uma nova busca pode trazer números um pouco diferentes. O arquivo `records_raw.csv` guarda a busca usada na dissertação.
2. **Etapa 1, automática** (`screen1.py`): exclui registros em outro idioma que não inglês ou português (E1, 27 registros), sem resumo (E2, 71) e sem coocorrência de conceito e contexto no título e no resumo (E3, 220). Ficam 525 registros. O script gera `records_stage1.csv`, que não está no repositório porque pode ser recriado.
3. **Etapa 2, leitura de título e resumo:** o pesquisador aplicou os critérios com apoio de uma ferramenta de IA. Os índices dos registros mantidos, contados dentro dos 525, estão em `stage2_included_idx.json`. Os demais ficam fora do escopo (E5, 457).
4. **Fechamento** (`finalize.py`): exclui os registros sem revisão por pares (E4, 9), como repositórios e Zenodo. O script também busca os autores dos 59 incluídos e grava os arquivos finais.
5. **Conferência:** o pesquisador leu os 59 incluídos e revisou os 122 excluídos como E5 que vieram das buscas S1, S5 e S6, as mais próximas do tema. Nenhuma decisão mudou, e por isso a coluna de decisão de `revisar_excluidos_E5_S1_S5_S6.csv` ficou em branco: todos continuaram excluídos (10/11/2026).

## Como reproduzir

Os scripts usam só a biblioteca padrão do Python 3.

```
python screen1.py     # recria records_stage1.csv a partir de records_raw.csv
python finalize.py    # consulta a OpenAlex para buscar os autores dos incluídos
```

Ao rodar a etapa 1 sobre `records_raw.csv`, os números saem iguais aos de `stage1_stats.json`. A etapa 2 aplicada aos índices também reproduz `records_screened.csv` sem divergências.

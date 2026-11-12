"""Triagem 1 (automática, reprodutível): E1 idioma fora de en/pt; E2 sem resumo; E3 sem coocorrência
de conceito-alvo (qualidade/proveniência/anomalia/validação/governança) e contexto (dados abertos/governo/portal/ambiental/CKAN/LLM sobre dados) no título+resumo."""
import csv, re, json
CONCEPT = r"data quality|quality assessment|quality monitoring|metadata quality|provenance|lineage|observability|anomal|outlier|validation|data contract|schema|business rule|integrity constraint|steward|governance|trust"
CONTEXT = r"open data|open government|government data|public sector|public data|data portal|ckan|environmental|administrative data|e-government|municipal|smart cit|official statistic"
LLM = r"large language model|\bllms?\b"
rows = list(csv.DictReader(open("records_raw.csv", encoding="utf-8")))
out = []; stats = {"total": len(rows), "E1_language": 0, "E2_no_abstract": 0, "E3_no_cooccurrence": 0, "kept": 0}
for r in rows:
    text = (r["title"] + " " + r["abstract"]).lower()
    if r["language"] and r["language"] not in ("en", "pt"): r["stage1"] = "E1"; stats["E1_language"] += 1
    elif len(r["abstract"]) < 200: r["stage1"] = "E2"; stats["E2_no_abstract"] += 1
    elif not (re.search(CONCEPT, text) and (re.search(CONTEXT, text) or (re.search(LLM, text) and re.search(r"anomal|data quality|validation", text)))):
        r["stage1"] = "E3"; stats["E3_no_cooccurrence"] += 1
    else: r["stage1"] = "keep"; stats["kept"] += 1
    out.append(r)
with open("records_stage1.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
json.dump(stats, open("stage1_stats.json", "w"), indent=1); print(stats)

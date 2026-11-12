"""Fecha a triagem: E4 = não revisado por pares (venue_type repository/sem veículo) aplicado aos pré-selecionados;
grava records_screened.csv com a decisão de cada registro, prisma.json e included.csv; busca autores dos incluídos."""
import csv, json, sys, time, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rows = list(csv.DictReader(open("records_stage1.csv", encoding="utf-8")))
keep = [r for r in rows if r["stage1"] == "keep"]
inc_idx = set(json.load(open("stage2_included_idx.json")))
for i, r in enumerate(keep):
    if i not in inc_idx: r["stage2"] = "E5_fora_do_escopo"
    elif r["venue_type"] in ("repository", "") or "zenodo" in r["venue"].lower(): r["stage2"] = "E4_sem_revisao_por_pares"
    else: r["stage2"] = "incluido"
for r in rows: r.setdefault("stage2", "")
inc = [r for r in rows if r["stage2"] == "incluido"]
ids = "|".join(r["id"].rsplit("/", 1)[1] for r in inc)
url = "https://api.openalex.org/works?" + urllib.parse.urlencode({"filter": f"openalex:{ids}", "per-page": 200, "select": "id,authorships,biblio,primary_location"})
d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "5ltep-rsl/1.0"}), timeout=90))
au = {w["id"]: ([a["author"]["display_name"] for a in w["authorships"]], w.get("biblio") or {}) for w in d["results"]}
for r in inc:
    names, b = au.get(r["id"], ([], {}))
    r["authors"] = "; ".join(names); r["volume"] = b.get("volume") or ""; r["issue"] = b.get("issue") or ""
    r["pages"] = "-".join(x for x in (b.get("first_page"), b.get("last_page")) if x)
fields = ["id", "doi", "title", "year", "type", "venue", "venue_type", "cited", "language", "strings", "stage1", "stage2"]
with open("records_screened.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
with open("included.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=fields[:10] + ["authors", "volume", "issue", "pages"], extrasaction="ignore"); w.writeheader(); w.writerows(inc)
counts = json.load(open("counts.json", encoding="utf-8")); s1 = json.load(open("stage1_stats.json"))
prisma = {"identified_per_string": {c["id"]: c["retrieved"] for c in counts}, "identified_total": sum(c["retrieved"] for c in counts),
          "duplicates_removed": sum(c["retrieved"] for c in counts) - len(rows), "screened": len(rows),
          "excluded_E1_language": s1["E1_language"], "excluded_E2_no_abstract": s1["E2_no_abstract"], "excluded_E3_no_cooccurrence": s1["E3_no_cooccurrence"],
          "title_abstract_screened": len(keep), "excluded_E5_scope": sum(r["stage2"] == "E5_fora_do_escopo" for r in keep),
          "excluded_E4_not_peer_reviewed": sum(r["stage2"] == "E4_sem_revisao_por_pares" for r in keep), "included": len(inc),
          "by_year": {y: sum(r["year"] == y for r in inc) for y in sorted({r["year"] for r in inc})}}
json.dump(prisma, open("prisma.json", "w"), indent=1); print(json.dumps(prisma))
for r in inc: print(r["year"], "|", r["authors"][:60], "|", r["title"][:80], "|", r["venue"][:30])

"""Busca reprodutível na OpenAlex: cada string, 2016-01-01 a 2026-11-09, tipos article|review. Salva registros brutos e contagens."""
import json, sys, time, urllib.request, urllib.parse, csv
Q = json.load(open("queries.json", encoding="utf-8"))
def abstract(inv):
    if not inv: return ""
    pos = [(i, w) for w, idx in inv.items() for i in idx]
    return " ".join(w for i, w in sorted(pos))
rows = {}; counts = []
for q in Q:
    f = f"title_and_abstract.search:{q['q']},from_publication_date:2016-01-01,to_publication_date:2026-11-09,type:article|review"
    page = 1; n = 0; total = None
    while page:
        time.sleep(1.2)
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode({"filter": f, "per-page": 200, "page": page,
              "select": "id,doi,title,publication_year,type,primary_location,abstract_inverted_index,cited_by_count,language"})
        d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "5ltep-rsl/1.0"}), timeout=90))
        total = d["meta"]["count"]
        for w in d["results"]:
            n += 1
            src = ((w.get("primary_location") or {}).get("source") or {})
            r = rows.setdefault(w["id"], dict(id=w["id"], doi=w.get("doi") or "", title=(w.get("title") or "").strip(), year=w.get("publication_year"),
                       type=w.get("type"), venue=src.get("display_name") or "", venue_type=src.get("type") or "", cited=w.get("cited_by_count"),
                       language=w.get("language") or "", abstract=abstract(w.get("abstract_inverted_index")), strings=[]))
            r["strings"].append(q["id"])
        page = page + 1 if d["results"] and page * 200 < total else None
    counts.append(dict(id=q["id"], topic=q["topic"], query=q["q"], total=total, retrieved=n))
    print(q["id"], total, n)
json.dump(counts, open("counts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open("records_raw.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["id", "doi", "title", "year", "type", "venue", "venue_type", "cited", "language", "strings", "abstract"])
    w.writeheader()
    for r in rows.values(): r = dict(r); r["strings"] = ";".join(r["strings"]); w.writerow(r)
print("unique", len(rows), "sum", sum(c["retrieved"] for c in counts))

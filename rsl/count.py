import json, sys, urllib.request, urllib.parse
Q = json.load(open(sys.argv[1], encoding="utf-8"))
import time
for q in Q:
    time.sleep(3)
    f = f"title_and_abstract.search:{q['q']},from_publication_date:2016-01-01,to_publication_date:2026-11-09"
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode({"filter": f, "per-page": 1, "group_by": "type"})
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "5ltep-rsl/1.0"}), timeout=60))
    tot = sum(g["count"] for g in d["group_by"])
    print(q["id"], tot, {g["key_display_name"]: g["count"] for g in d["group_by"]})

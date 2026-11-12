"""Segunda passada: data de lançamento (cadastro no sistema) x data do auto, por ano, 1988-2008."""
import csv, io, sys, zipfile, collections
sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(10**9)
z = zipfile.ZipFile(sys.argv[1])

def ano(s):
    s = (s or "").strip()
    if len(s) >= 10 and s[4] == "-":
        return int(s[:4])
    if len(s) >= 10 and s[2] == "/":
        return int(s[6:10])
    return None

def dia(s):
    return (s or "").strip()[:10]

print("ano_auto;n;n_UFs;pct_lanc_mesmo_ano_ou_seguinte;pct_lanc_2005_2006;top3_dias_lancamento;pct_unid_top1")
for y in range(1988, 2009):
    n = 0; ufs = set(); prox = 0; lote = 0; dias = collections.Counter(); unid = collections.Counter()
    with z.open(f"auto_infracao_{y}.csv") as fh:
        for r in csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"), delimiter=";"):
            n += 1
            ufs.add(r["UF"])
            a = ano(r["DT_LANCAMENTO"])
            if a is not None and a - y <= 1:
                prox += 1
            if a in (2005, 2006):
                lote += 1
            dias[dia(r["DT_LANCAMENTO"])] += 1
            unid[r["UNID_ARRECADACAO"]] += 1
    top = ", ".join(f"{d} ({c})" for d, c in dias.most_common(3))
    print(f"{y};{n};{len(ufs)};{100*prox/n:.0f};{100*lote/n:.0f};{top};{100*unid.most_common(1)[0][1]/n:.0f}")

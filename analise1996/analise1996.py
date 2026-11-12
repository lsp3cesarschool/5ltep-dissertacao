"""Investiga o salto de jan/1996 no arquivo público de autos de infração do IBAMA (somente leitura)."""
import csv, io, sys, zipfile, collections
sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(10**9)
z = zipfile.ZipFile(sys.argv[1])

def rows(year):
    with z.open(f"auto_infracao_{year}.csv") as fh:
        txt = io.TextIOWrapper(fh, encoding="utf-8", errors="replace")
        rd = csv.DictReader(txt, delimiter=";")
        for r in rd:
            yield r

first = next(rows(1996))
print("COLUNAS:", list(first.keys()))
print()
datecols = [c for c in first if c.upper().startswith(("DAT", "DT_", "DATA"))]
print("colunas de data:", datecols)

for y in range(1993, 1999):
    rs = list(rows(y))
    n = len(rs)
    mes = collections.Counter(r.get("DAT_HORA_AUTO_INFRACAO", "")[3:5] if "/" in r.get("DAT_HORA_AUTO_INFRACAO", "") else r.get("DAT_HORA_AUTO_INFRACAO", "")[5:7] for r in rs)
    print(f"== {y}: {n} registros; por mês: {dict(sorted(mes.items()))}")
    for c in ["TIPO_AUTO", "SERIE", "TP_ORIGEM", "DS_ORIGEM", "SIT_CANCELADO", "UF", "UNID_ARRECADACAO", "SISTEMA", "TIPO_INFRACAO", "DES_STATUS_FORMULARIO", "SIT_ELETRONICO", "FORMA_ENTREGA"]:
        if c in rs[0]:
            print(f"   {c}: {collections.Counter(r[c] for r in rs).most_common(6)}")
    for c in datecols:
        if c != "DAT_HORA_AUTO_INFRACAO":
            anos = collections.Counter((r[c] or "")[:4] if "-" in (r[c] or "")[:5] else (r[c] or "")[6:10] for r in rs)
            print(f"   ano de {c}: {anos.most_common(6)}")
    vazios = {c: sum(1 for r in rs if not (r[c] or "").strip()) / n for c in rs[0]}
    print("   % vazio (colunas >50%):", {c: round(v * 100) for c, v in vazios.items() if v > 0.5})

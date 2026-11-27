"""Periksa data.json sebelum di-commit. Jalankan: python3 scripts/validate.py"""
import json, re, sys
from datetime import date

SEKTOR = {"Perbankan", "Pembiayaan & Asuransi", "FMCG & Distribusi", "Ritel", "Manufaktur"}
WAJIB = ["program", "perusahaan", "tentang", "syarat", "info", "deadline", "iso", "status", "link", "sumber", "sektor", "tags", "cek"]

def main():
    errors = []
    try:
        data = json.load(open("data.json", encoding="utf-8"))
    except Exception as e:
        print(f"data.json tidak bisa dibaca: {e}"); return 1
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(data.get("updated", ""))):
        errors.append("'updated' harus berformat YYYY-MM-DD")
    jobs = data.get("jobs")
    if not isinstance(jobs, list) or not jobs:
        errors.append("'jobs' harus berupa daftar yang tidak kosong"); jobs = []
    seen = set()
    for n, j in enumerate(jobs, 1):
        tag = f"Program #{n} ({j.get('program', '?')})"
        for k in WAJIB:
            if k not in j: errors.append(f"{tag}: field '{k}' tidak ada")
        for k in ["program", "perusahaan", "syarat", "deadline", "status"]:
            if not str(j.get(k, "")).strip(): errors.append(f"{tag}: '{k}' kosong")
        for k in ["link", "sumber"]:
            if not str(j.get(k, "")).startswith("https://"): errors.append(f"{tag}: '{k}' harus diawali https://")
        iso = j.get("iso")
        if iso is not None:
            try: date.fromisoformat(iso)
            except Exception: errors.append(f"{tag}: 'iso' bukan tanggal YYYY-MM-DD atau null")
        if j.get("sektor") not in SEKTOR: errors.append(f"{tag}: sektor '{j.get('sektor')}' tidak dikenal")
        if not isinstance(j.get("tags"), list): errors.append(f"{tag}: 'tags' harus berupa daftar")
        if not isinstance(j.get("cek"), bool): errors.append(f"{tag}: 'cek' harus true atau false")
        key = (j.get("program"), j.get("perusahaan"))
        if key in seen: errors.append(f"{tag}: duplikat")
        seen.add(key)
    if errors:
        print("GAGAL:"); [print(" -", e) for e in errors]; return 1
    print(f"OK: {len(jobs)} program, update {data['updated']}")
    return 0

sys.exit(main())

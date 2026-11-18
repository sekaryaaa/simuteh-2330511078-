
"""bercak.py: analisis bercak SIMUTEH (dipakai ulang mulai P7)."""

import json
import cv2
import numpy as np

from utils_tepi import mask_daun_awal, bercak_awal


# Parameter bawaan
PARAM_BERCAK = {
    "kanal": 2,
    "k": 4.0,
    "se_bentuk": "elips",
    "se_open": 5,
    "se_close": 5,
    "luas_min": 20,
    "bulat_min": 0.5,
    "rasio_maks": 1.8,
    "batas_ringan": 0.1,
    "batas_berat": 2.0,
    "mm_per_px": 0.4375,
}


# Bentuk structuring element
_BENTUK = {
    "elips": cv2.MORPH_ELLIPSE,
    "persegi": cv2.MORPH_RECT,
    "silang": cv2.MORPH_CROSS
}


def _se(p, uk):
    """Membuat structuring element sesuai parameter."""
    return cv2.getStructuringElement(
        _BENTUK[p["se_bentuk"]],
        (uk, uk)
    )


def bersihkan(biner, p):
    """Membersihkan mask bercak menggunakan opening dan closing."""

    # TODO 1: Opening
    if p["se_open"] > 0:
        biner = cv2.morphologyEx(
            biner,
            cv2.MORPH_OPEN,
            _se(p, p["se_open"])
        )

    # TODO 2: Closing
    if p["se_close"] > 0:
        biner = cv2.morphologyEx(
            biner,
            cv2.MORPH_CLOSE,
            _se(p, p["se_close"])
        )

    return biner


def ukur_dan_saring(biner, p):
    """Mengukur dan menyaring komponen bercak berdasarkan ukuran dan bentuk."""

    # TODO 3: Label komponen terhubung dengan konektivitas 8
    n, lbl, st, cen = cv2.connectedComponentsWithStats(
        (biner > 0).astype(np.uint8),
        connectivity=8
    )

    keluar = np.zeros_like(biner)
    daftar = []

    # TODO 4: Mengukur setiap komponen
    for i in range(1, n):

        # Mengambil kontur komponen
        kontur, _ = cv2.findContours(
            (lbl == i).astype(np.uint8),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_NONE
        )

        if len(kontur) == 0:
            continue

        cnt = kontur[0]

        # Luas komponen dalam piksel
        A = int(st[i, cv2.CC_STAT_AREA])

        # Keliling komponen
        keliling = cv2.arcLength(cnt, True)

        # Kebulatan
        kebulatan = (
            0.0 if keliling == 0
            else 4 * np.pi * A / keliling**2
        )

        # Rasio aspek
        w, h = cv2.minAreaRect(cnt)[1]
        rasio = max(w, h) / max(min(w, h), 1)

        # Luas dalam mm persegi
        luas_mm2 = A * p["mm_per_px"]**2

        # TODO 5: Penyaringan berdasarkan luas, kebulatan, dan rasio
        if (
            A >= p["luas_min"]
            and kebulatan >= p["bulat_min"]
            and rasio <= p["rasio_maks"]
        ):

            keluar[lbl == i] = 255

            daftar.append({
                "label": i,
                "luas_px": A,
                "luas_mm2": round(luas_mm2, 2),
                "keliling_px": round(keliling, 1),
                "kebulatan": round(kebulatan, 2),
                "rasio_aspek": round(rasio, 2),
                "cx": int(cen[i][0]),
                "cy": int(cen[i][1])
            })

    return keluar, daftar


def analisis_daun(img_praproses, p=None):
    """Masukan: citra BGR hasil praproses. Keluaran: kamus hasil analisis."""

    p = {**PARAM_BERCAK, **(p or {})}

    # Membuat mask daun
    m_daun = mask_daun_awal(img_praproses)

    # Membuat mask bercak awal
    biner = bercak_awal(
        img_praproses,
        m_daun,
        kanal=p["kanal"],
        k=p["k"]
    )

    # Membersihkan dan menyaring bercak
    m_bersih = bersihkan(biner, p)
    m_bercak, daftar = ukur_dan_saring(m_bersih, p)

    # TODO 6: Menghitung persentase bercak
    luas_daun = cv2.countNonZero(m_daun)
    luas_bercak = cv2.countNonZero(m_bercak)

    if luas_daun > 0:
        persen = luas_bercak / luas_daun * 100
    else:
        persen = 0.0

    # TODO 7: Menentukan kelas kondisi daun
    if persen >= p["batas_berat"]:
        kelas = "Berat"
    elif persen >= p["batas_ringan"]:
        kelas = "Ringan"
    else:
        kelas = "Sehat"

    return {
        "mask_daun": m_daun,
        "mask_bercak": m_bercak,
        "jumlah_bercak": len(daftar),
        "persen_bercak": round(float(persen), 3),
        "kelas": kelas,
        "bercak": daftar
    }


def simpan_param(p, path="../hasil/param_bercak.json"):
    """Menyimpan parameter bercak ke file JSON."""

    with open(path, "w") as f:
        json.dump({**PARAM_BERCAK, **p}, f, indent=2)

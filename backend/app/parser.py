from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

SECTOR_7_MARKER = "Sector-7"
SECTOR_7_MULTIPLIER = 1.45


@dataclass
class ParseStats:
    rows: list[dict]
    malformed: int


def round_half_up(x: float) -> int:
    # PDF says "nearest whole number"; use schoolbook rounding (14.5 -> 15),
    # not Python's banker's rounding (round(14.5) == 14).
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def parse_manifest(text: str) -> ParseStats:
    rows: list[dict] = []
    malformed = 0
    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if line_no == 1 and "WEIGHT" in line.upper():
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 4:
            malformed += 1
            continue
        try:
            weight = float(parts[3])
        except ValueError:
            malformed += 1
            continue
        rows.append(
            {
                "cargo_id": parts[0],
                "origin": parts[1],
                "destination": parts[2],
                "weight": weight,
            }
        )
    return ParseStats(rows=rows, malformed=malformed)


def apply_business_rules(rows: list[dict]) -> tuple[list[dict], int]:
    saveable: list[dict] = []
    skipped_prime = 0
    for row in rows:
        weight = row["weight"]
        if SECTOR_7_MARKER in row["destination"]:
            weight = weight * SECTOR_7_MULTIPLIER
        weight_kg = round_half_up(weight)
        if is_prime(weight_kg):
            skipped_prime += 1
            continue
        saveable.append({**row, "weight_kg": weight_kg})
    return saveable, skipped_prime

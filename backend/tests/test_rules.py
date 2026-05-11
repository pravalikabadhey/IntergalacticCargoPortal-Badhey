import pytest

from app.parser import apply_business_rules, is_prime, parse_manifest


@pytest.mark.parametrize(
    "n,expected",
    [
        (-1, False),
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (5, True),
        (6, False),
        (7, True),
        (9, False),
        (11, True),
        (25, False),
        (97, True),
        (100, False),
        (145, False),  # 5 * 29
        (9999, False),  # 3 * 3 * 11 * 101
    ],
)
def test_is_prime(n, expected):
    assert is_prime(n) is expected


def _row(cargo_id, destination, weight):
    return {
        "cargo_id": cargo_id,
        "origin": "x",
        "destination": destination,
        "weight": weight,
    }


def test_sector7_multiplier_applied():
    saveable, skipped = apply_business_rules([_row("C1", "Sector-7", 100.0)])
    assert skipped == 0
    assert saveable[0]["weight_kg"] == 145  # 100 * 1.45


def test_sector7_substring_match_in_destination():
    saveable, _ = apply_business_rules([_row("C1", "Sector-7-Outpost", 10.0)])
    assert saveable[0]["weight_kg"] == 15  # 10 * 1.45 = 14.5 → 15 (composite)


def test_no_sector7_no_multiplier():
    saveable, _ = apply_business_rules([_row("C1", "Mars", 100.0)])
    assert saveable[0]["weight_kg"] == 100


def test_prime_weight_skipped():
    saveable, skipped = apply_business_rules([_row("C1", "Earth", 2.0)])
    assert saveable == []
    assert skipped == 1


def test_prime_only_after_multiplier_skipped():
    # 2 * 1.45 = 2.9 → round to 3 (prime) → skipped
    saveable, skipped = apply_business_rules([_row("C1", "Sector-7", 2.0)])
    assert saveable == []
    assert skipped == 1


def test_zero_and_one_are_not_prime_and_kept():
    saveable, skipped = apply_business_rules(
        [
            _row("C1", "Mars", 1.0),
            _row("C2", "Mars", 0.4),  # rounds to 0
        ]
    )
    assert skipped == 0
    assert [r["weight_kg"] for r in saveable] == [1, 0]


def test_parse_pipe_delimited_with_header_and_blank_lines():
    text = "ID|ORIGIN|DESTINATION|WEIGHT\nC1|Mars|Sector-7|100\n\nC2|Jupiter|Earth|50.5\n"
    stats = parse_manifest(text)
    assert stats.malformed == 0
    assert [r["cargo_id"] for r in stats.rows] == ["C1", "C2"]
    assert stats.rows[1]["weight"] == 50.5


def test_parse_malformed_rows_counted():
    text = "C1|Mars|Sector-7|100\nbad-line\nC2|Jupiter|Earth|not-a-number\nC3|x|y|3"
    stats = parse_manifest(text)
    assert stats.malformed == 2
    assert len(stats.rows) == 2

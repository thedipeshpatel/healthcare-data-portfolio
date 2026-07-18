"""
hedis_gap_in_care_calculator.py

Simplified HEDIS-style gap-in-care calculator.

Context
-------
Payer quality teams track "gaps in care" - members who are eligible for a
quality measure (e.g. Breast Cancer Screening, Diabetes HbA1c Testing) but
don't yet have a qualifying claim/supplemental record closing that gap.
Real HEDIS measures have detailed age/continuous-enrollment/exclusion logic
defined by NCQA; this script demonstrates the *pattern* used to evaluate
eligibility and gap status against a simplified rule set, using synthetic
member data (no PHI).

Usage
-----
    python hedis_gap_in_care_calculator.py
"""

from __future__ import annotations
import pandas as pd

# --- Simplified measure definitions -----------------------------------------
# Each measure: eligible population rule + the service that closes the gap.
MEASURES = {
    "BCS": {  # Breast Cancer Screening
        "name": "Breast Cancer Screening",
        "eligible": lambda m: m["gender"] == "F" and 50 <= m["age"] <= 74,
        "closing_codes": {"77067", "77066"},  # mammography CPT codes (example)
    },
    "CDC-HbA1c": {  # Comprehensive Diabetes Care - HbA1c testing
        "name": "Diabetes: HbA1c Testing",
        "eligible": lambda m: m["has_diabetes"] and 18 <= m["age"] <= 75,
        "closing_codes": {"83036", "83037"},  # HbA1c CPT codes (example)
    },
    "COL": {  # Colorectal Cancer Screening
        "name": "Colorectal Cancer Screening",
        "eligible": lambda m: 45 <= m["age"] <= 75,
        "closing_codes": {"45378", "45380", "82270"},  # colonoscopy / FOBT (example)
    },
}


def evaluate_gaps(members: pd.DataFrame, claims: pd.DataFrame) -> pd.DataFrame:
    """
    Returns one row per (member, measure) the member is eligible for, with a
    'gap_open' flag: True if no closing claim code was found for that member.
    """
    results = []
    claims_by_member = claims.groupby("member_id")["cpt_code"].apply(set).to_dict()

    for _, member in members.iterrows():
        member_codes = claims_by_member.get(member["member_id"], set())
        for measure_id, measure in MEASURES.items():
            if not measure["eligible"](member):
                continue
            gap_open = member_codes.isdisjoint(measure["closing_codes"])
            results.append(
                {
                    "member_id": member["member_id"],
                    "measure_id": measure_id,
                    "measure_name": measure["name"],
                    "gap_open": gap_open,
                }
            )

    return pd.DataFrame(results)


def _synthetic_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    members = pd.DataFrame(
        [
            {"member_id": "M001", "age": 55, "gender": "F", "has_diabetes": True},
            {"member_id": "M002", "age": 62, "gender": "F", "has_diabetes": False},
            {"member_id": "M003", "age": 48, "gender": "M", "has_diabetes": True},
            {"member_id": "M004", "age": 70, "gender": "M", "has_diabetes": False},
        ]
    )
    claims = pd.DataFrame(
        [
            {"member_id": "M001", "cpt_code": "77067"},   # closes BCS for M001
            {"member_id": "M003", "cpt_code": "83036"},   # closes CDC-HbA1c for M003
            {"member_id": "M004", "cpt_code": "99213"},   # unrelated office visit
        ]
    )
    return members, claims


def main() -> None:
    members, claims = _synthetic_data()
    gaps = evaluate_gaps(members, claims)

    print("Full eligibility/gap table:\n")
    print(gaps.to_string(index=False))

    open_gaps = gaps[gaps["gap_open"]]
    print(f"\n{len(open_gaps)} open gap(s) out of {len(gaps)} eligible measure-member pairs:\n")
    print(open_gaps.to_string(index=False))


if __name__ == "__main__":
    main()

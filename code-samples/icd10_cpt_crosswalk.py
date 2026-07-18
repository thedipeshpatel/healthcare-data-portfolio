"""
icd10_cpt_crosswalk.py

Small demo of a diagnosis-to-procedure "crosswalk" lookup - the kind of
utility used when reconciling clinical (ICD-10-CM) and claims (CPT/HCPCS)
coding systems during data mapping or quality-measure logic.

This ships with a tiny illustrative table (a handful of common codes). In a
real engagement this would be backed by NCQA/CMS reference files or a
terminology service, not a hardcoded dict.

Usage
-----
    python icd10_cpt_crosswalk.py E11.9
"""

from __future__ import annotations
import sys

# Illustrative subset only - NOT a complete or authoritative crosswalk.
CROSSWALK = {
    "E11.9": {  # Type 2 diabetes mellitus without complications
        "description": "Type 2 diabetes mellitus without complications",
        "related_cpt": ["83036", "83037", "82947"],  # HbA1c, glucose tests
    },
    "I10": {  # Essential (primary) hypertension
        "description": "Essential (primary) hypertension",
        "related_cpt": ["99213", "99214"],  # E/M visit codes commonly billed alongside
    },
    "Z12.31": {  # Encounter for screening mammogram
        "description": "Encounter for screening mammogram for malignant neoplasm of breast",
        "related_cpt": ["77067", "77066"],
    },
    "Z12.11": {  # Encounter for screening for colorectal cancer
        "description": "Encounter for screening for malignant neoplasm of colon",
        "related_cpt": ["45378", "45380", "82270"],
    },
}


def lookup(icd10_code: str) -> dict | None:
    return CROSSWALK.get(icd10_code.upper())


def main() -> None:
    codes = sys.argv[1:] or list(CROSSWALK.keys())

    for code in codes:
        entry = lookup(code)
        if entry is None:
            print(f"{code}: not found in demo crosswalk")
            continue
        print(f"{code} - {entry['description']}")
        print(f"  related CPT/HCPCS: {', '.join(entry['related_cpt'])}")


if __name__ == "__main__":
    main()

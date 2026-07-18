"""
fhir_bundle_validator.py

A lightweight, dependency-free validator for FHIR R4 Bundles.

Context
-------
Real-world healthcare interoperability projects ingest FHIR Bundles from many
sources (EHRs, HIEs, payer APIs). Before mapping resources into a warehouse or
forwarding them downstream, it's useful to run a fast structural check that
catches the most common malformed-resource issues without needing a full FHIR
validation server.

This is a teaching/demo version - it checks structure and required fields for
a handful of common resource types (Patient, Observation, Condition, Claim).
It is NOT a substitute for full FHIR profile validation (e.g. against US Core).

Usage
-----
    python fhir_bundle_validator.py sample_bundle.json

Or import and call `validate_bundle(bundle_dict)` directly.
"""

from __future__ import annotations
import json
import sys
from dataclasses import dataclass


@dataclass
class ValidationIssue:
    severity: str  # "error" | "warning"
    resource_type: str
    resource_index: int
    message: str

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] entry #{self.resource_index} ({self.resource_type}): {self.message}"


# Minimal required-field rules per resource type. Not exhaustive - illustrative.
REQUIRED_FIELDS = {
    "Patient": ["id", "gender"],
    "Observation": ["id", "status", "code", "subject"],
    "Condition": ["id", "subject", "code"],
    "Claim": ["id", "status", "type", "patient", "provider"],
}


def validate_resource(resource: dict, index: int) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    resource_type = resource.get("resourceType")

    if not resource_type:
        issues.append(ValidationIssue("error", "Unknown", index, "Missing 'resourceType'"))
        return issues

    required = REQUIRED_FIELDS.get(resource_type)
    if required is None:
        issues.append(
            ValidationIssue(
                "warning",
                resource_type,
                index,
                "No validation rules defined for this resource type (skipped required-field check)",
            )
        )
        return issues

    for field_name in required:
        if field_name not in resource:
            issues.append(
                ValidationIssue("error", resource_type, index, f"Missing required field '{field_name}'")
            )

    # A couple of resource-specific sanity checks
    if resource_type == "Observation" and "status" in resource:
        valid_status = {"registered", "preliminary", "final", "amended", "corrected", "cancelled", "entered-in-error", "unknown"}
        if resource["status"] not in valid_status:
            issues.append(
                ValidationIssue("error", resource_type, index, f"Invalid status '{resource['status']}'")
            )

    return issues


def validate_bundle(bundle: dict) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if bundle.get("resourceType") != "Bundle":
        issues.append(ValidationIssue("error", "Bundle", 0, "Root resourceType must be 'Bundle'"))
        return issues

    entries = bundle.get("entry", [])
    if not entries:
        issues.append(ValidationIssue("warning", "Bundle", 0, "Bundle has no entries"))

    for i, entry in enumerate(entries):
        resource = entry.get("resource")
        if resource is None:
            issues.append(ValidationIssue("error", "Unknown", i, "Entry missing 'resource'"))
            continue
        issues.extend(validate_resource(resource, i))

    return issues


def _demo_bundle() -> dict:
    """A small synthetic bundle used for the demo run / smoke test."""
    return {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [
            {
                "resource": {
                    "resourceType": "Patient",
                    "id": "pat-001",
                    "gender": "female",
                    "birthDate": "1984-02-11",
                }
            },
            {
                "resource": {
                    "resourceType": "Observation",
                    "id": "obs-001",
                    "status": "final",
                    "code": {"text": "Hemoglobin A1c"},
                    "subject": {"reference": "Patient/pat-001"},
                }
            },
            {
                "resource": {
                    "resourceType": "Observation",
                    "id": "obs-002",
                    "status": "not-a-real-status",  # intentional error
                    "code": {"text": "Blood Pressure"},
                    "subject": {"reference": "Patient/pat-001"},
                }
            },
            {
                "resource": {
                    "resourceType": "Claim",
                    "id": "claim-001",
                    "status": "active",
                    "type": {"text": "professional"},
                    "patient": {"reference": "Patient/pat-001"},
                    # missing 'provider' on purpose
                }
            },
        ],
    }


def main() -> None:
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            bundle = json.load(f)
    else:
        print("No file provided, running against a synthetic demo bundle...\n")
        bundle = _demo_bundle()

    issues = validate_bundle(bundle)
    if not issues:
        print("No issues found.")
    else:
        for issue in issues:
            print(issue)
        errors = sum(1 for i in issues if i.severity == "error")
        warnings = sum(1 for i in issues if i.severity == "warning")
        print(f"\n{errors} error(s), {warnings} warning(s)")


if __name__ == "__main__":
    main()

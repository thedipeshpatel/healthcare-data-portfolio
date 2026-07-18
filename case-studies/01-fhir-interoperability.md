# Case Study: Healthcare Data Interoperability (FHIR/HL7)

**Domain:** Provider & payer data exchange
**Standards:** HL7 v2, CCDA, FHIR R4, US Core

## The problem

Legacy EHR and HIE feeds typically arrive as HL7 v2 messages or CCDA documents,
while modern payer and app integrations expect FHIR resources. Organizations
migrating toward FHIR-first architectures need to reconcile both worlds during
the transition - without losing clinical fidelity or breaking downstream
consumers who still expect the old formats.

## Approach

- **Source inventory** - catalog every inbound feed (EHR, lab, HIE) by format,
  cadence, and the clinical concepts each one carries (demographics, problems,
  meds, labs, encounters).
- **Canonical mapping layer** - define a mapping from HL7 v2 segments / CCDA
  sections to FHIR R4 resources (Patient, Encounter, Condition, Observation,
  MedicationRequest), aligned to US Core profiles where applicable.
- **Validation gate** - structural + terminology validation before resources
  are persisted or forwarded (see [`fhir_bundle_validator.py`](../code-samples/fhir_bundle_validator.py)
  for a simplified illustration of the kind of check that runs at this stage).
- **Reconciliation & data quality** - identify duplicate patient records
  across source systems, resolve identifier conflicts (MRN vs. member ID vs.
  MPI), and track match/no-match rates over time.
- **Change management** - because interoperability failures are often
  organizational, not technical: involve clinical stakeholders early, and
  measure success by adoption rate of the new pipeline, not just message
  throughput.

## Common failure modes addressed

| Failure mode | Mitigation |
|---|---|
| Missing/invalid required fields on inbound resources | Structural validation gate before persistence |
| Inconsistent status/code values (e.g. invalid Observation.status) | Terminology validation against value sets |
| Duplicate patient identities across source systems | Identity resolution / MPI matching logic |
| Silent data loss during v2 → FHIR translation | Field-by-field mapping spec + reconciliation reports |
| Downstream consumers breaking on schema drift | Versioned mapping layer + validation gate on every release |

## Outcome pattern

Programs following this approach typically see fewer downstream data-quality
tickets, faster onboarding of new source systems (because the mapping layer
is reusable), and cleaner audit trails for compliance and quality reporting
(HEDIS, risk adjustment) that depend on this data being accurate.

---
*This case study describes a generalized approach based on real project
patterns. No client-identifying details, proprietary code, or PHI are
included.*

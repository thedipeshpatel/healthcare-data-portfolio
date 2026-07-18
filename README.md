# Healthcare Data Portfolio

**Dipesh Patel, PAHM** - Lead Consultant, Healthcare Data & Product
[LinkedIn](https://www.linkedin.com/in/thedipeshpatel/)

A portfolio of case studies and illustrative code samples covering the areas
I work in day-to-day: healthcare data exchange/interoperability, payer
quality measurement (HEDIS), revenue cycle management (RCM) analytics, and
data governance.

The code samples run against small, synthetic datasets - no PHI, no
client-specific logic or proprietary specifications. They're meant to
illustrate patterns and approach, not to be production-grade libraries.

## Case studies

| Case study | Focus |
|---|---|
| [FHIR/HL7 Interoperability](case-studies/01-fhir-interoperability.md) | Mapping legacy HL7 v2/CCDA feeds to FHIR R4, validation, identity resolution |
| [HEDIS & Quality Measures](case-studies/02-hedis-quality-measures.md) | Measure logic as code, supplemental data pipelines, gap-in-care reporting |
| [Payer/Provider RCM Analytics](case-studies/03-payer-provider-rcm-analytics.md) | Denial analytics, days-in-A/R, net collection rate, aging |
| [Data Governance & Metadata Management](case-studies/04-data-governance-metadata-management.md) | Clinical data dictionaries, lineage, terminology crosswalks |

## Code samples

| Sample | What it shows |
|---|---|
| [`fhir_bundle_validator.py`](code-samples/fhir_bundle_validator.py) | Structural validation of a FHIR R4 Bundle (required fields, status value sets) |
| [`hedis_gap_in_care_calculator.py`](code-samples/hedis_gap_in_care_calculator.py) | Simplified HEDIS-style eligible-population + gap-in-care evaluation (pandas) |
| [`icd10_cpt_crosswalk.py`](code-samples/icd10_cpt_crosswalk.py) | Diagnosis-to-procedure code crosswalk lookup pattern |
| [`claims_rcm_analytics.sql`](code-samples/claims_rcm_analytics.sql) | Denial rate, top denial reasons, days-in-A/R, net collection rate, aging buckets |

All Python samples run standalone:

```bash
python fhir_bundle_validator.py
python hedis_gap_in_care_calculator.py
python icd10_cpt_crosswalk.py E11.9
```

## Background

11+ years in healthcare data operations and interoperability, most recently
leading healthcare data functional & product work at Delphi Consulting
Middle East, previously at MRO (FIGmd, Inc.). Focus areas: FHIR/HL7
interoperability, payer/provider data analytics, RCM, data governance, and
applying generative AI to healthcare data workflows.

# Case Study: HEDIS & Quality Measure Analytics

**Domain:** Health plan quality reporting
**Standards:** NCQA HEDIS, ICD-10-CM, CPT/HCPCS, LOINC, RxNorm

## The problem

Payers report against dozens of HEDIS measures every year, each with its own
eligible-population logic, exclusion criteria, and acceptable "closing"
evidence (claims, supplemental data feeds, or chart review). Getting this
wrong doesn't just mean a bad Star Rating - it can mean under- or
over-counting members who genuinely need outreach.

## Approach

- **Measure logic as code, not tribal knowledge** - translate NCQA technical
  specifications into explicit, testable eligibility and gap-closure rules
  (see [`hedis_gap_in_care_calculator.py`](../code-samples/hedis_gap_in_care_calculator.py)
  for a simplified illustration of the pattern: eligible-population rule +
  set of closing codes, evaluated per member).
- **Supplemental data pipeline** - many measures can be closed by lab results,
  registry data, or provider-submitted supplemental files, not just claims.
  Building a reliable supplemental data ingestion path (with the same
  structural/terminology validation used in the interoperability work) is
  often the highest-leverage improvement to overall compliance rates.
- **Gap lists that clinicians actually use** - the calculation is only half
  the job; the other half is getting a clean, deduplicated gap list to care
  management and provider offices in a format they can act on before the
  measurement year closes.
- **Audit trail** - every gap-closure decision needs to be traceable back to
  the specific claim/supplemental record and code that closed it, for NCQA
  audit and HEDIS Compliance Audit (Roadmap) purposes.

## Common pitfalls

- Using the wrong lookback period (measurement year vs. continuous enrollment
  window) for eligibility.
- Missing exclusion logic (e.g. hospice, bilateral mastectomy exclusions for
  BCS) that inflates the denominator incorrectly.
- Treating all "closing" codes as equivalent when NCQA specs sometimes
  require a combination (e.g. two visits in different years for some chronic
  condition measures).
- Supplemental data arriving in formats that don't map cleanly to the
  expected value sets, silently dropping valid gap closures.

## Outcome pattern

A clean, code-driven measure engine plus a fast supplemental data pipeline
typically moves compliance rates measurably within a measurement year,
because outreach teams get accurate, timely gap lists instead of a year-end
scramble.

---
*Illustrative case study based on real project patterns. No client data,
PHI, or proprietary specifications are included.*

# Case Study: Healthcare Data Governance & Metadata Management

**Domain:** Data governance for payer/provider data platforms
**Standards:** ICD-10-CM, CPT/HCPCS, LOINC, RxNorm, NDC

## The problem

As healthcare data platforms grow, teams lose track of what a field actually
means, which system it came from, who owns it, and whether it's safe to
change. Without a metadata layer, every new analytics request starts with
someone re-discovering the same tribal knowledge.

## Approach

- **Clinical data dictionary** - a living reference that documents every
  clinical/claims field: source system, code system used (ICD-10 vs. CPT vs.
  LOINC), valid value sets, and known data-quality caveats.
- **Metadata management** - track lineage (which source feed populated a
  table), ownership (who to ask when something looks wrong), and
  classification (PHI-sensitive vs. de-identified) at the table/column level.
- **Standardized terminology mapping** - centralize crosswalks between coding
  systems (see [`icd10_cpt_crosswalk.py`](../code-samples/icd10_cpt_crosswalk.py)
  for the pattern) so every downstream measure/report uses the same mapping
  instead of each team maintaining its own.
- **Governance cadence, not a one-time document** - a data dictionary that
  isn't maintained goes stale within a quarter. Pairing it with a lightweight
  review cadence (new field → dictionary entry required before it ships) is
  what keeps it trustworthy.

## What good looks like

- A new analyst can find what a field means without pinging the person who
  built the table three years ago.
- Every clinical/claims code crosswalk used in production is centrally
  defined once, not copy-pasted across a dozen notebooks with silent drift.
- PHI-sensitive fields are labeled consistently, which materially speeds up
  access reviews and compliance audits.
- Data quality issues get traced back to a source system and owner instead
  of becoming an unsolved mystery in a downstream dashboard.

## Outcome pattern

Programs that invest in even a lightweight governance layer (data dictionary
+ lineage + terminology crosswalks) see fewer "why do these two reports
disagree" escalations, because the underlying definitions stop drifting
between teams.

---
*Illustrative case study based on real project patterns. No client-specific
schemas, proprietary mappings, or PHI are included.*

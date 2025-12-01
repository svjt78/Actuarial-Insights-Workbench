# Using AIW to Support Underwriting

## Purpose
How actuaries can leverage the Actuarial Insights Workbench (AIW) to deliver actionable input for underwriters.

## Core Uses
- Pricing guardrails: Use segment KPIs (loss ratio, frequency, severity, pure premium by geography/industry/policy size/risk rating) to propose rate changes, minimum premiums, or deductibles for specific slices.
- Account triage: Run loss ratio and severity predictions to flag high-risk submissions; give underwriters a short list for stricter terms vs. quick-bind candidates.
- Trend narratives: Generate GenAI explanations on emerging loss trends or segment shifts; provide concise talking points for broker/insured conversations.
- Reserve/emergence signals: Share loss triangle outputs (age-to-age factors, ultimate estimates, IBNR) to justify caution on deteriorating cohorts or relaxation on improving ones.
- Appetite alignment: Highlight segments with favorable performance for growth and segments needing tighter guidelines; back recommendations with dashboard visuals.
- Referral criteria: Translate KPI thresholds and prediction scores into referral rules (e.g., if modeled severity >X or loss ratio >Y, escalate); give underwriters clear triggers.
- Portfolio impact checks: Before binding larger accounts, simulate expected impact on segment KPIs; advise on offsets (rate, terms) to keep portfolio targets intact.
- Communication artifacts: Export charts/tables or summarize insights for UW memos, steering committees, and rate-filing support.

## Workflow Tips
- Keep data fresh: regenerate synthetic data or retrain models via `scripts/generate_data.py` and `scripts/train_models.py` when testing scenarios.
- Validate assumptions: review triangle factors and KPI shifts after any data refresh to ensure referral rules stay calibrated.
- Document changes: note any new thresholds or appetite rules in PRs alongside screenshots from the Streamlit dashboards.

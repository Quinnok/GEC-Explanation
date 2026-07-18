# Experimental Pattern Summary

## Common Patterns to Reuse

- Extract edits from source/reference/system outputs, then stratify by operation and error type.
- Separate correction quality from explanation quality.
- Compare automatic metrics with human judgments when claims concern helpfulness or free-text explanation quality.
- Report behavior strata rather than only aggregate F0.5.
- Include leakage controls when explanations reveal target tokens or raw edit strings.
- Use counterfactual perturbations to test invariance and directional behavior.

## Patterns to Avoid

- Do not treat source-reference templates as model explanations.
- Do not call generated labels human gold.
- Do not claim internal faithfulness from output reconstruction alone.
- Do not collapse wrong correction, overcorrection, and missed correction into one error bucket.
- Do not mix preprints or silver generated data with human annotated evidence without marking status.

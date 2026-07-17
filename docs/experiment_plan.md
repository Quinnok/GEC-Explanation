# Experiment Plan

Last updated: 2026-07-18

## Pilot Objective

Test whether reverse edit reconstruction can distinguish faithful explanations from hard negative explanations on a small, manually inspected edit-level sample.

## Current Data Status

No real GEC dataset, model output, or explanation annotation file was found locally. A toy sanity-check file is used only to verify code paths.

## Minimum Real Pilot

- 100-300 edit-level examples.
- At least one real GEC model output source.
- At least one edit extraction method.
- At least one explanation source.
- At least three hard-negative types.
- One simple baseline and one reverse reconstruction model.
- Manual inspection of a subset.

## Metrics

- Span exact match and span F1.
- Source text match.
- Target text match.
- Operation accuracy.
- Error type accuracy.
- Full edit exact match.
- Faithfulness classification accuracy and macro-F1.
- Negative rejection rate.

## Blocking Items

- Need real English GEC data and reference corrections.
- Need model predictions or permission to download/run a model.
- Need explanation generation or existing explanation data.
- Need human inspection protocol.


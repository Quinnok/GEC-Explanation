# Project Brief

Last updated: 2026-07-18

## Goal

Build an independent English AAAI paper on edit-level faithfulness evaluation for explainable grammatical error correction (GEC). The project is scoped as a conference paper, not a full master's thesis.

## Working Title

Counterfactual Edit Simulatability for Faithful Explanations of Grammatical Error Correction Edits

## Core Question

Can an explanation predict and constrain the actual edit behavior of a GEC model, including under controlled counterfactual perturbations?

## Current Hypothesis

Reverse reconstruction can test edit correspondence but is leakage-prone. A stronger behavioral hypothesis is that faithful explanations should remain predictive when error-irrelevant context changes preserve the model edit, and should change or fail when rule-relevant perturbations change the model edit.

## Scope

The paper focuses on model-produced edits: correct corrections, wrong corrections, and overcorrections. Missed corrections are treated as a separate missing-edit diagnosis problem because they do not correspond to a model-predicted edit.

## Evidence Status

The engineering pipeline is now validated on real EXPECT data and two real public GEC model outputs. Substantive faithfulness claims remain pending because natural-language explanation candidates are not human gold and the current Round 02 template results are leakage controls.

## Workspace Status

- Git is initialized; Round 02 is committed as `1bb4c57 Round 02 real EXPECT ERRANT pilot`.
- AAAI 2027 author kit is available under `AuthorKit27/`.
- The local opening report PDF has been read with PDF text extraction.
- At startup, no real GEC datasets, model outputs, explanation annotations, or previous experiment results were found in the workspace.
- Current real data: 300 EXPECT source/reference pairs, 600 model predictions, 1707 model-produced edits, and 300 open-source explanation candidates.
- Current literature package: 50 paper cards plus CSV/Markdown/XLSX matrices under `literature/`.

# Project Brief

Last updated: 2026-07-18

## Goal

Build an independent English AAAI paper on edit-level faithfulness evaluation for explainable grammatical error correction (GEC). The project is scoped as a conference paper, not a full master's thesis.

## Working Title

Can GEC Explanations Reconstruct the Edit? Evaluating Explanation Faithfulness via Reverse Edit Reconstruction

## Core Question

Do natural-language explanations for GEC edits faithfully correspond to the edits actually produced by a GEC system?

## Current Hypothesis

If an explanation faithfully describes a model-produced edit, then a reconstructor given only the source sentence and the explanation should be able to recover the corresponding edit structure.

## Scope

The paper focuses on model-produced edits: correct corrections, wrong corrections, and overcorrections. Missed corrections are treated as a separate missing-edit diagnosis problem because they do not correspond to a model-predicted edit.

## Evidence Status

The idea is not yet experimentally validated. All result-bearing claims must remain pending until real data and experiments are available.

## Workspace Status

- No Git repository is present in the current directory.
- AAAI 2027 author kit is available under `AuthorKit27/`.
- The local opening report PDF has been read with PDF text extraction.
- No real GEC datasets, model outputs, explanation annotations, or previous experiment results were found in the workspace at startup.


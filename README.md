# Anonymous Code Release

This repository contains the source code for the submitted paper. The codebase
provides utilities for benchmark construction, prompt generation, text rendering,
rendered-text verification, sample filtering, result post-processing, and
evaluation.

This release accompanies a double-blind submission and is provided for reviewer
inspection of the code-level claims. Author names, affiliations, project-specific
identifiers, and other potentially identifying information have been removed for
anonymous review.

## Overview

The project is organized around a benchmark construction and evaluation pipeline.

At a high level, the workflow consists of:

1. Constructing benchmark data.
2. Building prompts and rendering benchmark instances.
3. Verifying rendered texts.
4. Fixing formatting or consistency issues when necessary.
5. Removing invalid samples.
6. Running evaluation.
7. Post-processing scores.
8. Converting result files into analysis-friendly formats.

The repository contains two main code directories:

- `src/`: core reusable modules.
- `scripts/`: runnable scripts and notebooks for the experimental pipeline.

## Installation

We recommend using a clean Python environment.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install notebook
```

The code has been tested with Python 3.10+. Some scripts may require additional
dependencies depending on the model APIs, benchmark files, or rendering backend
used in the experiments.

## Source Files

The `src/` directory contains the core source files used by the runnable scripts.

### `src/benchmark_generator.py`

Provides utilities for generating benchmark samples or intermediate benchmark
objects. This module is used during the benchmark construction stage.

### `src/prompt_builder.py`

Provides utilities for constructing prompts used in the benchmark construction.

### `src/renderer.py`

Provides the rendering logic for converting benchmark samples into the final
textual format used by the evaluation pipeline.

## Scripts and Notebooks

The `scripts/` directory contains executable scripts and notebooks for running
the main experimental workflow.

### `scripts/benchmark_builder.ipynb`

Notebook for constructing or debugging benchmark data.

### `scripts/rendered_texts_verifier.py`

Verifies whether rendered benchmark texts satisfy the required format and
constraints.

### `scripts/rendered_texts_fixer.py`

Fixes formatting or consistency issues detected in rendered texts.

### `scripts/remove_invalid_samples.py`

Filters out invalid or malformed samples after multi-turns fixing.

### `scripts/ab_eval.py`

Runs evaluation.

### `scripts/recompute_scores_without_think.py`

Recomputes scores after removing or ignoring reasoning/thinking fields from
model outputs.

### `scripts/result_json_to_csv.ipynb`

Notebook for converting result files from JSON format to CSV format for further
analysis.

## Running the Pipeline

A typical workflow and examples usages are shown below.

```bash
# 1. Build or inspect benchmark data (you can do it step by step)
jupyter notebook scripts/benchmark_builder.ipynb 

# 2. Verify rendered benchmark texts
python scripts/rendered_texts_verifier.py \
  --input data/privacy_benchmark_rendered.json \
  --output data/privacy_benchmark_validation_report.json \
  --max-workers 5 \
  --judge-model meta-llama/Llama-3.3-70B-Instruct \
  --seed 42

# 3. Fix rendered texts if necessary (run multiplue rounds)
python scripts/rendered_texts_fixer.py \
  --rendered data/privacy_benchmark_rendered.json \
  --validation-report data/privacy_benchmark_validation_report.json \
  --output data/privacy_benchmark_rendered_repaired.json \
  --target-fields source_document_text task_instruction_text attacker_prompt_text \
  --max-workers 5 \
  --model meta-llama/Llama-3.3-70B-Instruct \
  --seed 42

# 4. Remove invalid samples
python scripts/remove_invalid_samples.py \
  --rendered-repaired data/privacy_benchmark_rendered_repaired.json \
  --validation-report data/privacy_benchmark_validation_report.json

# 5. Run evaluation
python scripts/ab_eval.py \
  --dataset data/privacy_benchmark_rendered_repaired.json \
  --model-a <model_a_name> \
  --domains <domain_1> <domain_2> \
  --samples-per-domain 25 \
  --max-rounds 6 \
  --seed 42 \
  --output results/ab_eval_results.json \
  --output-details results/ab_eval_results_detailed.json \
  --checkpoint results/ab_eval_results_detailed.json.checkpoint.json \
  --Anonymous-base-url https://examples.com \
  --model-b meta-llama/Llama-3.3-70B-Instruct \
  --max-workers 5 \
  --model-a-provider Anonymous \
  --defense none

# 6. Convert result JSON files to CSV (need set file path)
jupyter notebook scripts/result_json_to_csv.ipynb

# 7. Recompute scores without reasoning/thinking fields after converting json to csv
python scripts/recompute_scores_without_think.py \
  --details results/ab_eval_results_detailed.csv \
  --summary results/ab_eval_results.csv \
  --details-out results/ab_eval_results_detailed_recompute.csv \
  --summary-out results/ab_eval_results_recompute.csv \
  --progress-every 100
```

Depending on the experiment, some steps may be optional. For example,
`remove_invalid_samples.py` only needs to be run when the verification step
detects formatting or consistency issues after multi-turn fixing.

## Reproducibility

The reproducibility of structured data is deterministic as mentioned in the paper, but the results of LLM rendering is not deterministic if the endpoint is not launched with the settings enabling deterministic output. To maximize the reproducibility, please follow the guideline of deterministic inference of sglang.

## Data and Artifacts

Some files such as evaluation results, model output transcripts may not be included in this anonymized release.

## Expected Inputs and Outputs

Although the exact file names may differ across experiments, the pipeline
generally uses the following types of files:

```text
Input files:
  - benchmark samples
  - rendered benchmark texts

Intermediate files:
  - verified rendered texts
  - fixed rendered texts
  - filtered benchmark samples

Output files:
  - evaluation results
  - recomputed scores
  - CSV summaries
```

Generated outputs are typically written to `outputs/` or `results/`.

## Notes for Anonymous Review

This repository is prepared for double-blind review. We have removed author
names, institutional information, private paths, personal identifiers, and other
identifying metadata where possible.

All the data generated are completely synthetic/fake/artificial, they have totally no relation with the author, any use of a real-world-like (but still artificial) data is in order to augment the validity of the scenario and to expand the benchmark's range of applications as much as possible. Please do not attempt to identify the authors from these artificial data (which is impossible). 

Please do not attempt to identify the authors from code metadata, local paths,
comments, file history, or external resources. Any remaining identifying
information should be considered accidental.

## Troubleshooting

If a script cannot find an input file, please check that the required data or
intermediate artifact has been generated by the previous step and placed in the
expected directory.

If Jupyter notebooks fail to start, install Jupyter with:

```bash
pip install notebook
```

If Python cannot import modules from `src/`, run scripts from the repository root
or set the Python path manually:

```bash
export PYTHONPATH=$(pwd)
```

On Windows PowerShell, use:

```powershell
$env:PYTHONPATH = (Get-Location)
```

## License

- Code: MIT License
- Dataset: Creative Commons Attribution 4.0 International License (CC BY 4.0)

Copyright (c) 2026 Anonymous Authors.

The dataset is synthetically generated and does not contain real personal data.

## Citation

If you use Anonymous-Bench, please cite:
Anonymous atm
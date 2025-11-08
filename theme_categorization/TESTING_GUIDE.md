# Testing and Evaluation Guide

## Overview

This guide explains how to test the theme categorization code and calculate the metrics reported in your article:

- **82% theme identification rate**: Percentage of human-labeled themes identified by the model
- **21% novel themes**: Percentage of model-identified themes not in ground truth

## Setup

### 1. Install Dependencies

```bash
cd theme_categorization
pip install -e .
```

Or install manually:

```bash
pip install openai pandas tqdm numpy
```

### 2. Configure API Access

You have two options:

#### Option A: Use HuggingFace Inference Router (Recommended for testing)

1. Get your HuggingFace API token from https://huggingface.co/settings/tokens
2. Set environment variable:

**Windows (PowerShell):**

```powershell
$env:HF_TOKEN="your_huggingface_token_here"
```

**Windows (Command Prompt):**

```cmd
set HF_TOKEN=your_huggingface_token_here
```

**Linux/Mac:**

```bash
export HF_TOKEN="your_huggingface_token_here"
```

#### Option B: Use vLLM (Local Deployment)

If you have vLLM running locally:

1. Start vLLM server:

```bash
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.2-3B-Instruct \
    --port 8001
```

2. Set environment variable (or leave unset):

```bash
set HF_TOKEN=dummy_token
```

### 3. Place Dataset File

Make sure `Dataset_v6.csv` is in the project root directory (`G:\Hospital\Files\AI\`), or update the path in `test_evaluation.py`.

## Running the Evaluation

### Basic Test

Run the evaluation script:

```bash
cd theme_categorization
python test_evaluation.py
```

This will:

1. Load reviews from `Dataset_v6.csv`
2. Process them through the LLM pipeline
3. Compare predictions with ground truth (`ProcessedCode` column)
4. Calculate and display metrics

### Customizing the Test

Edit `test_evaluation.py` to change:

- **Number of reviews to test**: Change `limit=100` to your desired number
- **Dataset path**: Update `DataLoader("Dataset_v6.csv")` if your file is elsewhere
- **Model**: Set `HF_MODEL_NAME` environment variable or modify `Settings` in code

## Understanding the Metrics

### Theme Identification Rate (82%)

This measures: **How many of the human-labeled themes did the model find?**

```
Theme Identification Rate = (Identified Themes / Total Ground Truth Themes) × 100
```

Example:

- Ground truth has 100 themes total
- Model identified 82 of them
- Rate = 82%

### Novel Themes Percentage (21%)

This measures: **How many themes did the model find that weren't in the ground truth?**

```
Novel Themes Percentage = (Novel Themes / Total Predicted Themes) × 100
```

Example:

- Model predicted 100 themes total
- 21 of them were not in ground truth
- Percentage = 21%

## Code Structure

### Evaluation Module (`evaluator.py`)

The evaluation code that calculates these metrics:

1. **`parse_ground_truth()`**: Parses `ProcessedCode` column format like `"{'theme1', 'theme2'}"`
2. **`parse_llm_themes()`**: Extracts theme names from LLM JSON response
3. **`calculate_metrics()`**: Calculates metrics for a single review
4. **`evaluate_predictions()`**: Aggregates metrics across all reviews

### Data Loader (`data_loader.py`)

Updated to work with your dataset:

- Reads `Comment` column for input reviews
- Reads `ProcessedCode` column for ground truth
- Handles NaN values in `ProcessedCode`

## Example Output

```
======================================================================
EVALUATION RESULTS
======================================================================
Total reviews evaluated: 100

Theme Identification Rate: 82.00%
  (Percentage of human-labeled themes identified by model)
  Identified: 164 / 200 ground truth themes

Novel Themes Percentage: 21.00%
  (Percentage of model-identified themes not in ground truth)
  Novel themes: 42 / 200 predicted themes

Average themes per review: 2.00

Pipeline Metrics:
  Success rate: 98.00%
  Failed extractions: 2
```

## Troubleshooting

### Error: "File not found: Dataset_v6.csv"

- Make sure the CSV file is in the correct location
- Update the path in `test_evaluation.py`

### Error: "HF_TOKEN not set"

- Set the `HF_TOKEN` environment variable (see Setup section)
- Or use `dummy_token` for vLLM local deployment

### Error: "API timeout" or "Rate limit"

- Increase `HF_TIMEOUT` environment variable (default: 15 seconds)
- Increase `RATE_LIMIT_DELAY` to slow down requests

### Low Success Rate

- Check your API token is valid
- Verify vLLM server is running (if using local deployment)
- Check network connectivity

## Environment Variables Reference

| Variable           | Default                              | Description                                       |
| ------------------ | ------------------------------------ | ------------------------------------------------- |
| `HF_TOKEN`         | `"dummy_token"`                      | HuggingFace API token (or "dummy_token" for vLLM) |
| `HF_MODEL_NAME`    | `"meta-llama/Llama-3.2-3B-Instruct"` | Model to use                                      |
| `HF_TIMEOUT`       | `15`                                 | Request timeout in seconds                        |
| `LLM_TEMPERATURE`  | `0.7`                                | LLM temperature parameter                         |
| `LLM_MAX_TOKENS`   | `1000`                               | Maximum tokens in response                        |
| `RATE_LIMIT_DELAY` | `1.0`                                | Delay between API calls (seconds)                 |
| `LOG_LEVEL`        | `"INFO"`                             | Logging level (DEBUG, INFO, WARNING, ERROR)       |

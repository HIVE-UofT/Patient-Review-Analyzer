# Summary: Code Alignment with Reported Metrics

## What Part of Code Aligns with Your Metrics?

The code now includes an **evaluation module** (`evaluator.py`) that calculates the exact metrics you reported:

### 1. Theme Identification Rate (82%)

**Location**: `evaluator.py` → `evaluate_predictions()` function

**Calculation**:

```python
theme_identification_rate = (total_identified / total_ground_truth_themes) × 100
```

This measures: **How many of the human-labeled themes (from `ProcessedCode`) did the model identify?**

- Compares LLM-extracted themes with ground truth themes
- Counts how many ground truth themes were correctly identified
- Reports as percentage

### 2. Novel Themes Percentage (21%)

**Location**: `evaluator.py` → `evaluate_predictions()` function

**Calculation**:

```python
novel_themes_percentage = (total_novel / total_predicted_themes) × 100
```

This measures: **How many themes did the model find that weren't in the ground truth?**

- Finds themes predicted by LLM but not in `ProcessedCode`
- Counts these "novel" themes
- Reports as percentage of all predicted themes

## How It Works

1. **Data Loading** (`data_loader.py`):

   - Reads `Comment` column → input reviews
   - Reads `ProcessedCode` column → ground truth themes (format: `"{'theme1', 'theme2'}"`)

2. **Theme Extraction** (`llm_clients.py` + `pipeline.py`):

   - Processes reviews through LLM
   - Extracts themes in JSON format: `{"themes": [{"theme": "...", "description": "..."}]}`

3. **Evaluation** (`evaluator.py`):

   - Parses ground truth from `ProcessedCode` format
   - Parses LLM predictions from JSON
   - Compares them to calculate metrics

4. **Test Script** (`test_evaluation.py`):
   - Runs the full pipeline
   - Displays the metrics

## Key Functions

- `parse_ground_truth()`: Converts `"{'theme1', 'theme2'}"` → `{'theme1', 'theme2'}`
- `parse_llm_themes()`: Extracts theme names from LLM JSON response
- `evaluate_predictions()`: Calculates aggregate metrics across all reviews

The code structure now matches your evaluation methodology exactly!

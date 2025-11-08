# Quick Start Guide

## What I Fixed

I've added **evaluation code** that calculates your reported metrics (82% identification rate, 21% novel themes) by comparing LLM predictions with ground truth from `Dataset_v6.csv`.

## Files Added/Updated

1. **`evaluator.py`** - NEW: Calculates metrics by comparing predictions vs ground truth
2. **`data_loader.py`** - UPDATED: Now reads `Comment` and `ProcessedCode` columns
3. **`test_evaluation.py`** - NEW: Test script that runs evaluation
4. **`__init__.py`** - UPDATED: Exports evaluation functions

## How to Test

### Step 1: Configure API Token (Choose one method)

#### Option A: Using .env file (Recommended)

1. Create a `.env` file in the `theme_categorization` directory:

```bash
cd theme_categorization
```

2. Create `.env` file with your token:

```bash
# .env file
HF_TOKEN=your_huggingface_token_here
```

Or for vLLM local deployment:

```bash
HF_TOKEN=dummy_token
```

3. Install dependencies (includes python-dotenv):

```bash
pip install -e .
```

The `.env` file will be automatically loaded when you run the code!

#### Option B: Environment Variable

**Windows PowerShell:**

```powershell
$env:HF_TOKEN="your_token_here"
```

**Windows CMD:**

```cmd
set HF_TOKEN=your_token_here
```

**Linux/Mac:**

```bash
export HF_TOKEN="your_token_here"
```

Get token from: https://huggingface.co/settings/tokens

### Step 2: Run Test

```bash
cd theme_categorization
python test_evaluation.py
```

The script will:

- Load reviews from `Dataset_v6.csv` (in parent directory)
- Process them through LLM
- Compare with `ProcessedCode` ground truth
- Display metrics: identification rate and novel themes %

## Where Metrics Are Calculated

**Theme Identification Rate (82%)**:

- File: `evaluator.py`
- Function: `evaluate_predictions()`
- Formula: `(identified themes / total ground truth themes) × 100`

**Novel Themes Percentage (21%)**:

- File: `evaluator.py`
- Function: `evaluate_predictions()`
- Formula: `(novel themes / total predicted themes) × 100`

## Dataset Format

The code expects:

- **`Comment` column**: Patient review text (input)
- **`ProcessedCode` column**: Ground truth themes like `"{'theme1', 'theme2'}"` or `NaN`

## Troubleshooting

- **"File not found"**: Make sure `Dataset_v6.csv` is in `G:\Hospital\Files\AI\`
- **"HF_TOKEN not set"**: Set the environment variable (see Step 1)
- **Import errors**: Run `pip install -e .` from `theme_categorization` directory

See `TESTING_GUIDE.md` for detailed instructions.

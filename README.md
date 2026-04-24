# Derivatives Python Exercises

This repository contains small Python scripts for derivatives and futures practice calculations.

## What this project includes

- `call_option.py`: Computes the net profit of a call option position using a simple payoff formula.
- `margins.py`: Simulates a futures margin account balance over daily settlement prices, including variation margin calls.
- `binomial_option_tree.py`: Interactive binomial option tree visualizer with live controls.

## Binomial Tree Features

- Dynamic graph redraw when parameters change
- Slider controls for:
  - `S0` (initial stock price)
  - `K` (strike price)
  - `u` (up factor)
  - `d` (down factor)
  - `r` (risk-free rate)
  - `T` (time to expiration)
  - `steps` (tree depth)
- Manual numeric input fields next to each slider
- Input validation for invalid model combinations (for example `u <= d` or risk-neutral probability outside `[0, 1]`)
- Updated modern light-gray UI theme

## Requirements

- Python 3.10+ (any recent Python 3 version should work)
- Packages:
  - `numpy`
  - `pandas`
  - `networkx`
  - `matplotlib`

## Setup

```bash
python -m venv .venv
```

Activate the virtual environment:

- PowerShell: `./.venv/Scripts/Activate.ps1`
- CMD: `.venv\\Scripts\\activate.bat`

## Install dependencies

```bash
pip install numpy pandas networkx matplotlib
```

## Run scripts

```bash
python call_option.py
python margins.py
python binomial_option_tree.py
```

If your default `python` points to a different interpreter, run with project venv explicitly:

```bash
./.venv/Scripts/python.exe binomial_option_tree.py
```

## Typical workflow

```bash
git add .
git commit -m "Update derivatives scripts"
git push
```

# Biodiesel Kinetic Modeling

## Case study: transesterification of vegetable oil

This project develops a kinetic model for biodiesel production via transesterification of soybean oil, based on experimental data from Freedman et al. (1986). The model describes the three-step consecutive reaction:

**Triglyceride (TG) → Diglyceride (DG) → Monoglyceride (MG) → Glycerol (GL)**

with the formation of 3 moles of methyl esters (biodiesel) per mole of triglyceride.

---

## Objectives

- Calibrate kinetic constants (k₁, k₂, k₃) using experimental data
- Validate the model against data at different temperatures (50°C and 60°C)
- Perform sensitivity analysis (temperature, methanol/oil ratio)
- Optimize reaction conditions for maximum yield

---

## Project structure

biodiesel_kinetics_case_study/
│
├── data/
│ └── experimental_data.csv # Conversion vs time data
├── notebooks/
│ └── 01_data_analysis.ipynb # Day 1: data loading and visualization
├── output/
│ └── experimental_data.png # Generated plots
├── src/
│ ├── init.py
│ ├── kinetics_model.py # ODE system and solver
│ └── visualization.py # Plotting functions
├── requirements.txt
└── README.md

## Data source

Freedman, B., Butterfield, R. O., & Pryde, E. H. (1986). *Transesterification kinetics of soybean oil*. Journal of the American Oil Chemists' Society, 63(10), 1375-1380.

### Experimental data summary

| Temperature | Points | Time range | Conversion range |
|-------------|--------|------------|------------------|
| 50°C | 8 | 0-60 min | 0 → 96% |
| 60°C | 8 | 0-60 min | 0 → 99% |

---

## Results (preliminary)

- Initial reaction rate at 50°C: **0.056 %/min**
- Initial reaction rate at 60°C: **0.084 %/min** (1.5× higher)
- Complete conversion (>95%) reached in **50 min at 60°C**, **60 min at 50°C**

---

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
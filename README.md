# Biodiesel Kinetic Modeling: FAME vs HVO

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)
![NumPy](https://img.shields.io/badge/NumPy-1.21+-blue.svg)
![SciPy](https://img.shields.io/badge/SciPy-1.7+-blue.svg)
![License](https://img.shields.io/badge/License-Portfolio%20Use-lightgrey.svg)

**Case study on the kinetic modeling of biodiesel production from soybean oil (FAME) and hydrotreated vegetable oil (HVO).**

This repository contains the complete implementation of:

- **FAME model**: three‑step consecutive kinetics (TG → DG → MG → GL) calibrated on experimental data from Freedman et al. (1986).  
- **HVO model**: hydrodeoxygenation kinetics with Arrhenius temperature dependence, parameterized for different feedstocks (virgin oil, used oil, animal fat).  
- **Emissions analysis**: simplified Life Cycle Assessment (LCA) to estimate CO₂ emissions and reduction compared to fossil diesel.

## Key results
- FAME calibration: **R² = 0.9967**, **RMSE = 1.89%** (50 °C)
- Validation at 60 °C: **RMSE = 9.81%**
- HVO with used oil achieves **57.4% CO₂ reduction** vs fossil diesel

## Technologies
- Python 3.9+
- NumPy, SciPy (odeint, curve_fit), Pandas, Matplotlib
- Jupyter Notebooks for interactive analysis

## Repository structure
biodiesel_kinetics_case_study/
├── data/
│   └── experimental_data.csv
├── notebooks/
│   ├── 01_data_analysis.ipynb
│   ├── 02_kinetic_model.ipynb
│   ├── 03_parameter_estimation.ipynb
│   ├── 04_sensitivity_analysis.ipynb
│   ├── 05_HVO_comparison.ipynb
│   └── 06_HVO_advanced.ipynb
├── src/
│   ├── __init__.py
│   ├── kinetics_model.py
│   ├── hvo_model.py
│   └── emissions_analysis.py
├── output/
│   └── (tutti i PNG)
├── requirements.txt
└── README.md


## How to run
1. Clone the repository  
   `git clone https://github.com/AlfredoPeluso/biodiesel-kinetics-modeling.git`
2. Install dependencies  
   `pip install -r requirements.txt`
3. Launch Jupyter and explore the notebooks:  
   `jupyter notebook`

## References
Freedman, B., Butterfield, R. O., & Pryde, E. H. (1986). *Transesterification kinetics of soybean oil*. Journal of the American Oil Chemists' Society, 63(10), 1375–1380.

---

**Author:** Alfredo Peluso – [alfredopeluso@outlook.it](mailto:alfredopeluso@outlook.it)  
**License:** This project is for portfolio demonstration purposes.

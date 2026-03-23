"""
Simplified HVO (Hydrotreated Vegetable Oil) kinetic model with Arrhenius temperature dependence.

Hydrodeoxygenation reaction:
Triglyceride + 3H₂ → 3 n-alkanes + glycerol
"""

import numpy as np
from scipy.integrate import odeint


def hvo_kinetics(C, t, k):
    """
    Simplified HVO kinetic model (hydrodeoxygenation).
    
    Parameters:
    -----------
    C : array
        Concentrations [TG, H2, ALK, GL] (mol/L)
    t : float
        Time (min)
    k : array
        Kinetic constants [k1] (L/(mol·min))
    
    Returns:
    --------
    dCdt : array
        Derivatives of concentrations
    """
    TG, H2, ALK, GL = C
    k1 = k[0]
    
    # Rate law: r = k1 * [TG] * [H2]
    r = k1 * TG * H2
    
    # Mass balance equations
    dTGdt = -r
    dH2dt = -3 * r
    dALKdt = 3 * r
    dGLdt = r
    
    return [dTGdt, dH2dt, dALKdt, dGLdt]


def arrhenius(k_ref, T_ref, Ea, R, T):
    """
    Calculate k(T) using Arrhenius law.
    
    Parameters:
    -----------
    k_ref : float
        Rate constant at reference temperature (L/(mol·min))
    T_ref : float
        Reference temperature (K)
    Ea : float
        Activation energy (J/mol)
    R : float
        Gas constant (8.314 J/(mol·K))
    T : float
        Temperature of interest (K)
    
    Returns:
    --------
    k : float
        Rate constant at temperature T
    """
    return k_ref * np.exp(-Ea / R * (1/T - 1/T_ref))


def solve_hvo_kinetics(initial_concentrations, time_points, k):
    """Solve HVO ODE system."""
    solution = odeint(hvo_kinetics, initial_concentrations, time_points, args=(k,))
    return solution


def calculate_hvo_conversion(solution):
    """
    Calculate conversion of triglycerides (TG) to alkanes.
    """
    TG0 = solution[0, 0]
    TG_t = solution[:, 0]
    conversion = ((TG0 - TG_t) / TG0) * 100
    return conversion


# Typical kinetic parameters for HVO (from literature)
# Values for different feedstocks
HVO_KINETIC_PARAMS = {
    'virgin_oil': {'k1_ref': 0.05, 'Ea': 50000},      # L/(mol·min), J/mol
    'waste_oil': {'k1_ref': 0.06, 'Ea': 48000},
    'animal_fat': {'k1_ref': 0.055, 'Ea': 49000}
}


def get_hvo_k(T, feedstock='virgin_oil', T_ref=323.15):
    """
    Get HVO kinetic constant at temperature T using Arrhenius.
    
    Parameters:
    -----------
    T : float
        Temperature (K)
    feedstock : str
        Type of feedstock ('virgin_oil', 'waste_oil', 'animal_fat')
    T_ref : float
        Reference temperature (K) = 323.15 (50°C)
    
    Returns:
    --------
    k1 : float
        Rate constant at temperature T (L/(mol·min))
    """
    params = HVO_KINETIC_PARAMS.get(feedstock, HVO_KINETIC_PARAMS['virgin_oil'])
    R = 8.314  # J/(mol·K)
    
    k1 = arrhenius(params['k1_ref'], T_ref, params['Ea'], R, T)
    return k1


if __name__ == "__main__":
    # Example usage
    TG0 = 1.0
    H20 = 3.0
    initial_C = [TG0, H20, 0, 0]
    t = np.linspace(0, 60, 100)
    
    # Test at 50°C (323.15 K)
    k_hvo_50 = get_hvo_k(323.15, 'virgin_oil')
    solution = solve_hvo_kinetics(initial_C, t, [k_hvo_50])
    conversion_50 = calculate_hvo_conversion(solution)
    
    # Test at 60°C (333.15 K)
    k_hvo_60 = get_hvo_k(333.15, 'virgin_oil')
    solution = solve_hvo_kinetics(initial_C, t, [k_hvo_60])
    conversion_60 = calculate_hvo_conversion(solution)
    
    print(f"✅ HVO model with Arrhenius - Test completed")
    print(f"k1 at 50°C: {k_hvo_50:.4f} L/(mol·min)")
    print(f"k1 at 60°C: {k_hvo_60:.4f} L/(mol·min)")
    print(f"Conversion at 60 min (50°C): {conversion_50[-1]:.1f}%")
    print(f"Conversion at 60 min (60°C): {conversion_60[-1]:.1f}%")
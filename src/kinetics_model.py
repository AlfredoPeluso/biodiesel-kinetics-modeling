"""
Kinetic model for biodiesel production via transesterification.

Three-step consecutive reaction:
TG → DG → MG → GL
with formation of 3 moles of methyl esters (ME) per mole of TG.
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


def transesterification_kinetics(C, t, k):
    """
    System of ODEs for transesterification reaction.
    
    Parameters:
    -----------
    C : array
        Concentrations [TG, DG, MG, GL, ME] (mol/L)
    t : float
        Time (min)
    k : array
        Kinetic constants [k1, k2, k3] (1/min)
    
    Returns:
    --------
    dCdt : array
        Derivatives of concentrations
    """
    TG, DG, MG, GL, ME = C
    k1, k2, k3 = k
    
    # Mass balance equations
    dTGdt = -k1 * TG
    dDGdt = k1 * TG - k2 * DG
    dMGdt = k2 * DG - k3 * MG
    dGLdt = k3 * MG
    dMEdt = 3 * (k1 * TG + k2 * DG + k3 * MG)  # 3 moles ME per mole TG
    
    return [dTGdt, dDGdt, dMGdt, dGLdt, dMEdt]


def solve_kinetics(initial_concentrations, time_points, k):
    """
    Solve the ODE system for given initial conditions and kinetic constants.
    
    Parameters:
    -----------
    initial_concentrations : array
        [TG0, DG0, MG0, GL0, ME0] (mol/L)
    time_points : array
        Time points for solution (min)
    k : array
        Kinetic constants [k1, k2, k3] (1/min)
    
    Returns:
    --------
    solution : array
        Concentrations at each time point
    """
    solution = odeint(transesterification_kinetics, initial_concentrations, time_points, args=(k,))
    return solution


def calculate_conversion(solution):
    """
    Calculate conversion of triglycerides (TG) to biodiesel.
    
    Parameters:
    -----------
    solution : array
        Concentrations at each time point [TG, DG, MG, GL, ME]
    
    Returns:
    --------
    conversion : array
        Conversion of TG (%) based on TG consumed
    """
    # Initial TG concentration
    TG0 = solution[0, 0]
    
    # Current TG concentration
    TG_t = solution[:, 0]
    
    # Conversion = (initial - current) / initial * 100
    conversion = ((TG0 - TG_t) / TG0) * 100
    
    return conversion


def plot_results(t, solution, conversion, experimental_data=None):
    """
    Plot concentration profiles and conversion.
    
    Parameters:
    -----------
    t : array
        Time points
    solution : array
        Concentrations at each time point
    conversion : array
        Conversion values
    experimental_data : DataFrame, optional
        Experimental data for comparison
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Concentration profiles
    ax1.plot(t, solution[:, 0], 'b-', linewidth=2, label='TG (Triglyceride)')
    ax1.plot(t, solution[:, 1], 'g-', linewidth=2, label='DG (Diglyceride)')
    ax1.plot(t, solution[:, 2], 'orange', linewidth=2, label='MG (Monoglyceride)')
    ax1.plot(t, solution[:, 3], 'purple', linewidth=2, label='GL (Glycerol)')
    ax1.plot(t, solution[:, 4], 'r-', linewidth=2, label='ME (Methyl esters)')
    ax1.set_xlabel('Time (min)', fontsize=12)
    ax1.set_ylabel('Concentration (mol/L)', fontsize=12)
    ax1.set_title('Concentration Profiles', fontsize=14, fontweight='bold')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Conversion
    ax2.plot(t, conversion, 'r-', linewidth=2, label='Model prediction')
    
    if experimental_data is not None:
        ax2.scatter(experimental_data['time_min'], 
                   experimental_data['conversion'] * 100,
                   color='blue', s=80, zorder=5, 
                   label='Experimental data')
    
    ax2.set_xlabel('Time (min)', fontsize=12)
    ax2.set_ylabel('Conversion to ME (%)', fontsize=12)
    ax2.set_title('Biodiesel Yield', fontsize=14, fontweight='bold')
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


# Example usage and test (runs only if script is executed directly)
if __name__ == "__main__":
    # Initial concentrations (mol/L) - typical values
    TG0 = 1.0      # Triglyceride
    DG0 = 0.0      # Diglyceride
    MG0 = 0.0      # Monoglyceride
    GL0 = 0.0      # Glycerol
    ME0 = 0.0      # Methyl esters (biodiesel)
    
    initial_C = [TG0, DG0, MG0, GL0, ME0]
    
    # Time points (minutes)
    t = np.linspace(0, 60, 100)
    
    # Initial guess for kinetic constants (1/min)
    k_initial = [0.1, 0.05, 0.01]
    
    # Solve the system
    solution = solve_kinetics(initial_C, t, k_initial)
    
    # Calculate conversion
    conversion = calculate_conversion(solution)
    
    # Plot results
    fig = plot_results(t, solution, conversion)
    plt.savefig('../output/kinetics_test.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Test simulation completed!")
    print(f"Conversion at 60 min: {conversion[-1]:.1f}%")
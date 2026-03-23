"""
Emissions analysis for FAME and HVO biofuels.
Calculates CO₂ reduction compared to fossil diesel.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def emissions_reduction(process_type, feedstock, distance_km=500):
    """
    Calculate CO₂ emissions and reduction compared to fossil diesel.
    
    Parameters:
    -----------
    process_type : str
        'FAME' or 'HVO'
    feedstock : str
        'virgin_oil', 'waste_oil', 'animal_fat'
    distance_km : float
        Transport distance for feedstock (km)
    
    Returns:
    --------
    total_emissions : float
        Total CO₂ emissions (g CO2/MJ)
    reduction : float
        Percentage reduction compared to diesel
    """
    # Baseline diesel emissions (g CO2/MJ) - from EU RED II
    baseline_diesel = 94.0
    
    # Well-to-wheel emissions by process and feedstock (g CO2/MJ)
    # Values from JRC Technical Reports and literature
    emissions_data = {
        'FAME': {
            'virgin_oil': 45.0,
            'waste_oil': 25.0,
            'animal_fat': 30.0
        },
        'HVO': {
            'virgin_oil': 35.0,
            'waste_oil': 15.0,
            'animal_fat': 20.0
        }
    }
    
    # Get base emissions
    base_emissions = emissions_data[process_type][feedstock]
    
    # Transport emissions (simplified: 0.05 g CO2/MJ per km)
    transport_emissions = 0.05 * distance_km
    
    total_emissions = base_emissions + transport_emissions
    reduction = (baseline_diesel - total_emissions) / baseline_diesel * 100
    
    return total_emissions, reduction


def compare_all_feedstocks():
    """
    Generate comparison table for all feedstocks.
    """
    feedstocks = ['virgin_oil', 'waste_oil', 'animal_fat']
    feedstock_labels = ['Olio vergine', 'Oli usati', 'Grassi animali']
    
    results = []
    
    for feedstock, label in zip(feedstocks, feedstock_labels):
        for process in ['FAME', 'HVO']:
            emissions, reduction = emissions_reduction(process, feedstock)
            results.append({
                'Processo': process,
                'Materia prima': label,
                'Emissioni (g CO2/MJ)': round(emissions, 1),
                'Riduzione vs diesel (%)': round(reduction, 1)
            })
    
    df = pd.DataFrame(results)
    return df


def plot_emissions_comparison():
    """
    Create comparison plot for FAME vs HVO emissions.
    """
    feedstocks = ['virgin_oil', 'waste_oil', 'animal_fat']
    feedstock_labels = ['Olio vergine', 'Oli usati', 'Grassi animali']
    diesel_baseline = 94.0
    
    fame_emissions = []
    hvo_emissions = []
    
    for feedstock in feedstocks:
        fame_e, _ = emissions_reduction('FAME', feedstock)
        hvo_e, _ = emissions_reduction('HVO', feedstock)
        fame_emissions.append(fame_e)
        hvo_emissions.append(hvo_e)
    
    x = np.arange(len(feedstocks))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars1 = ax.bar(x - width/2, fame_emissions, width, 
                   label='FAME', color='#2E86C1', edgecolor='black', linewidth=0.5)
    bars2 = ax.bar(x + width/2, hvo_emissions, width, 
                   label='HVO', color='#28B463', edgecolor='black', linewidth=0.5)
    
    # Add baseline line
    ax.axhline(y=diesel_baseline, color='red', linestyle='--', 
               linewidth=2, label=f'Diesel fossile ({diesel_baseline} g CO2/MJ)')
    
    ax.set_xlabel('Materia prima', fontsize=12)
    ax.set_ylabel('Emissioni CO2 (g/MJ)', fontsize=12)
    ax.set_title('Confronto emissioni: FAME vs HVO vs Diesel fossile', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(feedstock_labels)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('../output/emissions_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Grafico salvato in output/emissions_comparison.png")


def plot_emissions_by_temperature():
    """
    Show how temperature affects emissions (via conversion efficiency).
    """
    temperatures = np.linspace(25, 80, 12)  # °C
    
    # Conversion efficiency at different temperatures (simplified)
    # Higher T = higher conversion = lower emissions per MJ
    conversion_efficiency = 0.7 + 0.3 * (1 - np.exp(-0.1 * (temperatures - 20)))
    conversion_efficiency = np.clip(conversion_efficiency, 0.7, 0.98)
    
    # Base emissions at 100% conversion
    base_emissions = 45.0  # g CO2/MJ for FAME virgin oil
    
    # Actual emissions = base / conversion efficiency
    actual_emissions = base_emissions / conversion_efficiency
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(temperatures, actual_emissions, 'b-', linewidth=2.5, 
            label='Emissioni effettive')
    ax.fill_between(temperatures, actual_emissions, base_emissions, 
                    alpha=0.3, color='green', label='Riduzione per effetto temperatura')
    
    ax.set_xlabel('Temperatura (°C)', fontsize=12)
    ax.set_ylabel('Emissioni CO2 (g/MJ)', fontsize=12)
    ax.set_title('Effetto della temperatura sulle emissioni (FAME - olio vergine)', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../output/emissions_temperature_effect.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Grafico salvato in output/emissions_temperature_effect.png")


if __name__ == "__main__":
    print("=" * 50)
    print("ANALISI EMISSIONI - FAME vs HVO")
    print("=" * 50)
    
    # Generate comparison table
    df = compare_all_feedstocks()
    print("\n📊 Tabella comparativa emissioni:\n")
    print(df.to_string(index=False))
    
    # Generate plots
    print("\n📈 Generazione grafici...")
    plot_emissions_comparison()
    plot_emissions_by_temperature()
    
    print("\n✅ Analisi completata!")
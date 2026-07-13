import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

#Style settings
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

print("Libraries loaded successfully")

#Load data
df = pd.read_excel('propertydata.xlsx', sheet_name='Szczecin_Listings')
nbp = pd.read_excel('propertydata.xlsx', sheet_name='NBP_Historical')

print(f"Listings loaded: {len(df)} rows")
print(f"NBP historical data loaded: {len(nbp)} rows")
print(f"\nListings columns: {df.columns.tolist()}")
print(f"NBP columns: {nbp.columns.tolist()}")

# ============================================================
# NEW: Auto-categorization (replaces manual Price/Size Category entry)
# Bands based on natural gaps found in the original 160-listing sample
# ============================================================
def categorize_price(price_per_m2):
    if price_per_m2 < 8000:
        return 'Tani'
    elif price_per_m2 < 10000:
        return 'Średni'
    elif price_per_m2 < 13000:
        return 'Drogi'
    else:
        return 'Premium'

def categorize_size(size_m2):
    if size_m2 < 35:
        return 'Kawalerka'
    elif size_m2 < 60:
        return 'Średnie'
    elif size_m2 < 90:
        return 'Duże'
    else:
        return 'Bardzo duże'

df['Price Category'] = df['Price/m2'].apply(categorize_price)
df['Size Category'] = df['Size (m2)'].apply(categorize_size)

#Basic statistics
print("CURRENT MARKET OVERVIEW")
print(f"Average Price/m2: {df['Price/m2'].mean():,.0f} PLN")
print(f"Median Price/m2: {df['Price/m2'].median():,.0f} PLN")
print(f"Min Price/m2: {df['Price/m2'].min():,.0f} PLN")
print(f"Max Price/m2: {df['Price/m2'].max():,.0f} PLN")
print(f"Std Deviation: {df['Price/m2'].std():,.0f} PLN")

print("\nBY MARKET TYPE")
print(df.groupby('Rynek')['Price/m2'].agg(['mean', 'median', 'std', 'count']).round(0))

print("\nTOP 10 DISTRICTS BY AVERAGE PRICE/M2")
district_avg = df.groupby('District')['Price/m2'].agg(['mean', 'count']).round(0)
district_avg.columns = ['Avg_Price_m2', 'Listings']
district_avg = district_avg[district_avg['Listings'] >= 3].sort_values('Avg_Price_m2', ascending=False)
print(district_avg.head(10))

print("\nPRICE CATEGORY DISTRIBUTION")
print(df['Price Category'].value_counts())

print("\nSIZE CATEGORY DISTRIBUTION")
print(df['Size Category'].value_counts())

#NBP historical analysis
nbp['Pierwotny_Change'] = nbp['Pierwotny (PLN/m2)'].pct_change() * 100
nbp['Wtorny_Change'] = nbp['Wtórny (PLN/m2)'].pct_change() * 100

print("NBP HISTORICAL PRICE CHANGES - SZCZECIN")
print(nbp[['Rok', 'Pierwotny (PLN/m2)', 'Wtórny (PLN/m2)', 'Pierwotny_Change', 'Wtorny_Change']].to_string(index=False))

print("\nVOLATILITY (Std Dev of annual changes)")
print(f"Primary market: {nbp['Pierwotny_Change'].std():.2f}%")
print(f"Secondary market: {nbp['Wtorny_Change'].std():.2f}%")

print("\nWORST ANNUAL DECLINE")
print(f"Primary market: {nbp['Pierwotny_Change'].min():.2f}% in {nbp.loc[nbp['Pierwotny_Change'].idxmin(), 'Rok']}")
print(f"Secondary market: {nbp['Wtorny_Change'].min():.2f}% in {nbp.loc[nbp['Wtorny_Change'].idxmin(), 'Rok']}")

print("\nBEST ANNUAL GAIN")
print(f"Primary market: {nbp['Pierwotny_Change'].max():.2f}% in {nbp.loc[nbp['Pierwotny_Change'].idxmax(), 'Rok']}")
print(f"Secondary market: {nbp['Wtorny_Change'].max():.2f}% in {nbp.loc[nbp['Wtorny_Change'].idxmax(), 'Rok']}")

#Monte Carlo stress testing
np.random.seed(42)
N_SIMULATIONS = 10000
N_YEARS = 5

#Historical volatility from NBP data
vol_primary = nbp['Pierwotny_Change'].std() / 100
vol_secondary = nbp['Wtorny_Change'].std() / 100

#Current prices
current_primary = nbp['Pierwotny (PLN/m2)'].iloc[-1]
current_secondary = nbp['Wtórny (PLN/m2)'].iloc[-1]

#Scenario assumptions
scenarios = {
    'Baseline': {'drift_primary': 0.02, 'drift_secondary': 0.01},
    'Adverse': {'drift_primary': -0.05, 'drift_secondary': -0.05},
    'Severely Adverse': {'drift_primary': -0.15, 'drift_secondary': -0.15}
}

print("MONTE CARLO STRESS TEST - 5 YEAR HORIZON")
print(f"Simulations: {N_SIMULATIONS:,}")
print(f"Current primary price: {current_primary:,} PLN/m2")
print(f"Current secondary price: {current_secondary:,} PLN/m2")
print(f"Historical volatility - Primary: {vol_primary*100:.2f}%")
print(f"Historical volatility - Secondary: {vol_secondary*100:.2f}%\n")

results = {}

for scenario, params in scenarios.items():
    #Simulate price paths
    primary_paths = np.zeros((N_SIMULATIONS, N_YEARS))
    secondary_paths = np.zeros((N_SIMULATIONS, N_YEARS))
    
    for t in range(N_YEARS):
        if t == 0:
            primary_paths[:, t] = current_primary * (1 + params['drift_primary'] + vol_primary * np.random.randn(N_SIMULATIONS))
            secondary_paths[:, t] = current_secondary * (1 + params['drift_secondary'] + vol_secondary * np.random.randn(N_SIMULATIONS))
        else:
            primary_paths[:, t] = primary_paths[:, t-1] * (1 + params['drift_primary'] + vol_primary * np.random.randn(N_SIMULATIONS))
            secondary_paths[:, t] = secondary_paths[:, t-1] * (1 + params['drift_secondary'] + vol_secondary * np.random.randn(N_SIMULATIONS))
    
    #Final year prices
    final_primary = primary_paths[:, -1]
    final_secondary = secondary_paths[:, -1]
    
    #Price changes
    primary_change = ((final_primary - current_primary) / current_primary) * 100
    secondary_change = ((final_secondary - current_secondary) / current_secondary) * 100
    
    results[scenario] = {
        'primary_mean': final_primary.mean(),
        'secondary_mean': final_secondary.mean(),
        'primary_var95': np.percentile(primary_change, 5),
        'secondary_var95': np.percentile(secondary_change, 5),
        'primary_var99': np.percentile(primary_change, 1),
        'secondary_var99': np.percentile(secondary_change, 1),
        'primary_prob_loss': (final_primary < current_primary).mean() * 100,
        'secondary_prob_loss': (final_secondary < current_secondary).mean() * 100
    }
    
    print(f"SCENARIO: {scenario}")
    print(f"  Primary market - Expected price in 5Y: {final_primary.mean():,.0f} PLN/m2 ({primary_change.mean():+.1f}%)")
    print(f"  Secondary market - Expected price in 5Y: {final_secondary.mean():,.0f} PLN/m2 ({secondary_change.mean():+.1f}%)")
    print(f"  VaR 95% (Primary): {results[scenario]['primary_var95']:.1f}%")
    print(f"  VaR 95% (Secondary): {results[scenario]['secondary_var95']:.1f}%")
    print(f"  Probability of price decline (Primary): {results[scenario]['primary_prob_loss']:.1f}%")
    print(f"  Probability of price decline (Secondary): {results[scenario]['secondary_prob_loss']:.1f}%")
    print()

#District risk scoring
district_risk = df.groupby('District').agg(
    Avg_Price_m2=('Price/m2', 'mean'),
    Volatility=('Price/m2', 'std'),
    Listings=('Price/m2', 'count'),
    Avg_Size=('Size (m2)', 'mean')
).round(2)

#Filter districts with at least 3 listings
district_risk = district_risk[district_risk['Listings'] >= 3]

#Calculate coefficient of variation as risk measure
district_risk['CV'] = (district_risk['Volatility'] / district_risk['Avg_Price_m2'] * 100).round(2)

#Risk score — higher CV and higher price = higher risk
district_risk['Risk_Score'] = (
    (district_risk['CV'] / district_risk['CV'].max() * 50) +
    (district_risk['Avg_Price_m2'] / district_risk['Avg_Price_m2'].max() * 50)
).round(2)

# ============================================================
# CHANGED: RAG rating now uses terciles (relative ranking) instead
# of fixed absolute thresholds (>66 / >33), so the classification
# always produces a spread across High/Medium/Low regardless of
# where the absolute scores happen to fall.
# ============================================================
district_risk['RAG'] = pd.qcut(
    district_risk['Risk_Score'],
    q=3,
    labels=['Low', 'Medium', 'High']
)

# ============================================================
# NEW: Sample confidence flag — flags how much weight the CV/Risk
# Score for a district should be given, based on sample size.
# ============================================================
district_risk['Sample_Confidence'] = district_risk['Listings'].apply(
    lambda x: 'Low' if x < 10 else ('Medium' if x < 20 else 'High')
)

district_risk = district_risk.sort_values('Risk_Score', ascending=False)

print("DISTRICT RISK SCORECARD")
print(district_risk[['Avg_Price_m2', 'CV', 'Risk_Score', 'RAG', 'Sample_Confidence', 'Listings']].to_string())

#Export results for Power BI
district_risk.reset_index(inplace=True)
district_risk.to_csv('district_risk_scores.csv', index=False)

#Export Monte Carlo summary
mc_summary = []
for scenario, r in results.items():
    mc_summary.append({
        'Scenario': scenario,
        'Primary_Expected_Price': round(r['primary_mean'], 0),
        'Secondary_Expected_Price': round(r['secondary_mean'], 0),
        'Primary_VaR95': round(r['primary_var95'], 2),
        'Secondary_VaR95': round(r['secondary_var95'], 2),
        'Primary_Prob_Decline': round(r['primary_prob_loss'], 1),
        'Secondary_Prob_Decline': round(r['secondary_prob_loss'], 1)
    })

mc_df = pd.DataFrame(mc_summary)
mc_df.to_csv('monte_carlo_results.csv', index=False)

#Export NBP with changes
nbp.to_csv('nbp_historical_clean.csv', index=False)

print("Exported:")
print("  district_risk_scores.csv")
print("  monte_carlo_results.csv")
print("  nbp_historical_clean.csv")

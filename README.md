# Szczecin Real Estate Risk Model

## Overview
With the study year finished, I've been exploring risk analysis and how financial institutions assess risk on a day-to-day basis. Being born and raised in Szczecin, Poland, I wanted to find out how risky it actually is to invest in my home city's real estate market, and more importantly, how a bank holding mortgages on Szczecin properties would stress test that exposure.

This project combines 639 current property listings from Otodom.pl with 20 years of official NBP transaction price data to build a district-level risk model, a 10,000-path Monte Carlo stress test, and a RAG-rated scorecard covering 19 Szczecin districts. Built using Python, Excel, Power Query, and Power BI, with findings framed against EBA real estate collateral guidelines.

## Business Problem
Banks and lenders holding mortgages need to understand how much capital is at risk if property values decline, and which areas of a city carry more risk than others. This project answers two questions from that perspective:

1. **District-level**: Which parts of Szczecin represent higher collateral risk, and why?
2. **City-wide**: Under a range of economic stress scenarios, how much could Szczecin property values fall, and how likely is that decline?

The goal isn't to judge which neighbourhoods are "nicer." It's to model capital exposure and price uncertainty the way a lender's risk team would.

## Data Sources
- **Otodom.pl listings** (639 current property listings, collected across 19 Szczecin districts, minimum 30 listings per district after data collection)
- **NBP (Narodowy Bank Polski) historical transaction data**: 20 years (2006-2025) of average price/m² for Szczecin's primary and secondary markets

## Methodology

**District Risk Scorecard**

Each district's risk score combines two equally-weighted factors (50 points each):
- **Price volatility (CV)**: the coefficient of variation of listing prices within the district, capturing price dispersion/unpredictability
- **Price level**: average price/m², capturing capital exposure (higher-value properties represent larger absolute losses if prices fall)

Districts are classified into **High / Medium / Low** risk using tercile splits (`pd.qcut`) on the composite Risk Score, rather than fixed absolute thresholds. This ensures a meaningful, relative spread across categories regardless of the underlying score distribution.

**Monte Carlo Stress Test**

10,000 simulated 5-year price paths were generated for both primary and secondary markets, using historical volatility derived from the NBP series, across three scenarios:
- **Baseline** (modest growth)
- **Adverse** (moderate decline)
- **Severely Adverse** (sharp decline)

Value at Risk (VaR) at the 95% confidence level was calculated per scenario, representing the price decline that would only be exceeded in the worst 5% of simulated outcomes.

**Candidate risk factors, tested and reassessed**

Beyond price and volatility, I tested four additional variables as potential risk factors: distance to city centre, listing density (liquidity proxy), average property size, and primary/secondary market mix. Rather than including a variable because it seemed intuitively plausible, each was tested for correlation with existing risk metrics before being added or excluded. See Limitations below for the full results, including how these findings changed as the dataset grew.

## Key Findings

- **Highest-risk district: Śródmieście-Północ** (Risk Score 97.9), driven almost entirely by price level (the highest average price/m² of any district) combined with the widest price dispersion in the sample. This is not the "worst" neighbourhood in a conventional sense; it reflects high capital exposure, not declining desirability.
- **Risk clusters geographically**: high-risk districts sit predominantly in central Szczecin, while lower-risk districts are concentrated on the periphery.
- **Historical volatility is modest**: even through the 2008 financial crisis, Szczecin's worst single-year price decline was -6.3% (primary market, 2010), a mild correction rather than a crash. The sharpest historical price movements were actually on the upside (+39.6% in 2007, +23.8% in 2022), suggesting the city's price risk has historically been driven more by rapid growth phases than severe downturns.
- **Stress scenarios escalate sharply**: 5-year VaR (95%) ranges from -29.7% (Baseline) to -74.3% (Severely Adverse). Probability of any price decline rises from 37% (Baseline) to 100% (Severely Adverse); under severe stress, a decline isn't just larger, it becomes near-certain.

## Regulatory Context
This project's framing is informed by EBA (European Banking Authority) guidance on real estate as loan collateral, which emphasises assessing both the value and the volatility of collateral when determining capital requirements and loss-given-default assumptions. The district Risk Score's combination of price level (exposure) and price volatility (uncertainty) reflects this two-factor logic, though this project is an independent learning exercise and does not implement the EBA framework in full regulatory detail.

## Tools Used
- **Python** (pandas, NumPy, SciPy): data cleaning, Monte Carlo simulation, statistical testing
- **Excel / Power Query**: data collection and preparation
- **Power BI** (DAX, custom theming): interactive 3-page dashboard, including a district risk map and scorecard, 20-year price trend and volatility analysis, and Monte Carlo/VaR comparison

## Limitations

**Sample coverage**: Podjuchy was excluded from the final scorecard due to insufficient available listings (fewer than 30 at the time of collection) to produce a statistically reliable estimate, reflecting a comparatively illiquid segment of the local market. All 19 remaining districts have a minimum of 30 listings.

**Candidate risk factors, full results**: Four additional variables were tested for correlation with district-level CV and Risk Score.
- *Listing density* (liquidity proxy): no meaningful correlation (r ≈ -0.07 to -0.08); rejected.
- *Average property size*: no meaningful correlation with CV or Risk Score (r ≈ 0.06 and -0.18 respectively); rejected.
- *Primary/secondary market mix*: weak on the original, smaller sample; moderate (r ≈ 0.34 with Risk Score) once the dataset reached full 30+ listings per district. Not incorporated into the current Risk Score formula, but flagged as worth further investigation with a larger sample.
- *Distance to city centre*: weak on the original, smaller sample (r ≈ -0.22); moderate (r ≈ -0.30 with Risk Score, -0.43 with CV) once the dataset reached full 30+ listings per district. This shift illustrates that correlation estimates from small samples (some districts originally had as few as 3-8 listings) can be unreliable, and conclusions should be re-tested as data improves rather than treated as final.

**Data quality**: One listing (Drzetowo-Grabowo) initially contained a data entry error in its Price/m² field, which inflated that district's apparent volatility (CV 36.4, corrected to 32.0) and Risk Score (63.4, corrected to 60.0) before being identified and corrected. This is noted as a reminder that composite scores built from many small inputs are sensitive to individual data entry errors, and spot-checking outlier rows is a necessary step before drawing conclusions from a scorecard like this one.

**Monte Carlo scenario assumptions**: Baseline/Adverse/Severely Adverse drift assumptions are illustrative, chosen to represent plausible directional scenarios rather than calibrated to a specific macroeconomic model or forecast.

**Volatility measurement**: District-level "volatility" (CV) reflects the *cross-sectional dispersion* of current listing prices within a district at one point in time, not a time-series measure. This is distinct from the NBP-based historical volatility (year-over-year price change over 20 years) used in the Monte Carlo simulation. The two should not be conflated.

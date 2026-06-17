# Szczecin Real Estate Risk Model

## Overview
With the study year finished, I've been exploring risk analysis and how financial institutions assess risk on a day-to-day basis. Being born and raised in Szczecin, Poland, I wanted to find out how risky it actually is to invest in my home city's real estate market - and more importantly, how a bank holding mortgages on Szczecin properties would stress test that exposure.
This project combines 160 current property listings from Otodom.pl with 20 years of official NBP transaction price data to build a district-level risk model, Monte Carlo stress test, and RAG-rated scorecard of Szczecin neighbourhoods. Built using Python, Excel, PowerQuery, and Power BI - with findings framed against EBA real estate collateral guidelines.
## Business Problem
When a bank issues a mortgage, the property acts as collateral. If property values fall, the bank's collateral deteriorates, increasing the risk of loss if the borrower defaults. Understanding which districts carry the most price risk, and how the overall market behaves under stress, is therefore a core function of any bank's risk team.

This project attempts to answer three questions:
- Which Szczecin districts carry the highest price risk for a bank holding mortgages?
- How volatile has the Szczecin market been historically, and what does that imply for future price paths?
- How would collateral values deteriorate under baseline, adverse, and severely adverse economic scenarios?
  
## Data Sources
**Otodom.pl — Current Market Listings (June 2026)**
160 property listings I have manually collected from Poland's largest real estate portal, covering both primary (rynek deweloperski) and secondary (rynek wtórny) markets across 35 Szczecin districts. Variables collected: asking price (PLN), size (m²), price per m², district, number of rooms, and market type.

**Narodowy Bank Polski (NBP) — Historical Transaction Prices**
Official quarterly transaction price data for Szczecin published by the National Bank of Poland, covering both primary and secondary markets from 2006 to 2025. This is the same data source used by Polish banks and regulators to monitor real estate market conditions. Available at: nbp.pl

**Data Processing**
Raw listing data was cleaned and transformed using PowerQuery in Excel - I had removed duplicates, standardised district names, and added derived categories (Price Category, Size Category) before loading into Python for analysis.

## Methodology

### 1. Exploratory Data Analysis
The first step was simply getting to know the data. I analysed current market listings to understand how prices are distributed across Szczecin's districts, how the primary and secondary markets compare, and where price variation is highest within individual neighbourhoods. Districts with fewer than 3 listings were excluded to keep the analysis grounded in reliable data rather than outliers.

### 2. Historical Volatility Analysis
To understand how the Szczecin market has actually behaved over time, I used 20 years of official NBP transaction price data to calculate annual price changes for both market types. Rather than making assumptions about volatility, I let the real data speak - standard deviation of annual returns gave me a historically calibrated measure of market uncertainty. The result: Szczecin's primary market has carried approximately 11% annual volatility over the past two decades.

### 3. Monte Carlo Stress Testing
This is where it got interesting. Using historical volatility to calibrate random price shocks, I ran 10,000 simulations of how property prices could evolve over the next 5 years. Three scenarios were tested:

- **Baseline** - modest growth (2% primary, 1% secondary annual drift)
- **Adverse** - moderate correction (-5% annual drift)
- **Severely Adverse** - sharp decline (-15% annual drift)

For each scenario I calculated the expected price in 5 years, the worst-case outcome in 95% of simulations, and the likelihood of prices falling at all. This paints a fuller picture of risk rather than just saying 'prices will go up or down by X%'.

### 4. District Risk Scoring
Finally, I built a risk scorecard for each Szczecin district by combining two factors: price level (higher prices mean greater absolute loss potential) and coefficient of variation (how much prices vary within a district - a proxy for uncertainty). Each district was then classified into a RAG framework - High, Medium, or Low risk to produce something a portfolio manager could actually use.

## Key Findings
**The market is more divided than it looks.**
Primary market properties (new builds) are on average 29% more expensive than secondary market properties: 12,725 PLN/m² vs 9,867 PLN/m². This gap matters for banks because new builds carry higher absolute loss potential if prices correct.

**Not all expensive districts are the most risky.**
Śródmieście-Północ topped the risk scorecard despite not being the most expensive district, because prices within it vary wildly (coefficient of variation of 59%). A bank holding mortgages there faces high uncertainty even before any market downturn. By contrast, Łasztownia and Zawadzkiego-Klonowica are expensive but consistent, offering lower uncertainty for the same price level.

**Even in a good scenario, decline is possible.**
Under the baseline scenario of modest growth, there is still a 37-45% probability of prices being lower in 5 years than today. The Szczecin market is not a one-way bet, even without a recession.

**Stress scenarios reveal significant tail risk.**
Under the adverse scenario, prices are expected to fall around 23% with an 87% probability of any decline. Under the severely adverse scenario, prices fall around 56% on average with a 100% probability of decline. For a bank with significant Szczecin mortgage exposure, these are material risk figures.

**The market is showing early signs of cooling.**
2025 NBP data shows secondary market transaction prices fell 1.55%, the first decline since 2015. Primary market growth slowed to just 1.98%. After years of rapid growth, the market may be entering a consolidation phase, which makes stress testing particularly timely.
## Regulatory Context
## Tools Used
## Limitations

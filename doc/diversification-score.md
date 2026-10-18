For portfolio concentration/diversification, the HHI and its inverse (Effective Number of Companies, Neff=1/HHIN_{eff}=1/HHI) are often easier to interpret if mapped to qualitative ratings.

A common approach is to rate according to the effective number of equally weighted holdings:

Effective N (1/HHI)	HHI Range	Rating< 5	> 0.20	Highly Concentrated
5 - 10	0.10 - 0.20	Concentrated
10 - 20	0.05 - 0.10	Moderately Diversified
20 - 40	0.025 - 0.05	Well Diversified
> 40	< 0.025	Highly Diversified

Example:

HHI = 0.25 → Effective N = 4 → Highly Concentrated
HHI = 0.10 → Effective N = 10 → Moderately Diversified
HHI = 0.025 → Effective N = 40 → Highly Diversified
Suggested terminology

For the metric itself:

Portfolio Concentration Score (HHI)
Diversification Index (1/HHI)
Effective Number of Holdings
Effective Number of Companies
Portfolio Breadth

For the rating levels:

Highly Concentrated
Concentrated
Moderately Diversified
Well Diversified
Highly Diversified

or a more investment-oriented scale:

Single-Stock Risk
High Concentration
Balanced
Diversified
Broadly Diversified
Python example
def diversification_rating(effective_n):
    if effective_n < 5:
        return "Highly Concentrated"
    elif effective_n < 10:
        return "Concentrated"
    elif effective_n < 20:
        return "Moderately Diversified"
    elif effective_n < 40:
        return "Well Diversified"
    else:
        return "Highly Diversified"


Then:

rating = diversification_rating(effective_n)

print(f"HHI: {hhi:.4f}")
print(f"Effective Number of Companies: {effective_n:.1f}")
print(f"Diversification Rating: {rating}")


If this is for equity portfolios, I would personally use "Effective Number of Companies" as the metric name and "Diversification Rating" as the qualitative label, since these are intuitive even for non-quantitative readers.

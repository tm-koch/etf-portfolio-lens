[[ETF Portfolio Lens]]

When you expand beyond two funds or portfolios (more than 2 kinds of shares or baskets), measuring portfolio overlap becomes more complex because overlapping can happen in pairs or across multiple funds simultaneously.

To define and measure portfolio overlap for **more than two funds**, financial analysts and portfolio tools typically use two main approaches: **Pairwise Overlap** and **Aggregate (Total) Look-Through Overlap**.

### 1. The Pairwise Overlap Approach (The Matrix Method)

If you have N funds (e.g., Funds A, B, and C), you can break down the overlap by evaluating every possible pair:

- **The Math:** For N funds, there are \frac{N(N-1)}{2} unique pairs to check (e.g., 3 funds have 3 pairs: A-B, B-C, and A-C; 4 funds have 6 pairs).
- **The Definition:** For each pair, overlap is traditionally defined as the percentage of common holdings (either by number of shares or by market value/weight) relative to the combined size of the two portfolios.
- **Visualization:** This is usually displayed as a **heatmap or correlation matrix**, showing which specific fund pairings have high duplication (e.g., Fund A and Fund B share 70% of their stocks, while Fund C is entirely distinct).

### 2. The Aggregate / Total Overlap Approach (The Look-Through Method)

Instead of comparing funds two at a time, this method melts all your holdings into **one unified portfolio** to evaluate true exposure:

- **The Definition:** Total overlap looks at the entire portfolio simultaneously to find out how many underlying securities are held by _two or more_ of your funds, and what percentage of your total wealth is tied up in those shared assets.
- **How It Is Calculated:**
    1. **Look-Through:** The tool extracts the underlying stock constituents and their weights from every fund you own.
    2. **Weight Aggregation:** If you hold Stock X in Fund 1 (where it makes up 5% of your money) and also in Fund 3 (where it makes up 3% of your money), your _total exposure_ to Stock X across your whole portfolio is 8%.
    3. **Overlap Summation:** The aggregate overlap score measures the sum of capital sitting in assets duplicated across multiple funds relative to your total portfolio value.

### Why Multi-Fund Overlap Matters

When you own three or more funds, you face **stacked concentration risk**. Even if your pairwise overlaps look moderate (e.g., Fund A overlaps 30% with Fund B, and Fund B overlaps 30% with Fund C), a look-through analysis might reveal that a few massive companies (like top tech stocks) are heavily bought by _all three_ funds.

This results in a portfolio where your actual capital concentration in those specific companies is much higher than you realize, defeating the primary purpose of diversification.

===

To apply the look-through method when you have **more than two funds or baskets of shares**, you break the calculation down into two stages: first, finding your **total exposure** to each underlying security, and second, calculating the **aggregate overlap** (duplicated capital) across the entire portfolio.

### Step 1: Calculate the Total Look-Through Weight for Each Security

Before measuring overlap, you must melt all the funds down to see how much of your _total_ wealth is tied up in any given stock or share (i), factoring in both direct holdings and indirect fund allocations.

The total portfolio weight (W_i) for security i is calculated as:

`W_i = \sum_{j=1}^{n} w_{F_j} \cdot s_{i,j}`

Where:

- n = Total number of funds/portfolios you hold.
- w_{F_j} = The allocation weight of fund j in your overall personal portfolio (e.g., if Fund A makes up 40% of your money, w_{F_A} = 0.40).
- s_{i,j} = The percentage weight of security i _inside_ fund j (e.g., if Apple is 5% of Fund A, s_{\text{Apple}, A} = 0.05).

### Step 2: Calculate the Aggregate Multi-Fund Overlap

Once you have the total portfolio weight (W_i) for every security, you can measure how much capital is tied up in **duplicated holdings** (assets that appear in more than one of your funds).

The aggregate overlap percentage (\text{Overlap}_{\text{total}}) represents the sum of all capital sitting in securities that are shared across multiple funds, minus their single largest individual fund contribution:

`\text{Overlap}_{\text{total}} = \sum_{i} \left( W_i - \max_{j} (w_{F_j} \cdot s_{i,j}) \right)`

- **How to read this formula:** For every security i, look at its total portfolio weight (W_i) and subtract the largest single contribution coming from any individual fund (\max_j (w_{F_j} \cdot s_{i,j})).
- If a security is only held in **one** fund, its total weight equals its maximum single fund contribution, resulting in an overlap contribution of 0.
- If a security is held in **multiple** funds, the difference represents the excess capital duplicated across your other holdings, which gets summed up into your total portfolio overlap score.

### Example in Practice

Imagine you have a $10,000 portfolio split equally into two funds (50\% in Fund A, 50\% in Fund B), and both funds hold Apple:

1. **Fund A** has a 50\% weight in your portfolio (w_{F_A} = 0.50), and Apple makes up 10\% of it (s_{\text{Apple}, A} = 0.10).
2. **Fund B** has a 50\% weight in your portfolio (w_{F_B} = 0.50), and Apple makes up 20\% of it (s_{\text{Apple}, B} = 0.20).

- **Step 1 (Total Exposure):** `W_{\text{Apple}} = (0.50 \times 0.10) + (0.50 \times 0.20) = 0.05 + 0.10 = 0.15 \text{ (or 15\%)}`
- **Step 2 (Overlap Contribution):** The maximum single contribution from either fund is 10\% (0.50 \times 0.20 = 0.10). `\text{Apple Overlap} = 0.15 - 0.10 = 0.05 \text{ (or 5\%)}`

This means out of your total portfolio, **5%** represents true duplication of Apple shares across both funds. For more than 2 funds, you simply loop this summation across all n funds for every overlapping asset.

===

To express the look-through portfolio overlap as a percentage, the raw decimal output from the calculation is simply **multiplied by 100%**.

Depending on what you want to communicate, this percentage can be expressed in two primary ways:

### 1. As a Share of Total Wealth (Duplicated Capital Percentage)

This is the most common interpretation. It answers the question: _"What percentage of my total portfolio's market value is tied up in assets that are duplicated across more than one fund?"_

- **The Formula:** `\text{Overlap Percentage} = \left[ \sum_{i} \left( W_i - \max_{j} (w_{F_j} \cdot s_{i,j}) \right) \right] \times 100\%`
- **How to read it:** If your calculation yields `0.18`, your total look-through overlap is **18%**. This means 18 cents of every dollar you own is sitting in securities that you accidentally or intentionally bought through multiple different funds.
- **The Scale:**
    - **0%:** Zero overlap (your funds hold entirely different securities).
    - **100%:** Complete overlap (every fund holds the exact same securities in the exact same proportions).

### 2. As an Aggregate Minimum Weight Sum (The Intersection Method)

If you want to view overlap as the literal "overlap area" of a Venn diagram involving more than two funds, you can sum the minimum overlapping weights across all assets.

For any given security i, its overlapping (duplicated) portion is the weight that exists _beyond_ its single largest fund contribution. Alternatively, looking at it through shared intersections:

`\text{Overlap Percentage} = \left( 1 - \sum_{i} \min_{j} (\text{non-overlapping parts}) \right) \times 100\%`

In practice, financial software calculates this by summing the capital that is _redundant_. For instance:

- If Fund A gives you 4\% of Apple and Fund B gives you 6\% of Apple, your total exposure is 10\%.
- Your "primary" source of Apple is 6\%, and the **2% overlap** is the redundant portion coming from Fund A.
- Summing that 2% (along with the redundancies of every other shared stock) and turning it into a percentage gives you your final **Portfolio Overlap Percentage**.

===

The result would be **50%** using the look-through portfolio formula (assuming you split your money evenly between them), even though the funds themselves are **100% identical**.

This distinction comes down to the difference between **fund-to-fund overlap** and **portfolio redundant capital**:

### 1. The Fund-to-Fund Overlap: 100%

If you compare Fund A and Fund B directly, their overlap is **100%**. Because they hold the exact same securities in the exact same proportions, they are literal clones of each other.

### 2. The Portfolio Look-Through Overlap: 50% (using the formula)

When you apply the look-through formula to your overall wealth—assuming you put **50% of your money in Fund A and 50% in Fund B**—the overlap calculation yields **50%**.

**Why does this happen?**

- **Total Exposure (W_i):** Because both funds are identical, your total exposure to any stock i is s_i (its weight inside the fund).
- **Max Single Contribution (\max_j):** The largest single chunk of any stock coming from one fund is half of that stock's weight (0.50 \times s_i).
- **The Math:** Subtracting that single contribution leaves you with s_i - 0.50s_i = 0.50s_i. Summing that up across all stocks means **half (50%) of your total portfolio value is redundant capital**.

### The Practical Rule of Thumb

- If someone asks: _"How much do these two funds overlap?"_ \rightarrow **100%** (they are identical).
- If someone asks: _"How much of my portfolio is redundant because I bought two identical funds 50/50?"_ \rightarrow **50%** (half your money is in an unnecessary duplicate fund).

_(Note: If you put 100% of your money into Fund A and 0% into Fund B, your portfolio overlap formula would result in **0%**, because you aren't actually duplicating capital across multiple active holdings in your account.)_
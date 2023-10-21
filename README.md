# APL - Anime Priority List

## What is APL?
APL is an automatic anime watch priority list maker.

## How does APL work?
APL uses AniList's API to gather a users completed and planning list which is then imported into a Google Sheet where the data can be sorted.

## What is the purpose of APL?
As I have over 250+ anime planning to watch I usually can't decide what to watch first so I created a spreadsheet by hand to sort which anime I should watch first. This program is just to add a quality of life change for me and stop me from staying up making spreadsheets by hand.

***

## APL Score v2
- Score = Anime score
- B = Bingability factor
- P = Previous season watched
- b & p Weights = 0.5

<img src="https://i.upmath.me/svg/(Score%20-%2075)%20%5Ctimes%200.01%20%26%20%5Ctext%7B%20if%20%7D%2012%20%3C%20Eps%20%3C%2023%20%5C%5C(Score%20-%2075)%20%5Ctimes%200.01%20%2B%20%5Cfrac%7B1%20%2B%20%5Cmax(0.05%20%5Ctimes%20(Eps%20-%2024)%2C%200)%7D%7B100%7D%20%26%20%5Ctext%7B%20if%20%7D%20Eps%20%5Cgeq%2024%5C%5C%5Ctext%7Botherwise%20%7D0%0A" alt="(Score - 75) \times 0.01 &amp; \text{ if } 12 &lt; Eps &lt; 23 \\(Score - 75) \times 0.01 + \frac{1 + \max(0.05 \times (Eps - 24), 0)}{100} &amp; \text{ if } Eps \geq 24\\\text{otherwise }0
" />

<img src="https://i.upmath.me/svg/aplScore%20%5Ctimes%20%5Cleft(1%20%2B%20(B%20%5Ctimes%20bWeight%20%2B%20P%20%5Ctimes%20pWeight)%5Cright)" alt="aplScore \times \left(1 + (B \times bWeight + P \times pWeight)\right)" />


***


# WIP #

```[tasklist]
To-do
- [x] Get google sheets or some other spreasheet to work again
- [] Get date with all lists
- [x] Pre sort by APL score
- [] Add relation data for series order
- [] Add series order
- [/] Better score weighting
- [] Update instructions
- [] Discord bot
```

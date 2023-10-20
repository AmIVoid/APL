# WIP #

```[tasklist]
### To-do
- [] Get google sheets or some other spreasheet to work again
- [] Get date with all lists
- [x] Pre sort by APL score
- [] Add relation data for series order
- [] Add series order
```

***

# APL - Anime Priority List

## What is APL?
APL is an automatic anime watch priority list maker.

## How does APL work?
APL uses AniList's API to gather a users completed and planning list which is then imported into a Google Sheet where the data can be sorted.

## What is the purpose of APL?
As I have over 250+ anime planning to watch I usually can't decide what to watch first so I created a spreadsheet by hand to sort which anime I should watch first. This program is just to add a quality of life change for me and stop me from staying up making spreadsheets by hand.

***

## APL Score v1
The APL Score is based on 3 factors:
1. Mean Score (M) - Base score of Anime.
2. B Factor (B) - Bingability of a series over 12 episodes long but less than 50 episodes long with a score over 75%. <img src="https://render.githubusercontent.com/render/math?math=B=(M-75)*10^-2">
3. P Factor (P) - If the previous season has been watched.
<img src="https://render.githubusercontent.com/render/math?math=APL%20Score%20=%20M%20\times%20(1%20%2B%20(B%20%2B%20P))">

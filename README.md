# APL
Automatic Anime watch priority list maker with AniList and Google Sheets

## Purpose
This program was made so I could more easily rank which anime I should watch first as I have a planning list of over 250+. This would make my previous method of ranking anime to watch first take significantly less time.

## Tutorial
WIP

## APL Score v1
The APL Score is based on 3 factors:
1. Mean Score (M) - Base score of Anime.
2. B Factor (B) - Bingability of a series over 12 episodes long but less than 50 episodes long with a score over 75%. <img src="https://render.githubusercontent.com/render/math?math=B=(M-75)*10^-2">
3. P Factor (P) - If the previous season has been watched.
<img src="https://render.githubusercontent.com/render/math?math=APL%20Score%20=%20M%20\times%20(1%20%2B%20(B%20%2B%20P))">


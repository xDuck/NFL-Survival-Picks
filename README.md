# NFL-Survival-Picks
Uses spread to most likely picks for each week.

1. Scrape spreads from [www.thelines.com](www.thelines.com)
2. Build edges between possible routes in the graph where all only positive spread games are connected and the weight is `-log(spread)`
3. Run bellman ford on the data
4. Result 

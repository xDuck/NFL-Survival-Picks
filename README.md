# NFL-Survival-Picks
Uses spread to most likely picks for each week.

1. Scrape spreads from [www.thelines.com](www.thelines.com)
2. Build edges between possible routes in the graph where all only positive spread games are connected and the weight is `-log(spread)`
3. Run bellman ford on the data
4. Result 

# 2019 Picks

* **Philadelphia** vs Redskins ✔
* **Baltimore** vs Cardinals ✔
* **New England** vs Jets ✔
* **LA Rams** vs Bucs
* **New Orleans** vs Bucs 
* **LA Chargers** vs Steelers 
* **Buffalo** vs Dolphins 
* **Pittsburgh** vs Steelers 
* **Seattle** vs Bucs 
* **Indianapolis** vs Dolphins 
* **San Francisco** vs Cardinals 
* **Chicago** vs Giants 
* **Dallas** vs Bills 
* **Cleveland** vs Bengals 
* **NY Giants** vs Dolphins 
* **Atlanta** vs Jaguars

*Note:* All teams picked were home teams
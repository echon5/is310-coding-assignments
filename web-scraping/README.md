# Bulbapedia Scraper: Which Pokémon Type Has the Highest Average Base Experience Yield?

## Wiki and Question
I'm scraping Bulbapedia (https://bulbapedia.bulbagarden.net), a community-run Pokémon encyclopedia built on MediaWiki.

**Question:** Which Pokémon type (element) has the highest average base experience yield?

**Why it might interest researchers:** Base experience yield is set by the game's designers and recorded by wiki editors, and it affects how quickly a player levels up by defeating different Pokémon. Comparing it across types shows which kinds of Pokémon the game rewards most, which could be a starting point for studying how design choices shape player strategies. This project measures only the designed values on the wiki, not what players actually do.

## Connection to Culture as Data
Bulbapedia is a community-built record of a game franchise, so the numbers I scraped reflect two layers of human decisions: the game designers who assigned each Pokémon a type and a base experience yield, and the wiki editors who chose to document those values and organize pages into type categories. Because defeating high-yield Pokémon levels a player's team faster, this number could shape which Pokémon players choose to battle when they want to level up quickly. My data does not show whether players actually behave that way, though. Answering that would need evidence of player practice, such as community leveling guides, forum discussions, or usage statistics. Treating the wiki as cultural data means asking how classification systems and documentation habits determine what can be measured, and what the numbers leave out.

## robots.txt
https://bulbapedia.bulbagarden.net/robots.txt

It allows crawling of `/wiki/` pages and disallows search, random page, `Shipping:` pages, page histories (`action=history`), and old revisions (`oldid=`). It requests a 5-second crawl delay.

My scraper stays within `/wiki/`, waits 5 seconds between requests, checks that each response has a 200 status before parsing, and identifies itself with an honest User-Agent that includes my NetID. I also reviewed the site's terms of use: I also reviewed the site's footer and copyright page. Bulbapedia's content is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 2.5, and I found nothing prohibiting small-scale scraping. My use is non-commercial, and I collect only a numeric value and Pokémon names from each page, not article text.

## How It Works
1. The script (`wiki_scraping.py`) downloads the category page for each of the 18 types (for example, `Category:Fire-type_Pokémon`) and collects the links to each Pokémon page.
2. It randomly samples up to 20 Pokémon per type (fixed seed of 310, so the sample is reproducible) and visits each Pokémon's page.
3. On each page it reads the "Base experience yield" row from the infobox. When the page lists several generation-specific values, it takes the last one, which is the most recent.
4. It saves every row to `bulbapedia_pokemon_xp.csv` (columns: pokemon, type, base_exp_yield, url) and prints the average by type. A Pokémon with two types appears once under each type.

## Results
Average base experience yield by type (sample of up to 20 Pokémon per type):

| Rank | Type | Average | n |
|---|---|---|---|
| 1 | Dragon | 223.1 | 20 |
| 2 | Fire | 210.9 | 20 |
| 3 | Electric | 198.2 | 20 |
| 4 | Fighting | 180.7 | 20 |
| 5 | Steel | 170.8 | 20 |
| 6 | Ice | 162.8 | 20 |
| 7 | Ghost | 162.3 | 20 |
| 8 | Fairy | 156.0 | 20 |
| 9 | Flying | 155.6 | 20 |
| 10 | Grass | 148.4 | 19 |
| 11 | Bug | 147.2 | 20 |
| 12 | Rock | 144.8 | 20 |
| 13 | Psychic | 144.6 | 20 |
| 14 | Dark | 144.3 | 20 |
| 15 | Poison | 133.4 | 20 |
| 16 | Water | 125.3 | 20 |
| 17 | Normal | 124.8 | 20 |
| 18 | Ground | 121.6 | 20 |

Dragon has the highest average. Grass has n=19 because one sampled Pokémon (Browt) had no base experience yield on the page, so it is left blank in the CSV and excluded from the average. 

## What I Actually Measured
I measured the base experience yield listed on Bulbapedia for a random sample of up to 20 Pokémon per type, using the most recent value when a page lists several generations. This is a game-mechanics number: how much experience a Pokémon gives when defeated. It is a proxy for "which type has the highest XP," not a measure of how strong, popular, or valuable a type is. The gap is that the ranking depends on which Pokémon landed in each sample. A type with a few high-yield Pokémon in its sample can look higher than it would across all its members, and the top few types are close enough that a different sample could reorder them. Dual-type Pokémon count toward both types, so the groups overlap. I also only read the first page of each category listing (up to 200 members), which may skew the sample toward certain generations. Someone would be wrong to conclude that Dragon-type Pokémon are the "best" type, or that this is the true average across every Pokémon of each type.

## AI Use
I used Claude (Anthropic) to help set up my environment, plan the scraper, and debug it. I reviewed and tested the code, spot-checked values against the wiki pages, and edited the README myself. 
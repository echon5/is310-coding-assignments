import csv
import json
import os
import random
import re
import time
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://bulbapedia.bulbagarden.net"
HEADERS = {"User-Agent": "is310-course-scraper/1.0 (student project; emchon2@illinois.edu)"}
REQUEST_DELAY = 5  # robots.txt Crawl-delay
OUTPUT_FILE = "bulbapedia_pokemon_xp.csv"
CACHE_FILE = "exp_cache.json"

TYPES = [
    "Normal", "Fire", "Water", "Electric", "Grass", "Ice",
    "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug",
    "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy",
]
SAMPLE_SIZE = 20  # Pokémon per type
random.seed(310)  # makes the sample reproducible


def fetch_soup(url):
    for attempt in range(3):
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
        except requests.exceptions.RequestException as error:
            print(f"Network problem ({error.__class__.__name__}). Waiting 30s, then retrying...")
            time.sleep(30)
            continue
        time.sleep(REQUEST_DELAY)
        if response.status_code != 200:
            print(f"Could not download {url}: HTTP {response.status_code}")
            return None
        return BeautifulSoup(response.text, "html.parser")
    print(f"Giving up on {url} after 3 attempts")
    return None


def get_pokemon_links(type_name):
    url = f"{BASE_URL}/wiki/Category:{type_name}-type_Pokémon"
    soup = fetch_soup(url)
    if soup is None:
        return []
    section = soup.find(id="mw-pages")
    if section is None:
        print(f"No mw-pages section on {url}")
        return []

    pokemon = []
    for item in section.find_all("li"):
        link = item.find("a", href=True)
        if link:
            name = link.get_text(strip=True).replace(" (Pokémon)", "")
            pokemon.append({"name": name, "url": BASE_URL + link["href"]})
    return pokemon


def get_base_exp(soup):
    label = soup.find(string=lambda s: s and "base experience yield" in s.lower())
    if label is None:
        return None
    cell = label.find_parent("td")
    if cell is None:
        return None
    text = cell.get_text(" ", strip=True)

    numbers = re.findall(r"\d+", text)  # last number = most recent generation's value
    return int(numbers[-1]) if numbers else None


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(cache, file)


def main():
    cache = load_cache()  # pages already scraped; also covers dual-type Pokémon
    print(f"Loaded {len(cache)} saved values from {CACHE_FILE}")
    rows = []

    for type_name in TYPES:
        print(f"Collecting {type_name}-type Pokémon...")
        members = get_pokemon_links(type_name)
        members = random.sample(members, min(SAMPLE_SIZE, len(members)))
        for member in members:
            if member["url"] not in cache:
                print(f"  Fetching {member['name']}")
                soup = fetch_soup(member["url"])
                exp = get_base_exp(soup) if soup else None
                if exp is not None:
                    cache[member["url"]] = exp
                    save_cache(cache)
            rows.append({
                "pokemon": member["name"],
                "type": type_name,
                "base_exp_yield": cache.get(member["url"]),
                "url": member["url"],
            })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["pokemon", "type", "base_exp_yield", "url"])
        writer.writeheader()
        writer.writerows(rows)

    totals = defaultdict(list)
    for row in rows:
        if row["base_exp_yield"] is not None:
            totals[row["type"]].append(row["base_exp_yield"])

    print("\nAverage base experience yield by type:")
    for type_name, values in sorted(totals.items(), key=lambda x: sum(x[1]) / len(x[1]), reverse=True):
        print(f"{type_name}: {sum(values) / len(values):.1f} (n={len(values)})")


if __name__ == "__main__":
    main()
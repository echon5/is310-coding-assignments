import requests
import json

# API 1: Wikipedia (MediaWiki Action API)
wiki_url = "https://en.wikipedia.org/w/api.php"

wiki_params = {
    "action": "query",
    "prop": "extracts",
    "exintro": True,
    "explaintext": True,
    "titles": "Vincent van Gogh",
    "format": "json"
}

headers = {
    "User-Agent": "IS310CultureResearch/1.0 (student educational project)"
}

wiki_response = requests.get(
    wiki_url,
    params=wiki_params,
    headers=headers,
    timeout=15
)

if wiki_response.status_code == 200:
    wiki_data = wiki_response.json()
    pages = wiki_data["query"]["pages"]
    wiki_page = list(pages.values())[0]

    wiki_item = {
        "pageid": wiki_page.get("pageid"),
        "title": wiki_page.get("title"),
        "extract": wiki_page.get("extract")
    }

    with open("wikipedia_vangogh.json", "w", encoding="utf-8") as file:
        json.dump(wiki_item, file, indent=4)

    print("Saved wikipedia_vangogh.json successfully!")
    print("WIKIPEDIA API RESPONSE:")
    print(json.dumps(wiki_data, indent=4))
else:
    print("Wikipedia API request failed:", wiki_response.status_code)


# API 2: Metropolitan Museum of Art
met_url = "https://collectionapi.metmuseum.org/public/collection/v1.1/search"
met_params = {
    "q": "Vincent van Gogh",
    "artistOrCulture": "true",
    "hasImages": "true",
    "limit": 10
}

try:
    met_response = requests.get(
        met_url,
        params=met_params,
        timeout=15
    )

    if met_response.status_code == 200:
        met_data = met_response.json()

        print("\nMET MUSEUM API RESPONSE:")
        print(json.dumps(met_data, indent=4))

        object_ids = met_data.get("objectIDs") or []

        if object_ids:
            object_id = object_ids[0]

            object_url = (
                "https://collectionapi.metmuseum.org/"
                f"public/collection/v1/objects/{object_id}"
            )

            object_response = requests.get(
                object_url,
                timeout=15
            )

            if object_response.status_code == 200:
                artwork = object_response.json()

                item_data = {
                    "objectID": artwork.get("objectID"),
                    "title": artwork.get("title"),
                    "artistDisplayName": artwork.get("artistDisplayName"),
                    "objectDate": artwork.get("objectDate"),
                    "medium": artwork.get("medium"),
                    "department": artwork.get("department")
                }

                print("\nCONNECTED ARTWORK:")
                print(json.dumps(item_data, indent=4))

                with open(
                    "met_artwork.json",
                    "w",
                    encoding="utf-8"
                ) as file:
                    json.dump(item_data, file, indent=4)

                print("\nSaved met_artwork.json successfully!")

            else:
                print("Artwork lookup failed:", object_response.status_code)

        else:
            print("No matching artworks found.")

    else:
        print("Met API request failed:", met_response.status_code)

except requests.RequestException as error:
    print("Met API error:", error)
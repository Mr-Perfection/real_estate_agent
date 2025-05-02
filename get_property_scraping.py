from apify_client import ApifyClient
import os
from dotenv import load_dotenv

load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")

client = ApifyClient(APIFY_TOKEN)

def get_zillow_listing(zillow_url):
    run_input = { 
        "searchUrls": [
            { 
                "url": zillow_url
            }
        ],
        "maxItems": 1  # Limit to 1 item in the output
    }

    # Run the actor with the input
    run = client.actor("maxcopell/zillow-scraper").call(run_input=run_input)

    # Output dataset link
    print("💾 View full dataset here:", f"https://console.apify.com/storage/datasets/{run['defaultDatasetId']}")

    # Iterate over the dataset and stop once you get the first item
    dataset = client.dataset(run["defaultDatasetId"])
    listing_arr = []

    # Limit to the first item
    for idx, item in enumerate(dataset.iterate_items()):
        if idx >= 1:  # Stop after the first result
            break
        listing_arr.append("-"* 40)
        listing_arr.append(f"Address: {item.get('address')}")
        listing_arr.append(f"Price: {item.get('price')} ")
        listing_arr.append(f"Bedrooms: {item.get('bedrooms')}")
        listing_arr.append(f"Detail URL: {item.get('detailUrl')}")
    
    return "\n".join(listing_arr)
        
def parse_property_string(property_string: str) -> dict:
    # Split the string by lines
    lines = property_string.strip().split('\n')

    # Extract address, price, and description
    address = lines[0].replace("Address: ", "").strip()
    price = lines[1].replace("Price: ", "").strip()
    bedrooms = lines[2].replace("Bedrooms : ", "").strip()

    # Convert price to an integer (remove currency symbol and commas)
    price = int(price.replace('$', '').replace(',', '').strip())
    return {
        'address': address,
        'price': price,
        'bedrooms': bedrooms
    }
    
def main(zillow_url):
    property_string = get_zillow_listing(zillow_url=zillow_url)
    parse_property_string(property_string=property_string)
    return parse_property_string

if __name__ == "__main__":
    main()
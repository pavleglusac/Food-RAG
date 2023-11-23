import requests
import json

def get_pasta_ingredients():
    # Define the URL for the OLS API
    ols_api_url = "https://www.ebi.ac.uk/ols/api/"
    
    # Endpoint for searching within an ontology
    search_endpoint = "search?q={}&ontology=foodon"

    # Query for 'pasta' in FoodOn
    response = requests.get(ols_api_url + search_endpoint.format("pasta"))
    
    if response.status_code == 200:
        # Process the response JSON
        results = response.json()
        pretty_results = json.dumps(results, indent=4)
        with open("foodon.json", "w") as f:
            f.write(pretty_results)
        # Extract and return relevant information
        # Modify this part based on how you want to process the results
        return pretty_results
    else:
        return "Error: Unable to access OLS"

# Example Usage
pasta_ingredients = get_pasta_ingredients()
print(pasta_ingredients)

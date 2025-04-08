import requests
import pandas as pd
import re
from serpapi import GoogleSearch
from PyPDF2 import PdfReader
import os


SERPAPI_API_KEY = ''

# List of models
models = [
    "Seagate Barracuda 7200.12 500GB",
    "Western Digital Caviar Black 1TB",
    "Toshiba DT01ACA100 1TB",
    "Seagate ST2000DM008 2TB",
    "Hitachi Deskstar 7K1000.D 1TB",
    "Western Digital Green 2TB",
    "Seagate FreeAgent GoFlex 1TB",
    "Samsung Spinpoint F3 1TB",
    "Western Digital Caviar Blue 500GB",
    "Seagate Barracuda XT 3TB",
    "Hitachi Deskstar 5K3000 2TB",
    "Western Digital VelociRaptor 600GB",
    "Toshiba MQ01ABD100 1TB",
    "Seagate Momentus 7200.4 500GB",
    "Western Digital My Passport 500GB",
    "Seagate Constellation ES 2TB",
    "Western Digital RE4 2TB",
    "Hitachi Travelstar 5K500 500GB",
    "Samsung Spinpoint F4 2TB",
    "Seagate Barracuda 7200.11 1TB"
]

# Function to search for HDD model specifications using SerpAPI
def search_hdd_specs(model_name):
    search_url = f"https://serpapi.com/search.json?q={model_name.replace(' ', '+')}&api_key={SERPAPI_API_KEY}"
    response = requests.get(search_url)
    search_results = response.json()

    model_data = []
    
    if "organic_results" in search_results:
        for result in search_results["organic_results"]:
            model = result.get("title", "Unknown Model")
            link = result.get("link", "No Link")
            
            # Check if link is a PDF (this could be adjusted to better handle PDFs)
            if link.endswith(".pdf"):
                year = extract_year_from_pdf(link)
            else:
                year = "Unknown"

            model_data.append({
                "Model Name": model,
                "Link": link,
                "Year": year
            })
    
    return model_data

# Function to extract year from PDF
def extract_year_from_pdf(pdf_url):
    try:
        response = requests.get(pdf_url)
        pdf_file = response.content
        # Save the PDF temporarily
        with open("temp.pdf", "wb") as f:
            f.write(pdf_file)
        
        # Read the PDF content
        reader = PdfReader("temp.pdf")
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        # Search for year in the text (you can adjust the regex as needed)
        year_match = re.search(r"\b(20\d{2})\b", text)
        
        # Clean up the temporary PDF file
        os.remove("temp.pdf")
        
        return year_match.group(1) if year_match else "Unknown"
    
    except Exception as e:
        print(f"Error extracting from PDF {pdf_url}: {e}")
        return "Unknown"

# Main function to process the models and save the results in a CSV
def main():
    all_model_data = []
    
    for model in models:
        print(f"Searching for {model}...")
        model_data = search_hdd_specs(model)
        all_model_data.extend(model_data)
    
    # Convert the data to a DataFrame and save to a CSV
    df = pd.DataFrame(all_model_data)
    df.to_csv("hdd_models_specifications.csv", index=False)
    print("Results saved to 'hdd_models_specifications.csv'")

if __name__ == "__main__":
    main()

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from colorama import init, Fore

# Initialize colorama for colored output
init(autoreset=True)

def get_keyword_rank_and_volume(keyword, domain, region='in'):
    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1200,800')

    # Path to your chromedriver (download the correct version)
    chrome_driver_path = "chromedriver.exe"

    # Start the service
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Construct the search URL
    search_url = f"https://www.google.com/search?q={keyword}&gl={region}&num=20"

    try:
        driver.get(search_url)
        sleep(3)  # Give time for the page to load

        # Extract search result URLs
        all_results = driver.find_elements(By.CSS_SELECTOR, '.yuRUbf a')


        filtered_urls = []
        
        for result in all_results:
            # Check if the result is inside an element with class 'Wt5Tfe'
            try:
                parent = result.find_element(By.XPATH, './ancestor::*[contains(@class, "Wt5Tfe")]')
                if parent:
                    continue  # Skip results within the 'Wt5Tfe' class
            except NoSuchElementException:
                # If the parent is not found, the result is valid
                href = result.get_attribute('href')
                if href:
                    filtered_urls.append(href)

        # Print the filtered URLs in green
        print(Fore.GREEN + "Filtered results:", Fore.GREEN + str(filtered_urls))

        # Normalize the domain for matching (ignore 'www')
        normalized_domain = domain.replace("www.", "")
        rank = -1

        # Check ranking of the domain in search results
        for i, url in enumerate(filtered_urls):
            extracted_domain = url.split('/')[2].replace("www.", "")
            if extracted_domain == normalized_domain:
                rank = i + 1
                break

        if rank != -1:
            print(f"Domain '{domain}' found at position {rank}")
        else:
            print(f"Domain '{domain}' not found in top results")

        driver.quit()
        return rank if rank != -1 else 'Not Found'

    except Exception as e:
        print("An error occurred:", e)
        driver.quit()
        return None

# Example usage
keyword = 'games'
domain = 'olympics.com'
region = 'in'
rank = get_keyword_rank_and_volume(keyword, domain, region)
























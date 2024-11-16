import undetected_chromedriver as uc 
from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv

# A driver 
driver = Driver(uc = True, headless = True)
driver.get(r"https://codeforces.com/problemset")

# Landing page
page_0 = driver.page_source.encode()

# General pipeline to scrape
# Loop through tab (which contains list of files)
# First column: index
# Second column: Problem
# Third column: tags 
# Then, find the link of the problem and use Selenium to click
# Find the p tag which contains the problem statement (potentially in div class="problem-statement")
# Get the problem statement. 

# Skipping page 6 because something over there has a string which mess up the script
# Maybe will diagnose later

# Some are PDFs and not webpages
# Skip them 
skip = ["1939B", "1939A", "1938M", "1938L"]

num_pages = 100 # Number of pages to scrape
with open('problems2.csv', 'w') as f:
    prob_writer = csv.writer(f, delimiter = " ")

    for page in range(7, num_pages + 1):
        # Suburl differs depending on number of pages 
        # The first time, url doesn't matter 
        # Otherwise, we add .../problemset/page/<page-num> to the end 
        if page == 1:
            pass 
        else:
            new_url = f"https://codeforces.com/problemset/page/{page}"
            driver.get(new_url)

        # Find the table 
        tab = driver.find_element(By.TAG_NAME, "tbody")

        # A bunch of problems and their tags. In this format
        # First line: index
        # Second line: Problem
        # Third line: tags
        # Fourth line: rating 
        tab = tab.text
        lines = tab.splitlines()[1:]

        for x in range(0, len(lines), 4):
            index = lines[x] 
            name = lines[x+1]
            tags = lines[x+2]
            rating = lines[x+3]

            print(f"Looking for problem name: {name}")
            # Find the link of the problem and click it 
            driver.find_element(By.LINK_TEXT, name).click()

            # Get the source of the HTML
            page_source = str(driver.page_source.encode())

            # Beautiful soup parser 
            parser = BeautifulSoup(page_source, "html.parser")

            # Find the problem statement by the tag and class
            prob_div = parser.find('div', attrs = {'class' : 'problem-statement'})

            # Some problems are in PDF form so will have no HTML. In this case, skip them 
            if prob_div is None:
                continue
            
            paragraphs = [str(p_tag.get_text()) for p_tag in prob_div.find_all("p")]
            prob_text = '\n'.join(paragraphs)

            # Go back to the previous page in the driver 
            driver.back()

            # Write the row 
            prob_writer.writerow([index, name, tags, prob_text, rating])

        print(f"Finished page {page}")

driver.close()

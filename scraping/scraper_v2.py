import undetected_chromedriver as uc 
from selenium import webdriver
from seleniumbase import Driver 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time

NUM_PAGES = 100 

# Beautiful soup has a weird way of giving output
# Strip the output accordingly
def clean_output (string):
    return string.replace('\\n', '').strip()

# A driver 
driver = Driver(uc = True, headless = True)
driver.get(r"https://codeforces.com/problemset")

# Landing page 
page_0 = str(driver.page_source.encode())
page_0_parser = BeautifulSoup(page_0, "html.parser")

# Loop through all the rows. Except first row, which is header 
with open("problemsSecondHalf.csv", "w") as f:
    prob_writer = csv.writer(f, delimiter = " ")

    # Scraper stopped in the middle. 
    # Restart at page 47
    for page in range(47, NUM_PAGES + 1):
    # For the first page, don't do anything. We're already at the landing page 
    # Otherwise, we need to go to a new URL 
        if page != 1:
            url = f"https://codeforces.com/problemset/page/{page}"
            driver.get(url)
        
        # Get the page source 
        source = str(driver.page_source.encode())
        source_parser = BeautifulSoup(source, "html.parser")

        # Wait for the page to load 
        time.sleep(8)

        # Find the table 
        table = source_parser.find('table', attrs = {'class' : 'problems'})
        table = table.find('tbody')

        # Loop through all rows except the first, which is the header
        for row in table.find_all('tr')[1:]:
            # Get all the cells in the td tags 
            cells = row.find_all('td')

            # First cell has the index in an a tag 
            index = clean_output(cells[0].find('a').get_text())

            # Second cell has two divs 
            # First div stores the name, in an a tag 
            second_cell_divs = cells[1].find_all('div')
            name = clean_output(second_cell_divs[0].find('a').get_text())

            # Second div has a bunch of a tags, each one storing a paritcular problem tag 
            # But the tags could be empty. Default: NA signifies no tags are available
            tags = ["NA"]
            if second_cell_divs[1].find_all('a'):
                tags = [clean_output(link.get_text()) for link in second_cell_divs[1].find_all('a')]
            tags = ",".join(tags)

            # Ignore the third td tag 

            # The fourth td tag has the rating; a number in a span tag 
            # Again, it can be empty. We'll use -999 to signify a missing rating 
            if cells[3].find('span') is None:
                rating = -999
            else:
                rating = int(clean_output(cells[3].find('span').get_text()))

            # Get the problem statement now. 
            # Find the link of the problem name and click it
            # Many things can go wrong here, so this is wrapped in a try catch block
            try:
                # Find the link of the problem name and click it 
                driver.find_element(By.LINK_TEXT, name).click()

                # Get the HTML and create a new parser for it 
                subpage_source = str(driver.page_source.encode())
                subpage_parser = BeautifulSoup(subpage_source, "html.parser")

                # Find the div tag of the problem statement
                prob_div = subpage_parser.find('div', attrs = {'class' : 'problem-statement'})

                # Tenth div in the problem statement has the relevant text. 
                # This was manually counted and hard coded. 
                # Of fucking course, this is the only div which doesn't have an id or class
                prob_div = prob_div.find_all('div')[10]

                prob_statement = clean_output(prob_div.get_text())
            except:
                # No need to do anything fancy. Just move on 
                pass 
            finally:
                # Tell the driver to go back to the main page 
                driver.back()

            # Finally, write a row to the csv file 
            prob_writer.writerow([index, name, tags, prob_statement, rating])
            print(f"Writing problem {name} successful")
        
        print(f"Finished writing {page}")
            

        
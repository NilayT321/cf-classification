import undetected_chromedriver as uc 
import selenium
import time

options = uc.ChromeOptions()
options.headless = True

# A driver 
driver = uc.Chrome(use_subprocess = True, options = options)
driver.get("https://nowsecure.nl/")

time.sleep(20)

driver.save_screenshot("nowsecure.png")
driver.close()

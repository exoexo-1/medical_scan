from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import csv
import time
import requests

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # Keeps browser open
driver = webdriver.Chrome(options=options)

# Base URL format
BASE_URL = "https://openi.nlm.nih.gov/gridquery?coll=mc&it=xg&q=brain%20scan&m={m}&n={n}"

# Create folder to store images
SAVE_DIR = "brain_scan_images"
os.makedirs(SAVE_DIR, exist_ok=True)

# List of possible scan types (checking for variations)
SCAN_TYPES = ["CT", "MRI", "X-ray", "Ultrasound", "PET", "Microscopy", "Graphics", "Photographs", "Video",
              "Tomography", "Magnetic resonance", "FDG-PET","MR","computed-tomography"]

# Prepare CSV file
csv_filename = "brain_scan_dataset.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Image Name", "Scan Type(s)", "Scan Description", "Bottom Line", "Source URL"])

    # Loop through 12 pages (increments of 100)
    for page in range(12):
        m = page * 100 + 1  # Starting index for this page
        n = (page + 1) * 100  # Ending index for this page
        url = BASE_URL.format(m=m, n=n)

        print(f"\n🔍 Scraping Page {page + 1}: {url}")
        driver.get(url)
        time.sleep(5)  # Allow page to load fully

        # Extract all image elements
        image_elements = driver.find_elements(By.CLASS_NAME, "jg-entry")

        for idx, elem in enumerate(image_elements):
            img_tag = elem.find_element(By.TAG_NAME, "img")
            src_attr = img_tag.get_attribute("src")

            # Ensure correct URL formatting
            img_url = src_attr if src_attr.startswith("http") else "https://openi.nlm.nih.gov" + src_attr
            img_name = f"image{(page * 100) + idx + 1:04d}.png"

            # Extract scan description (ensuring full extraction)
            scan_description = "No description"
            try:
                desc_elem = elem.find_element(By.CLASS_NAME, "imageToolTipCaption")
                scan_description = desc_elem.get_attribute("innerText").strip()
            except:
                pass  # No description found

            # Extract bottom line (if available)
            bottom_line = "No bottom line"
            try:
                bottom_elem = elem.find_element(By.CLASS_NAME, "imageToolTipBottomLine")
                bottom_line = bottom_elem.get_attribute("innerText").strip()
            except:
                pass  # No bottom line found

            # Identify all scan types present in the description
            scan_types_found = [scan for scan in SCAN_TYPES if scan.lower() in scan_description.lower()]
            scan_type_str = ", ".join(scan_types_found) if scan_types_found else "Unknown"

            # Save image with better error handling
            img_path = os.path.join(SAVE_DIR, img_name)
            try:
                response = requests.get(img_url, timeout=10)
                response.raise_for_status()
                with open(img_path, "wb") as img_file:
                    img_file.write(response.content)
                print(f"✅ Downloaded: {img_name}")
                csv_writer.writerow([img_name, scan_type_str, scan_description, bottom_line, img_url])
            except requests.exceptions.RequestException as e:
                print(f"❌ Failed to download: {img_url} - Error: {e}")

            time.sleep(2)  # Delay between requests

driver.quit()  # Close browser after scraping
print(f"\n🎉 Scraping complete! Dataset saved as {csv_filename}")

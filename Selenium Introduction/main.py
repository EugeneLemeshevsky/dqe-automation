import time
import os
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class SeleniumWebDriverContextManager:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def __enter__(self) -> WebDriver:
        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()


def extract_table(driver: WebDriver, output_path: str):
    try:
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table"))
        )
        columns = table.find_elements(By.CLASS_NAME, "y-column")

        data = {}
        for column in columns:
            header = column.find_element(By.ID, "header").text.strip()
            cells = column.find_elements(By.CLASS_NAME, "cell-text")
            values = [cell.text.strip() for cell in cells if cell.text.strip() != header]
            data[header] = values

        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
        print(f"Table saved to {output_path}")
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error extracting table: {e}")


def extract_doughnut(driver: WebDriver, output_dir: str):
    try:
        doughnut = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pielayer"))
        )
        scrollbox = driver.find_element(By.CLASS_NAME, "scrollbox")
        filters = scrollbox.find_elements(By.CLASS_NAME, "traces")

        def get_chart_data():
            labels = doughnut.find_elements(By.CSS_SELECTOR, "text.slicetext[data-notex='1']")
            rows = []
            for label in labels:
                tspans = label.find_elements(By.TAG_NAME, "tspan")
                if len(tspans) >= 2:
                    rows.append([tspans[0].text.strip(), tspans[1].text.strip()])
            return rows

        def save_screenshot_and_csv(index):
            driver.save_screenshot(os.path.join(output_dir, f"screenshot{index}.png"))
            rows = get_chart_data()
            if rows:
                df = pd.DataFrame(rows, columns=["Category", "Value"])
            else:
                df = pd.DataFrame(columns=["Category", "Value"])
            df.to_csv(os.path.join(output_dir, f"doughnut{index}.csv"), index=False)
            print(f"Saved screenshot{index}.png and doughnut{index}.csv")

        # Initial state
        save_screenshot_and_csv(0)

        # Click each filter
        for i, f in enumerate(filters, start=1):
            try:
                f.click()
                time.sleep(0.5)
                save_screenshot_and_csv(i)
            except Exception as e:
                print(f"Error clicking filter {i}: {e}")

    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error extracting doughnut chart: {e}")


if __name__ == "__main__":
    with SeleniumWebDriverContextManager() as driver:
        file_path = os.path.abspath("report.html")
        driver.get(f"file:///{file_path}")
        time.sleep(2)

        output_dir = os.path.dirname(os.path.abspath(__file__))

        extract_table(driver, os.path.join(output_dir, "table.csv"))
        extract_doughnut(driver, output_dir)

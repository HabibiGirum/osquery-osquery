from selenium import webdriver

def open_google():
    try:
        # Specify the path to the ChromeDriver executable
        chrome_driver_path = '/Applications/Google Chrome.app/Contents/MacOS/chromedriver'
        
        # Create a new instance of the Chrome driver
        driver = webdriver.Chrome(executable_path=chrome_driver_path)

        # Open Google.com
        driver.get("https://www.google.com")

        # Optional: You can perform further actions or interact with the page here

    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Close the browser window
        if driver:
            driver.quit()
            print("Browser window closed.")

if __name__ == "__main__":
    open_google()

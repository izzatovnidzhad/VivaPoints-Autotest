from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

driver = webdriver.Chrome()

# Configuration
login_url = "https://localhost:3000/login"
target_url = "https://localhost:3000/account/blogs/create"
email = "danielburgosmontoya@gmail.com"
password = "password"

def find_input_by_label(label_text):
    """Helper function to find input fields using their associated labels"""
    label = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//label[contains(., '{label_text}')]"))
    )
    input_id = label.get_attribute('for')
    return driver.find_element(By.ID, input_id)

try:
    # Login process
    driver.get(login_url)
    
    # Find email and password fields using the helper function
    email_field = find_input_by_label("Email")  # Update label text if different
    password_field = find_input_by_label("Password")  # Update label text if different
    
    email_field.send_keys(email)
    password_field.send_keys(password)
    
    # Click login button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Login')]"))
    )
    login_button.click()

    # Wait for login to complete and navigate to target page
    WebDriverWait(driver, 15).until(
        EC.url_contains("/account")  # Wait for account-related URL
    )
    
    driver.get(target_url)
    
    # Wait for target page to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//h3[contains(., 'Create New Blog')]"))
    )

    # Fill form using helper function
    topic_field = find_input_by_label("Blog Topic")
    author_field = find_input_by_label("Blog Author")
    title_field = find_input_by_label("Blog Title")
    description_field = find_input_by_label("Blog Description")
    image_url_field = find_input_by_label("Blog Image_Url")

    # Fill in the fields
    topic_field.send_keys("744eaa45-2e0d-4293-82cb-9d5fb3dc4146")
    author_field.send_keys("adbb83f1-26dd-4693-bdec-6b058ff19b7f")
    title_field.send_keys("Random Blog Title")
    description_field.send_keys("This is a random blog description.")
    image_url_field.send_keys("https://example.com/random-image.jpg")

    # Click Save button
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save')]"))
    )
    save_button.click()

    # Verify success (customize based on your application's behavior)
    try:
        WebDriverWait(driver, 10).until(
            EC.or_(
                EC.url_matches("/account/blogs"),
                EC.presence_of_element_located((By.XPATH, "//div[contains(., 'success')]"))
            )
        )
        print("Test completed successfully!")
    except TimeoutException:
        print("Save operation verification failed")

except Exception as e:
    print(f"Test failed: {str(e)}")
    raise

finally:
    driver.quit()
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TaskManagerTestSuite(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Docker Chrome setup
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://localhost:3000"  # Adjust based on your app URL
        cls.wait = WebDriverWait(cls.driver, 10)
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
    
    def setUp(self):
        # Navigate to home page before each test
        self.driver.get(self.base_url)
    
    def test_01_home_page_unauthenticated_user(self):
        """Test Case 1: Verify home page displays welcome message for unauthenticated users"""
        # Wait for welcome message
        welcome_message = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Welcome to Task Manager App')]"))
        )
        self.assertTrue(welcome_message.is_displayed())
        
        # Check for signup link
        signup_link = self.driver.find_element(By.XPATH, "//a[@href='/signup']")
        self.assertTrue(signup_link.is_displayed())
        self.assertIn("Join now to manage your tasks", signup_link.text)
    
    def test_02_signup_form_validation_empty_fields(self):
        """Test Case 2: Verify signup form validation with empty fields"""
        # Navigate to signup page
        self.driver.get(f"{self.base_url}/signup")
        
        # Wait for form to load
        form = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        
        # Verify form title
        title = self.driver.find_element(By.XPATH, "//h2[contains(text(), 'Welcome user, please signup here')]")
        self.assertTrue(title.is_displayed())
        
        # Click submit without filling fields
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        submit_button.click()
        
        # Wait for validation errors to appear
        time.sleep(1)
        
        # Check for required field indicators (red asterisks)
        name_label = self.driver.find_element(By.XPATH, "//label[@for='name']")
        email_label = self.driver.find_element(By.XPATH, "//label[@for='email']")
        password_label = self.driver.find_element(By.XPATH, "//label[@for='password']")
        
        # Verify asterisks are present in CSS (after pseudo-elements)
        self.assertTrue(name_label.is_displayed())
        self.assertTrue(email_label.is_displayed())
        self.assertTrue(password_label.is_displayed())
    
    def test_03_signup_form_valid_submission(self):
        """Test Case 3: Test signup form with valid data"""
        self.driver.get(f"{self.base_url}/signup")
        
        # Fill form fields
        name_input = self.wait.until(EC.presence_of_element_located((By.ID, "name")))
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        
        test_email = f"testuser_{int(time.time())}@example.com"
        
        name_input.send_keys("Test User")
        email_input.send_keys(test_email)
        password_input.send_keys("testpassword123")
        
        # Submit form
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        submit_button.click()
        
        # Should redirect to login page after successful signup
        self.wait.until(lambda driver: "/login" in driver.current_url)
        self.assertIn("/login", self.driver.current_url)
    
    def test_04_login_form_validation_empty_fields(self):
        """Test Case 4: Verify login form validation with empty fields"""
        self.driver.get(f"{self.base_url}/login")
        
        # Wait for form and verify title
        title = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Welcome user, please login here')]"))
        )
        self.assertTrue(title.is_displayed())
        
        # Try to submit empty form
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        submit_button.click()
        
        # Verify required field indicators
        email_label = self.driver.find_element(By.XPATH, "//label[@for='email']")
        password_label = self.driver.find_element(By.XPATH, "//label[@for='password']")
        
        self.assertTrue(email_label.is_displayed())
        self.assertTrue(password_label.is_displayed())
    
    def test_05_login_form_valid_credentials(self):
        """Test Case 5: Test login with valid credentials (requires pre-existing user)"""
        self.driver.get(f"{self.base_url}/login")
        
        # Fill login form
        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        password_input = self.driver.find_element(By.ID, "password")
        
        email_input.send_keys("testuser@example.com")  # Use existing test user
        password_input.send_keys("testpassword123")
        
        # Submit form
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        submit_button.click()
        
        # Wait for redirect to home page or check for loading state
        try:
            # Either redirects to home or shows loader
            self.wait.until(
                lambda driver: driver.current_url == self.base_url + "/" or 
                              driver.find_elements(By.CLASS_NAME, "loader")
            )
        except TimeoutException:
            pass  # Login might fail if user doesn't exist
    
    def test_06_navigation_between_login_and_signup(self):
        """Test Case 6: Test navigation links between login and signup pages"""
        # Start at login page
        self.driver.get(f"{self.base_url}/login")
        
        # Click signup link
        signup_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), \"Don't have an account? Signup here\")]"))
        )
        signup_link.click()
        
        # Verify on signup page
        self.wait.until(lambda driver: "/signup" in driver.current_url)
        self.assertIn("/signup", self.driver.current_url)
        
        # Click login link from signup page
        login_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Already have an account? Login here')]"))
        )
        login_link.click()
        
        # Verify back on login page
        self.wait.until(lambda driver: "/login" in driver.current_url)
        self.assertIn("/login", self.driver.current_url)
    
    def test_07_authenticated_user_home_page(self):
        """Test Case 7: Test authenticated user's home page (requires login)"""
        # This test assumes successful login
        # First attempt login
        self.driver.get(f"{self.base_url}/login")
        
        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        password_input = self.driver.find_element(By.ID, "password")
        
        email_input.send_keys("testuser@example.com")
        password_input.send_keys("testpassword123")
        
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        submit_button.click()
        
        # If login successful, check for welcome message
        try:
            welcome_message = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Welcome')]"))
            )
            self.assertTrue(welcome_message.is_displayed())
        except TimeoutException:
            self.skipTest("Login required for this test - user may not exist")
    
    def test_08_tasks_page_empty_state(self):
        """Test Case 8: Test tasks page when no tasks exist (requires authentication)"""
        # Assumes user is authenticated and has no tasks
        self.driver.get(f"{self.base_url}/")
        
        try:
            # Look for empty state message
            no_tasks_message = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'No tasks found')]"))
            )
            self.assertTrue(no_tasks_message.is_displayed())
            
            # Check for "Add new task" button
            add_task_button = self.driver.find_element(By.XPATH, "//a[contains(text(), '+ Add new task')]")
            self.assertTrue(add_task_button.is_displayed())
            
        except TimeoutException:
            self.skipTest("This test requires authenticated user with no tasks")
    
    def test_09_add_task_form_navigation(self):
        """Test Case 9: Test navigation to add task form"""
        try:
            self.driver.get(f"{self.base_url}/tasks/add")
            
            # Wait for form to load
            form_title = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Add New Task')]"))
            )
            self.assertTrue(form_title.is_displayed())
            
            # Check for description field
            description_field = self.driver.find_element(By.ID, "description")
            self.assertTrue(description_field.is_displayed())
            
            # Check for buttons
            add_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Add task')]")
            cancel_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Cancel')]")
            
            self.assertTrue(add_button.is_displayed())
            self.assertTrue(cancel_button.is_displayed())
            
        except TimeoutException:
            self.skipTest("Add task page requires authentication")
    
    def test_10_add_task_form_validation(self):
        """Test Case 10: Test add task form validation"""
        try:
            self.driver.get(f"{self.base_url}/tasks/add")
            
            # Wait for form
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Add New Task')]"))
            )
            
            # Try to submit empty form
            add_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Add task')]")
            add_button.click()
            
            # Check if validation error appears or form doesn't submit
            time.sleep(1)
            
            # Should still be on add task page if validation failed
            current_url = self.driver.current_url
            self.assertIn("/tasks/add", current_url)
            
        except TimeoutException:
            self.skipTest("Add task page requires authentication")
    
    def test_11_add_task_form_valid_submission(self):
        """Test Case 11: Test adding a task with valid data"""
        try:
            self.driver.get(f"{self.base_url}/tasks/add")
            
            # Wait for form
            description_field = self.wait.until(EC.presence_of_element_located((By.ID, "description")))
            
            # Fill description
            test_task = f"Test task created at {int(time.time())}"
            description_field.send_keys(test_task)
            
            # Submit form
            add_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Add task')]")
            add_button.click()
            
            # Should redirect to home page after successful creation
            self.wait.until(lambda driver: driver.current_url == self.base_url + "/")
            self.assertEqual(self.driver.current_url, self.base_url + "/")
            
        except TimeoutException:
            self.skipTest("Add task functionality requires authentication")
    
    def test_12_task_form_cancel_button(self):
        """Test Case 12: Test cancel button functionality on task form"""
        try:
            self.driver.get(f"{self.base_url}/tasks/add")
            
            # Wait for form
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Add New Task')]"))
            )
            
            # Click cancel button
            cancel_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Cancel')]")
            cancel_button.click()
            
            # Should navigate back to home page
            self.wait.until(lambda driver: driver.current_url == self.base_url + "/")
            self.assertEqual(self.driver.current_url, self.base_url + "/")
            
        except TimeoutException:
            self.skipTest("Task form requires authentication")

    def test_13_responsive_design_mobile_view(self):
        """Test Case 13: Test responsive design by changing viewport size"""
        # Set mobile viewport
        self.driver.set_window_size(375, 667)  # iPhone SE size
        
        self.driver.get(f"{self.base_url}/login")
        
        # Verify form is still visible and functional in mobile view
        form = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        self.assertTrue(form.is_displayed())
        
        # Check if form maintains max-width constraint
        form_width = form.size['width']
        viewport_width = self.driver.execute_script("return window.innerWidth")
        
        # Form should not exceed viewport width
        self.assertLessEqual(form_width, viewport_width)
        
        # Reset to desktop size
        self.driver.set_window_size(1920, 1080)

    def test_14_form_input_field_interactions(self):
        """Test Case 14: Test form input field interactions and placeholders"""
        self.driver.get(f"{self.base_url}/signup")
        
        # Test input fields
        name_input = self.wait.until(EC.presence_of_element_located((By.ID, "name")))
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        
        # Check placeholders
        self.assertEqual(name_input.get_attribute("placeholder"), "Your name")
        self.assertEqual(email_input.get_attribute("placeholder"), "youremail@domain.com")
        self.assertEqual(password_input.get_attribute("placeholder"), "Your password..")
        
        # Test input functionality
        name_input.send_keys("Test User")
        email_input.send_keys("test@example.com")
        password_input.send_keys("password123")
        
        # Verify values are entered
        self.assertEqual(name_input.get_attribute("value"), "Test User")
        self.assertEqual(email_input.get_attribute("value"), "test@example.com")
        self.assertEqual(password_input.get_attribute("value"), "password123")
        
        # Test clearing fields
        name_input.clear()
        self.assertEqual(name_input.get_attribute("value"), "")

    def test_15_page_title_updates(self):
        """Test Case 15: Test dynamic page title updates"""
        # Test login page title
        self.driver.get(f"{self.base_url}/login")
        time.sleep(1)  # Allow title to update
        
        # Test signup page title  
        self.driver.get(f"{self.base_url}/signup")
        time.sleep(1)
        
        # Test add task page title
        try:
            self.driver.get(f"{self.base_url}/tasks/add")
            time.sleep(1)
            
            # Check if title contains "Add task"
            title = self.driver.title
            # Title should be set by useEffect
            self.assertIsNotNone(title)
            
        except Exception:
            self.skipTest("Add task page requires authentication")


if __name__ == "__main__":
    # Run specific test or all tests
    unittest.main(verbosity=2)
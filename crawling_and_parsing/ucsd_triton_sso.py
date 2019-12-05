from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

def initiate_sso_login(driver):
	'''
	function that initiates SSO login for UCSD students. Assumes that DUO push or call for approval
	are automatically sent without requiring any human intervention
	:param driver: driver object for browser
	:type driver: webdriver.firefox.webdriver.WebDriver
	'''
	assert isinstance(driver, webdriver.firefox.webdriver.WebDriver), "driver has to be of type webdriver.firefox.webdriver.WebDriver"

	username = None
	password = None

	assert username is not None, "You forgot to provide username for SSO"
	assert password is not None, "You forgot to provide password for SSO"

	status = WebDriverWait(driver, 60, poll_frequency=0.5).\
	    	until(lambda x: x.find_element_by_id('ssousername'), "Timed out waiting for SSO page!")

	print("*********** Initiating a SSO login ***********")
	# username for SSO
	driver.find_element_by_id('main-content').find_element_by_id('ssousername').send_keys(username)

	# password for SSO
	driver.find_element_by_id('main-content').find_element_by_id('ssopassword').send_keys(password)

	# click to login
	driver.find_element_by_id('main-content').find_element_by_name('_eventId_proceed').click()

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

def initiate_sso_login(driver):
	'''
	'''
	assert isinstance(driver, webdriver.firefox.webdriver.WebDriver), "driver has to be of type webdriver.firefox.webdriver.WebDriver"

	status = WebDriverWait(driver, 60, poll_frequency=0.5).\
	    	until(lambda x: x.find_element_by_id('ssousername'), "Timed out waiting for SSO page!")

	print("*********** Initiating a SSO login ***********")
	# username for SSO
	driver.find_element_by_id('main-content').find_element_by_id('ssousername').send_keys('xxxxxxxxx')

	# password for SSO
	driver.find_element_by_id('main-content').find_element_by_id('ssopassword').send_keys('xxxxxxxx')

	# click to login
	driver.find_element_by_id('main-content').find_element_by_name('_eventId_proceed').click()

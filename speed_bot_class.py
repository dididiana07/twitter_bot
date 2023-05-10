from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from time import sleep

class InternetSpeed:
    """Class that recollects the speed of your internet and sends tweet complaining to your provider."""
    def __init__(self, chromedriver_path):
        self.url_internet_speed = "https://www.speedtest.net/"
        self.url_twitter_login = "https://twitter.com/i/flow/login"
        self.chromedriver_path = chromedriver_path
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path)

    def __str__(self):
        return "Internet Speed."

    def speed_internet(self) -> tuple:
        """Returns a tuple with the up speed and the down speed of your internet."""
        show_results = "/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/div/div[2]/a"
        self.driver.get(url=self.url_internet_speed)
        sleep(2)
        self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        sleep(5)
        self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a').click()
        sleep(60)
        try:
            self.driver.find_element(By.XPATH, show_results).click()
        except NoSuchElementException:
            pass
        except ElementNotInteractableException:
            pass
        sleep(5)
        results = [result.text for result in self.driver.find_elements(By.CLASS_NAME, 'result-data-large')]
        return results[0], results[1]

    def generate_tweet(self):
        """Get the text that will be in your tweet."""
        up, down = self.speed_internet()
        TEXT = f"Hey internet provider, why is my internet speed {down}down/{up}up, " \
               f"when I pay for 150down/10up."
        return TEXT

    def send_tweet(self, twitter_user: str, twitter_password: str):
        """Send tweet complaining about the speed of your internet."""
        tweet = self.generate_tweet()
        tweet_btn = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/' \
                    'div/div[2]/div[3]/div/div/div[2]/div[3]'
        self.driver.get(url=self.url_twitter_login)
        sleep(5)
        user_input = self.driver.find_element(By.NAME, 'text')
        user_input.send_keys(twitter_user)
        user_input.send_keys(Keys.ENTER)
        sleep(5)
        password_input = self.driver.find_element(By.NAME, 'password')
        password_input.send_keys(twitter_password)
        password_input.send_keys(Keys.ENTER)
        sleep(5)
        tweet_input = self.driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-block')
        tweet_input.send_keys(tweet)
        sleep(5)
        tweet_button = self.driver.find_element(By.XPATH, tweet_btn)
        tweet_button.click()
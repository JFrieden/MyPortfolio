"""Class initializes as a webdriver connection
to the popular online game 2048. Contains 2 user facing methods.
One to observe the environment, and one to make moves"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains




options = Options()
options.add_argument('--disable-logging')
options.add_argument("--log-level=3")
options.add_argument('--headless')

class Env2048():
    def __init__(self) -> None:
        self.driver:webdriver.Chrome  = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get("https://play2048.co/")
        self.board = self.driver.find_element(By.CLASS_NAME, "game-container")
        self.done = False
        self.action_channel = ActionChains(self.driver)
        self.state = self.observe()
        self.driver.implicitly_wait(0.1)
        self.actions = [Keys.ARROW_UP,Keys.ARROW_DOWN,Keys.ARROW_LEFT, Keys.ARROW_RIGHT]
        
    def reset(self):
        self.driver.refresh()
        time.sleep(0.5)
        self.board = self.driver.find_element(By.CLASS_NAME, "game-container")
        self.tiles = self.driver.find_element(By.CLASS_NAME,'tile-container').find_elements(By.CLASS_NAME, "tile")
        self.state = self.observe()
        self.done = False
        return self.state
    
    def observe(self):
        self.state = [0]*16
        tiles = self.driver.find_element(By.CLASS_NAME,'tile-container').find_elements(By.CLASS_NAME, "tile")
        for tile in tiles:
            pos= tile.get_attribute("class").split()[2][-3:].split('-')
            self.state[((int(pos[1])-1) * 4) + int(pos[0])-1] = int(tile.find_element(By.CLASS_NAME, "tile-inner").text)
        return self.state
    
    def step(self, action):
        self.board.click()
        self.action_channel.send_keys(action)
        self.action_channel.perform()
        self.board = self.driver.find_element(By.CLASS_NAME, "game-container")
        if self.driver.find_elements(By.CLASS_NAME, "game-over"):
            self.done = True
        score_text = (self.driver.find_element(By.CLASS_NAME, "score-container").text).split()
        reward = int(score_text[1][1:]) if len(score_text)==2 else 0

        return self.observe(), reward, self.done
    
    
        
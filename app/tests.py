import re
import sys
import os
import time
import unittest
import logging
import subprocess
from selenium import webdriver

from app import app
from database import Database

class TestCase(unittest.TestCase):
    client = None

    def setUp(self):
        self.app = app.test_client()
        self.db = Database()
        self.db.create_table()

    def tearDown(self):
        self.db.drop_table()
        self.db.close_conn()

    def test_create_movie(self):
        expectedName = 'Minions'
        expectedCover = 'https://image.tmdb.org/t/p/w185_and_h278_bestv2/q0R4crx2SehcEEQEkYObktdeFy.jpg'
        self.db.insert_movie(expectedName, expectedCover)
        result = self.db.fetch_one(expectedName)
        assert result[1] == expectedName
        assert result[2] == expectedCover

    def test_fetch_movies(self):
        movies = []
        movies.append({
            'id' : 1,
            'name' : 'Spider-Man: Homecoming',
            'cover' : 'https://image.tmdb.org/t/p/w185_and_h278_bestv2/c24sv2weTHPsmDa7jEMN0m2P3RT.jpg'
        })
        movies.append({
            'id' : 2,
            'name' : 'Wonder Woman',
            'cover' : 'https://image.tmdb.org/t/p/w185_and_h278_bestv2/imekS7f1OuHyUP2LAiTEM0zBzUz.jpg'
        })
        for movie in movies:
            self.db.insert_movie(movie['name'], movie['cover'])
        result = self.db.fetch_movies()
        assert result == movies

    def test_selenium(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/app.py'
        p = subprocess.Popen(['python', path], stdout=subprocess.PIPE)
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            self.client = webdriver.Chrome(chrome_options=options,
                service_args=["--verbose", "--log-path=test-reports/chrome.log"])
        except Exception as e:
            print(e)
            self.skipTest('Web browser not available')
        # navigate to index page
        self.client.get('http://localhost:5000/')
        time.sleep(2)
        # get hello stranger text from the div element by xpath and css class name
        div_element = self.client.find_element_by_xpath('//div[@class="col-md-12"]').text
        self.assertTrue('Hello, Stranger!', div_element)
        # get name text box by name and type the given text
        self.client.find_element_by_name('name').send_keys('Avengers')
        # get cover text box by id and type the given the text
        self.client.find_element_by_id('cover').send_keys('https://image.tmdb.org/t/p/w1280/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg')
        # get button element by css selector class and click
        button = self.client.find_element_by_css_selector('.btn-success')
        button.click()
        time.sleep(1)
        page_source = self.client.page_source
        self.assertTrue(r'<h4 class="card-title ng-binding">Avengers</h4>' in page_source)
        self.assertTrue(r'src="https://image.tmdb.org/t/p/w1280/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg"' in page_source)
        self.client.get('http://localhost:5000/shutdown')
        self.client.quit()
        p.kill()

if __name__ == "__main__":
    unittest.main()

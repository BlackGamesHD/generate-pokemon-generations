# -*- coding: latin-1 -*-
import unidecode
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json


def main():
    generate_link_generations(1, 8)


def generate_link_generations(start, end):
    for generation in range(start, end+1):
        # Setting url
        if generation == 1:
            url = "https://en.wikipedia.org/wiki/List_of_generation_I_Pok%C3%A9mon"
            filename = "./output/first_generation.json"
        elif generation == 2:
            url = "https://en.wikipedia.org/wiki/List_of_generation_II_Pok%C3%A9mon"
            filename = "./output/second_generation.json"
        elif generation == 3:
            url = "https://en.wikipedia.org/wiki/List_of_generation_III_Pok%C3%A9mon"
            filename = "./output/third_generation.json"
        elif generation == 4:
            url = "https://en.wikipedia.org/wiki/List_of_generation_IV_Pok%C3%A9mon"
            filename = "./output/fourth_generation.json"
        elif generation == 5:
            url = "https://en.wikipedia.org/wiki/List_of_generation_V_Pok%C3%A9mon"
            filename = "./output/fifth_generation.json"
        elif generation == 6:
            url = "https://en.wikipedia.org/wiki/List_of_generation_VI_Pok%C3%A9mon"
            filename = "./output/sixth_generation.json"
        elif generation == 7:
            url = "https://en.wikipedia.org/wiki/List_of_generation_VII_Pok%C3%A9mon"
            filename = "./output/seventh_generation.json"
        elif generation == 8:
            url = "https://en.wikipedia.org/wiki/List_of_generation_VIII_Pok%C3%A9mon"
            filename = "./output/eighth_generation.json"
        else:
            return

        # Selenium configs
        option = Options()
        option.headless = False
        driver = webdriver.Chrome("./chromedriver.exe", options=option)

        # Openning page
        driver.get(url)

        # Searching table on page HTML
        if generation != 7:
            table_element = driver.find_element_by_xpath('//*[@id="mw-content-text"]/div/table[2]')
        elif generation == 7:
            table_element = driver.find_element_by_xpath('//*[@id="mw-content-text"]/div/table[3]')
        html_content = table_element.get_attribute('outerHTML')

        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find(name='table')

        # Creating table with Pandas
        df_full = pd.read_html(str(table))[0]
        df = df_full[["Name"]]
        df.columns = ["Name", ""]

        links = []
        for x in df["Name"]:
            # Replacing blank spaces and dots
            x = x.replace(" ", "-").replace(".", "").replace(":", "").replace("'", "")
            # Detecting female nidoran and male nidoran
            if x == "Nidoran\u2640":
                x = "nidoran-f"
            elif x == "Nidoran\u2642":
                x = "nidoran-m"

            current_link = "https://pokemondb.net/pokedex/" + unidecode.unidecode(x)
            if current_link in links:
                print("Repeated")
            elif current_link == "https://pokemondb.net/pokedex/MissingNo":
                print("Invalid")
            elif current_link == "https://pokemondb.net/pokedex/Unnamed-Legendary-Pokemon-(1)":
                print("Invalid")
            elif current_link == "https://pokemondb.net/pokedex/Unnamed-Legendary-Pokemon-(2)":
                print("Invalid")
            else:
                links.append(current_link)

        # Generating JSON
        js = (json.dumps(links))
        fp = open(filename, 'w')
        fp.write(js)
        fp.close()

        driver.quit()


main()

import json
import math
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup


def format_height(height):
    return height[0:height.index("m")+1]


def format_weight(weight):
    return weight[0:weight.index("kg")+2]


def generate_pokedex(start, end):
    for generation in range(start, end + 1):
        if generation == 1:
            source_file = "./output/first_generation.json"
            filename = "./pokedex/pokedex_first_generation.json"
        elif generation == 2:
            source_file = "./output/second_generation.json"
            filename = "./pokedex/pokedex_second_generation.json"
        elif generation == 3:
            source_file = "./output/third_generation.json"
            filename = "./pokedex/pokedex_third_generation.json"
        elif generation == 4:
            source_file = "./output/fourth_generation.json"
            filename = "./pokedex/pokedex_fourth_generation.json"
        elif generation == 5:
            source_file = "./output/fifth_generation.json"
            filename = "./pokedex/pokedex_fifth_generation.json"
        elif generation == 6:
            source_file = "./output/sixth_generation.json"
            filename = "./pokedex/pokedex_sixth_generation.json"
        elif generation == 7:
            source_file = "./output/seventh_generation.json"
            filename = "./pokedex/pokedex_seventh_generation.json"
        elif generation == 8:
            source_file = "./output/eighth_generation.json"
            filename = "./pokedex/pokedex_eighth_generation.json"
        else:
            return

        # Initializing pokedex dictionary
        pokedex = {"pokemon": []}

        # Selenium configs
        option = Options()
        option.headless = False
        driver = webdriver.Chrome("./chromedriver.exe", options=option)

        with open(source_file) as BOB:
            data = json.load(BOB)

        for url in data:
            # Open url
            driver.get(url)

            # Getting page elements
            body_main_element = driver.find_element_by_xpath('/html/body/main')
            page_body_html = body_main_element.get_attribute('outerHTML')

            # Parsing HTML and retrieving elements with BeautifulSoup
            page_soup = soup(page_body_html, "html.parser")
            pokemon_name_element = page_soup.find("h1")
            evolution_chart = page_soup.find("div", {"class": "infocard-list-evo"})
            effectiveness_table = page_soup.findAll("table", {"class": "type-table type-table-pokedex"})
            table = page_soup.find("table", {"class": "vitals-table"})

            # Creating pokemon effectiveness table with Pandas
            df_first = pd.read_html(str(effectiveness_table[0]))[0]
            df_second = pd.read_html(str(effectiveness_table[1]))[0]
            df_full = pd.concat([df_first, df_second], 1).fillna("0").astype(str)
            effectiveness = {
                "normal": df_full["Nor"].values[0],
                "fire": df_full["Fir"].values[0],
                "water": df_full["Wat"].values[0],
                "electric": df_full['Ele'].values[0],
                "grass": df_full['Gra'].values[0],
                "ice": df_full['Ice'].values[0],
                "fighting": df_full['Fig'].values[0],
                "poison": df_full['Poi'].values[0],
                "ground": df_full['Gro'].values[0],
                "flying": df_full['Fly'].values[0],
                "psychic": df_full['Psy'].values[0],
                "bug": df_full['Bug'].values[0],
                "rock": df_full['Roc'].values[0],
                "ghost": df_full['Gho'].values[0],
                "dragon": df_full['Dra'].values[0],
                "dark": df_full['Dar'].values[0],
                "steel": df_full['Ste'].values[0],
                "fairy": df_full['Fai'].values[0],
            }

            # Getting evolution

            # Creating general info table with Pandas
            df_full = pd.read_html(str(table))[0]
            df = df_full[[0, 1]]
            df.columns = ["Field", "Value"]

            # Dictionary with pokemon info
            pokemon_info = {"num": df["Value"][0], "name": pokemon_name_element.text, "type": df["Value"][1].split(" "),
                            "height": format_height(df["Value"][3]), "weight": format_weight(df["Value"][4]),
                            "img": "https://www.serebii.net/pokemongo/pokemon/" + df["Value"][0] + ".png",
                            "effectiveness": effectiveness}

            # Pushing pokemon to Pokedex
            pokedex["pokemon"].append(pokemon_info)

        # Generating JSON
        js = (json.dumps(pokedex))
        fp = open(filename, 'w')
        fp.write(js)
        fp.close()
        driver.quit()


def main():
    generate_pokedex(1,8)

main()
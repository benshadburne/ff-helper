from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from nameparser import HumanName
import time
import sys

#run in ff-helper directory

drafting = True
html_old = ""
team_name = "Team S"
playertiers = {}
players_removed = []
driver = webdriver.Firefox()
loading_speed = 4  # number of characters to print out per second
loading_string = "." * 6  # characters to print out one by one (6 dots in this example)

#give url of draft
# url = input()
# driver.get(r'https://fantasy.espn.com/football/draft?leagueId=636918829&seasonId=2022&teamId=14&memberId={DE6199FE-FA25-414E-A199-FEFA25814E8E}')
# driver.get(r'')
driver.get(r'https://www.espn.com')

print('Wait until you enter the draft, then copy the url here: ')

connection = False

while not connection:
    try:
    
        url = str(input()).encode('unicode-escape').decode()
        driver.get(url)
        connection = True
    except:
        print('Error with URL, try again.')
        pass

time.sleep(3)

text_file = open("C:/Users/bhsha/OneDrive/Documents/GitHub/ff-helper/tiers.txt", "r")
tiers = text_file.readlines()

#populate playertiers dictionary from local tiers file
for line in tiers:
    a = line.split(':     ')[0]
    b = line.split(':     ')[1].rstrip().split(', ')
    playertiers[a] = b

def return_abr_name(name):
    full_name =""
    if name.first[0:1] == 'J' and name.last == "Williams":
        full_name = name.first[0:4] + '. ' + name.last
    elif 'D/ST' in name:
        full_name = name.first + ' DST'
    else:
        if name.title:
            full_name = full_name + name.title[0:1] + '. '
        if name.first:
            full_name = full_name + name.first[0:1] + '. '
        if name.last:
            full_name = full_name + name.last + ' '
        if name.suffix:
            full_name = full_name + name.suffix
    full_name = full_name.strip()
    return full_name


    # if name.suffix:
    #     name = name.first[0:1] + '. ' + name.last + ' ' + name.suffix
    #     name.strip()
    # elif name.title and not name.first:
    #     name = name.title[0:1] + '. ' + name.last
    #     name.strip()
    # elif 'D/ST' in name:
    #     name = name.first + ' DST'
    #     name.strip()
    # elif name.first[0:1] == 'J' and name.last == "Williams":
    #     name = name.first[0:4] + '. ' + name.last
    # else:
    #     name = name.first[0:1] + '. ' + name.last
    #     name.strip()
    # return name

def remove_player(name):
    if name not in players_removed:
        for key in playertiers:
            if name in str(playertiers[key]):
                a = playertiers[key]
                a.remove(name)
                playertiers[key] = a
                players_removed.append(name)
                print('Player Drafted: ',name)

def update_right_column(soup):
    try:
        for child in soup.main.div.div.div.next_sibling.next_sibling.div.next_sibling.next_sibling.div.div.next_sibling.div.ul.children:
            name = HumanName(child.div.div.next_sibling.span.contents[0])
            name = return_abr_name(name)
            remove_player(name)
    except:
        print('Waiting for ad to finish')
        pass

def update_from_teams(driver):
    # picks = driver.find_elements(by=By.CLASS_NAME, value="pick-component")
    # for pick in picks:
    a = driver.find_element(by=By.CLASS_NAME, value="dropdown__select")
    teams = a.find_elements(By.XPATH, "//child::option")
    try:
        my_team = ""
        for team in teams:
            if team.text.startswith('TEAM '):
                team.click()
                if team.text.endswith("TEAM S"):
                    my_team = team
                time.sleep(.1)
                html2 = driver.find_element(By.XPATH, "//html").get_attribute('outerHTML')
                soup2 = BeautifulSoup(html2, 'html.parser')
                # print(team.text, ' Clicked')
                for child in soup2.main.div.div.div.next_sibling.next_sibling.div.div.div.next_sibling.div.next_sibling.div.div.div.div.div.next_sibling.table.tbody.children:
                    try:
                        # print(player.td.next_sibling.div.div.div.span.text)
                        name = HumanName(child.td.next_sibling.div.div.div.span.text)
                        name = return_abr_name(name)
                        remove_player(name)
                    except:
                        pass
                        # print('player read error')
        my_team.click()

            # print(pick.text)
            # pick.click()
            # for player in soup.main.div.div.div.next_sibling.next_sibling.div.div.div.next_sibling.div.next_sibling.div.div.div.div.div.next_sibling.table.tbody.children:

            # for player in soup.main.div.div.div.next_sibling.next_sibling.div.div.div.next_sibling.div.next_sibling.div.div.div.div.div.next_sibling.table.tbody.children:
            #     try:
            #         print(player.td.next_sibling.div.div.div.span.text)
            #         name = HumanName(player.td.next_sibling.div.div.div.span.text)
            #         name = return_abr_name(name, child)
            #         remove_player(name)
            #     except:
            #         print('player read error')
            
            # /main/div/div/div[3]/div[1]/div[1]/div[2]/div[2]/div/div/div/div/div[2]/table/tbody

            # /main/div/div/div[3]/div[1]/div[1]/div[2]/div[2]/div/div/div/div/div[2]/table/tbody/tr[1]/td[2]/div/div/div/div/span[1]/a

    except:
        print("button click error")

    # buttons = driver.find_elements(By.TAG_NAME, 'button')
    # for button in buttons:
    #     if 'Pick History' in button.text:
    #         button.click()

    #         try:
    #             for round in soup.main.div.div.div.next_sibling.next_sibling.div.next_sibling.div.next_sibling.div.div.div.next_sibling.div.div.next_sibling.children:
    #                 for player in round.div.next_sibling.div.div.div.div.div.next_sibling.next_sibling.children:
    #                     name = name = HumanName(player.div.div.div.next_sibling.div.div.next_sibling.div.div.div.div.div.div.next_sibling.div.span.span.a.contents[0])
    #                     name = return_abr_name(name)
    #                     remove_player(name)
    #         except:
    #             print("An exception occurred")
            
        # /main/div/div/div[3]/div[2]/div[2]/div/div/div[2]/div/div[2] rounds list

        # /main/div/div/div[3]/div[2]/div[2]/div/div/div[2]/div/div[2]    /div[1]  /div[2]/div/div[1]/div/div/div[3]   /div[1] players list

        # /main/div/div/div[3]/div[2]/div[2]/div/div/div[2]/div/div[2]    /div[1]   /div[2]/div/div[1]/div/div/div[3]  /div[1] /div/div/div[2]/div/div[2]/div/div/div/div/div/div[2]/div[1]/span/span/a path to name of player

    # for child in soup.main.div.div.div.next_sibling.next_sibling.div.div.div.next_sibling.div.next_sibling.div.div.div.div.div.next_sibling.table.tbody.children:
    #     name = HumanName(child.td.next_sibling.div.div.div.div.span.a.contents[0])

def loading():
    #  track both the current character and its index for easier backtracking later
    for index, char in enumerate(loading_string):
        # you can check your loading status here
        # if the loading is done set `loading` to false and break
        sys.stdout.write(char)  # write the next char to STDOUT
        sys.stdout.flush()  # flush the output
        time.sleep(2.0 / loading_speed)  # wait to match our speed
    index += 1  # lists are zero indexed, we need to increase by one for the accurate count
    # backtrack the written characters, overwrite them with space, backtrack again:
    sys.stdout.write("\b" * index + " " * index + "\b" * index)
    sys.stdout.flush()  # flush the output

while drafting:
    html = driver.find_element(By.XPATH, "//html").get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    update_right_column(soup)

    # update_from_history(soup)
    # #update picked players from right column
    # for child in soup.main.div.div.div.next_sibling.next_sibling.div.next_sibling.next_sibling.div.div.next_sibling.div.ul.children:
    #     name = HumanName(child.div.div.next_sibling.span.contents[0])
    #     # print(name.first, name.last, name.suffix)
    #     if name.suffix:
    #         name = name.first[0:1] + '. ' + name.last + ' ' + name.suffix
    #         name.strip()
    #     elif name.title and not name.first:
    #         name = name.title[0:1] + '. ' + name.last
    #         name.strip()
    #     elif name.suffix == 'D/ST':
    #         name = child.div.div.next_sibling.span.next_sibling.contents + ' DST'
    #         name.strip()
    #     else:
    #         name = name.first[0:1] + '. ' + name.last
    #         name.strip()

    #     if name not in players_removed:
    #         for key in playertiers:
    #             if name in str(playertiers[key]):
    #                 a = playertiers[key]
    #                 a.remove(name)
    #                 playertiers[key] = a
    #                 players_removed.append(name)
    #                 print('Player Drafted: ',name)

    #update picked players from teams

            
    #determine if it's your pick
    if 'You are on the clock!' in str(soup):
        update_from_teams(driver)
        for key in playertiers:
            print(key, ": ", str(playertiers[key]).replace('[','').replace(']','').replace("'",''))
        while 'You are on the clock!' in str(soup):
            html = driver.find_element(By.XPATH, "//html").get_attribute('outerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            loading()
            
    
    #wait 2s
    loading()
    if "Your roster is now full and you've completed your draft!" in str(soup):
        drafting = False

print('Draft done')
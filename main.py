import login
from pygame.locals import *
import os
import uno_cards
import sqlite3
import sys
import gui
import logging
import datetime


def menu(u):
    """A Function that gives the user options on what they want to do next"""
    logger = logging.getLogger(f"{__name__}")
    logger.info(f"Currently on the Main Menu, current user is: {u}")
    user = u
    while True:
        option = gui.main_menu_loop()
        if option == "play":
            logger.info(f"Pressed the play button")
            main_game_uno(user)
        if option == "leaderboard":
            logger.info(f"Pressed the stats button")
            leaderboard(user)
        if option == "quit":
                logger.info(f"Pressed the quit button")
                sys.exit()
        if option == "back_button":
            logger.info(f"{user} has logged out")
            user = gui.startloop()
            gui.welcomeloop(user)
        


def leaderboard(user):
    """Calls the leaderboard menu in GUI module"""
    logger.info(f"{user} pressed leaderboard")
    gui.lead_menu(user)
    


def main_game_uno(user):
    """Function main purpose is to start a new game and iterate through this game until, it end condition is met. The loop also contains checks to run certain code"""
    choice = gui.choice_loop()
    logger.info(f"User chocie/gamemode: {choice}")
    if choice == "backtomenu":
        logger.info(f"{user} returned back to the menu choice = {choice}")
        return
    logger.info(f"{user} has chosen the {choice} gamemode")
    uno_deck = uno_cards.deck(choice)
    uno_deck.shuffle_cards()
    game = uno_cards.UNO(uno_deck,uno_deck.deal_hand(7),uno_deck.deal_hand(7),uno_deck.deal_hand(7),uno_deck.deal_hand(7),choice)

    first_card = uno_deck.deal_card()
    first_card_check = str(first_card).split(" ")
    logger.info(f"first card before {first_card_check}")
    while first_card_check[0] == "wild": #check if the first card is wild. If it is it will draw another car
        logger.warning(f"first card was equal to wild: {first_card_check}")
        first_card = uno_deck.deal_card()
        first_card_check = str(first_card).split(" ")

    logger.info(f"first card after {first_card_check}")
    game.game_setter(first_card)
    pick_up = uno_deck.deal_card()
    while game.end_check(user) != True: #game loop
        try:

            if True:
                if game.pick_up_card_used() == True:
                    logger.info("game.pick_up_card_used() is True")
                    pick_up = uno_deck.deal_card()
                    logger.info(f"pick up cards is: pick_up = {str(pick_up)}")
                    if pick_up == "end":
                        logger.warning("Game has ended and Index error is rasied due to no more cards") #No more cards
                        raise IndexError
                    game.player_move(pick_up,user) 
                else:
                    logger.info(f"pick_up card has not changed: {str(pick_up)}")
                    game.player_move(pick_up,user) #pick_up
            
            if game.plus_4_check() == True: #checks if player played plus 4
                logger.info("Plus 4 check is TRUE")
                add_card = []
                for i in range(4):
                    add_card.append(uno_deck.deal_card())
                logger.info(f"add_cards = {add_card} for plus 4")
                game.append_cards(add_card)

            if game.plus_2_check() == True: #checks if player played plus 2
                logger.info("Plus 2 check is TRUE")
                add_card = []
                for i in range(2):
                    add_card.append(uno_deck.deal_card())
                game.append_cards(add_card)


        except IndexError: #Game ended as draw 
            
            logger.info("Game ended with a draw")
            gui.drawloop()
            con = sqlite3.connect("uno_database.db")
            c = con.cursor()

            table = c.execute(f"""SELECT Games,Draws
                        FROM {choice}
                        WHERE UserName = '{user}'
                        """)
            table = [int(i) for i in c.fetchone()]
            logger.info(f"Games = {table[0]}, Draws = {table[1]}")
            table[0] += 1 # games
            table[1] += 1 # draws

            c.execute(f"""UPDATE {choice}
            SET Games = {table[0]}, Draws = {table[1]}
            WHERE UserName = '{user}'""")   
            logger.info(f"Games played {table[0]}, User Draws {table[1]}")
            con.commit()
            con.close()
            break





if __name__ == "__main__":
    logger = logging.getLogger(f"{__name__}")
    x = datetime.datetime.now()
    x = 'application_' + str(x.strftime("%x")) + " T"+ str(x.strftime("%X")) + '.log'
    x = str(x).replace("/","-").replace(" ","--").replace(":","-")
    logging.basicConfig(filename=f"Logs/{x}",filemode='w',format='%(name)s - %(asctime)s - %(levelname)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S',level=logging.INFO) #for logging
    logger.info(f'Application started')

    if os.path.exists("uno_database.db"): 
        logger.info(f"Database is already created")
    else:
        logger.info(f"Database does not exist")
        login.create()
        if os.path.exists("uno_database.db"):
            logger.info(f"Databse created")
        else:
            logger.error(f"Database does not exist")

    user = gui.startloop()
    logger.info(f"Player Username: {user}")
    gui.welcomeloop(user)
    menu(user)
        




    
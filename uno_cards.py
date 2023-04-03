from random import shuffle
from random import randint
import sqlite3
import gui
import extra_module
import logging

logger = logging.getLogger(f"{__name__}")

class cards:
    def __init__(self,colour,value):
        self._colour = colour
        self._value = value

    def __repr__(self):
        return f"{self._colour} {self._value}"
    
class deck:
    def __init__(self,string):
        self.__colour = ["red","green","blue","yellow"]
        self.__special_no_colour = ["plus_4","switch"]
        self.__special = ["block","reverse","plus_2"]
        self.__value = [str(i) for i in (range(0,10))]*2  
        self._deck_choice = string
        self._card = self._carddeck()
    
    def _carddeck(self):
        if self._deck_choice == "Numbers":
            card = [cards(c,v) for c in self.__colour for v in self.__value]
        elif self._deck_choice == "NoWilds":
            card = [cards(c,v) for c in self.__colour for v in self.__value] + [cards(c,v) for c in self.__colour for v in self.__special]*2
        elif self._deck_choice == "Normal":
            card = [cards(c,v) for c in self.__colour for v in self.__value] + [cards(c,v) for c in self.__colour for v in self.__special]*2 + [cards("wild",v) for v in self.__special_no_colour]*4 #4
        logger.info(f"Cards in the gamemode: {self._deck_choice} deck: {card}")
        return card


    def get_card(self):
        return self._card
    
    def get_count(self):
        return len(self._card)

    def shuffle_cards(self):
        shuffle(self._card)
        logger.info(f"shuffles cards: {self._card}")
        return self.get_card()

    def _deal(self, num):
        count = self.get_count()
        actual = min([count,num])
        logger.info(f"count: {count} and actual: {actual} and num: {num}")
        if count == 0:
            None
        cards = self._card[-actual:]
        logger.info(f"cards/self._cards: {cards}")
        self._card = self._card[:-actual]
        return cards

    def deal_hand(self,hand_size):
        return self._deal(hand_size)

    def deal_card(self):
        try:
            return self._deal(1)[0]
        except IndexError:
            logger.info(f"IndexError Raised to end game")
            return "end"



class UNO():
    def __init__(self,uno_deck,player1,player2,player3,player4,gamemode):
        self._deck = uno_deck
        self._player1 = player1
        self._player2 = player2
        self._player3 = player3
        self._player4 = player4
        self._order = [self._player1,self._player2,self._player3,self._player4]
        self._order_postion = 0
        self._chosen_card = None
        self._topcard = None
        self._cards_weight = {"plus_2":5,"plus_4":10,"block":3,"reverse":2,"switch":5} 
        self._postion_weight = 0
        self._turns = 0
        self._clockwise = True
        self._pickup = False
        self._colour = ""
        self._gamemode = gamemode


    def user_deck(self):
        """Returns the players deck"""
        return [str(i) for i in self._order[0]]

    def players_deck_len(self):
        """Returns the length of the players deck"""
        return [len(self._order[0]),len(self._order[1]),len(self._order[2]),len(self._order[3])]


    def postion_state(self):
        """Used to find where the current player is compared to the player front. If the Number retunred is #i=2 winning #i=0 drawing #-2 losing. i is postion_weight but as local variavble.
        z is the amount of cards in next person deck"""
        logger.info("Postion State")
        def postioing(i,z):
            if i < z:
                i = 2
            elif i > z:
                i = -2
            else:
                i = 0
            return i


        self._postion_weight = 0
        i = len(self._order[self._order_postion])
        logger.info(f"postion states clockwise = {self._clockwise}, order postion = {self._order_postion}")
        if self._clockwise == True:
            logger.info(f"postion states clockwise True, order postion = {self._order_postion}")
            if self._order_postion == 3:
                z = len(self._order[0])
                i = postioing(i,z)

            else:
                z = len(self._order[self._order_postion + 1])
                i = postioing(i,z)

        elif self._clockwise == False:
            if self._order_postion == 0:
                z = len(self._order[self._order[3]])
                i = postioing(i,z)

            else:
                z = len(self._order[self._order_postion - 1])
                i = postioing(i,z)

        logger.info(f"postion weight is {i} and z is = {z} and i was og {len(self._order[self._order_postion])} #i=2 winning #i=0 drawing #-2 losing")
        self._postion_weight = i

            
             


    def card_states(self):
        """Finds out what the best possible cards for the AI to use. It then uses the method postion weight to decide what would be problilty of what cards should be played"""

        def ai_choice(postion):
            logger.info(f"{list_for_cards} the psotion looking {list_for_cards[postion]}")
            for z in self._order[self._order_postion]:
                card_check = str(z).split(" ")
                if card_check[0] == list_for_cards[postion][0] and card_check[1] == list_for_cards[postion][1]:
                    logger.info(f"ai_choice broke with {card_check} and is was == to {list_for_cards[postion]} ")
                    break
            return str(z)

        top_current_card = str(self._topcard).split(" ")
        list_for_cards = []
        #Card counts:
        red_count = 0
        green_count = 0
        yellow_count = 0
        blue_count = 0
        logger.info(f"counts before: red {red_count} blue {blue_count} green {green_count} yellow {yellow_count}")


        for i in self._order[self._order_postion]:
            i = str(i).split() #splits cards into two strings e.g ["red" "2"]
            g = self._cards_weight.get(i[1],1) #g uses i to get the cards values/weights from a dictionay
            logger.info(f"This is g (card weight): {g}")
            logger.info(f"This after (cardname,weight) appended to list for cards: {[i[0],i[1],g]}")
            list_for_cards.append([i[0],i[1],g]) #appends to a list with the: card and its weights
        
        logger.info(f"list_for_cards before non playbale cards are removed: {list_for_cards}")
        #The list sorts and removes cards that cannot be equal too the card on top and appends pick up too
        list_for_cards = list(filter(lambda x: x[0] == top_current_card[0] or x[1] == top_current_card[1] or x[0] == "wild",list_for_cards)) + [["pick_up",None,0]]
        logger.info(f"list_for_cards after non playbale cards are removed: {list_for_cards}")
        count = len(list_for_cards)

        #For loop is used to give cards that are repeated more value/weight
        for i in range(count):
            if list_for_cards[i][0] == "red":
                red_count += 1
            elif list_for_cards[i][0] == "green":
                green_count += 1
            elif list_for_cards[i][0] == "yellow":
                yellow_count += 1
            elif list_for_cards[i][0] == "blue":
                blue_count += 1
        
        logger.info(f"counts after/amount_of_card_weight: red {red_count} blue {blue_count} green {green_count} yellow {yellow_count}")
        #Creates a new list with card colours and there weights/counts and sorts the from the heightst value to the 
        #lowest
        amount_of_card_weight = [["red",red_count],["green",green_count],["yellow",yellow_count],["blue",blue_count]]

        logger.info(f"Player {self._order_postion + 1} card colour weights/counts {amount_of_card_weight}")

        
        #Adds these values to current list with all the players cards and weights 
        for b in amount_of_card_weight:
            for z in range(len(list_for_cards)):
                if b[0] == list_for_cards[z][0]:
                    list_for_cards[z][2] += b[1] 

        logger.info(f"Player {self._order_postion + 1} deck with  new weights {list_for_cards}")
        
        list_for_cards = extra_module.quicksort(list_for_cards)
        logger.info(f"Player {self._order_postion + 1} quicksort used to sort deck: {list_for_cards}")
        
        self.postion_state() #Call postion state
        logger.info(f"Player {self._order_postion + 1} postion state is {self._postion_weight}")
        #Depending on the users postion state and chacne, is used to decide the player choice
        chance = randint(1,100) 
        if count >= 4:
            if self._postion_weight == 2:
                if chance > 0 and chance < 10:
                    logger.info(f"Player {self._order_postion + 1} played his best card")
                    return ai_choice(0)
                
                elif chance >= 10 and chance < 40:
                    logger.info(f"Player {self._order_postion + 1} played his second best card")
                    return ai_choice(1)

                else:
                    return ai_choice(2)
            elif self._postion_weight == 0:
                if chance > 0 and chance < 30:
                    logger.info(f"Player {self._order_postion + 1} played his best card")
                    return ai_choice(0)
                
                elif chance >= 30 and chance < 70:
                    logger.info(f"Player {self._order_postion + 1} played his second best card")
                    return ai_choice(1)

                else:
                    logger.info(f"Player {self._order_postion + 1} played worse card out of his options")
                    return ai_choice(2)
            else:
                if chance > 0 and chance < 50:
                    logger.info(f"Player {self._order_postion + 1} played his best card")
                    return ai_choice(0)
                
                elif chance >= 50 and chance < 80:
                    logger.info(f"Player {self._order_postion + 1} played his second best card")
                    return ai_choice(1)

                else:
                    logger.info(f"Player {self._order_postion + 1} played worse card out of his options")
                    return ai_choice(2)

        elif count == 3:
            
            if self._postion_weight == 2:
                if chance <= 50:
                    logger.info(f"Player {self._order_postion + 1} played his best card")
                    return ai_choice(0)
                else:
                    logger.info(f"Player {self._order_postion + 1} played worse card out of his options")
                    return ai_choice(1)
            elif self._postion_weight == 0:
                if chance <= 30:
                    logger.info(f"Player {self._order_postion + 1} played his best card")
                    return ai_choice(0)
                else:
                    logger.info(f"Player {self._order_postion + 1} played his second best card")
                    return ai_choice(1)
            else:
                if chance <= 15:
                    logger.info(f"Player {self._order_postion + 1} played his best card")
                    return ai_choice(0)
                else:
                    logger.info(f"Player {self._order_postion + 1} played worse card out of his options")
                    return ai_choice(1)

        elif count == 2:
            logger.info(f"Player {self._order_postion + 1} played his only card")
            return ai_choice(0)

        elif count == 1:
            logger.info(f"Player {self._order_postion + 1} has picked up")
            return "pick_up"
            
    def pick_up_card_used(self):
        if self._pickup == True:
            logger.info(f"self._pickup is True ")
            self._pickup = False
            return True
        return False

    def set_turn(self):
        """Set turns"""
        self._turns = 0
        logger.info(f"turns are set to {self._turns}")

    def set_order_clockwise(self):
        """Set order postion for the Uno players"""
        self._order_postion = 0



    def set_order_anti_clockwise(self):
        """Set order postion for the Uno players"""
        self._order_postion = 3


    def next_turn(self):
        """Changes who turn it is to play. Check which way the order is going too"""
        if self._clockwise == True:
            logger.info(f"Clockwise, bool should be True. self._clockwise = {self._clockwise}")
            if self._order_postion == 3: 
                self.set_order_clockwise()
            else:
                self._order_postion = self._order_postion + 1
        elif self._clockwise == False:
            logger.info(f"Anti Clockwsie, bool should be False. self._clockwise = {self._clockwise}")
            if self._order_postion == 0:
                self.set_order_anti_clockwise()
            else:
                self._order_postion = self._order_postion - 1

    def card_in_deck(self,pick_up_card):
        """Check if the card trying to be played is in the deck. Returns True if the if it in the deck else it returns False
        and force the user pick up a card without being able to play"""

        for i in self._order[self._order_postion]:
            if str(i) == str(self._player_move):
                logger.info(f"check if card in deck: {str(i)} should be the same as {str(self._player_move)}")
                return True

        if self._pickup == False:
            self._order[self._order_postion].append(pick_up_card)
            logger.info(f"check if card in deck: Deck after player {self._order_postion} picked up")
        return False
    

    def plus_4_check(self):
        """Returns True if card is == plus_4"""

        current_card = str(self._player_move).split(" ")
        try:
            if current_card[1] == "plus_4":
                logger.info(f"player {self._order_postion + 1} plus 4 test is True current_card[1] = {current_card[1]}")
                return True
            else:
                logger.info(f"player {self._order_postion + 1} plus 4 test is False")
                return False
        except IndexError:
            logger.warning(f"Index Error at Plus 4 check current card = {current_card}")


    def plus_2_check(self):
        """Returns True if card is == plus_2"""

        top_current_card = str(self._topcard).split(" ")
        current_card = str(self._player_move).split(" ")
        try:
            if current_card[0] == top_current_card[0] and current_card[1] == "plus_2":
                logger.info(f"player {self._order_postion + 1} plus 2 test is True: {top_current_card} == {current_card}")
                return True
            else:
                logger.info(f"player {self._order_postion + 1} plus 2 test is False")
                return False
        except IndexError:
            None


    def append_cards(self,*args):
        """Appends cards to the next player hand. The amount of cards depends on what function calls it"""
        for i in args:
            if self._clockwise == True:
                logger.info(f"player {self._order_postion + 1}  + {i}, clockwise True")
                self._order[self._order_postion].extend(i)
            else:
                logger.info(f"player {self._order_postion + 1}  + {i}, clockwise False")
                self._order[self._order_postion].extend(i)
            logger.info(f"player {self._order_postion + 1} deck is now {self._order[self._order_postion]}")
        


    
    def colour_check(self,colour): #check if it has use
        """Check if the string (colour), matches the colours. If it does it return TRUE else FAlSE"""
        if colour in ["red","green","yellow","blue"]:
            return True
        else:
            return False


    def update_player_hand(self,current_card):
        """A algorithm that removes a SINGLE card from current player hand after the card was played"""

        count = 0
        card_list = []
        for y in self._order[self._order_postion]:
            if current_card != str(y).split(" "):
                logger.info(f"current card: {current_card} should not == {str(y)}")
                card_list.append(y)
            else:
                logger.info(f"current card: {current_card} should  == {str(y)}")
                if count == 0:
                    count +=1 
                    logger.info(f"{y} will removed out of the deck and count == {count}")
                else:
                    logger.info(f"count should equal 1 already: {count}")
                    card_list.append(y)
        self._order[self._order_postion] = card_list
        logger.info(f"player {self._order_postion + 1} should not have {current_card} in it deck: {self._order[self._order_postion]}")



    def game_setter(self,top_card_setter):
        """Sets the top card, set the turn by calling a function and set the order by calling a function"""

        self._topcard = top_card_setter
        logger.info(f"Game Setter Called, top current card/startng card is {self._topcard}")
        self.set_turn()
        self.set_order_clockwise()


    def end_check(self,user):
        """This function connects to database, then it does a condtitional check to see if the current player meets the
        condititons. If they do, if it player 1: the user will recive addition to games and wins in. If player 1 loses 
        then player 1 recives additoion to games and loss by 1. ELSE if end check condtion is not TRUE then this code is skipped.
        The databasee is then close after."""

        def database_updates(user,worl):
            user_worl = c.execute(f"""SELECT Games, {worl}
            FROM {self._gamemode}
            WHERE UserName = '{user}'
            """)

            user_worl = [int(i) for i in c.fetchone()]
            logger.info(f"{user} Games Played {user_worl[0]} and {worl} {user_worl[1]}")
            user_worl[0] += 1 
            user_worl[1] += 1
            logger.info(f"After it been incremented {user} Games Played {user_worl[0]} and {worl} {user_worl[1]}")

            c.execute(f"""UPDATE {self._gamemode}
            SET Games = {user_worl[0]}, {worl} = {user_worl[1]}
            WHERE UserName = '{user}'""")


        con = sqlite3.connect("uno_database.db")
        c = con.cursor()
        end = False
        for i in range(4):
            g = len(self._order[i])
            # for x in self._order[i]:
            #     g = g + 1 #amount of cards in deck
            if g == 0:
                logger.info(f"Player {i+1} has trigged the end game")
                end = True
                e = i #Player who won is e
                break

        if end == True:
            if e == 0:
                logger.info(f"{user} has won")
                gui.winloop(user)
                database_updates(user,"Wins")

        
            else:
                logger.info(f"{user} has loss")
                gui.lossloop(e)
                database_updates(user,"Loss")

                
            con.commit()
            con.close()
            return True 

        con.close()

    def player_move(self,pick_up_card,user):
        """Displays the top card. Ask the current player what card he wants to play. If the player does not want to play
        the user can pick up card and is given a second chance to play a cards. It then calls function to check the card and
        saves it variable as boolean datatype. Then calls a fucntion to check if player mmets end condtions. After calls a 
        function for the next user turn"""
        self._colour = "" #set colour choice to nothing
        logger.info(f"Amount of cards all players have: {user}: {len(self._order[0])} cards | Player 2: {len(self._order[1])} cards | Player 3: {len(self._order[2])} cards | Player 4: {len(self._order[3])} cards")
        logger.info(f"all players decks: {user}: {self._order[0]} cards | Player 2: {self._order[1]} cards | Player 3: {self._order[2]} cards | Player 4: {self._order[3]} cards")
        logger.info(f"Card On Top: {self._topcard}")
        if self._order_postion == 0: #player1/user turn
            self._player_move = gui.playloop(user,self.user_deck(),self.players_deck_len(),self._topcard,pick_up_card)

            logger.info(f"{user} player_move is {self._player_move}")

            if self._player_move == "endgamerightnow": #ends game
                raise IndexError
            logger.info(f"Player{self._order_postion + 1}/{user}: {self._player_move} card played")
            if self._player_move[0].split()[0] == "wild": #check if player card is a wild
                logger.info(f"Player move is willd")
                self._colour = self._player_move[1]
                self._player_move = self._player_move[0]
        
                
                
            if self._player_move[0].replace(" ", "_") == "pick_up" or self._player_move == "":#Player picked up
                logger.info(f"Picked up card: {pick_up_card}")
                self._order[self._order_postion].append(pick_up_card)
                logger.info(f"Pick card should be in {user} deck: {self._order[self._order_postion]}")
                second_chance = self._player_move[1]
                self._pickup = True 
                
                if second_chance== "yes":
                    logger.info(f"second chance is True / {second_chance} == yes")
                    wild_check = str(self._order[self._order_postion][-1]).split()
                    if wild_check[0] == "wild":
                        logger.info(f"{wild_check} True / wild_check[0]: {wild_check[0]} == wild ")
                        self._player_move = gui.colour_loop(user,self.players_deck_len(),self._topcard,pick_up_card)
                        logger.info(f"self._player_move after wild/colour_loop: {self._player_move}")
                        self._colour = self._player_move[1]
                        self._player_move = self._player_move[0]
                        

                    self._player_move = self._order[self._order_postion][-1]
                    logger.info(f"{user} plays {self._player_move}")




        else: #AI
            self._player_move = self.card_states() #AI
            gui.displayloop(user,self.user_deck(),self.players_deck_len(),self._topcard,self._order_postion+1)
            logger.info(f'Player{self._order_postion + 1} Turn')
            logger.info(f'Player{self._order_postion + 1} wants to play {self._player_move}')

        
            if self._player_move.lower().replace(" ", "_") == "pick_up":
                logger.info(f"Player{self._order_postion + 1} wants to pick up, deck before pick up {self._order[self._order_postion]}")
                self._order[self._order_postion].append(pick_up_card)
                self._pickup = True
                logger.info(f"Player{self._order_postion + 1} deck after pick up {self._order[self._order_postion]}")
                self._player_move = self._order[self._order_postion][-1] #if AI player picked up they will always try to play because there already a saftey net so they cannot cheat 


        #AI and Player
        is_card_in_deck = self.card_in_deck(pick_up_card)
        if is_card_in_deck == True:
            self.play_card(pick_up_card)
        logger.info(f'Player{self._order_postion + 1} Move: {self._player_move}')

        self.next_turn() 
        

    def play_card(self,pick_up_card):
        """This functions replaces the top current card, with the card the user wants to play. It checks for what
        card it is to see if it has any special uses e.g. wild plus_4. Then function calls other functons to excute cards uses"""
        current_card = ""
        top_current_card = ""
        
        current_card = str(self._player_move).split(" ")
        top_current_card = str(self._topcard).split(" ")
        
        logger.info(f"current_card = {current_card} and top_current_card = {top_current_card}")

        if current_card[0] == "wild":

            logger.info(f"Current card is a wild")

            if self._order_postion == 0: #user playing
                logger.info(f"Player 1 played a wild")

                colour = self._colour
                logger.info(f"Player 1 chose the colour {colour}")
                if current_card[1] == "switch":
                    logger.info(f"Card is a switch/change colour")
                    colour = self._colour

                elif current_card[1] == "plus_4":
                    logger.info(f"Card is a plus 4")
                    if self.plus_4_check() == True:
                        colour = self._colour
                self._topcard = cards(colour,"")
                self.update_player_hand(current_card)


            else: #Ai players
                logger.info(f"Player {self._order_postion + 1} played a wild")
                red_count = 0
                blue_count = 0
                yellow_count = 0
                green_count = 0
                list_for_cards = []
                for i in self._order[self._order_postion]:
                    i = str(i).split()
                    g = self._cards_weight.get(i[1],1)
                    list_for_cards.append([i[0],i[1],g])

                logger.info(f"list_for_cards card weights without checking amount of card colours in total: {list_for_cards}")

                for i in range(len(self._order[self._order_postion])):
                    if list_for_cards[i][0] == "red":
                        red_count = red_count + 1
                    elif list_for_cards[i][0] == "green":
                        green_count = green_count + 1
                    elif list_for_cards[i][0] == "yellow":
                        yellow_count = yellow_count + 1
                    elif list_for_cards[i][0] == "blue":
                        blue_count = blue_count + 1


                amount_of_card_weight = [["red",red_count],["green",green_count],["yellow",yellow_count],["blue",blue_count]]

                logger.info(f"All card weights in total unsorted: amount_of_card_weight = {amount_of_card_weight}")

                #Merge sort
                amount_of_card_weight = extra_module.merge_sort(amount_of_card_weight)

                logger.info(f"All card weights in total sorted: amount_of_card_weight = {amount_of_card_weight}")
                
                chance = randint(1,20)
                if chance > 7 or list_for_cards[1][1] == 0:
                    colour = amount_of_card_weight[0][0]
                    logger.info(f"Chose the best colour {colour}")
                else:
                    colour = amount_of_card_weight[1][0]
                    logger.info(f"Chose the second best colour {colour}")
                
                self._topcard = cards(colour,"")
                self.update_player_hand(current_card)

            
                
        elif current_card[0] == top_current_card[0] and current_card[1] == "reverse":
            if self._clockwise == True:
                self._clockwise = False
            elif self._clockwise == False:
                self._clockwise = True
            logger.info(f"Deck to be reversed, clockwise is now {self._clockwise}")
            self._topcard = cards(current_card[0],current_card[1])
            self.update_player_hand(current_card)
        
        elif current_card[0] == top_current_card[0] and current_card[1]  == "block":
            self.update_player_hand(current_card)
            self._topcard = cards(current_card[0],current_card[1])
            #for i in range(1):
            self.next_turn()
            logger.info(f"player{self._order[self._order_postion]} to be blocked")


        elif current_card[0] == top_current_card[0] and current_card[1] == "plus_2":
            self.plus_2_check()
            self._topcard = cards(current_card[0],current_card[1])
            self.update_player_hand(current_card)

        
        elif current_card[0] == top_current_card[0] or current_card[1] == top_current_card[1]:
            #saftey net code, if th if statement fails this code catches them and where ordianry cards go
            if current_card[1] == "reverse": 
                if self._clockwise == True:
                    self._clockwise = False
                elif self._clockwise == False:
                    self._clockwise = True
                logger.warning(f"Deck to be reversed, clockwise is now {self._clockwise}")
                self._topcard = cards(current_card[0],current_card[1])
                self.update_player_hand(current_card)
            elif current_card[1]  == "block":
                self.update_player_hand(current_card)
                self._topcard = cards(current_card[0],current_card[1])
                #for i in range(1):
                self.next_turn()
                logger.warning(f"player{self._order[self._order_postion]} to be blocked")
            else:
                self._topcard = cards(current_card[0],current_card[1])
                self.update_player_hand(current_card)
        else:
            if self._order_postion == 0 and self._pickup == False:
                self._pickup = True
                logger.warning(f"After before{self._order[self._order_postion]}")
                self._order[self._order_postion].append(pick_up_card)
                logger.warning(f"After pick up{self._order[self._order_postion]}")

                





        
        

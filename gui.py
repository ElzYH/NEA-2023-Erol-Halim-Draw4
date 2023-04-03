import pygame
import pygame_textinput
import pygame.freetype
import sys
import login
import sqlite3
import logging

pygame.init()

#Create display window
SCREEN_HEIGHT = 768 
SCREEN_WIDTH = 1366 

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("UNO")
icon = pygame.image.load('Assets/uno_icon.ico')
pygame.display.set_icon(icon)
pygame.key.set_repeat(0,0)


#Fonts and Images
GAME_FONT = pygame.freetype.Font("Assets/Fonts/AOTFShinGoProMedium.otf",18)
GAME_FONT2 = pygame.freetype.Font("Assets/Fonts/AOTFShinGoProMedium.otf",12.5)
WELCOME_FONT = pygame.freetype.Font("Assets/Fonts/AOTFShinGoProMedium.otf",37.5)
WELCOME_FONT2 = pygame.freetype.Font("Assets/Fonts/AOTFShinGoProMedium.otf",22)
PLAYER_FONT = pygame.freetype.Font("Assets/Fonts/AOTFShinGoProMedium.otf",28)
TEXT_FONT = pygame.freetype.Font("Assets/Fonts/AOTFShinGoProMedium.otf",16.5)
END_FONT = pygame.freetype.Font("Assets/Fonts/YeastyFlavorsRegular-yweyd.ttf",1)
WII_FONT = pygame.freetype.Font("Assets/Fonts/AOTFShinGoProMedium.otf",18)

logger = logging.getLogger(f"{__name__}")

back = pygame.image.load("Assets/Cards/back.png").convert_alpha()
back_hi = pygame.image.load("Assets/Cards/back_hi.png").convert_alpha()
signup_img = pygame.image.load('Assets/sign_up.png').convert_alpha()
signup_img_hi = pygame.image.load('Assets/sign_up_hi.png').convert_alpha()
card_button = pygame.image.load('Assets/more_cards.png').convert_alpha()
card_button_hi = pygame.image.load('Assets/more_cards_hi.png').convert_alpha()

signin_img = pygame.image.load('Assets/sign_in.png').convert_alpha()
signin_img_hi = pygame.image.load('Assets/sign_in_hi.png').convert_alpha()

uno_logo = pygame.image.load('Assets/uno_logo.png').convert_alpha()
play_img = pygame.image.load('Assets/play.png').convert_alpha()
play_hi_img = pygame.image.load('Assets/play_hi.png').convert_alpha()
leaderboard_img = pygame.image.load('Assets/leaderboard.png').convert_alpha()
leaderboard_hi_img = pygame.image.load('Assets/leaderboard_hi.png').convert_alpha()

setting_img = pygame.image.load('Assets/settings.png').convert_alpha()
setting_hi_img = pygame.image.load('Assets/settings_hi.png').convert_alpha()

quit_img = pygame.image.load('Assets/quit.png').convert_alpha()
quit_hi_img = pygame.image.load('Assets/quit_hi.png').convert_alpha()

temp_uno = pygame.image.load('Assets/Cards/green 1.png').convert_alpha()
temp_uno2 = pygame.image.load('Assets/Cards/green 0.png').convert_alpha()

pu_img = pygame.image.load('Assets/pickup.png').convert_alpha()
pu_img_hi = pygame.image.load('Assets/pickup_hi.png').convert_alpha()

separte = pygame.image.load('Assets/separate.png').convert_alpha()
separte_hi = pygame.image.load('Assets/separate_hi.png').convert_alpha()

compare = pygame.image.load('Assets/compare.png').convert_alpha()
compare_hi = pygame.image.load('Assets/compare_hi.png').convert_alpha()

redimg= pygame.image.load('Assets/red_button.png').convert_alpha()
redimghi= pygame.image.load('Assets/red_button_hi.png').convert_alpha()

blueimg= pygame.image.load('Assets/blue_button.png').convert_alpha()
blueimghi= pygame.image.load('Assets/blue_button_hi.png').convert_alpha()

yellowimg= pygame.image.load('Assets/yellow_button.png').convert_alpha()
yellowimghi= pygame.image.load('Assets/yellow_button_hi.png').convert_alpha()

greenimg= pygame.image.load('Assets/green_button.png').convert_alpha()
greenimghi= pygame.image.load('Assets/green_button_hi.png').convert_alpha()


games_img = pygame.image.load('Assets/gamesplayed.png').convert_alpha()
games_hi_img = pygame.image.load('Assets/gamesplayed_hi.png').convert_alpha()

wins_img = pygame.image.load('Assets/wins.png').convert_alpha()
wins_hi_img = pygame.image.load('Assets/wins_hi.png').convert_alpha()

losses_img = pygame.image.load('Assets/losses.png').convert_alpha()
losses_hi_img = pygame.image.load('Assets/losses_hi.png').convert_alpha()

draws_img = pygame.image.load('Assets/draws.png').convert_alpha()
draws_hi_img = pygame.image.load('Assets/draws_hi.png').convert_alpha()

black_back_img = pygame.image.load('Assets/back.png').convert_alpha()
black_back_hi_img = pygame.image.load('Assets/back_hi.png').convert_alpha()

all_numbers_img = pygame.image.load('Assets/numbers.png')
all_numbers_hi_img = pygame.image.load('Assets/numbers_hi.png')

no_wild_img = pygame.image.load('Assets/no_wilds.png')
no_wild_hi_img = pygame.image.load('Assets/no_wilds_hi.png')

all_cards = pygame.image.load('Assets/all_cards.png')
all_cards_hi = pygame.image.load('Assets/all_cards_hi.png')


bg = pygame.image.load("Assets/uno_background.png")
bg2 = pygame.image.load("Assets/end_screen.png")



class Button():
    """Creates Buttons that change image when the user mouse postion is over the button"""
    def __init__(self,x,y,image,image_hi,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.image_hi = pygame.transform.scale(image_hi,(int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.pages = 0

    def draw(self):
        """Returns action and changes self.clicked if the user press the mouse ontop of the image"""
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            screen.blit(self.image_hi, (self.rect.x,self.rect.y))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True


        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        if self.rect.collidepoint(pos):
            screen.blit(self.image_hi, (self.rect.x,self.rect.y))

        else:
            screen.blit(self.image, (self.rect.x,self.rect.y))
        return action

    


class Enter_Text:
    """Text that the user can type into and can be saved"""
    def __init__(self,x,y,font,font_size,anti,text_manger):
        self.font = pygame.font.SysFont(font,font_size)
        self.anti = anti
        self.cords = x,y
        self.textinput = pygame_textinput.TextInputVisualizer(manager=text_manger,font_object=self.font)
        self.name = ""

    def create(self):
        """Changes antialias to True or False"""
        self.textinput.antialias = self.anti

    def draw(self,events,rect_x,rect_y,rect_w,rect_h):
        """Draws a box for the user to type in and to contrast with the background"""
        self.textinput.update(events)
        inputs_rect = pygame.Rect(rect_x,rect_y,rect_w,rect_h)
        colour = pygame.Color("ghostwhite")
        pygame.draw.rect(screen,colour,inputs_rect)
        screen.blit(self.textinput.surface, (self.cords))

    def enter(self,events):
        """If Enter button is clicked it would save the text input"""
        if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN]:
            self.name = str(self.textinput.value)

    def access(self):
        """Returns the user username"""
        return self.name 

    def clear_text(self):
        """Clears the Current text"""
        self.name = ""
        self.textinput.value = ""


class Text:
    def __init__(self,text,colour,x,y):
        """Creates and display text with differnt fonts and sizes"""
        self.text = text
        self.colour = colour
        self.x = x
        self.y = y

    def create(self):
        text_surface, rect = WELCOME_FONT.render(self.text, (self.colour))
        screen.blit(text_surface, (self.x, self.y))

    def create_2(self):
        text_surface, rect = GAME_FONT.render(self.text, (self.colour))
        screen.blit(text_surface, (self.x, self.y))

    def create_3(self):
        text_surface, rect = PLAYER_FONT.render(self.text, (self.colour))
        screen.blit(text_surface, (self.x, self.y))

    def create_4(self):
        text_surface, rect = TEXT_FONT.render(self.text, (self.colour))
        screen.blit(text_surface, (self.x, self.y))

    def create_5(self):
        text_surface, rect = TEXT_FONT.render(self.text, (self.colour))
        screen.blit(text_surface, (self.x, self.y))

    def create6(self):
        text_surface, rect = WELCOME_FONT2.render(self.text, (self.colour))
        screen.blit(text_surface, (self.x, self.y))

    def create7(self):
        text_surface, rect = GAME_FONT2.render(self.text, (self.colour))
        screen.blit(text_surface, (self.x, self.y))

    def create8(self):
        text_surface, rect = WII_FONT.render(self.text, (self.colour))
        screen.blit(text_surface, (self.x, self.y))
        

    def clear(self):
        text_surface, rect = END_FONT.render("", (self.colour))
        screen.blit(text_surface, (self.x, self.y))

        

class Image():
    """Displays Images"""
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def display(self):
        """Draws Images"""
        screen.blit(self.image, (self.rect.x,self.rect.y))

class UnoCards(Button):
    """A version of the button class above but with couple of changes for Uno Cards in the game """
    def __init__(self,x,y,image,image_hi,scale,postion):
        super().__init__(x,y,image,image_hi,scale)
        self.postion = postion #the current card basically


    def get_card(self):
        if self.clicked == True:
            self.clicked = False
            return self.postion


    def clear(self):
        blank = pygame.image.load('Assets/blank.png').convert_alpha()
        screen.blit(blank, (self.rect.x,self.rect.y))




def lead_menu(user): 
    """Menu to display the leaderboard"""
    logger.info(f"Leaderboard menu")
    screen.fill((0,0,0))
    for i in range(8):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                logger.info("Quit Application")
                sys.exit()

        pygame.display.update()
        clock.tick(60)
    screen.fill((0,0,0))
    back_button = Button(20,20,black_back_img,black_back_hi_img,1)
    compare_button = Button(300,340,compare,compare_hi,1)
    separte_button = Button(700,340,separte,separte_hi,1)
    compare_option = False #compare menu with gamemodes
    separte_option = False #seprate menu to chose stats
    separte_continue = False #chose table
    comsep = True #compare and menu screen
    compaere_menu = False #compare with stats 
    while True:
        while comsep == True:
            screen.fill((0,0,0))
            if compare_button.draw() == True:
                compare_option = True
                comsep = False
            elif separte_button.draw() == True:
                separte_option = True
                comsep = False
            elif back_button.draw() == True:
                comsep = False
                screen.fill((0,0,0))
                for i in range(6):
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            logger.info("Quit Application")
                            sys.exit()

                    pygame.display.update()
                    clock.tick(60)
                return


            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    logger.info("Quit Application")
                    sys.exit()

            pygame.display.update()
            clock.tick(60)

        
        if separte_option == True:
            screen.fill((0,0,0))
            options = Text("Press 1: Normal | Press 2: NoWilds | Press 3: Number",(240,248,255),75,700)
            options.create()

            while separte_option == True:
                if back_button.draw() == True:
                    separte_option = False
                    comsep = True
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        logger.info("Quit Application")
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            separte_option = False
                            separte_continue = True
                            gamemode = "Normal"

                        elif event.key == pygame.K_2:
                            separte_option = False
                            separte_continue = True
                            gamemode = "Nowilds"

                        elif event.key == pygame.K_3:
                            separte_continue = True
                            separte_option = False
                            gamemode = "Numbers"

                events = pygame.event.get()
                pygame.display.update()
                clock.tick(60)
            


            if separte_continue == True:
                screen.fill((0,0,0))
                des = Text("Press 1: Games | Press 2: Wins | Press 3: Losses | Press 4: Draws",(240,248,255),20,700)
                choice = ""
                contin = False

                con = sqlite3.connect("uno_database.db")
                c = con.cursor()

                def leaderboard_choice(choice,text,user,gamemode):
                    """To access SQL Table and pull it infomation for it to be displayed"""

                    con = sqlite3.connect("uno_database.db")
                    c = con.cursor()

                    c.execute(f"""SELECT UserName,{choice}
                        From {gamemode}
                        ORDER BY {choice} DESC
                        """)
                    board = []
                    player_postions = [i for i in c.fetchall()]
                    for i in range(0,len(player_postions)):
                            if i < 99:
                                leader = (f"{str(i+1):3}. Name: {player_postions[i][0].capitalize():6} {text}: {player_postions[i][1]}")
                                board.append(leader)
                                if player_postions[i][0] == user:
                                    user_postion = str(i + 1)
                                    user_games = player_postions[i][1]
                    curent_user = f"{user_postion:3}. Name: {user.capitalize():6}  {text}: {user_games}"
                    return [board,curent_user]

                page = 0
                des.create()
                while separte_continue == True:
                    if page == 1:
                        choice = leaderboard_choice("Games","Games Played",user,gamemode)
                        contin = True

                    elif page == 2:
                        choice = leaderboard_choice("Wins","Games Won",user,gamemode)
                        contin = True

                    elif page == 3:
                        choice = leaderboard_choice("Loss","Games Loss",user,gamemode)
                        contin = True

                    elif page == 4:
                        choice = leaderboard_choice("Draws","Games Drawn",user,gamemode)
                        contin = True

                    if back_button.draw() == True:
                        con.close()
                        separte_option = True
                        separte_continue = False
                        #break

                    if contin == True:
                        contin = False
                        screen.fill((0,0,0))
                        if back_button.draw() == True:
                            con.close()
                            separte_option = True
                            separte_continue = False
                            #break
                        #Displays the current user leaderboard preview
                        user_text = Text(choice[1],(240,248,255),10,750)
                        user_text.create7()
                        y = 10
                        for i in range(len(choice[0])):
                            if i < 25:
                                y += 26
                                board = Text(choice[0][i],(240,248,255),620,y)
                                board.create8()



                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            logger.info("Quit Application")
                            sys.exit()

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_1:
                                page = 1

                            elif event.key == pygame.K_2:
                                page =2 

                            elif event.key == pygame.K_3:
                                page =3

                            elif event.key == pygame.K_4:
                                page =4



                    pygame.display.update()
                    clock.tick(60)

        elif compare_option == True:
            screen.fill((0,0,0))
            optionslist = []
            coptions = Text("PRESS TWO KEYS TO COMPARE OPTIONS: PRESS 1: NORMAL | PRESS 2: NO WILDS | PRESS 3: NUMBERS",(240,248,255),20,730)
            coptions.create6()

            while compare_option == True:

                if back_button.draw() == True:
                    compare_option = False
                    comsep = True

                gamemode_choices = Text(" ".join(optionslist),(255,255,255),443,355)
                gamemode_choices.create()

                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        logger.info("Quit Application")
                        sys.exit()

                    if len(optionslist) < 3:
                        if event.type == pygame.KEYDOWN:
                            if len(optionslist) == 2: 
                                compaere_menu = True
                                compare_option = False

                            
                            if event.key == pygame.K_1:
                                if "Normal" not in optionslist:
                                    optionslist.append("Normal")

                            elif event.key == pygame.K_2:
                                if "NoWilds" not in optionslist:
                                    optionslist.append("NoWilds")

                            elif event.key == pygame.K_3:
                                if "Numbers" not in optionslist:
                                    optionslist.append("Numbers")

                    pygame.display.update()
                    clock.tick(60)
    

                        
            if compaere_menu == True:
                screen.fill((0,0,0))
                contin = False
                des = Text("Press 1: Games | Press 2: Wins | Press 3: Losses | Press 4: Draws",(240,248,255),20,700)
                def leaderboard_choice(choice,text,user,gamemode1,gamemode2):
                    """To access SQL Table and pull it infomation for it to be displayed"""

                    user_postion = 0
                    user_games = ""
                    con = sqlite3.connect("uno_database.db")
                    c = con.cursor()
                    print(gamemode1,gamemode2)
                    c.execute(f"""SELECT {gamemode1}.UserName,{gamemode1}.{choice},{gamemode2}.{choice}
                        FROM {gamemode1} INNER JOIN {gamemode2}
                        ON {gamemode1}.UserName == {gamemode2}.UserName
                        ORDER BY {gamemode1}.{choice} DESC
                        """)


                    board = []
                    player_postions = [i for i in c.fetchall()]
                    for i in range(0,len(player_postions)):
                            if i < 99:
                                leader = (f"{str(i+1):3}. Name: {player_postions[i][0].capitalize():6}{gamemode1}:  {text}: {player_postions[i][1]}  |  {gamemode2} {text} {player_postions[i][2]}")
                                board.append(leader)
                                if player_postions[i][0] == user:
                                    user_postion = str(i + 1)
                                    user_games = [player_postions[i][1],player_postions[i][2]]
                    curent_user = f"{user_postion:3}. Name: {user.capitalize()}  {gamemode1}:  {text}: {user_games[0]}  |  {gamemode2} {text} {user_games[1]}"
                    con.close()
                    return [board,curent_user]

                page = 0
                des.create()

                while compaere_menu == True:

                    if back_button.draw() == True:
                        compaere_menu = False
                        compare_option = True

                    if page == 1:
                        choice = leaderboard_choice("Games","Games Played",user,optionslist[0],optionslist[1])
                        contin = True

                    elif page == 2:
                        choice = leaderboard_choice("Wins","Games Won",user,optionslist[0],optionslist[1])
                        contin = True

                    elif page == 3:
                        choice = leaderboard_choice("Loss","Games Loss",user,optionslist[0],optionslist[1])
                        contin = True

                    elif page == 4:
                        choice = leaderboard_choice("Draws","Games Drawn",user,optionslist[0],optionslist[1])
                        contin = True





                    if contin == True:
                        contin = False
                        screen.fill((0,0,0))
                        if back_button.draw() == True:
                            compaere_menu = False
                            compare_option = True
                            optionslist = []


                        #Displays the current user leaderboard preview
                        user_text = Text(choice[1],(240,248,255),10,750)
                        user_text.create7()
                        y = 10
                        for i in range(len(choice[0])):
                            if i < 25:
                                y += 26
                                board = Text(choice[0][i],(240,248,255),560,y)
                                board.create8()



                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            logger.info("Quit Application")
                            sys.exit()

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_1: #Number keys to change options
                                page = 1

                            elif event.key == pygame.K_2:
                                page =2 

                            elif event.key == pygame.K_3:
                                page =3

                            elif event.key == pygame.K_4:
                                page =4

                    pygame.display.update()
                    clock.tick(60)

                pygame.display.update()
                clock.tick(60)



def displayloop(user,user_deck,len_decks_list,topcard,current_player):
    """Display the same infomation to the user during other players turns"""
    screen.fill((248,248,255))
    screen.blit(bg, (0,0))
    display_all_cards = Text(f"{str(user).capitalize()}: {len_decks_list[0]} cards | Player 2: {len_decks_list[1]} cards | Player 3: {len_decks_list[2]} cards | Player 4: {len_decks_list[3]} cards",("#6d6dba"),355,206)
    topcard = pygame.image.load(f'Assets/Cards/{topcard}.png').convert_alpha()
    topcard = Image(640,330,topcard,1)
    display_all_cards.create_4()
    page = 1
    display_player = Text(f"Player{current_player} Turn...",(205,51,51),int((SCREEN_WIDTH//2)-100),60)
    display_player.create_3()


    def cards_show(start,end):
        x = 190
        y = 600
        for num in range(len_decks_list[0]):
            if num >= start and num <= end:
                x += 110
                cards = UnoCards(x,y,user_cards[num][0],user_cards_hi[num],1,user_cards[num][1])
                cards.draw()


    for i in range(84):
        screen.blit(bg, (0,0))
        display_player.create_3()
        display_all_cards.create_4()
        topcard.display()
        user_cards = [[pygame.image.load(f'Assets/Cards/{i}.png').convert_alpha(),str(i)] for i in user_deck]
        user_cards_hi = [pygame.image.load(f'Assets/Cards/{x}_hi.png').convert_alpha() for x in user_deck]

        events = pygame.event.get()
        x = 190
        y = 600

        if page == 1:
            cards_show(0,6)

        elif page == 2:
            cards_show(7,13)

        elif page == 3: 
            cards_show(14,20)


        elif page == 4:
            cards_show(21,27)

        elif page == 5:
            cards_show(28,34)
                               
                        

        for event in events:
            if event.type == pygame.QUIT:
                logger.info("Quit Application")
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    page = 1

                elif event.key == pygame.K_2:
                    page =2 

                elif event.key == pygame.K_3:
                    page =3
                
                elif event.key == pygame.K_4:
                    page =4

                elif event.key == pygame.K_5:
                    page =5
        pygame.display.update()
        clock.tick(60)



def winloop(user):
    """show a win screen for temp amount of time"""
    screen.fill((248,248,255))
    screen.blit(bg2, (0,0))

    for x in range(320):
        screen.blit(bg2, (0,0))
        win = Text(f"{str(user).capitalize()} WIIIIINNNNNSSSSS",("#42e54a"),((SCREEN_WIDTH//2)-260),x*1.051)
        win.create()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                logger.info("Quit Application")
                sys.exit()


        pygame.display.update()
        clock.tick(60)


def lossloop(player):
    screen.fill((248,248,255))

    for x in range(320):
        screen.blit(bg2, (0,0))
        win = Text(f"Player{str(player + 1).capitalize()} WIIIIINNNNNSSSSS",("#ee2525"),((SCREEN_WIDTH//2)-260),x*1.051)
        win.create()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                logger.info("Quit Application")
                sys.exit()

        pygame.display.update()
        clock.tick(60)




def drawloop():
    """show a draw screen for temp amount of time"""
    screen.fill((248,248,255))
    screen.blit(bg2, (0,0))
    win = Text(f"DRAW",("#ffffff"),578,360)
    win.create()

    for x in range(80):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                logger.info("Quit Application")
                sys.exit()

        pygame.display.update()
        clock.tick(60)

def choice_loop():
    """A scrren to chose from selection of game mode with press of a button"""
    pygame.time.wait(50)
    screen.fill((255,255,255))
    no_wilds = Button(550,340,no_wild_img,no_wild_hi_img,1)
    number = Button(300, 340, all_numbers_img, all_numbers_hi_img, 1)
    normal = Button(800,340, all_cards,all_cards_hi,1)
    back_button = Button(20,20,black_back_img,black_back_hi_img,1)

    def temp_white_screen():
        for i in range(7):
            screen.fill((255,255,255))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    logger.info("Quit Application")
                    sys.exit()
            pygame.display.update()
            clock.tick(60)
        


    while True:
        events = pygame.event.get()

        if no_wilds.draw() == True:
            temp_white_screen()
            return "NoWilds"
        elif number.draw() == True:
            temp_white_screen()
            return "Numbers"
        elif normal.draw() == True:
            temp_white_screen()
            return "Normal"
        elif back_button.draw() == True:
            temp_white_screen()
            return "backtomenu"



        for event in events:
            if event.type == pygame.QUIT:
                logger.info("Quit Application")
                sys.exit()

        pygame.display.update()
        clock.tick(60)

def playloop(user,user_deck,len_decks_list,topcard,pickup):
    """Loop for user to chose his card from several pages of cards"""
    logger.info("In playloop")
    screen.fill((248,248,255))
    screen.blit(bg, (0,0))  
    display_all_cards = Text(f"{str(user).capitalize()}: {len_decks_list[0]} cards | Player 2: {len_decks_list[1]} cards | Player 3: {len_decks_list[2]} cards | Player 4: {len_decks_list[3]} cards",("#6d6dba"),355,206)
    topcard = pygame.image.load(f'Assets/Cards/{topcard}.png').convert_alpha()
    topcard = Image(640,330,topcard,1)
    display_all_cards.create_4()
    page = 1
    pick_up_button = UnoCards(800,330,back,back_hi,1,"pick up")
    play_pu = Button(520,375,pu_img,pu_img_hi,1)

    red_button = Button(100,150,redimg,redimghi,1)
    blue_button = Button(100,250,blueimg,blueimghi,1)
    yellow_button = Button(100,350,yellowimg,yellowimghi,1)
    green_button = Button(100,450,greenimg,greenimghi,1)
    current_card = ""
    back_button = Button(20,20,black_back_img,black_back_hi_img,1)
    pu_bool = False
    change_colour = False
    player1_text = Text(f"{str(user).capitalize()} Turn...",("#6d6dba"),50,650)

    current_card = ""

    while True:
        screen.blit(bg, (0,0))
        player1_text.create_3()
        display_all_cards.create_4()
        topcard.display()
        user_cards = [[pygame.image.load(f'Assets/Cards/{i}.png').convert_alpha(),str(i)] for i in user_deck]
        user_cards_hi = [pygame.image.load(f'Assets/Cards/{x}_hi.png').convert_alpha() for x in user_deck]
        pick = UnoCards(400,330,pygame.image.load(f'Assets/Cards/{pickup}.png'),pygame.image.load(f'Assets/Cards/{pickup}_hi.png').convert_alpha(),1,pickup)
        events = pygame.event.get()
        x = 190
        y = 600

        def options(start,end,x,y,len_decks_list):
            for num in range(start,len_decks_list): #Loops through and displays all cards #we do all to avoid errors by guessing the size of player deck
                if num >= start and num <= end:
                    if num <= end: #Minmise the cards shown
                        x += 110 #movees a new card postion
                        cards1 = UnoCards(x,y,user_cards[num][0],user_cards_hi[num],1,user_cards[num][1])
                        if cards1.draw() == True:
                            current_card = cards1.get_card()
                            a = user_cards[num][1]
                            if current_card == a:
                                return current_card


        
        if page == 1 and pu_bool == False and change_colour == False:
            current_card = options(0,6,x,y,len_decks_list[0])
            if current_card == "wild plus_4" or current_card == "wild switch":
                change_colour = True
            elif current_card not in ["wild plus_4","wild switch","",None] and change_colour == False:
                return current_card

        

        elif page == 2 and pu_bool == False and change_colour == False:
            current_card = options(7,13,x,y,len_decks_list[0])
            if current_card == "wild plus_4" or current_card == "wild switch":
                change_colour = True
            elif current_card not in ["wild plus_4","wild switch","",None] and change_colour == False:
                return current_card
           


        elif page == 3 and pu_bool == False and change_colour == False:
            current_card = options(14,20,x,y,len_decks_list[0])
            if current_card == "wild plus_4" or current_card == "wild switch":
                change_colour = True
            elif current_card not in ["wild plus_4","wild switch","",None] and change_colour == False:
                return current_card



        elif page == 4 and change_colour == False and pu_bool == False:
            current_card = options(21,27,x,y,len_decks_list[0])
            if current_card == "wild plus_4" or current_card == "wild switch":
                change_colour = True
            elif current_card not in ["wild plus_4","wild switch","",None] and change_colour == False:
                return current_card


        elif page == 5 and change_colour == False and pu_bool == False:
            current_card = options(28,34,x,y,len_decks_list[0])
            if current_card == "wild plus_4" or current_card == "wild switch":
                change_colour = True
            elif current_card not in ["wild plus_4","wild switch","",None] and change_colour == False:
                return current_card



        if pick_up_button.draw() == True:
            pu_bool = True

        if back_button.draw() == True:
            logger.info(f"Game Ended {'endgamerightnow'}")
            return "endgamerightnow"
        
        if pu_bool == True: #pu_bool means pick up button pressed (True or False)
                if pick.draw() == True: #pick up and play
                    logger.info(f"Picked up and play")
                    pu_bool = False
                    return ["pick up","yes"]

                if play_pu.draw() == True: #pick up and not play
                    logger.info(f"Picked up and not played")
                    pu_bool = False
                    return ["pick up","no"]

        if change_colour == True:
            if red_button.draw() == True:
                logger.info(f"A colour button clicked : {str(current_card)} {'red'}")
                return [str(current_card),"red"]
            elif green_button.draw() == True:
                logger.info(f"A colour button clicked : {str(current_card)} {'green'}")
                return [str(current_card),"green"]
            elif yellow_button.draw() == True:
                logger.info(f"A colour button clicked : {str(current_card)} {'yellow'}")
                return [str(current_card),"yellow"]
            elif blue_button.draw() == True:
                logger.info(f"A colour button clicked : {str(current_card)} {'blue'}")
                return [str(current_card),"blue"]


        for event in events:
            if event.type == pygame.QUIT:
                logger.info("Quit Application")
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: #Changes the pages of cards, with key presses
                    page = 1 

                elif event.key == pygame.K_2:
                    page =2 

                elif event.key == pygame.K_3:
                    page =3

                elif event.key == pygame.K_4:
                    page =4

                elif event.key == pygame.K_5:
                    page =5

            
        pygame.display.update()
        clock.tick(60)




def colour_loop(user,len_decks_list,topcard,current_card):
    """Used for displaying all colours for the player to pick from. Only used for wild cards"""
    logger.info("On colour loop")
    screen.fill((248,248,255))
    screen.blit(bg, (0,0))  
    display_all_cards = Text(f"{str(user).capitalize()}: {len_decks_list[0]} cards | Player 2: {len_decks_list[1]} cards | Player 3: {len_decks_list[2]} cards | Player 4: {len_decks_list[3]} cards",("#6d6dba"),355,206)
    topcard = pygame.image.load(f'Assets/Cards/{topcard}.png').convert_alpha()
    topcard = Image(640,330,topcard,1)
    display_all_cards.create_4()


    red_button = Button(100,150,redimg,redimghi,1)
    blue_button = Button(100,250,blueimg,blueimghi,1)
    yellow_button = Button(100,350,yellowimg,yellowimghi,1)
    green_button = Button(100,450,greenimg,greenimghi,1)


    player1_text = Text(f"{str(user).capitalize()} Turn...",("#6d6dba"),50,650)

    player1_text.create_3()
    display_all_cards.create_4()
    topcard.display()

    
    while True:
        events = pygame.event.get()
        if red_button.draw() == True:
            logger.info(f"A colour button clicked : {str(current_card)} {'red'}")
            return [str(current_card),"red"]
        elif green_button.draw() == True:
            logger.info(f"A colour button clicked : {str(current_card)} {'green'}")
            return [str(current_card),"green"]
        elif yellow_button.draw() == True:
            logger.info(f"A colour button clicked : {str(current_card)} {'yellow'}")
            return [str(current_card),"yellow"]
        elif blue_button.draw() == True:
            logger.info(f"A colour button clicked : {str(current_card)} {'blue'}")
            return [str(current_card),"blue"]


        for event in events:
            if event.type == pygame.QUIT:
                logger.info("Quit Application")
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    page = 1

                elif event.key == pygame.K_2:
                    page =2 

                elif event.key == pygame.K_3:
                    page =3

                elif event.key == pygame.K_4:
                    page =4

                elif event.key == pygame.K_5:
                    page =5

        pygame.display.update()
        clock.tick(60)


def main_menu_loop():
    """Displays the main menu with buttons to display choices"""
    pygame.time.wait(50)
    logger.info("On Main Menu")
    logo = Image(510,20,uno_logo,1)
    screen.fill((255,255,255))
    play_button = Button(555, 240, play_img,play_hi_img,1)
    leaderboard_button = Button(555, 360, leaderboard_img,leaderboard_hi_img,1)
    quit_button = Button(555,480,quit_img,quit_hi_img,1)
    back_button = Button(20,20,black_back_img,black_back_hi_img,1)
    option = ""
    while True:
        events = pygame.event.get()
        logo.display()
        if play_button.draw() == True:
            logger.info("Pressed Play")
            return "play"
        if leaderboard_button.draw() == True:
            logger.info("Pressed Stats")
            return "leaderboard"
        if quit_button.draw() == True:
            logger.info("Quit Application")
            sys.exit()
        if back_button.draw() == True:
            logger.info("Pressed Back")
            return "back_button"


        for event in events:
            #quit game
            if event.type == pygame.QUIT:
                logger.info("Quit Application")
                sys.exit()
                
        pygame.display.update()
        clock.tick(60)


def welcomeloop(user):
    """show a welcome screen for temp amount of time"""
    logger.info("On welcome Loop")
    for i in range(120):
        welcome_text = Text(f"Hi {str(user).capitalize()}",(0,0,0),500,325)
        welcome_text2 = Text("Welcome To Uno",(0,0,0),500,375)
        screen.fill((198,226,255))
        welcome_text.create()
        welcome_text2.create()
        events = pygame.event.get()
        for event in events:
                #quit game
                if event.type == pygame.QUIT:
                    logger.info("Quit Application")
                    sys.exit()
        pygame.display.update()
        clock.tick(60)
    

#create buttonm
def startloop():
    """Login and Sign up menus. First loaded at the start of the application and can be return too, to switch user"""
    logger.info("In startloop / Login and Main menu loop")
    in_button= Button(200, 260, signin_img,signin_img_hi,1)
    up_button = Button(750, 260, signup_img,signup_img_hi,1)
    back_button = Button(20,20,black_back_img,black_back_hi_img,1)
    #username = Image(100,210,user_name_img,1)
    error = ""
    text2 = Text(error,(0,0,0),240,350)

    manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= 6)
    text1 = Enter_Text(505,306,"Cambria",22,True,manager)
    text1.create()


    menu =""
    #event handler
    while True:
        events = pygame.event.get()

        screen.fill((198,226,255))
        text2 = Text(error,(255,48,48),200,550)
        if menu != "clicked":
            if in_button.draw() == True:
                option = "sign in"
                menu = "clicked"
            elif up_button.draw() == True:
                option = "sign up"
                menu ="clicked"
                text2.clear()
            else:
                text2.create8()

        if text1.access() != "":
            list_1 = login.login_or_sign(option,text1.access())
            user = list_1[0]
            error = list_1[1]
            text1.clear_text()
            if user != "":
                logger.info(f"User has enterted : {list_1}")
                return user
            else:
                user = ""
                menu = ""

                
        if menu == "clicked":
            if back_button.draw() == True:
                menu = ""
            text1.draw(events,500,301,140,32)
            text_surface, rect = GAME_FONT.render("Enter Username: ", (0, 0, 0))
            screen.blit(text_surface, (337, 308))
            

        for event in events:
            #quit game
            if event.type == pygame.QUIT:
                logger.info("Quit Application")
                sys.exit()

            text1.enter(events)

        pygame.display.update()
        clock.tick(60)






import pygame, random, sys, math
from Other.Utils import scale_image

pygame.init()

BACKGROUND = pygame.image.load("Assets/Backgrounds/BgDay2.png")
TRANSITION_BG = pygame.image.load("Assets/Backgrounds/PlainBlack.png")
LEADERBOARDINFO = pygame.image.load("Assets/LeaderBoard/AfterGameInfoGlow.png")

WIDTH, HEIGHT = BACKGROUND.get_width(), BACKGROUND.get_height()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Hunt!")
FPS = 60
clock = pygame.time.Clock()
last_update = pygame.time.get_ticks()

#Assets#####################

#--------------------------------------------------------------------------------------------------#
#R = Right L = Left
Duck1_R, Duck1_L, Duck2_R, Duck2_L, Duck3_R, Duck3_L = [], [], [], [], [], [] #List to store all the images
SCOPES = [] #Store all the types of scopes the user could of chosen from
for i in range(5):
    Duck1_R.append(pygame.image.load(f"Assets/Ducks/Duck1/Right/Duck1_{i+1}.png").convert_alpha())
    Duck1_L.append(pygame.image.load(f"Assets/Ducks/Duck1/Left/Duck1_{i+6}.png").convert_alpha())
    Duck2_R.append(pygame.image.load(f"Assets/Ducks/Duck2/Right/Duck2_{i+1}.png").convert_alpha())
    Duck2_L.append(pygame.image.load(f"Assets/Ducks/Duck2/Left/Duck2_{i+6}.png").convert_alpha())
    Duck3_R.append(pygame.image.load(f"Assets/Ducks/Duck3/Right/DuckB_{i+1}.png").convert_alpha())
    Duck3_L.append(pygame.image.load(f"Assets/Ducks/Duck3/Left/DuckB_{i+6}.png").convert_alpha())

    SCOPES.append(pygame.image.load(f"Assets/Scopes/InGame/Scope{i+1}.png").convert_alpha())

#The falling state of the ducks
DUCK1_HIT = pygame.image.load("Assets/Ducks/Duck1/Duck1_Hit.png").convert_alpha()
DUCK2_HIT = pygame.image.load("Assets/Ducks/Duck2/Duck2_Hit.png").convert_alpha()
DUCK3_HIT = pygame.image.load("Assets/Ducks/Duck3/Duck3_Hit.png").convert_alpha()
#--------------------------------------------------------------------------------------------------#

#info
INFO = pygame.image.load("Assets/Info/InfoBar.png")
HealthBar = [pygame.image.load("Assets/Info/HealthBar.png"), pygame.image.load("Assets/Info/HealthBar2.png"), pygame.image.load("Assets/Info/HealthBar3.png")]
Bullet1 = pygame.image.load("Assets/Info/Bullet.png")
Bullet2 = pygame.image.load("Assets/Info/Bullet2.png")
UNLIMITED = pygame.image.load("Assets/Info/Infinity.png")
SLOWMO = pygame.image.load("Assets/Info/SlowMo.png")
ALLBLUE = pygame.image.load("Assets/Info/AllBlue.png")
TWOX = pygame.image.load("Assets/Info/2X.png")
#Info

#Used for the transition between screens
BLACKSCREEN = pygame.image.load("Assets/Backgrounds/PlainBlack1.png").convert_alpha()

#Buttons for the game
RESUME_Standard = scale_image(pygame.image.load("Assets/Buttons/Resume/RESUME_Standard.png"), 0.35)
RESUME_Standard_Rect = RESUME_Standard.get_rect()
RESUME_Standard_Rect.topleft = (100, 340)

RESUME_Hover = scale_image(pygame.image.load("Assets/Buttons/Resume/RESUME_Hover.png"), 0.35)
RESUME_Hover_Rect = RESUME_Hover.get_rect()
RESUME_Hover_Rect.topleft = (100, 340)

MAIN_MENU_Standard = scale_image(pygame.image.load("Assets/Buttons/MainMenu/Main_Menu_Standard.png"), 0.35)
MAIN_MENU_Standard_Rect = MAIN_MENU_Standard.get_rect()
MAIN_MENU_Standard_Rect.topleft = (100, 540)

MAIN_MENU_Hover = scale_image(pygame.image.load("Assets/Buttons/MainMenu/Main_Menu_Hover.png"), 0.35)
MAIN_MENU_Hover_Rect = MAIN_MENU_Hover.get_rect()
MAIN_MENU_Hover_Rect.topleft = (100, 540)

EXIT_Standard = scale_image(pygame.image.load("Assets/Buttons/Exit/EXIT_Standard.png"), 0.26)
EXIT_Standard_Rect = EXIT_Standard.get_rect()
EXIT_Standard_Rect.topleft = (1475, 853)

EXIT_Hover = scale_image(pygame.image.load("Assets/Buttons/Exit/EXIT_Hover.png"), 0.26)
EXIT_Hover_Rect = EXIT_Hover.get_rect()
EXIT_Hover_Rect.topleft = (1475, 853)

#Assets#####################

####################################Variables for the Ducks####################################

DUCKS = [Duck1_R, Duck1_L, Duck2_R, Duck2_L, Duck3_R, Duck3_L]

AnimationList = [[], [], [], [], [], []] # Stores Multiple lists together as one variable, 2D Array!

flying_animation = 5 #Amount of animations in a sprite sheet
SIZEOFASSET = 0.4 #To either increase/decrease the assets size
animation_cooldown = 100 #How often the sprite is updated #Starts from 0 to length of list for the animations
DuckHit = False 
TypeOfRanMov = [(10, 20), (10, 25), (10, 30), (10, 32), (10, 35)] #Difficulty of movement for wave 1 - 5
####################################Variables for the Ducks####################################

#####################Colours&Fonts#####################
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SALMOON_PINK = (255, 145, 164)
BLUE = (153, 255, 255)
LIGHT_GREY = (170,170,170)
FONT = pygame.font.Font("freesansbold.ttf", 32)
#####################Colours&Fonts#####################

#Nested loop
for x in range(0, 6):
    #Goes through each image inside the 2D list and resized the images automatically
    for y in range(flying_animation):
        #Used a scalling function that is build in pygame to change the sizes
        image = pygame.transform.scale(DUCKS[x][y], (int(DUCKS[x][y].get_width() * SIZEOFASSET), int(DUCKS[x][y].get_height() * SIZEOFASSET))) #Changes the size of each asset to be the same for the animation
        #I append the changes to a new list
        AnimationList[x].append(image) #Puts each sprite in designated list

class Ducks():

    #Global variables used within the class
    Score_Value, Multiplier = 0, 1
    Missed, MissesInRow, DuckHit, HitsInRow, Killed = 0, 0, -1, 0, 0
    Cycles = 0
    Duck1Hit, Duck2Hit, Duck3Hit = 0, 0, 0

    def __init__(self, pos_x, pos_y, Duckx, Ducky, Bonusbird, Duckdir, Listnum):
        #Any private attributes each duck will have, to make them unique
        self.Pos_X = pos_x
        self.Pos_Y = pos_y
        self.DuckX = Duckx
        self.DuckY = Ducky
        self.BounusBird = Bonusbird
        self.DuckDir = Duckdir
        self.DuckHit, self.Clicked = False, False
        self.ListNum = Listnum
        self.DuckRect = AnimationList[self.ListNum][0].get_rect()
        self.DuckRect.topleft = (pos_x, pos_y)
        self.DuckGone = 0
        self.Execution = 19
        self.Time, self.RanXPos, self.RanYPos = self.Random("Hit", 1)
        self.XMulti, self.YMulti = self.Random("Movement", 1)

    def Bouncing(self, DuckXmultiplier, DuckYmultiplier, Frame): 

        #Decides how much the duck will move up/down or right/left
        self.DuckRect.x += (self.DuckX * DuckXmultiplier)
        self.DuckRect.y += (self.DuckY * DuckYmultiplier)

        #This part of the code controls if the duck is about to go past the screen
        #And then changes its direction of flight
        if (self.DuckRect.right >= WIDTH or self.DuckRect.left <= 0):
            self.DuckX *= -1
            if self.DuckDir == self.ListNum:
                self.DuckDir += 1
            else:
                self.DuckDir -= 1
        if (self.DuckRect.bottom >= HEIGHT or self.DuckRect.top <= 0):
            self.DuckY *= -1

        #This part displays the ducks from its animation to its movement
        for i in range(flying_animation):
            WIN.blit(scale_image(AnimationList[(self.DuckDir)][Frame], (1)), (self.DuckRect))

    def Random(self, Type, SlowMo): #Use 25 XOrY for high point birds!
        #A check to see what function it shoudl use.
        if Type == "Movement":
            #Does a chekc to see if its the "Bounus" bird aka the blue one
            if self.BounusBird == True:
                self.XMulti = random.randrange(TypeOfRanMov[Round-1][0]*2, TypeOfRanMov[Round-1][1]*2)
                self.YMulti = random.randrange(TypeOfRanMov[Round-1][0], TypeOfRanMov[Round-1][1])
                if SlowMo == 2:
                    self.XMulti, self.YMulti = self.XMulti/SlowMo, self.YMulti/SlowMo
                return self.XMulti, self.YMulti  
            #Only does the random movement every so often
            self.Execution += 1
            if (self.Execution%20) == 0:
                if self.Execution == 300:
                    self.Execution = 29
                #Use of random to generate random integers to create the movement
                self.XMulti = random.randrange(TypeOfRanMov[Round-1][0]*2, TypeOfRanMov[Round-1][1]*2)
                self.YMulti = random.randrange(TypeOfRanMov[Round-1][0], TypeOfRanMov[Round-1][1])
                #Part for the power ups
                if SlowMo == 2:
                    self.XMulti, self.YMulti = self.XMulti/SlowMo, self.YMulti/SlowMo
                return self.XMulti, self.YMulti
        #A check to see what function it shoudl use.
        if Type == "Hit":
            rantime = random.randrange(40, 100)
            ranx_pos = random.randrange(50, 1700)
            rany_pos = random.randrange(HEIGHT-300, 900)
            return rantime, ranx_pos, rany_pos

    def MosClicked(self, TempMultiplier):
        #Does a check if the left click mouse button was pressed
        if pygame.mouse.get_pressed()[0] == 1 and self.Clicked == False and Crosshair.NumBullets != 0:
            Ducks.Cycles += 1
            Ducks.Multiplier = float( "1." + str(Ducks.HitsInRow*2))
            if Ducks.HitsInRow > 5: Ducks.Multiplier = 2
            #This checks if the bird was "hit"
            if self.DuckRect.collidepoint(pygame.mouse.get_pos()):
                if self.ListNum == 0:
                    Ducks.Duck1Hit += 1
                elif self.ListNum == 2:
                    Ducks.Duck2Hit += 1
                elif self.ListNum == 4:
                    Ducks.Duck3Hit += 1
                Ducks.HitsInRow += 1
                Ducks.Killed += 1
                self.DuckHit, self.Clicked = True, True
                #Takes the value at the exact point on the screen where the duck was hit
                self.XHit, self.YHit = self.DuckRect.center
                #Adds points to the corresponding ducks
                if self.BounusBird == True:
                    Ducks.Score_Value += 500*Ducks.Multiplier*TempMultiplier
                else:
                    Ducks.Score_Value += 100*Ducks.Multiplier*TempMultiplier
                self.Stop = True
                Ducks.Cycles, Ducks.Missed, Ducks.DuckHit = 0, 0, True
            if Ducks.Cycles == len(Duck_Group) and Ducks.DuckHit != True:
                Ducks.DuckHit = False
            if Ducks.Cycles == len(Duck_Group) and Ducks.DuckHit == True:
                Ducks.Cycles, Ducks.DuckHit = 0, -1

        if Ducks.DuckHit == False and CrossHair.NumBullets != 6:
            Ducks.Cycles = 0    
            Ducks.DuckHit = -1
            self.Clicked = True
            Ducks.Missed += 1
            Ducks.HitsInRow = 0 
            if Ducks.Missed == 3:
                Ducks.MissesInRow += 1
                Ducks.Missed = 0

        if pygame.mouse.get_pressed()[0] == 0 and self.Clicked == True:
            self.Clicked = False
            Ducks.Cycles = 0

    def Hit(self):
        #Does a check to see if a bird has been hit
        if self.DuckHit == True:
            #Will display the correct falling image, to the duck that had been hit
            if self.ListNum == 0:
                WIN.blit(pygame.transform.scale(DUCK1_HIT, (56.5, 112.5)), (self.XHit, self.YHit))
            elif self.ListNum == 2:
                WIN.blit(pygame.transform.scale(DUCK2_HIT, (56.5, 112.5)), (self.XHit, self.YHit))
            elif self.ListNum == 4:
                WIN.blit(pygame.transform.scale(DUCK3_HIT, (56.5, 112.5)), (self.XHit, self.YHit))
            #This is used to randomise where the duck will spawn back in
            if self.Stop == True:
                self.Time, self.RanXPos, self.RanYPos = self.Random("Hit", 1)
                self.Stop = False
            self.YHit += 35
            self.DuckRect.topleft = (-200, -200)
            self.DuckGone += 1
        if self.ListNum != 4 and self.DuckGone == self.Time: #Randomises when the ducks respawn back into the game & Makes sure the bounus bird isnt spawned back in
            self.DuckGone = 0
            self.DuckHit = False
            self.DuckRect.topleft = (self.RanXPos, self.RanYPos) #Randomises where the ducks spawn on the screen

class Crosshair:

    NumBullets = 5

    def __init__(self, img):
        self.Img = img
        self.Rect = self.Img.get_rect()
        self.Clicked = False
        self.Shot = 0
        self.Gunshot = pygame.mixer.Sound("Assets/Sounds/gunshot.wav")

    def update(self, CrossHair):
        self.Rect.center = pygame.mouse.get_pos()
        WIN.blit(SCOPES[int(CrossHair)], (self.Rect))

    def Bullets(self):
        if Crosshair.NumBullets != 6:   
            if len(Bullet_Group) < Crosshair.NumBullets:
                for i in range (Crosshair.NumBullets):
                    Bullet_Group.append(Bullet1)
            global JustPause
            if pygame.mouse.get_pressed()[0] == 1 and self.Clicked == False and JustPause == False and Crosshair.NumBullets != 0:
                self.Shot += 1
                self.Gunshot.play()
                self.Clicked = True
                Crosshair.NumBullets -= 1
                index = len(Bullet_Group) - list(reversed(Bullet_Group)).index(Bullet1) -  1
                Bullet_Group.pop(index)
                Bullet_Group.append(Bullet2)
        else:
            #This is for the power up - Unlimited
            if pygame.mouse.get_pressed()[0] == 1 and self.Clicked == False and JustPause == False:
                print("True")
                self.Shot += 1
                self.Clicked = True
                self.Gunshot.play()
                print(self.Shot)
        if pygame.mouse.get_pressed()[0] == 0:
            self.Clicked = False
            JustPause = False

    def settings():
        with open("Settings.txt", "r") as f:
            C_hair = f.readline(1)
            return C_hair

class EndGame:
    Scroll = 0
    Warning = ["Max 6 Character!", "UserName Already Exist!", "Actual UserName"]
    def __init__(self, pos_x, pos_y, rgb, font):
        self.Pos_X = pos_x
        self.Pos_Y = pos_y
        self.RGB = rgb
        self.Font = pygame.font.Font(f"{font}", 64)
        self.UserName = "Max 6 Character!"
        self.Top10, self.Top10User, self.Top10Score = [], [], []
    
    def TextInput(self, Enter, Exist):
        if Exist == True: self.UserName = "UserName Already Exist!"
        Input_Box = pygame.Rect(WIDTH/2-325, HEIGHT/2-100, 140, 64)
        RGB = LIGHT_GREY
        while Enter == False:
            for i in range(0, 2):
                WIN.blit(BACKGROUND, (i * WIDTH + EndGame.Scroll, 0))
                EndGame.Scroll -= 2.5
            if EndGame.Scroll*-1 > WIDTH:
                EndGame.Scroll = 0
            WIN.blit(BLACKSCREEN, (0, 0))
            WIN.blit(((pygame.font.Font("freesansbold.ttf", 64)).render(f"Your final score is: {int(Ducks.Score_Value)}", True, WHITE)), (WIDTH/2-350, 25))
            WIN.blit(((pygame.font.Font("freesansbold.ttf", 48)).render("Please Enter Your Username:", True, WHITE)), (WIDTH/2-375, 350))
            pygame.draw.rect(WIN, SALMOON_PINK, Input_Box, 2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        for i in range (len(EndGame.Warning)):
                            if self.UserName == EndGame. Warning[i]:
                                self.UserName = ""
                        self.UserName = self.UserName[:-1]
                    elif event.key == pygame.K_RETURN:
                        if " " in self.UserName:
                            self.UserName = EndGame.Warning[3]
                            self.TextInput(False, False)
                        else:
                            Enter = True
                            return Enter
                    else:
                        for i in range (len(EndGame.Warning)):
                            if self.UserName == EndGame. Warning[i]:
                                self.UserName = ""
                        RGB = self.RGB
                        if len(self.UserName) < 6:
                            self.UserName += event.unicode
            
            User = self.Font.render(self.UserName, True, (RGB))
            WIN.blit(User, (Input_Box.x+5, Input_Box.y+2.5))
            Input_Box.w = User.get_width() + 10

            pygame.display.update()
    
    def LeaderBoardInfo(self):
        with open ("Scoreboard.txt", "r") as f:
            for i in f:
                UserName, Score = i.split(" : ")
                Score = Score.strip()
                self.Top10.append((UserName, int(Score)))
        with open ("Scoreboard.txt", "a") as f:
            for i in range(len(self.Top10)):
                while str(self.UserName) == str(self.Top10[i][0]):
                    self.TextInput(False, True)
            f.write(str(self.UserName)+" : "+str(int(Ducks.Score_Value))+"\n")
            self.Top10.append((self.UserName, int(Ducks.Score_Value)))
            self.Top10.sort(key=lambda Top10:Top10[1], reverse=True)
            for i in self.Top10:
                user, score = str(i).split(",")
                user = user.strip("'(), ")
                score = score.strip("'(), ")
                self.Top10User.append(user)
                self.Top10Score.append(score)
            return

    def Leaderboard(self):
        Transition()
        running = True
        WIN.blit(LEADERBOARDINFO, (5, 0))
        MAIN_MENU_Standard_Rect.topleft, MAIN_MENU_Hover_Rect.topleft = (1432, 637), (1432, 637)
        Clicked = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            for i in range(10):
                try:
                    User = self.Top10User[i]
                    Score = self.Top10Score[i]
                except:
                    User = "Empty"
                    Score = 0
                if User == "Empty":
                    WIN.blit(((pygame.font.Font("freesansbold.ttf", 64)).render(str(User), True, LIGHT_GREY)), (100,190+75*(i+1)))
                    WIN.blit(((pygame.font.Font("freesansbold.ttf", 64)).render(str(Score), True, LIGHT_GREY)), (500,190+75*(i+1)))
                else:
                    WIN.blit(((pygame.font.Font("freesansbold.ttf", 64)).render(str(User), True, WHITE)), (100,190+75*(i+1)))
                    WIN.blit(((pygame.font.Font("freesansbold.ttf", 64)).render(str(Score), True, WHITE)), (500,190+75*(i+1)))
            if self.Top10Score.index(str(int(Ducks.Score_Value))) == 0:
                WIN.blit(((pygame.font.Font("freesansbold.ttf", 64)).render("1st", True, WHITE)), (1200,180))
            elif self.Top10Score.index(str(int(Ducks.Score_Value))) == 1:
                WIN.blit(((pygame.font.Font("freesansbold.ttf", 64)).render("2nd", True, WHITE)), (1200,180))
            elif self.Top10Score.index(str(int(Ducks.Score_Value))) == 2:
                WIN.blit(((pygame.font.Font("freesansbold.ttf", 64)).render("3rd", True, WHITE)), (1200,180))
            else:
                WIN.blit(((pygame.font.Font("freesansbold.ttf", 64)).render(f"{(self.Top10User.index(str(self.UserName)))+1}th", True, WHITE)), (1175,185))
            
            WIN.blit(((pygame.font.Font("freesansbold.ttf", 96)).render(str(Ducks.Duck1Hit), True, WHITE)), (1150,375))
            WIN.blit(((pygame.font.Font("freesansbold.ttf", 96)).render(str(Ducks.Duck2Hit), True, WHITE)), (1150,595))
            WIN.blit(((pygame.font.Font("freesansbold.ttf", 96)).render(str(Ducks.Duck3Hit), True, WHITE)), (1150,825))

            WIN.blit(scale_image(MAIN_MENU_Standard, (0.9)), (MAIN_MENU_Standard_Rect))
            WIN.blit(EXIT_Standard, (EXIT_Standard_Rect))
            if MAIN_MENU_Standard_Rect.collidepoint(pygame.mouse.get_pos()):
                WIN.blit(scale_image(MAIN_MENU_Hover, (0.9)), (MAIN_MENU_Hover_Rect))
                if pygame.mouse.get_pressed()[0] == 1 and Clicked == False:
                    import Menus
                    del sys.modules["Menus"]
                    del Menus
            if EXIT_Standard_Rect.collidepoint(pygame.mouse.get_pos()):
                WIN.blit(EXIT_Hover, (EXIT_Hover_Rect))
                if pygame.mouse.get_pressed()[0] == 1 and Clicked == False:
                    pygame.quit()
                    exit()
            if pygame.mouse.get_pressed()[0] == 0:
                Clicked = False
            pygame.display.update()

def EndMenu():
    UserName.TextInput(False, False)
    UserName.LeaderBoardInfo()
    UserName.Leaderboard()

def Transition():
    Opacity = 0
    while Opacity != 250:
        TRANSITION_BG.set_alpha(Opacity)
        WIN.blit(TRANSITION_BG, (0, 0))
        Opacity += 5
        pygame.display.update()
    Opacity = 0
    while Opacity != 250:
        BACKGROUND.set_alpha(Opacity)
        WIN.blit(BACKGROUND, (0, 0))
        Opacity += 10
        pygame.display.update()

def Info():
    Timer_Rounds = FONT.render("Wave " + str(Wave) + "| Time Left: " + str(CountDown), True, (BLACK))
    score = FONT.render('Score: ' + str(int(Ducks.Score_Value)), True, (SALMOON_PINK))
    Percentage =  (Ducks.Killed/(CrossHair.Shot or not CrossHair.Shot))*100 #Python will display "ZeroDivisionError" if you divide something with zero so use  "or not"
    ShotAccuracy = FONT.render("Shot Accuracy: " + str(int(Percentage)) + "%", True, (SALMOON_PINK))
    #WIN.blit(HealthBar[Ducks.MissesInRow], (WIDTH/2-112.5, 990))#Original
    #WIN.blit(HealthBar[Ducks.MissesInRow], (10, 10))
    WIN.blit(HealthBar[Ducks.MissesInRow], (25, 985))
    WIN.blit(score, (1700, 970))
    WIN.blit(Timer_Rounds, (WIDTH/2-200, 25))
    WIN.blit(ShotAccuracy, (1565, 1030))
    WIN.blit(UNLIMITED, (WIDTH/2-200, 967))
    WIN.blit(SLOWMO, (WIDTH/2-50, 967))
    WIN.blit(TWOX, (WIDTH/2+100, 967))

##################PAUSED##################
def Pause(Paused):
    pygame.mouse.set_visible(True)
    WIN.blit(BLACKSCREEN, (0, 0))
    Clicked = False
    while Paused:
        global JustPause

        WIN.blit(RESUME_Standard, (RESUME_Standard_Rect))
        WIN.blit(MAIN_MENU_Standard, (MAIN_MENU_Standard_Rect))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Paused = False
                    JustPause = True

        if RESUME_Standard_Rect.collidepoint(pygame.mouse.get_pos()):
            WIN.blit(RESUME_Hover, (RESUME_Hover_Rect))
            if pygame.mouse.get_pressed()[0] == 1 and Clicked == False:
                Paused = False
                JustPause = True

        if MAIN_MENU_Standard_Rect.collidepoint(pygame.mouse.get_pos()):
            WIN.blit(MAIN_MENU_Hover, (MAIN_MENU_Hover_Rect))
            if pygame.mouse.get_pressed()[0] == 1 and Clicked == False:
                Paused = False
                import Menus
                del sys.modules["Menus"]
                del Menus


        if pygame.mouse.get_pressed()[0] == 0:
            Clicked = False
                    
        pygame.display.update()
##################PAUSED##################

def Rounds(FirstRound, BonusBird):
    if BonusBird == 0:
        if FirstRound == 0:
            Duck_Group.clear()
        for i in range(math.ceil(Round*1.75)):
            if random.choice([0, 2]) == 0:
                DuckSprites = Ducks(random.randrange(HEIGHT-300, 1700), random.randrange(50, 900), 1, 1, False, 0, 0) #Last two paramaters define what type of bird is being used (especially the second last one)
            else:
                DuckSprites = Ducks(random.randrange(HEIGHT-300, 1700), random.randrange(50, 900), 1, 1, False, 2, 2) #Creates new classes for the duck sprites
            Duck_Group.append(DuckSprites)
    elif BonusBird == 1:
        if random.randrange(0, 4) == 0: #First Numbeer is included(0) and the last isn't(4) so 25% Chance
            BonusBird = Ducks(random.randrange(HEIGHT-300, 1700), random.randrange(50, 900), 1, 1, True, 4, 4)
            Duck_Group.append(BonusBird)

Duck_Group, Bullet_Group = [], []

CrossHair = Crosshair(SCOPES[0])
UserName = EndGame(100, 100, BLUE, "freesansbold.ttf")

running, Clicked = True, False
frame, Execution, CountDown = 0, 9, 15
LastCount = pygame.time.get_ticks()
Round, Wave, j = 1, 1, 0
JustPause, Reloading = False, False
PowerUp, Unlimited, SlowMoDone, SlowMo, TempMulti = False, True, False, 1, 1
CoolDownCount, CoolDown = 3, False
Rounds(1, 0)

while running:
    pygame.mouse.set_visible(False) #Allows to have the mouse point on or off
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Pause(True)
            elif event.key == pygame.K_r:
                if Crosshair.NumBullets < 5:
                    Reloading = True
            if CoolDown == False and PowerUp == False:
                if event.key == pygame.K_z:
                    if Unlimited == True:
                        Crosshair.NumBullets, Unlimited, PowerUp = 6, False, True
                        Bullet_Group = [Bullet1, Bullet1, Bullet1, Bullet1, Bullet1]
                        PowerUpCount = 5
                elif event.key == pygame.K_x:
                    if SlowMo == 1 and SlowMoDone == False:
                        SlowMo, PowerUpCount, PowerUp = 2, 5, True
                        for i in range (0, len(Duck_Group)):
                            Duck_Group[i].Random("Movement", SlowMo)
                elif event.key == pygame.K_c:
                    if TempMulti == 1:
                        TempMulti, PowerUpCount, PowerUp = 2, 5, True

    if Reloading == True:
        Execution += 1
        if Bullet_Group[4] == Bullet1 or j == 5:
            Reloading, j = False, 0
            Crosshair.NumBullets = 5
        if (Execution%10) == 0:
            GunReloading = pygame.mixer.Sound("Assets/Sounds/GunReloading.wav")
            GunReloading.play()
            Bullet_Group[j+Crosshair.NumBullets] = Bullet1
            j += 1
 
#############Blitting Images#############
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(INFO, (0, 954))
#############Blitting Images#############)

    #Update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(AnimationList[0]):
            frame = 0

    if CountDown == 0:
        if Round < 5:
            Round += 1
            Opacity = 0
            while Opacity != 250:
                TRANSITION_BG.set_alpha(Opacity)
                WIN.blit(TRANSITION_BG, (0, 0))
                Opacity += 5
                pygame.display.update()
            Rounds(0, 0)
        Rounds(0, 1)
        Wave += 1
        CountDown = 15

    #Count down for each round
    if CountDown > 0:
        if current_time - LastCount > 1000:
            if CoolDown == True:
                if CoolDownCount == 0:
                    CoolDown, PowerUp = False, False
                CoolDownCount -= 1
            if Unlimited == False and Crosshair.NumBullets == 6:
                if PowerUpCount == 0:
                    Crosshair.NumBullets, CoolDown = 5, True
                PowerUpCount -= 1
                UNLIMITED.set_alpha(255-51*(5-PowerUpCount))
            if SlowMo == 2 and SlowMoDone == False:
                if PowerUpCount == 0:
                    SlowMoDone, SlowMo, CoolDown = True, 1, True
                PowerUpCount -= 1
                SLOWMO.set_alpha(255-51*(5-PowerUpCount))
            if TempMulti == 2:
                if PowerUpCount == 0:
                    TempMulti, CoolDown = 1, True
                PowerUpCount -= 1
                TWOX.set_alpha(255-51*(5-PowerUpCount))
            CountDown -= 1
            LastCount = current_time

    for i in range (len(Duck_Group)):
        Duck_Group[i].Random("Movement", SlowMo)
        Duck_Group[i].Bouncing(Duck_Group[i].XMulti, Duck_Group[i].YMulti, frame)
        Duck_Group[i].MosClicked(TempMulti)
        Duck_Group[i].Hit()

    if Ducks.MissesInRow == 3:
        pygame.mouse.set_visible(True)
        UserName.TextInput(False, False)
        UserName.LeaderBoardInfo()
        UserName.Leaderboard()

    scope = Crosshair.settings()
    CrossHair.Bullets()
    CrossHair.update(scope)

    Info()
    for i in range(5):
        WIN.blit(Bullet_Group[i], (235+32.5*(i+1), 975))

    pygame.display.update()
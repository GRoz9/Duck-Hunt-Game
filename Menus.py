import pygame, os, sys
from Other.Utils import scale_image

pygame.init()
pygame.mixer.init()

#Variables
WIDTH, HEIGHT = 1920, 1080

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu!")
FPS = 60
clock = pygame.time.Clock()

SIZEOFBUTTONS = 0.25

BACKGROUND = pygame.image.load("Assets/Backgrounds/MenuBg.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (1920, 1080))
TRANSITION_BG = pygame.image.load("Assets/Backgrounds/PlainBlack.png")
INFO = pygame.image.load("Assets/Info/InfoPage.png")
LEADERBOARD = pygame.image.load("Assets/LeaderBoard/BeforeGame2.png")

OPTIONS_BG = pygame.image.load("Assets/Backgrounds/Options.png")
OPTIONS_BG = pygame.transform.scale(OPTIONS_BG, (1920, 1080))

PLAY_Standard = scale_image(pygame.image.load("Assets/Buttons/Play/PLAY_Standard.png"), SIZEOFBUTTONS)
PLAY_Standard_Rect = PLAY_Standard.get_rect()
PLAY_Standard_Rect.topleft = (100, 200)

PLAY_Hover = scale_image(pygame.image.load("Assets/Buttons/Play/PLAY_Hover.png"), SIZEOFBUTTONS)
PLAY_Hover_Rect = PLAY_Standard.get_rect()
PLAY_Hover_Rect.topleft = (100, 200)

EXIT_Standard = scale_image(pygame.image.load("Assets/Buttons/Exit/EXIT_Standard.png"), SIZEOFBUTTONS)
EXIT_Standard_Rect = EXIT_Standard.get_rect()
EXIT_Standard_Rect.topleft = (100, 600)

EXIT_Hover = scale_image(pygame.image.load("Assets/Buttons/Exit/EXIT_Hover.png"), SIZEOFBUTTONS)
EXIT_Hover_Rect = EXIT_Hover.get_rect()
EXIT_Hover_Rect.topleft = (100, 600)

BACK_Standard = scale_image(pygame.image.load("Assets/Buttons/Back/BACK_Standard.png"), SIZEOFBUTTONS)
BACK_Standard_Rect = BACK_Standard.get_rect()
BACK_Standard_Rect.topleft = (1635, 985)

BACK_Hover = scale_image(pygame.image.load("Assets/Buttons/Back/BACK_Hover.png"), SIZEOFBUTTONS)
BACK_Hover_Rect = BACK_Hover.get_rect()
BACK_Hover_Rect.topleft = (1635, 985)

SCOPES_Standard = scale_image(pygame.image.load("Assets/Buttons/Scopes/SCOPES_Standard.png"), SIZEOFBUTTONS)
SCOPES_Standard_Rect = SCOPES_Standard.get_rect()
SCOPES_Standard_Rect.topleft = (100, 400)

SCOPES_Hover = scale_image(pygame.image.load("Assets/Buttons/Scopes/SCOPES_Hover.png"), SIZEOFBUTTONS)
SCOPES_Hover_Rect = SCOPES_Hover.get_rect()
SCOPES_Hover_Rect.topleft = (100, 400)
SSCOPE_BG = pygame.image.load("Assets/Backgrounds/ScopeBackground.png")

PLAY = scale_image(pygame.image.load("Assets/Sounds/AudioOn.png"), 0.5)
PLAY_Rect = PLAY.get_rect()
PLAY_Rect.topleft = (1770, 935)
PAUSE = scale_image(pygame.image.load("Assets/Sounds/AudioOff.png"), 0.5)
PAUSE_Rect = PAUSE.get_rect()
PAUSE_Rect.topleft = (1770, 935)

WHITE = (255, 255, 255)
LIGHT_GREY = (170,170,170)
Play = True
#Variables

#Scopes
SCOPES = []
for i in range(5):
    SCOPES.append(pygame.image.load(f"Assets/Scopes/ScopeChoice/Scope{i+1}.png").convert_alpha())

pygame.mixer.music.load("Assets/Sounds/Music/Song.wav")
#-1 means the music will run infinitely
pygame.mixer.music.play(-1)

#This function saves the scope the user will use
def Files(file, crosshair):
    with open (file, "w") as f:
        #Replaces the original data from the last line as a string
        f.write(str(crosshair))

def Scopes():
    Scopes, start, Opacity, Clicked = True, 0, 0, False
    WIN.blit(TRANSITION_BG, (0, 0))
    while Scopes:
        if Opacity != 250:
            OPTIONS_BG.set_alpha(Opacity)
            Opacity += 10
        WIN.blit(OPTIONS_BG, (0, 0))
        WIN.blit(SSCOPE_BG, (0, 0))
        WIN.blit(((pygame.font.Font("freesansbold.ttf", 64)).render(str(start+1)+"/5", True, (255, 145, 164))), (WIDTH/2-35, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if start < 4:
                        start += 1
                if event.key == pygame.K_LEFT:
                    if start > 0:
                        start -= 1
                if event.key == pygame.K_ESCAPE:
                    print("Enter key was pressed")
                    Menu()
                    Scopes = False
                if event.key == pygame.K_RETURN:
                    Files("Settings.txt", start)
        if start -1 >= 0:
            left = SCOPES[start-1]
            left.set_alpha(100)
            WIN.blit(left, (435, 415))
        if start + 1 <= 4:
            right = SCOPES[start+1]
            right.set_alpha(100)
            WIN.blit(right, (1235, 415))

        middle = SCOPES[start]
        middle.set_alpha(255)
        WIN.blit(middle, (835, 415))

        WIN.blit(BACK_Standard, (BACK_Standard_Rect))
        if BACK_Standard_Rect.collidepoint(pygame.mouse.get_pos()):
            WIN.blit(BACK_Hover, (BACK_Hover_Rect))
            if pygame.mouse.get_pressed()[0] == 1 and Clicked == False:
                Files("Settings.txt", start)
                Menu()

        pygame.display.update()

#Write to a file of chosen scope and try changing the code for it by using classes!

def Info():
    #Set variables before the loop
    Options = True
    BgOpacity = 0
    WIN.blit(INFO, (0, 0))
    while Options:
        while BgOpacity != 250:
            OPTIONS_BG.set_alpha(BgOpacity)
            BgOpacity += 10
            WIN.blit(OPTIONS_BG, (0, 0))
            WIN.blit(INFO, (0, 0))
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            #Checks for any input on a keyboard
            if event.type == pygame.KEYDOWN:
                Opacity = 0
                #Transition after an input is detected
                while Opacity != 255:
                    TRANSITION_BG.set_alpha(Opacity)
                    WIN.blit(TRANSITION_BG, (0, 0))
                    Opacity += 15
                    pygame.display.update()
                #Imports the  main game
                import MainGame
                del sys.modules["MainGame"]
                del MainGame

        pygame.display.update()

Top10User = []
Top10Score = []
Top10 = []

def LeaderBoardInfo():
    with open ("Scoreboard.txt", "r") as f:
        for i in f:
            UserName, Score = i.split(" : ")
            Score = Score.strip()
            Top10.append((UserName, int(Score)))
        Top10.sort(key=lambda Top10:Top10[1], reverse=True)
        for i in Top10:
            user, score = str(i).split(",")
            user = user.strip("'(), ")
            score = score.strip("'(), ")
            Top10User.append(user)
            Top10Score.append(score)

LeaderBoardInfo()

def Menu():
    clock.tick(FPS)
    Menu = True
    Scroll, Opacity = 0, 0 
    while Menu:
        global Play
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        if Opacity != 250:
            BACKGROUND.set_alpha(Opacity)
            Opacity += 10
        
        for i in range(0, 2):
            WIN.blit(BACKGROUND, (i * WIDTH + Scroll, 0))
        Scroll -= 7

        if Scroll*-1 > WIDTH:
            Scroll = 0

        WIN.blit(LEADERBOARD, (1210, 5))
        for i in range(10):
            try:
                User = Top10User[i]
                Score = Top10Score[i]
            except:
                User = "Empty"
                Score = 0
            if User == "Empty":
                WIN.blit(((pygame.font.Font("freesansbold.ttf", 50)).render(str(User), True, LIGHT_GREY)), (1300,140+68*(i+1)))
                WIN.blit(((pygame.font.Font("freesansbold.ttf", 50)).render(str(Score), True, LIGHT_GREY)), (1650,140+68*(i+1)))
            else:
                WIN.blit(((pygame.font.Font("freesansbold.ttf", 50)).render(str(User), True, WHITE)), (1300,140+68*(i+1)))
                WIN.blit(((pygame.font.Font("freesansbold.ttf", 50)).render(str(Score), True, WHITE)), (1650,140+68*(i+1)))

        WIN.blit(PLAY_Standard, (PLAY_Standard_Rect))
        if PLAY_Standard_Rect.collidepoint(pygame.mouse.get_pos()):
            WIN.blit(PLAY_Hover, (PLAY_Hover_Rect))
            if pygame.mouse.get_pressed()[0] == 1 and Clicked == False:
                Opacity = 0
                while Opacity != 255:
                    TRANSITION_BG.set_alpha(Opacity)
                    WIN.blit(TRANSITION_BG, (0, 0))
                    Opacity += 15
                    pygame.display.update()
                Info()

        WIN.blit(SCOPES_Standard, (SCOPES_Standard_Rect))
        if SCOPES_Standard_Rect.collidepoint(pygame.mouse.get_pos()):
            WIN.blit(SCOPES_Hover, (SCOPES_Hover_Rect))
            if pygame.mouse.get_pressed()[0] == 1 and Clicked == False:
                Menu = False
                Opacity = 0
                while Opacity != 255:
                    TRANSITION_BG.set_alpha(Opacity)
                    WIN.blit(TRANSITION_BG, (0, 0))
                    Opacity += 15
                    pygame.display.update()
                Scopes()

        WIN.blit(EXIT_Standard, (EXIT_Standard_Rect))
        if EXIT_Standard_Rect.collidepoint(pygame.mouse.get_pos()):
            WIN.blit(EXIT_Hover, (EXIT_Hover_Rect))
            if pygame.mouse.get_pressed()[0] == 1 and Clicked == False:
                pygame.quit()
                exit()


        if Play == True:
            WIN.blit(PLAY, (PLAY_Rect))
            pygame.mixer.music.unpause()
            if PLAY_Rect.collidepoint(pygame.mouse.get_pos()):
                WIN.blit(pygame.transform.scale(PLAY, (175, 175)), (1742, 902))
                if pygame.mouse.get_pressed()[0] == 1 and Clicked == False:
                    Play = False
        else:
            WIN.blit(PAUSE, (PAUSE_Rect))
            pygame.mixer.music.pause()
            if PAUSE_Rect.collidepoint(pygame.mouse.get_pos()):
                WIN.blit(pygame.transform.scale(PAUSE, (175, 175)), (1742, 902))
                if pygame.mouse.get_pressed()[0] == 1 and Clicked == False:
                    Play = True

        if pygame.mouse.get_pressed()[0] == 0:
            Clicked = False

        pygame.display.update()

if __name__ == "__main__" or "__MainGame__":
    Menu()
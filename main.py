import pygame
import math
import random
from pygame import mixer

pygame.init()

mixer.music.load("background.wav")
mixer.music.play(-1)

Width, Height = 800, 600
win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Hangman Game!')
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

radius = 20
gap = 15
letters = []
startX = round((Width - (radius * 2 + gap) * 13) / 2)
startY = 480
A = 65
for i in range(26):
    x = startX + gap * 2 + ((radius * 2 + gap) * (i % 13))
    y = startY + ((i // 13) * (gap + radius * 2))
    letters.append([x, y, chr(A+i), True])

images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

hangman_status = 0
words = ['MONOPOLY','BUZZED','SISTER','PUZZLE','BROTHER','BRONZE','PLANET','BLOOD','CYPHER','IMPOSTOR','BUTTERFLY','ICON','DELETE',
'COMPUTER','MOTHER','SCRABBLE','FATHER','UNIQUE','UNCLE','AMAZE','COUNTRY','BANK','RIVER','OPERA','SUGAR','STAR','WAR','ENTER',
'COMIC','SPAGHETTI','HACKER','HANGMAN','MEME','PIZZA','PYTHON','PASTA','SELFIE','CAMERA','WINE','BOTTLE','FIRE','CALENDAR',
'SPECTACLES','SNAKE','CALCULATOR','GOOGLE','DEVELOPER','OPERA','ABROAD','DATE','ACCEPT','STALKER','ABSTRACT','WATER','POTATO',
'FIG','MANGO','EDUCATION','MANIAC','SKATE','GUN','SKATEBOARD','BOX','OCEANIA','ZEBRA','ALLY','PHOENIX','HOUSE','DONKEY','DINNER']
word = random.choice(words)
guessed = []

white = (255, 255, 255)
black = (0, 0, 0)

font1 = pygame.font.SysFont('comicsans', 40)
font2 = pygame.font.SysFont('comicsans', 60)
font3 = pygame.font.SysFont('comicsans', 70)

FPS = 60
clock = pygame.time.Clock()
run = True


def draw():
    win.fill(white)

    text = font3.render("Hangman Game", 1, black)
    win.blit(text, (Width/2 - text.get_width()/2, 20))

    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = font2.render(display_word, 1, black)
    win.blit(text, (400, 200))

    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, black, (x, y), radius, 3)
            text = font1.render(ltr, 1, black)
            win.blit(text, (x-text.get_width()/2, y-text.get_height()/2))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()

def display_text(text):
        pygame.time.delay(1000)
        win.fill(white)
        text = font2.render(text, 1, black)
        win.blit(text, (Width/2 - text.get_width()/2, Height/2 - text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(3000)
print(len(words))
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                    if dis < radius:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            loseSound = mixer.Sound("game_over.wav")
                            loseSound.play()
                            hangman_status += 1 

    draw()

    won = False
    for letter in word:
        if letter not in guessed:
            won = False
            break
        elif letter in guessed:
            won = True

    if won:
        winSound = mixer.Sound("win.wav")
        winSound.play()
        display_text("You WON!!")
        break

    if hangman_status == 6:
        loseSound = mixer.Sound("game_over.wav")
        loseSound.play()
        display_text("Sorry You LOST! \n Word: " + word.lower())
        break

pygame.quit()

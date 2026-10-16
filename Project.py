#this imports pygame into my code, With shorthands
import pygame as pg
import json
import constants as c
#These codes link files to my main project file
from enemy import Enemy
from world import World
from tower import Tower
from button import Button
from tower_data import TOWER_DATA as tdata
from enemy_data import ENEMY_SPAWN_DATA as espawndata

#initialise py game
pg.init()

#create clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL ,c.SCREEN_HEIGHT))
pg.display.set_caption("War Tower Defence")

#game variables
game_state = "menu"
tower_type = "None"
difficulty = "None"
Total_waves = 0

placing_tower = False
selected_tower = None
last_enemy_spawn = pg.time.get_ticks()
level_started = False
game_over = False
game_outcome = 0 #-1 = Lose, 1 = win



#load images-------------------------------------
#load map
map_image = pg.image.load('levels/level.png').convert_alpha()

#individual tower image for mouse cursor
cursor_tower = pg.image.load('assets/images/towers/TowerTest.png').convert_alpha()
cursor_tower2 = pg.image.load('assets/images/towers/Tower2Test.png').convert_alpha()


#load tower spitesheet
tower_spritesheets = {
    "tower": [],
    "tower2": []
}

for level in range(1, c.TOWER_LEVELS+1):    
    tower_img = pg.image.load(f'assets/images/towers/tower{level}u.png').convert_alpha()
    tower2_img = pg.image.load(f'assets/images/towers/tower2_{level}u.png').convert_alpha()
    tower_spritesheets["tower"].append(tower_img)
    tower_spritesheets["tower2"].append(tower2_img)

#load enemies:
enemy_images = {
    "weak": pg.image.load("assets/images/enemies/enemy_weak.png").convert_alpha(),
    "normal": pg.image.load("assets/images/enemies/enemy_normal.png").convert_alpha(),
    "strong": pg.image.load("assets/images/enemies/enemy_strong.png").convert_alpha()
}

#GAMEstate MEnu
#button 
play_image = pg.image.load('assets/images/buttons/play.png').convert_alpha()
quit_image = pg.image.load('assets/images/buttons/quit.png').convert_alpha()
#GUI 
WarTDLogo_image = pg.image.load('assets/images/GUI/war_tower_defence_logo.png').convert_alpha()

#Game state Map Select
#Button
Map1B = pg.image.load('assets/images/buttons/map1Buton.png').convert_alpha()
Map2B_WIP = pg.image.load('assets/images/buttons/wipbutton.png').convert_alpha()
back_image = pg.image.load('assets/images/buttons/back.png').convert_alpha()

#GAME STATE Difficulty 
#Buttons
EasyButton_img = pg.image.load("assets/images/buttons/Difficulty/EzButon.png").convert_alpha()
NormalButton_img = pg.image.load("assets/images/buttons/Difficulty/NormButon.png").convert_alpha()
HardButton_img = pg.image.load("assets/images/buttons/Difficulty/HardButon.png").convert_alpha()




#buttons for Gamestate game
buy_tower_image = pg.image.load('assets/images/buttons/Buy_tower.png').convert_alpha()
cancel_image = pg.image.load('assets/images/buttons/Calcel.png').convert_alpha()
upgrade_image = pg.image.load('assets/images/buttons/upgrade.png').convert_alpha()
start_image = pg.image.load('assets/images/buttons/start.png').convert_alpha()
retry_image = pg.image.load('assets/images/buttons/retry.png').convert_alpha()
fast_forward_image = pg.image.load('assets/images/buttons/2xspeed.png').convert_alpha()
tower_image = pg.image.load('assets/images/buttons/tower.png').convert_alpha()
tower2_image = pg.image.load('assets/images/buttons/tower2.png').convert_alpha()
exit_image = pg.image.load('assets/images/buttons/exit.png').convert_alpha()
home_image = pg.image.load('assets/images/buttons/home.png').convert_alpha()
#Gui
riplose = pg.image.load('assets/images/GUI/lose.png').convert_alpha()

#---------------------------------------------------

#load json data for level
with open('levels/level.tmj') as file:
    world_data = json.load(file)


#load fonts for displaying text on the screen
text_font = pg.font.SysFont("Consolas", 24, bold = True)
large_text_font = pg.font.SysFont("Consolas", 36)



#Functions -------------------------------------------------------------------
def draw_text(text, font, text_col, x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def create_tower(mouse_pos, tower_type):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    #calculate the sequential number of the tile
    mouse_tile_num = (mouse_tile_y * c.COLUMNS) + mouse_tile_x
    #check if that tile is grass
    if world.tile_map[mouse_tile_num] == 7:
        #checks if there is a tower already placed
        spacefree = True
        for tower in tower_group:
            if (mouse_tile_x,mouse_tile_y) == (tower.tile_x,tower.tile_y):
                spacefree = False
        #if space us free tower can be placed
        if spacefree == True:
            new_tower = Tower(tower_spritesheets, mouse_tile_x,mouse_tile_y, tower_type)
            tower_group.add(new_tower)
            #TAKES MONEY WHEN BUYING TOWER
            world.money-= tdata[tower_type][0]["cost"]

def select_tower(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for tower in tower_group:
            if (mouse_tile_x,mouse_tile_y) == (tower.tile_x,tower.tile_y):
                return tower

def clear_selection():
    for tower in tower_group:
        tower.selected = False


#CREATE OBJECTS I THINK-------------------------------------------------------------------

#create groups
enemy_group = pg.sprite.Group()
tower_group = pg.sprite.Group()

#create buttons-----------------------------------------------------
#gamestate menu
play_button = Button(400, 500, play_image, True)
quit_button = Button(425, 570, quit_image, True)

#Gamestate Map Select
Map1B_button = Button(150, 100, Map1B, True)
Map2B_WIP_button = Button(600, 100, Map2B_WIP, True)
back_button = Button(25, 25, back_image, True)

#GAME STATE Difficulty
easy_button = Button(50, 400, EasyButton_img, True)
norm_button = Button(250, 400, NormalButton_img, True)
hard_button = Button(450, 400, HardButton_img, True)





#gamestate game
buy_button = Button(c.SCREEN_WIDTH + 30, 120, buy_tower_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, False)
upgrade_button = Button(c.SCREEN_WIDTH + 50, 200, upgrade_image, True)
start_button = Button(c.SCREEN_WIDTH + 50, 400, start_image, True)

fast_forward_button = Button(c.SCREEN_WIDTH + 50, 350, fast_forward_image, False)
tower_button = Button(c.SCREEN_WIDTH + 30, 25, tower_image, True)
tower2_button = Button(c.SCREEN_WIDTH + 150, 25, tower2_image, True)
exit_button = Button(c.SCREEN_WIDTH + 150, 600, exit_image, True)
home_button = Button(600, 300, home_image, True)
retry_button = Button(400, 300, retry_image, True)




#game loop the window will stay open unless run is switched to false
run = True
while run:

    clock.tick(c.FPS)

    if game_state == "menu":
        screen.fill("grey")
        screen.blit(WarTDLogo_image,(200,50))
        if play_button.draw(screen):
            game_state = "mapselect"
        if quit_button.draw(screen):
            run = False
            

    if game_state == "mapselect":
        screen.fill("grey")
        draw_text("map selector:",large_text_font,"black", 150,25)
        if Map1B_button.draw(screen):
            game_state = "diffselect"
        if Map2B_WIP_button.draw(screen):
            game_state = "map2"
        if back_button.draw(screen):
            game_state = "menu"
        
    if game_state == "diffselect":
            screen.fill("grey")
            draw_text("Difficutly selector:",large_text_font,"black", 150,25)
            draw_text("HMMMMM what difficulty should you pick? ",large_text_font,"black", 150,200)
            draw_text(" idk pcik the one that is eassiest for u",large_text_font,"black", 150,300)
            if easy_button.draw(screen):
                difficulty = "easy"
            if norm_button.draw(screen):
                difficulty = "normal"
            if hard_button.draw(screen):
                difficulty = "hard"
            if back_button.draw(screen):
                game_state = "mapselect"

            if difficulty != "None":
                #create world
                Total_waves = len(espawndata[difficulty])
                world = World(world_data, map_image)
                world.process_data()
                world.process_enemies(difficulty)
                game_state = "game"

    if game_state == "map2":
        screen.fill("grey")
        draw_text("map 2 has not been made yet sorry :p",large_text_font,"black", 100,300)
        if back_button.draw(screen):
            game_state = "mapselect"

            

    if game_state == "game":
        #UPDATING SECTION----------------------------------------------
        if game_over == False:
            #check if player lost
            if world.health <= 0:
                game_over = True
                game_outcome = -1 #lost
            if world.wave > Total_waves:
                game_over = True
                game_outcome = 1 #win

            #update grouos
            enemy_group.update(world)
            tower_group.update(enemy_group, world)

            #highlight selected tower
            if selected_tower:
                selected_tower.selected = True


        
        #DRAWING SECTION------------------------------------------------
        screen.fill("grey100")

        #draw level
        world.draw(screen)

        #draw enemy path
        #pg.draw.lines(screen, "grey0", False, world.waypoints)

        #draw groups
        enemy_group.draw(screen)
        for tower in tower_group:
            tower.draw(screen)

        draw_text(str(world.health), text_font, "red", 0, 0)
        draw_text(str(world.money), text_font, "yellow", 0, 30)
        draw_text(tower_type, text_font, "#90D5FF", c.SCREEN_WIDTH+ 150, 0)
        draw_text(("wave "+str(world.wave)+"/" + str(Total_waves)), text_font, "#90D5FF", c.SCREEN_WIDTH, 0)


        if game_over == False:
            #check if level has started or not
            if level_started == False:
                if start_button.draw(screen):
                    level_started = True
            else:
                #fast forward option
                world.game_speed = 1
                if fast_forward_button.draw(screen):
                    world.game_speed = 2
                    
                #Spawns enemies yay
                if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
                    if world.spawned_enemies < len(world.enemy_list):
                        enemy_type = world.enemy_list[world.spawned_enemies]
                        enemy = Enemy(enemy_type,world.waypoints, enemy_images)
                        enemy_group.add(enemy)
                        world.spawned_enemies += 1
                        last_enemy_spawn = pg.time.get_ticks()

            #Checks if wave is completed
            if world.check_wave_complete() == True:
                world.money += c.WAVE_BONUS
                world.wave += 1
                level_started = False
                last_enemy_spawn = pg.time.get_ticks()
                world.reset_level()
                if world . wave <= Total_waves:
                    world.process_enemies(difficulty)

            #Draw buttons
            #button for placing towers
            if tower_button.draw(screen):
                tower_type = "tower"
            if tower2_button.draw(screen):
                tower_type = "tower2"
            if exit_button.draw(screen):
                game_state = "menu"

            if buy_button.draw(screen):
                placing_tower = True
            #if palcing towers then show the cancel button aswell
            if placing_tower == True:
                #Decides to show which cusor tower will be displayed
                if tower_type == "tower":  
                    cursor_rect = cursor_tower.get_rect()
                    cursor_pos = pg.mouse.get_pos()
                    cursor_rect.center = cursor_pos
                    if cursor_pos[0] <= c.SCREEN_WIDTH: 
                        screen.blit(cursor_tower,cursor_rect)
                if tower_type == "tower2": 
                    cursor_rect = cursor_tower.get_rect()
                    cursor_pos = pg.mouse.get_pos()
                    cursor_rect.center = cursor_pos
                    if cursor_pos[0] <= c.SCREEN_WIDTH: 
                        screen.blit(cursor_tower2,cursor_rect)


                if cancel_button.draw(screen):
                    placing_tower = False
            #if a tower has been selected it will show the upgrade button
            if selected_tower:
                #IF a tower can be upgraded, upgrade button is shown
                if selected_tower.upgrade_level < c.TOWER_LEVELS:
                    if upgrade_button.draw(screen):
                        if world.money >= c.UPGRADE_COST:
                            selected_tower.upgrade()
                            world.money -= c.UPGRADE_COST
        else:
            screen.fill("grey")
            if game_outcome == -1:
                screen.blit(riplose,(130,167))
                draw_text("RIP SOLDIER U DIED A HRO!", large_text_font, "grey0", 310, 230)
            elif game_outcome == 1:
                draw_text("You win ", large_text_font, "grey0", 310, 230)
            #restart level
            if retry_button.draw(screen):
                game_over = False
                level_started = False
                placing_tower = False
                selected_tower = None
                last_enemy_spawn = pg.time.get_ticks()
                world = World(world_data, map_image)
                world.process_data()
                world.process_enemies(difficulty)
                #empty groups
                enemy_group.empty()
                tower_group.empty()
            if home_button.draw(screen):
                game_over = False
                level_started = False
                placing_tower = False
                selected_tower = None
                last_enemy_spawn = pg.time.get_ticks()
                enemy_group.empty()
                tower_group.empty()
                difficulty = "None"
                game_state = "menu"

    #event handler
    for event in pg.event.get():
        #quit program
        if event.type == pg.QUIT:
            run = False
        #mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #check if mouse is in the game area
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                #clear the selected tower
                selected_tower = None
                clear_selection()
                if placing_tower == True and tower_type != "None":
                        if world.money >= tdata[tower_type][0]["cost"]:
                            create_tower(mouse_pos,tower_type)
                else:
                    selected_tower = select_tower(mouse_pos)

    #update display
    pg.display.flip()
pg.quit()

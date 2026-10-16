import pygame as pg
import math
import constants as c
from tower_data import TOWER_DATA


class Tower(pg.sprite.Sprite):
    def __init__(self, sprite_sheets, tile_x,tile_y, tower_type):
        pg.sprite.Sprite.__init__(self)
        self.tower_type = tower_type
        self.upgrade_level = 1
        self.range = TOWER_DATA[self.tower_type][self.upgrade_level - 1].get("range")
        self.cooldown = TOWER_DATA[self.tower_type][self.upgrade_level - 1].get("cooldown")
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None

        #postition variables
        self.tile_x = tile_x
        self.tile_y = tile_y
        #calculates center coordinates
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE

        #animation variables
        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images(self.sprite_sheets[self.tower_type][self.upgrade_level -1 ])
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

    #udate images 
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

        #show the range of tower with transparent circle.
        self.range_image = pg.Surface((self.range *2, self.range*2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def load_images(self, sprite_sheet):
        #extract the images from sprite sheet
        size = sprite_sheet.get_height()
        self.animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            self.animation_list.append(temp_img)
        return self.animation_list
    
    def update(self, enemy_group, world):
        #if the target is picked, start the foromg amo,ation!!
        if self.target:
            self.play_animation()
        else:
            #ssearch for new target once tower has cooled down!
            if pg.time.get_ticks() - self.last_shot > (self.cooldown / world.game_speed):
                self.pick_target(enemy_group)
        
    def play_animation(self):
        #update image
        self.original_image = self.animation_list[self.frame_index]
        #check if  enough time has passed since last update
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            #check if aniimation is finisshed AND resets it back idele.
            if self.frame_index >= len(self.animation_list):
                self.frame_index =0
                #record completed time and clear target so cooldown can begin
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def pick_target(self, enemy_group):
        #find an enemy to target
        x_dist = 0
        y_dist = 0
        #check distance to each enemy to see if it is in range
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist**2 + y_dist**2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    #dmg the enemy
                    self.target.health -= c.DAMAGE
                    break
                    #print("EMEMMYY FOUND selected")

    def upgrade(self):
        self.upgrade_level += 1
        self.range = TOWER_DATA[self.tower_type][self.upgrade_level - 1].get("range")
        self.cooldown = TOWER_DATA[self.tower_type][self.upgrade_level - 1].get("cooldown")
        #upgrade turret image
        self.animation_list = self.load_images(self.sprite_sheets[self.tower_type][self.upgrade_level -1 ])
        self.original_image = self.animation_list[self.frame_index]

        #upgraded range circle
        self.range_image = pg.Surface((self.range *2, self.range*2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw(self,surface):
        self.image = pg.transform.rotate(self.original_image, self.angle-90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect) 
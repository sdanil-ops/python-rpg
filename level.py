import json
import random

import pygame

from debug import debug
from player import Player
from settings import *
from support import import_csv_layout, import_folder
from tile import Tile
from weapon import Weapon


class Level:
    player: Player = None

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = Box()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None

        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
        }
        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects'),

        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for column_index, column in enumerate(row):
                    if column != '-1':
                        x = column_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = random.choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)
                        if style == 'object':
                            surface = graphics['objects'][int(column)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surface)

        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

        # debug
        debug_info = {
            'game status': game_status,
            'active key': self.player.pressed_key,
            'active weapon': self.player.weapon,
            'player status': self.player.status,
            'player direction': (round(self.player.direction[0]), round(self.player.direction[1])),
            'player is attacking': self.player.attacking,
            'player can switch weapon': self.player.weapon_can_switch,
        }
        if DEBUG:
            pass
        else:
            debug_info = {
                'game status': game_status,
            }
        debug(debug_info)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_with = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.floor_surface = pygame.image.load('graphics/tilemap/ground.png').convert_alpha()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # trigonometry

        self.offset.x = player.rect.centerx - self.half_with
        self.offset.y = player.rect.centery - self.half_height
        point_x = 150 + self.offset.x * 10 - self.offset.y * 10,
        point_y = 100 + self.offset.x * 5 + self.offset.y * 5,
        floor_offset_position = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_position)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)


class Box(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera_offset
        self.half_with = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        # box setup
        self.camera_borders = camera_borders
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rectangle = pygame.Rect(l, t, w, h)
        # ground
        self.ground_surface = pygame.image.load('graphics/tilemap/ground.png').convert_alpha()
        self.ground_rectangle = self.ground_surface.get_rect(topleft=(0, 0))

    def box_target_camera(self, target):
        if target.rect.left < self.camera_rectangle.left:
            self.camera_rectangle.left = target.rect.left
        if target.rect.right > self.camera_rectangle.right:
            self.camera_rectangle.right = target.rect.right
        if target.rect.top < self.camera_rectangle.top:
            self.camera_rectangle.top = target.rect.top
        if target.rect.bottom > self.camera_rectangle.bottom:
            self.camera_rectangle.bottom = target.rect.bottom

        self.offset.x = self.camera_rectangle.left - self.camera_borders['left']
        self.offset.y = self.camera_rectangle.top - self.camera_borders['top']

    def custom_draw(self, player):
        # trigonometry

        self.box_target_camera(player)
        floor_offset_position = self.ground_rectangle.topleft - self.offset
        self.display_surface.blit(self.ground_surface, floor_offset_position)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)


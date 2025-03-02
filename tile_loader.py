
import csv
import pygame

class TileLoader:
    def __init__(self, tile_size, csv_file):
        self.tile_size = tile_size
        self.csv_file = csv_file
        self.tiles = {}  
        self.map_data = [] 
        self.load_map()

    def load_map(self):
       
        with open(self.csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            self.map_data = [list(map(int, row)) for row in reader]

    def load_tile_images(self, tile_images):
        
        for tile_id, image_path in tile_images.items():
            self.tiles[tile_id] = pygame.image.load(image_path).convert_alpha()

    def draw(self, screen):
       
        for y, row in enumerate(self.map_data):
            for x, tile_id in enumerate(row):
                if tile_id != 0:  
                    tile_image = self.tiles.get(tile_id)
                    if tile_image:
                        screen.blit(tile_image, (x * self.tile_size, y * self.tile_size))


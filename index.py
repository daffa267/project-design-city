import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Ukuran sel
CELL_SIZE = 10

# Ukuran kota (dalam sel)
CITY_SIZE = 150

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load gambar rumput, rumah, dan gedung
grass_img = pygame.image.load('images/grass.png')
house_img = pygame.image.load('images/house.png')
building_img = pygame.image.load('images/building1.png')

# Resize gambar sesuai ukuran sel
grass_img = pygame.transform.scale(grass_img, (CELL_SIZE, CELL_SIZE))
house_img = pygame.transform.scale(house_img, (CELL_SIZE*2, CELL_SIZE*2))
building_img = pygame.transform.scale(building_img, (CELL_SIZE*5, CELL_SIZE*5))

# Inisialisasi layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("City")

def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

def draw_city(city):
    for x in range(CITY_SIZE):
        for y in range(CITY_SIZE):
            if city[x][y] == 0:  # Rumput
                screen.blit(grass_img, (x * CELL_SIZE, y * CELL_SIZE))
            elif city[x][y] == 1:  # Rumah
                screen.blit(house_img, (x * 2, y * 2))
            elif city[x][y] == 2:  # Gedung
                screen.blit(building_img, (x * 5, y * 5))

def generate_city():
    city = [[0 for _ in range(CITY_SIZE)] for _ in range(CITY_SIZE)]
    num_houses = 0
    # Tempatkan rumah secara acak hingga mencapai batas jumlah rumah
    while num_houses < 10:
        x = random.randint(0, CITY_SIZE - 2)  # Hindari agar rumah tidak keluar dari batas kota
        y = random.randint(0, CITY_SIZE - 1)
        if city[x][y] == 0 and city[x + 1][y] == 0:  # Pastikan sel yang dipilih belum ditempati
            city[x][y] = 1
            city[x + 1][y] = 1
            num_houses += 1

    # Tempatkan 1 gedung secara acak di dalam kota
    building_placed = False
    while not building_placed:
        x = random.randint(0, CITY_SIZE - 5)  # Hindari agar gedung tidak keluar dari batas kota
        y = random.randint(0, CITY_SIZE - 5)
        # Pastikan area gedung kosong
        building_clear = True
        for i in range(x, x + 5):
            for j in range(y, y + 5):
                if city[i][j] != 0:
                    building_clear = False
                    break
            if not building_clear:
                break
        # Jika area gedung kosong, tempatkan gedung
        if building_clear:
            for i in range(x, x + 5):
                for j in range(y, y + 5):
                    city[i][j] = 2  # Gunakan angka lain untuk gedung
            building_placed = True

    return city

def main():
    city = generate_city()

    while True:
        screen.fill(GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Tombol untuk meredesain
                    city = generate_city()

        draw_grid()
        draw_city(city)

        pygame.display.flip()

if __name__ == "__main__":
    main()

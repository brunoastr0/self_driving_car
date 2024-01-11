import pygame
from src.Deprecated.Colors import Colors


def load_image(directory):
    return pygame.image.load(f"images/{directory}")

def scale_image(img, factor):
    size = round(img.get_width()*factor), round(img.get_height()*factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(surface, img, angle, position):
    rotated_image = pygame.transform.rotate(img,angle)
    new_rect = rotated_image.get_rect(center = img.get_rect(topleft = position).center)
    surface.blit(rotated_image , new_rect.topleft)


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


def getPixelArray(surface):
    hex = ['6F7073']
    width = surface.get_width()
    height = surface.get_height()
    matrix = [[0] * width for _ in range(height)]
    for i in range(width):
        for j in range(height):
            
            color = surface.get_at((i, j))
            to_hex = rgb_to_hex((color[0], color[1], color[2]))
            if color[0] == 111 and color[1] == 112 and color[2] == 115: 
                # print(to_hex)
                matrix[j][i] = 1
            else:  
                #print(color)
                matrix[j][i] = 0
    # print(matrix[150][150])
    save_pixels_to_file(matrix)
    return matrix
    


    
def save_pixels_to_file(pixels):
    path = "images/track/track.txt"

    with open(path, 'w') as file:

         for item in pixels:
            file.write(str(item))


def open_track():
    file_path = "images/track/track.txt"

    matrix = []

# Open the file in read mode
    with open(file_path, 'r') as file:
        content = file.read()

    # Print the content of the file for debugging
       

        # Extract sequences within square brackets
        sequences = content.split('][')

        # Iterate over each sequence
        for sequence in sequences:
            # Remove square brackets and split by commas
            sequence = sequence.replace('[', '').replace(']', '').strip()
            row = [int(num) for num in sequence.split(',')]

            # Append the row to the matrix
            matrix.append(row)
    
    return matrix
        
def draw_track(pixels,surface):
    # pixels = open_track()
    width = surface.get_width()
    height = surface.get_height()
    for i in range(width):
        for j in range(height):
            if pixels[j][i] == 1:
                surface.set_at((i,j), Colors.RED.value)
            else:
                surface.set_at((i,j), Colors.WHITE.value)

            
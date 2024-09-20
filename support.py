from csv import reader
from os import walk
import pygame

import pygame.image


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ",")
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []
    for data in walk(path):
        for _,__,img_files in walk(path):
            for image in img_files:
                full_path = path + "/" + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)
    return surface_list


def read_file_to_list(file_path):
    """
    Reads a text file and returns a list of its lines.

    Args:
        file_path (str): The path to the text file.

    Returns:
        list: A list where each element is a line from the file.
    """
    lines = []
    try:
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except IOError:
        print(f"Error: An IO error occurred while trying to read the file at {file_path}.")

    return lines

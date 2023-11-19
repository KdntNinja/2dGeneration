from colorama import init, Fore
import numpy as np
import threading

number: int = 2


class BlockType:
    Grass = 0
    Air = 1
    Water = 2


class Chunk:
    def __init__(self, grass_level=30, water_level=40):
        self.xMax = 240
        self.yMax = 100
        self.zMax = 20
        self.frequency = 0.2
        self.amplitude = 10
        self.xOffsetIncrement = 0.1
        self.zOffsetIncrement = 0.05
        self.grass_level = grass_level

        x_values = np.arange(self.xMax)
        y_values = np.arange(self.yMax)
        z_values = np.arange(self.zMax)

        x_offsets = self.compute_offset(x_values, self.xOffsetIncrement)
        z_offsets = self.compute_offset(z_values, self.zOffsetIncrement)

        x_offsets = x_offsets[:self.xMax]
        z_offsets = z_offsets[:self.zMax]

        surface_y = self.grass_level + x_offsets[:, np.newaxis] + z_offsets

        new_water_level = 160

        self.data = np.where(
            (y_values[:, np.newaxis, np.newaxis] < surface_y) & (y_values[:, np.newaxis, np.newaxis] < new_water_level),
            BlockType.Grass,
            np.where(y_values[:, np.newaxis, np.newaxis] < water_level, BlockType.Water, BlockType.Air)
        )

    def compute_offset(self, values, offset_increment):
        return np.sin(values * self.frequency) * (self.amplitude - 5) + \
            np.sin(values * (self.frequency - offset_increment)) * (self.amplitude + 5) + \
            np.sin(values * (self.frequency + offset_increment)) * self.amplitude


def print_chunk_2d(chunk, z_slice):
    for i in range(chunk.yMax - 1, -1, -1):
        row_chars = []
        for j in range(chunk.xMax):
            block_value = chunk.data[i, j, z_slice]
            print_char: str

            if block_value == BlockType.Grass:
                print_char = f"{Fore.GREEN}#{Fore.RESET}"
            elif block_value == BlockType.Water:
                print_char = f"{Fore.BLUE}~{Fore.RESET}"
            elif block_value == BlockType.Air:
                print_char = "^"
            else:
                print_char = f"{Fore.RED}@{Fore.RESET}"

            row_chars.append(print_char)

        print(''.join(row_chars))


def main():
    init()
    chunk_x = 0
    chunk_z = 0

    world_size = [2, 2]

    if chunk_x >= world_size[0] or chunk_z >= world_size[1]:
        print("Error: Chunk does not exist")
        return 1

    grass_level = 30
    chunk = Chunk(grass_level=grass_level, water_level=grass_level + 10)
    chunk_thread = threading.Thread(target=print_chunk_2d, args=(chunk, 15))
    chunk_thread.start()

    return 0


if __name__ == "__main__":
    main_thread = threading.Thread(target=main)
    main_thread.start()
    main_thread.join()

    while True:
        pass

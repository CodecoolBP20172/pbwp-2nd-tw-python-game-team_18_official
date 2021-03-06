import sys
import os
import readchar


def main():
    """The game has 3 levels, each in separate files. First it reads the file according to the level,
    then it converts it to a list, places the player to the maze (to the same place on each level) and prints
    to the screan. It asks keyboard input from the player untils (s)he reaches the victory location.
    Then it repeats with the next level. At the end, the players reward will be a beautiful win picture.
    """
    os.system("clear")
    level = 0
    print_intro(level)

    while level < 3:
        filename = next_level(level)
        map_string = map_reading(filename)
        maze = map_convert_to_list(map_string)
        player_pos = initialization(maze)
        level = move_player(player_pos, maze, level)

    win_game()


def print_intro(level):
    intro_string = map_reading("intro.txt")
    for i in intro_string:
        if i == "x":
            print("\033[0;31;41mx\033[0m", end="")
        elif i == "L":
            print("\033[2;37;40m  Labirinth  \033[0m")
        else:
            print(i, end="")
    any_key = readchar.readchar()
    os.system("clear")


def next_level(level):
    if level == 0:
        return "map0.txt"
    elif level == 1:
        return "map1.txt"
    elif level == 2:
        return "map2.txt"


def map_reading(filename="map0.txt"):
    try:
        with open(filename) as map_string:
            map_string = map_string.read()
            return map_string

    except FileNotFoundError:
        print("These are not the drones you are looking for.")
        print("We're sorry, but the maps are somewhere in the galaxy.")
    sys.exit()


def map_convert_to_list(map_string):
    maze = []
    row_num = map_string.count("\n")
    column_num = map_string.find("\n")
    component = 0

    for row in range(row_num):
        maze.append([])
        for column in range(column_num):
            maze[row].append(color_map_component(map_string, component))
            component += 1
            if map_string[component] == "\n":
                component += 1
    return maze


def color_map_component(map_string, component):
    if map_string[component] == "x":
        return "\033[0;30;40mx\033[0m"
    elif map_string[component] == " ":
        return "\033[0;37;47m "
    elif map_string[component] == "s":
        return "\033[0;33;42ms"
    elif map_string[component] == "o":
        return "\033[0;36;46mo"
    elif map_string[component] == "k":
        return "\033[0;34;47mk"
    elif map_string[component] == "u":
        return "\033[0;31;41mu"
    elif map_string[component]:
        return map_string[component]


def initialization(maze):
    player_pos = [1, 1]
    maze[player_pos[0]][player_pos[1]] = "\033[0;33;42ms"
    print_board(maze)
    return player_pos


def print_board(maze):
    for row in maze:
        print("".join(row))
    print("\nDirection (wsad) or q to quit:")


def move_player(player_pos, maze, level):
    do_i_have_a_key = 0
    map_component = {
                    "door": "\x1b[0;31;41mu",
                    "key": "\x1b[0;34;47mk",
                    "wall": "\x1b[0;30;40mx\x1b[0m",
                    "exit": "\x1b[0;36;46mo",
                    "floor": "\x1b[0;37;47m ",
                    "player": "\x1b[0;33;42ms",
                    }
    while True:
        directions = {
                     "current": maze[player_pos[0]][player_pos[1]],
                     "up": maze[player_pos[0]-1][player_pos[1]],
                     "down": maze[player_pos[0]+1][player_pos[1]],
                     "left": maze[player_pos[0]][player_pos[1]-1],
                     "right": maze[player_pos[0]][player_pos[1]+1],
                     }

        direction_input = key_input(maze)

        if direction_input in ("w", "a", "s", "d"):
            maze[player_pos[0]][player_pos[1]] = map_component["floor"]

        if direction_input == "q":
            quit_game()

        elif direction_input == "w":
            if (directions["up"] not in (map_component["wall"], map_component["door"]) or
               (directions["up"] == map_component["door"]) and (do_i_have_a_key > 0)):

                if directions["up"] == map_component["key"]:
                    do_i_have_a_key += 1
                player_pos[0] -= 1

        elif direction_input == "s":
            if (directions["down"] not in (map_component["wall"], map_component["door"]) or
               (directions["down"] == map_component["door"]) and (do_i_have_a_key > 0)):

                if directions["down"] == map_component["key"]:
                    do_i_have_a_key += 1
                player_pos[0] += 1

        elif direction_input == "a":
            if (directions["left"] not in (map_component["wall"], map_component["door"]) or
               (directions["left"] == map_component["door"]) and (do_i_have_a_key > 0)):

                if directions["left"] == map_component["key"]:
                    do_i_have_a_key += 1
                player_pos[1] -= 1

        elif direction_input == "d":
            if directions["right"] == map_component["exit"]:
                os.system("clear")
                if level < 2:
                    print("Level Up!")
                level += 1
                return level

            if (directions["right"] not in (map_component["wall"], map_component["door"]) or
               (directions["right"] == map_component["door"]) and (do_i_have_a_key > 0)):

                if directions["right"] == map_component["key"]:
                    do_i_have_a_key += 1
                player_pos[1] += 1

        maze[player_pos[0]][player_pos[1]] = map_component["player"]
        os.system("clear")

        print_board(maze)


def key_input(maze):

    correct_input_given = False

    while not correct_input_given:

        direction_input = readchar.readchar()

        if direction_input in ("w", "a", "s", "d", "q"):
            correct_input_given = True

        else:
            os.system("clear")
            print_board(maze)
            print("Please choose from these valid inputs: w, a, s, d, q - quit")

    return direction_input


def quit_game():
            print(
                  "Are you sure you want to leave the game?\n"
                  "Press 'q'' again if yes OR space if no."
                  )
            quit_input = readchar.readchar()
            while quit_input not in ("q", " ", "Q"):
                print("Press 'q'' again if yes OR space if no.")
                quit_input = readchar.readchar()

            if quit_input == ("q" or "Q"):
                sys.exit()


def win_game():
    os.system("clear")
    intro = map_reading("win.txt")
    for i in intro:
        if i == "x":
            print("\033[0;32;42mx\033[0m", end="")
        else:
            print(i, end="")
    print("\n\n\n")


if __name__ == '__main__':
    sys.exit(main())

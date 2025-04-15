# 游戏的脚本可置于此文件中。

# 游戏在此开始。

label puzzle_game:

    $ setup_puzzle()
    call screen puzzle_game_screen

label puzzle_game_finished:
    e "Puzzle Done!"
    jump start

label start:
    $ check_window_size()

    scene bg room
    menu:
        "What's next?"
        "Puzzle Game":
            jump puzzle_game
    return

init python:
    import pygame
    def check_window_size():
        size = pygame.display.get_surface().get_size()
        renpy.notify("{}x{}".format(size[0], size[1]))
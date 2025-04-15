default PIECES_TOTAL = 12 # 拼图总数量
default PIECES_DESTINATION = [
    (1047, 47),
    (1283, 47),
    (1472, 47),
    (1047, 211),
    (1274, 190),
    (1220, 366),
    (1328, 376),
    (1047, 578),
    (1289, 640),
    (1047, 812),
    (1346, 878),
    (1578, 738)
] # 拼图终点位置
default PIECES_ROTATION = [] # 拼图初始旋转角度为n*90度，n为0-3的整数，将会在游戏需要时随机生成
default PIECES_OUTSET = [] # 拼图起点位置，将会在游戏需要时随机生成
default FINISHED_PIECES = 0 # 已经挪动到正确位置的拼图数量
default ROTATE_FUN = False # 是否允许旋转拼图，0表示不允许，1表示允许

screen puzzle_game_screen():
    add "puzzle-border.png":
        xpos 1047-6
        ypos 47-6
    
    draggroup:
        for i in range(PIECES_TOTAL): # 设置左侧的杂乱拼图碎块
            drag:
                drag_name "piece_{}".format(i)
                pos PIECES_OUTSET[i]
                anchor (0.5, 0.5)
                drag_raise True
                if ROTATE_FUN:
                    image "piece-{}.png".format(i) rotate (PIECES_ROTATION[i]*90)
                else:
                    image "piece-{}.png".format(i)
                # image "piece-{}.png".format(i)
                focus_mask True # 只有非透明区域可交互
                draggable True
                
                clicked Function(rotate_piece, piece_index=i)

        for i in range(PIECES_TOTAL): # 设置右侧的拼图目标位置
            drag:
                drag_name "piece_{}".format(i)
                pos PIECES_DESTINATION[i]
                droppable True
                dropped piece_drop # 自定义碎片落入终点的事件
                draggable False
                focus_mask True # 只有非透明区域可交互
                image "piece-{}.png".format(i) alpha 0.05

init python:

    def setup_puzzle():
        for i in range(PIECES_TOTAL):
            PIECES_OUTSET.append((renpy.random.randint(278, 278+194), renpy.random.randint(242, 242+268)))
        for i in range(PIECES_TOTAL):
            PIECES_ROTATION.append(renpy.random.randint(0, 3) if ROTATE_FUN else 0)

    def piece_drop(dropped_on, dragged_piece_list): # dropped_on 表示目标位置碎片
        global FINISHED_PIECES
        dragged_piece = dragged_piece_list[0] # 获取拖动的拼图
        piece_number = int(dragged_piece.drag_name.split("_")[1])
        piece_rotation = PIECES_ROTATION[piece_number] % 4 # 计算拼图的当前旋转次数

        is_in_right_place = False # 是否在正确位置
        if ROTATE_FUN:
            is_in_right_place = dragged_piece.drag_name == dropped_on.drag_name and piece_rotation == 0
        else:
            is_in_right_place = dragged_piece.drag_name == dropped_on.drag_name

        if is_in_right_place:
            if ROTATE_FUN:
                dragged_piece.x = dropped_on.x
                dragged_piece.y = dropped_on.y
            else:
                dragged_piece.snap(dropped_on.x, dropped_on.y, 0.5)
            print("dragged_piece.x:{}, dragged_piece.y:{}, dropped_on.x:{}, dropped_on.y:{}".format(dragged_piece.x, dragged_piece.y, dropped_on.x, dropped_on.y))
            dragged_piece.draggable = False
            dragged_piece.clicked = None
            FINISHED_PIECES += 1

            if FINISHED_PIECES == PIECES_TOTAL:
                renpy.jump("puzzle_game_finished")

    def rotate_piece(piece_index):
        if not ROTATE_FUN:
            return
        global PIECES_ROTATION
        PIECES_ROTATION[piece_index] = (PIECES_ROTATION[piece_index] + 1) % 4  # 增加旋转次数，模 4 循环
        renpy.restart_interaction()  # 刷新界面以更新旋转角度
        print("After rotate {}: pos ({}), angle {}".format(piece_index, PIECES_OUTSET[piece_index], PIECES_ROTATION[piece_index] * 90))
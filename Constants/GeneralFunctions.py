from Constants import Constants


def out_of_range(x: int, y: int) -> bool:
    if x < 0 or x > Constants.WINDOW_WIDTH or y < 0 \
            or y > Constants.WINDOW_HEIGHT:
        return True
    else:
        return False

from time import sleep
import eyes
import images as img
import macro_writer
import pywinauto

debug = False
display = False
threshold = 0.8
eyes.set_debug(debug)
eyes.set_display(display)
eyes.set_threshold(threshold)
actions = 0
start_time = 0
crystal_time = 0
crystal_limit = 15 * 60

app = pywinauto.application.Application().connect(best_match='BlueStacks')

# def create_input_command(command="tap", *args):
#     return ["adb", "shell", "input", "mouse", command, *(str(a) for a in args)]


def combine_stones(stone1, stone2, offset=0):
    # subprocess.run(create_input_command(
    #     "swipe", stone1[0], offset + stone1[1], stone2[0], offset + stone2[1], randint(1000, 2000)))
    
    macro_writer.write_macro(
        "swipe", stone1[0], offset + stone1[1], stone2[0], offset + stone2[1], 50)
    
def start_macro():
    app.top_window().send_keystrokes("{VK_PAUSE}")


def click(pos, offset=0):
    # subprocess.run(create_input_command("tap", pos[0], offset + pos[1]))
    return

import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    screenshot_full, offset_full = img.screenshot()

    match_points = eyes.match_name("safe_rgba", screenshot_full, threshold)
    second_row_y = -1

    if len(match_points) > 0:
        second_row_y = match_points[0][1] - 60

    while (True):
        print("I am wake")
        screenshot_full, offset_full = img.screenshot()
        screenshot_half, offset_half = img.screenshot(second_row_y, 300)
        for name in img.singles:
            match_points = eyes.match_name(name, screenshot_full, threshold)
            if len(match_points) > 0:
                for pos in match_points:
                    if pos[1] < second_row_y - 60:
                        click(match_points[0])

        matched_stone = False
        for name in img.stones:
            match_points = eyes.match_name(name, screenshot_half, threshold)
            if len(match_points) >= 2:
                while len(match_points) > 1:
                    combine_stones(match_points[0], match_points[1], offset_half)
                    match_points.pop(0)
                    match_points.pop(0)
                    matched_stone = True
        
        if (matched_stone):
            sleep_amt = macro_writer.dump_objs()
            start_macro()
            sleep((sleep_amt / 1000))
        else:
            sleep(1)

else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

import sys
import io
import time
import os
import pickle
import curses
from visconAnimations import plotpolygonalcurve
from visconAnimations import animation_3d

# Program uses curses to find terminal size, which improves
# pretty-printing; if curses is not available, simply comment
# out 'import curses', the defintion of get_size, the call
# to curses.wrapper after "if __name__ is '__main__':", and
# manually adjust lines and cols so that they correspond to
# the number of rows and columns of the terminal.

lines = 0
cols = 0


def get_size(stdscr):
    global lines
    global cols
    lines, cols = (curses.LINES, curses.COLS)


def pprint(text, indent, length):
    text = text.split(' ')
    line = indent * " "
    result = ""
    for word in text:
        newline = 1 if "\n" in word else 0
        word = word.strip("\n")
        if len(line) + len(word) + 1 <= length:
            line += word
            line += " "
            if newline == 1:
                line += "\n"
                result += line
                line = indent * " "
        else:
            line += "\n"
            result += line
            line = indent * " "
            if len(line) + len(word) + 1 > length:
                return result
            else:
                line += word
                line += " "
                if newline == 1:
                    line += "\n"
                    result += line
                    line = indent * " "
    result += line
    print(result)


def std_pp(text):
    pprint(text, 2, cols-4)


def indent_pp(text):
    pprint(text, 4, cols-8)


def cent_pp(text):
    if len(text) > cols:
        print(text)
    else:
        text = (int((cols-len(text))/2) * " ") + text
        print(text)


def title(text):
    global cols
    if len(text) + 4 > cols:
        print(text)
    else:
        result_text = "  \033[7m"
        result_text += int((cols - 4 - len(text))/2) * " "
        result_text += text
        result_text += (cols - 2 - len(result_text)) * " "        
        result_text += "  \033[27m"
        print(result_text)


start = []
start_fmt = []
sols = []
sols_fmt = []
target = []
target_fmt = []
tracker_runs = 0
tracker_data = []
visual_opts = []
visited = {i: 0 for i in range(8)}
total_vis = 0
tracker_data = []

sol_num = 0
gamma = 0
min_step = 0
max_step = 0
num_steps = 0

current_screen = 0
next_screen = 0


def Intro():
    std_pp("")
    title("Visualization")
    std_pp("")
    text = "Load tracker data from tracker_data.dat?"
    std_pp(text)
    std_pp("")
    user_choice = input("\033[35;1mLoad data? [Y/n] \033[0m")
    global next_screen
    if user_choice != "n" and user_choice != "N":
        global tracker_data
        tracker_data = pickle.load(open("tracker_data.dat", "rb"))
        next_screen = 1
    else:
        next_screen = -1


def Visualize():
    std_pp("")
    title("Success")
    std_pp("")
    text = "Which kind of plot or animation would you like to create?"
    std_pp(text)
    std_pp("")
    std_pp("(1) Plot of all solution curves (superimposed)")
    std_pp("(2) 3D animation of path tracking")
    user_choice = input("\033[35;1mChoose a number: [1/2/3] \033[0m")
    global next_screen
    if user_choice == 2:
        vis_path = os.getcwd()
        vis_path += "/tracker_run_{}".format(tracker_runs)
        vis_path += "/vis_{}".format(total_vis) 
        plotpolygonalcurve(tracker_data[tracker_runs-1][2][0], "Real part",
                           "Imaginary part", vis_path)
        next_screen = 9
        return
    else:
        solution_curves = [tracker_data[i][2][0] for i in range(len(tracker_data))]
        print(solution_curves)
        plotpolygonalcurve(solution_curves, "Real part", "Imaginary part",
                           "allcurves")
        next_screen = -1
        return

def PlotCurves():
    std_pp("")
    title("Plot solution curve")
    std_pp("")
    text = "Solution curve has been plotted! Would you like to create more " \
           "visualizations?"
    std_pp(text)
    std_pp("")
    user_choice = input("\033[35;1mMore visualizations? [y/N] \033[0m")
    global next_screen
    if user_choice != 'n' and user_choice != 'N':
        next_screen = 8
        return
    else:
        next_screen = 11
        return


def Anim3D():
   global next_screen
   next_screen = -1


def MoreVis():
    std_pp("")
    title("Track more solutions")
    std_pp("")
    text = "Would you like to run the path tracker again?"
    std_pp(text)
    std("")
    input("")
    global next_screen
    next_screen = -1


screens = {0: Intro, 1: Visualize, 2: PlotCurves, 3: Anim3D}

if __name__ == '__main__':
    sys.stdout.write("\x1b[2J\x1b[H")
    curses.wrapper(get_size)
    while 0 <= current_screen:
        screens[current_screen]()
        visited[current_screen] = 1
        current_screen = next_screen
    sys.stdout.write("\x1b[2J\x1b[H")

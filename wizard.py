import sys
import io
import time
import os
import curses
from phcutils import wiz_sols_to_phc_sols
from phcutils import run_tracker

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

sol_num = 0
gamma = 0
min_step = 0
max_step = 0
num_steps = 0

current_screen = 0
next_screen = 0


def Intro():
    std_pp("")
    title("Welcome!")
    std_pp("")
    text = "This program is an interface to phcpy, a Python " \
           "front-end to the PHCpack software package. PHCpack " \
           "solves systems of polynomial equations using homotopy " \
           "continuation methods. Given a system of polynomial " \
           "equations with known solutions, PHCpack \"deforms\" " \
           "the system little-by-little into a target system of " \
           "polynomial equations whose solutions are not known, " \
           "tracking the solutions of the original system to " \
           "solutions of the target system along the way. The " \
           "wizard will guide you through the process of solving " \
           "a system of equations using PHCpack's path tracker " \
           "and visualizing the data the tracker produces.\n"
    std_pp(text)
    user_choice = input("\033[35;1mContinue? [Y/n] \033[0m")
    global next_screen
    if user_choice != "n" and user_choice != "N":
        next_screen = 1
    else:
        next_screen = -1


def StartSys():
    std_pp("")
    title("Start system")
    std_pp("")
    text = "Please enter the polynomials of the start system in standard " \
           "form (i.e. with all nonzero terms on the left hand side). " \
           "For example, if your start system is"
    std_pp(text)
    text = "(-1+1*i) + (0-1*i)*x + (-1-1*i)*y + x*y = 0\n " \
           "(1+1*i)*x = (-1+0*i)*x*y"
    indent_pp(text)
    text = "then"
    std_pp(text)
    text = "(-1+1*i) + (0-1*i)*x + (-1-1*i)*y + x*y"
    indent_pp(text)
    text = "and"
    std_pp(text)
    text = "(1+1*i)*x + (1+0*i)*x*y"
    indent_pp(text)
    text = "are the polynomials which should be entered.\n"
    std_pp(text)
    global next_screen
    global start
    global start_fmt
    user_choice = "a"
    if visited[current_screen] == 1:
        std_pp("Start system:")
        for polynomial in start_fmt:
            std_pp("\033[36m   " + polynomial + " = 0\033[0m")
        std_pp("")
        user_choice = input("\033[35;1mAdd/Remove/Continue/Back/Quit: "
                            "[a/r/C/b/q] \033[0m")
    while True:
        if user_choice == "a":
            poly = input("Please enter a polynomial:\n> ")
            start_fmt.append(poly)
            start.append(poly + ";")
        elif user_choice == "r":
            start_fmt = start_fmt[:-1]
            start = start[:-1]
        elif user_choice == "b":
            next_screen = 0
            return
        elif user_choice == "q":
            next_screen = -1
            return
        else:
            next_screen = 2
            return
        std_pp("")
        std_pp("Start system:")
        for polynomial in start_fmt:
            indent_pp("\033[36m" + polynomial + " = 0\033[0m")
        std_pp("")
        user_choice = input("\033[35;1mAdd/Remove/Continue/Back/Quit: "
                            "[a/r/C/b/q] \033[0m")


def Sols():
    std_pp("")
    title("Solutions")
    std_pp("")
    text = "Please enter solutions to the start system. For example, if the " \
           "start system was"
    std_pp(text)
    text = "(-1+1*i) + (0-1*i)*x + (-1-1*i)*y + x*y = 0\n " \
           "(1+1*i)*x + (1+0*i)*x*y = 0"
    indent_pp(text)
    text = "then"
    std_pp(text)
    text = "x:1+1*i;y:-1-1*i"
    indent_pp(text)
    text = "and"
    std_pp(text)
    text = "x:0;y:0+1*i"
    indent_pp(text)
    text = "are what should be entered.\n"
    std_pp(text)
    global next_screen
    global sols
    global sols_fmt
    user_choice = "a"
    if visited[current_screen] == 1:
        std_pp("Solutions:")
        for sol in sols_fmt:
            std_pp("\033[36m   " + sol + " = 0\033[0m")
        std_pp("")
        user_choice = input("\033[35;1mAdd/Remove/Continue/Back/Quit: "
                            "[a/r/C/b/q] \033[0m")
    while True:
        if user_choice == "a":
            sol = input("Please enter a solution:\n> ")
            sols_fmt.append(sol)
            sol = sol.replace("i", "j")
            sol = sol.replace("*", "")
            sol = sol.split(";")
            sol = [item.split(":") for item in sol]
            sol = [[item[0] for item in sol], [item[1] for item in sol]]
            sols.append(sol)
        elif user_choice == "r":
            sols_fmt = sols_fmt[:-1]
            sols = sols[:-1]
        elif user_choice == "b":
            next_screen = 1
            return
        elif user_choice == "q":
            next_screen = -1
            return
        else:
            next_screen = 3
            return
        std_pp("")
        std_pp("Solutions:")
        for sol in sols_fmt:
            indent_pp("\033[36m" + sol + "\033[0m")
        std_pp("")
        user_choice = input("\033[35;1mAdd/Remove/Continue/Back/Quit: "
                            "[a/r/C/b/q] \033[0m")


def TargetSys():
    std_pp("")
    title("Target system")
    std_pp("")
    text = "Please enter the polynomials of the target system in " \
           "standard form. For example, if your target system is"
    std_pp(text)
    text = "(-2+6*i) + (-1-2*i)*x + (-2-2*i)*y + x*y = 0\n " \
           "(-1+3*i) + (2-1*i)*x + (-1+1*i)*y = (-1+0*i)*x*y"
    indent_pp(text)
    text = "then"
    std_pp(text)
    text = "(-2+6*i) + (-1-2*i)*x + (-2-2*i)*y + x*y"
    indent_pp(text)
    text = "and"
    std_pp(text)
    text = "(-1+3*i) + (2-1*i)*x + (-1+1*i)*y + (1+0*i)*x*y"
    indent_pp(text)
    text = "are the polynomials which should be entered.\n"
    std_pp(text)
    global next_screen
    global target
    global target_fmt
    user_choice = "a"
    if visited[current_screen] == 1:
        std_pp("Target system:")
        for polynomial in target_fmt:
            std_pp("\033[36m   " + polynomial + " = 0\033[0m")
            std_pp("")
            user_choice = input("\033[35;1mAdd/Remove/Continue/Back/Quit: "
                                "[a/r/C/b/q] \033[0m")
    while True:
        if user_choice == "a":
            poly = input("Please enter a polynomial:\n> ")
            target_fmt.append(poly)
            target.append(poly + ";")
        elif user_choice == "r":
            target_fmt = target_fmt[:-1]
            target = target[:-1]
        elif user_choice == "b":
            next_screen = 2
            return
        elif user_choice == "q":
            next_screen = -1
            return
        else:
            next_screen = 4
            return
        std_pp("")
        std_pp("Target system:")
        for polynomial in target_fmt:
            indent_pp("\033[36m" + polynomial + " = 0\033[0m")
        std_pp("")
        user_choice = input("\033[35;1mAdd/Remove/Continue/Back/Quit: "
                            "[a/r/C/b/q] \033[0m")


def Summary():
    std_pp("")
    title("Summary")
    std_pp("")
    std_pp("Start system:")
    for polynomial in start_fmt:
        indent_pp("\033[36m" + polynomial + " = 0\033[0m")
    std_pp("Solutions:")
    for sol in sols_fmt:
        indent_pp("\033[36m" + sol + "\033[0m")
    std_pp("Target system:")
    for polynomial in target_fmt:
        indent_pp("\033[36m" + polynomial + " = 0\033[0m")
    global next_screen
    std_pp("")
    user_choice = input("\033[35;1mContinue/Back/Quit: [C/b/q] \033[0m")
    if user_choice == "b":
        next_screen = 3
        return
    elif user_choice == "q":
        next_screen = -1
        return
    else:
        next_screen = 5
        return


def TrackerSettings():
    global sols
    global sol_num
    global gamma
    global min_step
    global max_step
    global num_steps
    sols = wiz_sols_to_phc_sols(sols)
    std_pp("")
    title("Tracker settings")
    std_pp("")
    text = "Which solution of the start system would you like to track? " \
           "(If unsure, press Enter and solution \033[36m{}\033[0m will " \
           "be tracked.".format(tracker_runs + 1)
    std_pp(text)
    sol_num = input("> ")
    sol_num = tracker_runs + 1 if sol_num == "" else int(sol_num)
    text = "What value would you like to use for gamma? (If unsure, press " \
           "Enter and the default value of \033[36m1\033[0m will be used.)"
    std_pp(text)
    gamma = input("> ")
    gamma = 1+0j if gamma == "" else complex(gamma)
    text = "What is the minimum step size you would like to use? (If " \
           "unsure, press Enter and the default value of " \
           "\033[36m0.001\033[0m will be used.)"
    std_pp(text)
    min_step = input("> ")
    min_step = 0.001 if min_step == "" else float(min_step)
    text = "What is the maximum step size you would like to use? (If " \
           "unsure, press Enter and the default value of " \
           "\033[36m0.1\033[0m will be used.)"
    std_pp(text)
    max_step = input("> ")
    max_step = 0.1 if max_step == "" else float(max_step)
    text = "How many steps would you like the path tracker to take? (If " \
           "unsure, press Enter and the default value of " \
           "\033[36m1000\033[0m will be used.)"
    std_pp(text)
    num_steps = input("> ")
    num_steps = 1000 if num_steps == "" else int(num_steps)
    global next_screen
    next_screen = 6


def StartTrack():
    std_pp("")
    title("Start tracker")
    std_pp("")
    user_choice = input("\033[35;1mRun the path tracker? "
                        "[Y/n] \033[0m")
    global next_screen
    if user_choice != "n" and user_choice != "N":
        next_screen = 7
        global tracker_data
        original_out = (os.dup(1), os.dup(2))
        os.dup2(os.open(os.devnull, os.O_RDWR), 1)
        os.dup2(os.open(os.devnull, os.O_RDWR), 2)
        tracker_data.append(run_tracker(start, sols, target, sol_num,
                                        gamma, min_step, max_step, num_steps))
        os.dup2(original_out[0], 1)
        os.dup2(original_out[1], 2)
        os.close(original_out[0])
        os.close(original_out[1])
        global tracker_runs
        tracker_runs += 1
    else:
        next_screen = 5


def TrackingComplete():
    std_pp("")
    title("Success")
    std_pp("")
    text = "Tracking is complete. Would you like to create graphs " \
           "or animations from the data which the path tracker " \
           "produced?"
    std_pp(text)
    std_pp("")
    user_choice = input("\033[35;1mVisualize the data? "
                        "[Y/n] \033[0m")
    global next_screen
    if user_choice != "n" and user_choice != "N":
        next_screen = 8
    else:
        next_screen = -1


def Visualize():
    std_pp("")
    title("Visualize data")
    std_pp("")
    text = "Which kind of plot or animation would you like to create?"
    std_pp(text)
    std_pp("")
    std_pp("(1) Plot of solution curve")
    std_pp("(2) 3D animation of path tracking")
    std_pp("")
    user_choice = input("\033[35;1mChoose a number: [1/2] \033[0m")
    global next_screen
    if user_choice == 1:
        next_screen = 9
        return
    else:
        next_screen = 10
        return

def PlotCurve():
    std_pp("")
    title("Plot solution curve")
    std_pp("")
    text = "Solution curve has been plotted! Would you like to create more " \
           "visualizations?"
    std_pp("")
    user_choice = input("\033[35;1mMore visualizations? [y/N] \033[0m")
    global next_screen
    if user_choice != 'n' and user_choice != 'N':
        next_screen = 8
        return
    else:
        next_screen = 11
        return


screens = {0: Intro, 1: StartSys, 2: Sols, 3: TargetSys, 4: Summary,
           5: TrackerSettings, 6: StartTrack, 7: TrackingComplete,
           8: Visualize, 9: PlotCurve, 10: 3DAnim, 11: MoreVis}
# 7: Farewell}

if __name__ == '__main__':
    sys.stdout.write("\x1b[2J\x1b[H")
    curses.wrapper(get_size)
    while 0 <= current_screen:
        screens[current_screen]()
        visited[current_screen] = 1
        current_screen = next_screen
    sys.stdout.write("\x1b[2J\x1b[H")

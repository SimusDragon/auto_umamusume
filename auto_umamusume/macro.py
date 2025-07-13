import pyautogui
import view
import time
import json

from resolution import Screen
screen = Screen()

with open("events.json", "r", encoding="utf-8") as f:
    events = json.load(f)

claw_waits = (1.67, 0.82, 0.47)

race_steps = [
    ((700, 920), 1),    #Enter
    ((700, 920), 1),
    ((700, 780), 1),
    ((650, 1000), 10),  #Quick race
    ((650, 1000), 20),  #Loading
    ((820, 1040), 0.5), #Skip
    ((820, 1040), 0.5),
    ((820, 1040), 5),
    ((820, 1040), 0.5),
    ((900, 1040), 5),
    ((550, 1000), 5),   #Next
    ((680, 1000), 5),
    ((550, 950), 10),   #Goal list
    ((550, 950), 5)]

support_slots = [0, 0, 0, 0, 0]
limit_stat = 1050 #Soft cap
total_stats = 5

def debugger(text):
    if False: print(text)

def move_mouse(x, y, times=1):
    pyautogui.moveTo(x, y)
    pyautogui.click(clicks=times, interval=0.1)

def run_macro(stop_macro, pause_macro):
    prev_training = 0
    prev_race = 0
    turn = 0

    onRace = None
    onGoal = None

    onEvent = None
    options = None

    #Skip dialogue
    #skip_position = screen.scale_point(570, 1050)
    #move_mouse(*skip_position, 2)

    while not stop_macro.is_set():
        #Events
        if not onEvent and pause_macro.is_set():
            debugger("Event")
            time.sleep(0.2)
            onEvent = view.get_event()

        if onEvent and pause_macro.is_set():
            #Fan Goals
            if "Goal" in onEvent:
                time.sleep(15)

                for i in range(2):
                    move_mouse((550, 950))
                    time.sleep(5)

                onEvent = None
                continue
            
            if onEvent == "Inspiration":
                debugger("Inspiration")
                time.sleep(10)

                inspiration_position = screen.scale_point(545, 885)
                move_mouse(*inspiration_position)

                onEvent = None
                time.sleep(15) #Loading
                continue
            if onEvent == "ClawMachine!":
                debugger("Claw Machine")
                time.sleep(15)

                for i in claw_waits:
                    pyautogui.mouseDown()
                    time.sleep(i)
                    pyautogui.mouseUp()
                    time.sleep(20)

                end_claw_position = screen.scale_point(550, 1000)
                move_mouse(*end_claw_position)

                onEvent = None
                time.sleep(15)
                continue

            try:
                debugger(onEvent)
                options = events[onEvent]
            except KeyError:
                onEvent = None
                debugger("No Event")

            if options:
                time.sleep(5)

                best_option = None
                best_score = float('-inf')

                for idx, option in enumerate(options):
                    score = score_event(option, energy, mood, stats)

                    if score > best_score:
                        best_score = score
                        best_option = idx

                debugger(f"Option: {best_option}")
                if best_option is not None:
                    total_options = len(options)

                    event_offset = screen.scale_offset_y(110 * (total_options - 1 - best_option))
                    event_position = screen.scale_point(292, 756 - event_offset)

                    move_mouse(*event_position)

                onEvent = None
                options = None
    
                time.sleep(5)
                continue

        if not stop_macro.is_set() and not pause_macro.is_set():
            #Race
            if view.get_race() or (not view.get_goal() and prev_race < 2 and turn > 11):
                debugger("Race")
                onGoal = view.get_race()
                onRace = True

                if onGoal and turn > 15:
                    skill_position = screen.scale_point(425, 920)
                    move_mouse(*skill_position)

                    time.sleep(1)
                    get_skills(stop_macro, pause_macro)

                #Skip race
                quick_race = None
                for idx, (pos, wait_time) in enumerate(race_steps):
                    if stop_macro.is_set() or (idx < 12 and pause_macro.is_set()):
                        break

                    #Skip steps
                    if quick_race and idx in {4, 5, 6, 7, 8}:
                        continue

                    #Goal list
                    if not onGoal and idx == 12:
                        break

                    debugger(f"Step: {idx}, Wait: {wait_time}")
                    time.sleep(wait_time)

                    #Quick race
                    if idx == 3:
                        quick_race = view.get_quick_race()

                        if quick_race:
                            debugger("Quick Race")
                            move_mouse(*screen.scale_point(450, 1000))
                            continue

                    move_mouse(*screen.scale_point(pos[0], pos[1]))
                prev_race += 1
                onRace = False

                time.sleep(5)
            elif not onRace:
                if view.get_infirmary():
                    infirmary_position = screen.scale_point(400, 950)
                    move_mouse(*infirmary_position)

                    prev_race = 0
                    time.sleep(5)
                    continue

                energy = view.get_energy()
                stats = view.get_stats()
                mood = view.get_mood()

                priority = [0, 1, 2, 3, 4] if energy > 75 else [0, 4, 1, 2, 3]

                #Rest
                if energy > 40:
                    if stop_macro.is_set():
                        break

                    if pause_macro.is_set():
                        continue

                    #Mood
                    if mood < 2 and energy < 80 and not view.get_summer():
                        debugger(f"Mood: {mood}")
                        recreation_position = screen.scale_point(550, 950)
                        move_mouse(*recreation_position)

                        prev_training = 0   #Recreation resets training position
                        prev_race = 0

                        time.sleep(5)
                        continue

                    #Train
                    train_position = screen.scale_point(550, 840)
                    move_mouse(*train_position)

                    #Affinity
                    if turn < 15:
                        total_supports = view.get_supports()
                        support_slots[prev_training] = total_supports

                        for i in range(total_stats):
                            if stop_macro.is_set() or pause_macro.is_set():
                                break
                      
                            if i == prev_training:
                                continue
                            time.sleep(0.5)

                            offset_x = screen.scale_offset_x(105 * i)
                            x, y = screen.scale_point(340, 870)

                            train_position = (x + offset_x, y)
                            move_mouse(*train_position)

                            total_supports = view.get_supports()
                            support_slots[i] = total_supports
                        max_slot = max(support_slots)
                        debugger(f"Supports: {max_slot}")  
                    for i in priority:
                        if stop_macro.is_set() or pause_macro.is_set():
                            break

                        if turn < 15 and not support_slots[i] == max_slot:
                            continue

                        if stats[i] >= limit_stat:
                            continue

                        offset_x = screen.scale_offset_x(105 * i)
                        x, y = screen.scale_point(340, 870)

                        train_position = (x + offset_x, y)
                        move_mouse(*train_position, 2)

                        debugger(f"Train: {i}")
                        prev_training = i
                        prev_race = 0

                        turn += 1
                        break
                else:
                    if stop_macro.is_set() or pause_macro.is_set():
                        continue

                    debugger(f"Rest: {energy}")
                    rest_position = screen.scale_point(350, 840)
                    move_mouse(*rest_position)

                    if view.get_summer():   #Summer resets training position
                        prev_training = 0
                    prev_race = 0
            time.sleep(5)   #Loading

def get_skills(stop_macro, pause_macro):
    config = '-c tessedit_char_whitelist=0123456789 --psm 7'
    skillpt = view.get_skillpt()
    limit_times = 10
    times = 0

    skip = skillpt < 300
    if not skip:
        while skillpt > 140 and times < limit_times:
            if stop_macro.is_set() or pause_macro.is_set():
                break
            times += 1

            moveTo = screen.scale_point(550, 700)
            pyautogui.moveTo(moveTo)
            pyautogui.mouseDown()

            moveTo = screen.scale_point(550, 537)
            pyautogui.moveTo(moveTo, duration=0.5)

            time.sleep(0.5)
            pyautogui.mouseUp()

            cost_region = screen.scale_region(715, 465, 60, 30)
            cost = view.read_screen(cost_region, config)

            if not cost:
                continue

            cost = int(cost)
            if skillpt > cost:
                add_position = screen.scale_point(800, 480)
                move_mouse(*add_position)

                extra_cost = view.read_screen(cost_region, config)
                if extra_cost:
                    cost += int(extra_cost)
                    pyautogui.click()

                skillpt -= cost

    confirm_position = ((555, 915), (670, 1000), (215, 1045), (215, 1045))
    for idx, pos in enumerate(confirm_position):
        if skip and idx != 3:
            continue

        moveTo = screen.scale_point(*pos)
        move_mouse(*moveTo)
        time.sleep(3)

def monitor_pause(stop_macro, pause_macro):
    while not stop_macro.is_set():
        if not pause_macro.is_set() and view.get_dialogue():
            debugger("Dialogue")  
            pause_macro.set()
        elif pause_macro.is_set() and not view.get_dialogue():
            debugger("Resume")
            pause_macro.clear()

        if view.get_lose() or view.get_win():
            debugger("Finish")
            stop_macro.set()

        time.sleep(0.2)
    debugger("Stop")
    pause_macro.clear()

def score_event(option, energy, mood, stats):
    score = 0

    weights = {
        "skill": 10,
        "skillpt": 0.4,
        "random": 1,
        "speed": 1.5,
        "stamina": 1,
        "power": 1,
        "guts": 0.7,
        "wisdom": 1.2
    }

    if "energy" in option:
        if option["energy"] > 0 and energy + option["energy"] <= 100:
            score += option["energy"] * 20
        else:
            score -= abs(option["energy"]) * 40

    if "mood" in option:
        if option["mood"] > 0 and mood + option["mood"] < 2:
            score += option["mood"] * 20
        else:
            score -= abs(option["mood"]) * 40

    if "skill" in option:
        score += option["skill"] * weights["skill"]

    if "skillpt" in option:
        score += option["skillpt"] * weights["skillpt"]

    if "random" in option:
        score += option["random"] * weights["random"]

    stat_names = ["speed", "stamina", "power", "guts", "wisdom"]
    for idx, stat in enumerate(stat_names):
        if stat in option:
            if stats[idx] + option[stat] <= limit_stat:
                score += option[stat] * weights[stat]
            else:
                score -= abs(option[stat]) * weights[stat]

    return score

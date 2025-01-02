from psychopy import visual, core, event, sound # type: ignore
import random
import os
import csv
from enum import Enum

def validate_files():
    required_files = ["mask.png", "440.wav", "659.25.wav"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"Error: Required file '{file}' not found!")
            core.quit()
    print("Files validated successfully")
    
validate_files()

win = visual.Window(size=(800, 600), color=(0, 0, 0), units="pix")

fixation = visual.TextStim(win, text="+", color=(1, 1, 1), height=40) 
start_message = visual.TextStim(win, text="Kliknij START, aby rozpocząć", pos=(0, -100), color=(1, 1, 1), height=30)

target = visual.TextStim(win, text="→", color=(1, 1, 1), pos=(-200, 0), height=40)
mask = visual.ImageStim(win, image="mask.png", pos=(200, 0), size=(100, 100))

win_width, win_height = win.size
target.pos = (-win_width // 4, 0)
mask.pos = (win_width // 4, 0)

stimulus_delay = 0.2  # Time before displaying the stimulus
stimulus_duration = 0.8  # Time to display the stimulus
auditory_cue_delay = 0.1 # Time before playing auditory cue

try:
    auditory_cue_low = sound.Sound("440.wav")
    auditory_cue_high = sound.Sound("659.25.wav")
except Exception as e:
    print(f"Error loading sound files: {e}")
    core.quit()

def play_auditory_que(auditory_cue):
    auditory_cue.seek(0)
    auditory_cue.play()
    core.wait(0.5)
    auditory_cue.stop()

class ErrorType(Enum):
    OK = (1, "Ok.")
    USER_TERMINATED = (2, "Terminated by user.")
    UNKNOWN = (99, "Unknown error occured.")
    
    def __init__(self, code, message):
        self.code = code
        self.message = message
    
    def print(self):
         print(f"Error Code: {self.code}, Message: {self.message}")

def handle_error(error):
    if error == ErrorType.USER_TERMINATED:
        error.print()
        core.quit()
        return
    else:
        error.print()
        return 
    
class Trial:
    def __init__(self, category, trial_num, filename):
        self.category = category
        self.trial_num = trial_num
        self.filename = filename
        self.timer = core.Clock()
    
    def save_to_file(self, data):
        with open(self.filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(data)
    
    def run(self, win):
        fixation.draw()
        start_message.draw()
        win.flip()
        while True:
            keys = event.getKeys()
            if 'space' in keys:
                break
        
        target_direction = random.choice(["R", "L"])
        target.text = self.get_target_text(target_direction)
        
        fixation.draw()
        core.wait(stimulus_delay)
        
        target.draw()
        mask.draw()
        win.flip()
        core.wait(auditory_cue_delay)
        
        self.start_timer()
        if self.category == "A":
            play_auditory_que(auditory_cue_low)
        else:
            play_auditory_que(auditory_cue_high)

        core.wait(stimulus_duration)

        win.flip()
        response_message = visual.TextStim(win, text="Która strona? (← lub →)", color=(1, 1, 1), height=30, pos=(0, 0))
        response_message.draw()
        win.flip()
        
        # Clear event buffer (user could press arrow before)
        event.clearEvents()
        response = None
        while True:
            keys = event.getKeys()
            if 'escape' in keys:
                handle_error(ErrorType.USER_TERMINATED)
            elif 'left' in keys:
                response = "L"
                break
            elif 'right' in keys:
                response = "R"
                break
        reaction_time = self.get_time()
        correct = response == target_direction
        print(f"Odpowiedź: {response}, Poprawna: {target_direction}, Czy poprawna: {correct}")
        
        data = [self.category, self.trial_num, target_direction, response, correct, reaction_time]
        self.save_to_file(data)
    
    def start_timer(self):
        self.timer.reset()
    
    def get_time(self):
        return self.timer.getTime()
    
    def get_target_text(self, target_direction):
        if target_direction == "L":
            return "←"
        return "→"
    
class Block:
    def __init__(self, name, n_trials, filename):
        self.name = name
        self.filename = filename
        self.trials = self.create_trials(n_trials, filename)
        
    
    def create_trials(self, n_trials, filename):
        categories = ['A', 'B']
        trials = [Trial(random.choice(categories), i, filename) for i in range(n_trials)]
        return trials
    
    def run(self, win):
        print(f"Starting block: {self.name}")
        for i, trial in enumerate(self.trials, 1):
            progress_message = visual.TextStim(
            win,
            text=f"Block: {self.name}, Trial: {i}/{len(self.trials)}",
            color=(1, 1, 1),
            height=30,
            pos=(0, 250)  # Position at the top of the screen
            )
            progress_message.draw()
            trial.run(win)
            core.wait(0.5)
    

            
            

def main():
    headers = [ "Category", "Trial", "Target Direction", "Response", "Correct", "Reaction Time"]
    output_file = 'results.csv'
    
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
    
    blocks = [Block('L', 5, output_file), Block('R', 5, output_file)]
    for block in blocks:
        block.run(win)
    
    win.close()
    core.quit()
    
if __name__ == "__main__":
    main()
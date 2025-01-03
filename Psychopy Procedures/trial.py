from errors import ErrorType, handle_error
from psychopy import visual, core, event # type: ignore
import random
import csv

from config import fixation, start_message, target, mask, stimulus_delay, auditory_cue_low, auditory_cue_high, auditory_cue_delay, stimulus_duration

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
    
    def show_instruction(self, win):
        fixation.draw()
        start_message.draw()
        win.flip()
        while True:
            keys = event.getKeys()
            if 'space' in keys:
                break
    
    def show_trial(self, win):
        target_direction = random.choice(["R", "L"])
        target.text = self.get_target_text(target_direction)
        
        fixation.draw()
        core.wait(stimulus_delay)
        
        target.draw()
        mask.draw()
        win.flip()
        
        return target_direction
    
    def play_audio(self, auditory_cue):
        auditory_cue.seek(0)
        auditory_cue.play()
        core.wait(0.5)
        auditory_cue.stop()
    
    def play_auditory_cue(self):
        if self.category == "A":
            self.play_audio(auditory_cue_low)
        else:
            self.play_audio(auditory_cue_high)

    def collect_response(self, win, target_direction):
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
        return data

    def run(self, win):
        self.show_instruction(win)
        target_direction = self.show_trial(win)
        
        core.wait(auditory_cue_delay)
        self.start_timer()

        self.play_auditory_cue()

        core.wait(stimulus_duration)
        win.flip()
        
        data = self.collect_response(win, target_direction)
        self.save_to_file(data)
    
    def start_timer(self):
        self.timer.reset()
    
    def get_time(self):
        return self.timer.getTime()
    
    def get_target_text(self, target_direction):
        if target_direction == "L":
            return "←"
        return "→"
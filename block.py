from psychopy import visual, core
import random

from trial import Trial


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
    
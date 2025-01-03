from psychopy import visual, core, event, sound
import os

win_size = (800, 600)
win_color = (0, 0, 0)
text_color = (1, 1, 1)
target_height = 40
mask_size = (100, 100)
stimulus_delay = 0.2
stimulus_duration = 0.8
auditory_cue_delay = 0.1

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

headers = [ "Category", "Trial", "Target Direction", "Response", "Correct", "Reaction Time"]
output_file = 'results.csv'
required_files = ["mask.png", "440.wav", "659.25.wav"]

def validate_files():
    for file in required_files:
        if not os.path.exists(file):
            print(f"Error: Required file '{file}' not found!")
            core.quit()
    print("Files validated successfully")


validate_files()

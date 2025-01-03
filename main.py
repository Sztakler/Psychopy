from psychopy import core
import csv

from config import win, output_file, headers
from block import Block

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(headers)

blocks = [Block('L', 5, output_file), Block('R', 5, output_file)]
for block in blocks:
    block.run(win)

win.close()
core.quit()

import sys
import time

def loading_animation():
    underscores = '-' * 50  # Number of underscores to display
    delay = 0.1  # Delay between each frame
    
    while True:
        for i in range(len(underscores)):
            sys.stdout.write('\r' + 'Loading ' + underscores[:i] + ' ')
            sys.stdout.flush()
            time.sleep(delay)

loading_animation()

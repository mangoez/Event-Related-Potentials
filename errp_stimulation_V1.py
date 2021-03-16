import pygame
from datetime import datetime
from random import seed
from random import randint
import serial


def main():
    pygame.init()

    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # win = pygame.display.set_mode((1620, 800))

    pygame.display.set_caption("ErrP Experimental paradigm")

    BLACK = (0, 0, 0)
    x = (randint(0, 19)*41)+380
    x_orig = x
    y = 480
    width = 80
    height = 80
    vel = 100
    screen_size = 1680
    right_side_box = (randint(0, 1) > 0)
    steps = randint(1, 3)
    run = True

    error_y = []
    # trial_start = []
    # feedback_start = []
    key_pressed = False

    for trials in range(75): # How many trials?
        while run:
            pygame.time.delay(50) # Refresh rate of game
            randomiser = (randint(1, 10) > 8) # 80% it will be correct

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]: # Pressed the left key
                if ((right_side_box) and (x >= (vel + width))):
                    x -= vel
                    error_y.append(2)
                elif (randomiser and (x < (screen_size - width - vel))):
                    x += vel
                    error_y.append(1)
                elif (not randomiser and (x >= (vel + width))):
                    x -= vel
                    error_y.append(0)
                elif (randomiser and (x >= (screen_size - width - vel))):
                    x -= vel
                    error_y.append(0)

                pygame.time.delay(200) # Wait for a bit
                key_pressed = True # We pressed a key



            if keys[pygame.K_RIGHT]: # Pressed right key
                if ((not right_side_box) and (x < (screen_size - width - vel))):
                    x += vel
                    error_y.append(2)
                elif (randomiser and (x >= (vel + width))):
                    x -= vel
                    error_y.append(1)
                elif (not randomiser and (x < (screen_size - width - vel))):
                    x += vel
                    error_y.append(0)
                elif (randomiser and (x < (vel + width))):
                    x += vel
                    error_y.append(0)


                pygame.time.delay(200) # Wait for a bit
                key_pressed = True # We pressed a key



            win.fill((0, 0, 0))
            pygame.draw.rect(win, (0, 100, 0), (x, y, width, height))

            if (right_side_box and (x != (x_orig+(vel*steps)))):
                pygame.draw.rect(win, (255, 0, 0), (x_orig+(vel*steps), y, width, height))
            elif ((not right_side_box) and (x != (x_orig-(vel*steps)))):
                pygame.draw.rect(win, (0, 0, 255), (x_orig-(vel*steps), y, width, height))
            elif (((x == (x_orig+(vel*steps))) and (right_side_box)) or ((x == (x_orig-(vel*steps))) and (not right_side_box))):
                run = False


            pygame.display.update() # Display rectangles


            if key_pressed: # Only record the time if we pressed a key
                arduino.write(b'1')
                # feedback_start.append(datetime.now()) # Record time
                key_pressed = False
                # pygame.time.delay(1000) # Wait for a bit
                #
                # win.fill(BLACK)
                # pygame.display.flip()
                pygame.time.delay(1000 + randint(1, 1000)) # Wait for a bit


        pygame.time.delay(1000 + randint(1, 500))
        x = (randint(0, 19)*41)+380
        x_orig = x
        right_side_box = (randint(0, 1) > 0)
        steps = randint(1, 3)
        run = True


    # feedback_start_s = [feedback_start[0]]
    # for i in range(1, len(feedback_start)):
    #     feedback_start_s.append(round((feedback_start[i]-feedback_start[0]).total_seconds() * 125))
    #
    # print(error_y, feedback_start_s, feedback_start)
    print(error_y)

if __name__ == '__main__':
    arduino = serial.Serial(port='/dev/tty.usbmodem14201', baudrate=115200, timeout=.1)
    print("Connection establised")

    main()
    pygame.quit()

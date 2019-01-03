# motor.py
import pigpio

gpio = pigpio.pi()
if not gpio.connected:
    quit = 1         # set quit flag so main loop exits immediately

MOTOR1A  = 6        # pin 31
MOTOR1B  = 13       # pin 33
MOTOR2A  = 19       # pin 35
MOTOR2B  = 26       # pin 37
MOTOR1EN = 20       # pin 38
MOTOR2EN = 21       # pin 40

gpio.set_mode(MOTOR1A,  pigpio.OUTPUT)
gpio.set_mode(MOTOR1B,  pigpio.OUTPUT)
gpio.set_mode(MOTOR2A,  pigpio.OUTPUT)
gpio.set_mode(MOTOR2B,  pigpio.OUTPUT)
gpio.set_mode(MOTOR1EN, pigpio.OUTPUT)
gpio.set_mode(MOTOR2EN, pigpio.OUTPUT)

def drive(speed1, speed2):
  # drive motors 1 and 2 at speed1 and speed2

  # map ranges of speed1 and speed2 onto acceptable PWM ranges. PWM can
  # range from 0 to 255. 255 is full ahead, 0 is stop. TODO need to handle
  # negative speeds as well
  # minimum duty cycle to get both motors moving seems to be somewhere
  # between 60 and 90
  gpio.write(MOTOR1A, 1)    # TODO program hangs here after Ctrl-C
  gpio.write(MOTOR1B, 0)

  gpio.write(MOTOR2A, 0)
  gpio.write(MOTOR2B, 1)

  if speed1 == 0:
    gpio.write(MOTOR1EN, 0)
  else:
    gpio.set_PWM_dutycycle(MOTOR1EN, abs(speed1))
    
  if speed2 == 0:
    gpio.write(MOTOR2EN, 0)
  else:
    gpio.set_PWM_dutycycle(MOTOR2EN, abs(speed2))

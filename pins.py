import gpiozero
import time
import logging


# NOTE: These values are hard-coded.

button = gpiozero.Button(2)
led_green = gpiozero.LED(21)
led_red = gpiozero.LED(3)
relay = gpiozero.LED(13)


def turn_green_led(interval):
    """ Turns green led on. """
    logging.debug(f'Green led switched ON for #{interval} seconds!')
    led_green.on()
    time.sleep(interval)
    logging.debug('Green led switched OFF!')
    led_green.off()


def turn_red_led(interval):
    """ Turns red led on. """
    logging.debug(f'Red led switched ON for #{interval} seconds!')
    led_red.on()
    time.sleep(interval)
    logging.debug('Red led switched OFF!')
    led_red.off()


def open_the_door(interval):
    """ Opens the door and switches green light. """
    logging.debug(f'Relay switched ON for #{interval} seconds!')
    led_green.on()
    relay.on()
    time.sleep(interval)
    logging.debug('Relay switched OFF!')
    led_green.off()
    relay.off()


def register_button(button_file):
    """ Registers callbacks for button actions. """
    def button_pressed():
        logging.info(f'Button was pressed, creating the file: {button_file}')
        open(button_file, 'a').close()

    def button_released():
        logging.info(f'Button was released, removing the file: {button_file}')
        os.remove(button_file)

    button.when_pressed = button_pressed
    button.when_released = button_released
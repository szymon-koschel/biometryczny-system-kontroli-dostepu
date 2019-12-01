import argparse
import cv2
import face_recognition
import pins
import os
import time
import numpy as np
import logging


class Image:
    """ Represents processed image by face_recognition module. """
    def __init__(self, name, path):
        self.name = name
        self.raw_binary = face_recognition.load_image_file(path)
        self.encoded_binary = face_recognition.face_encodings(self.raw_binary)[0]


class Webcam:
    """ Represents video camera. """
    def __init__(self, video_num):
        self.handle = cv2.VideoCapture(video_num)

    def capture_frame(self):
        """ Returns frame in RGB color scheme or None. """
        ret, frame = self.handle.read()
        if ret:
            # OpenCV uses BGR color scheme, so we need to convert.
            rgb_frame = frame[:, :, ::-1]
            return rgb_frame
        else:
            return None


def scan_picture(rgb_frame):
    """ Locates faces, encodes them, and returns. """
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    return face_encodings


def match_faces(authorized_images, face_encodings):
    """ Compares face_encodings with encodings from authorized_images. """
    known_face_encodings = [image.encoded_binary for image in authorized_images]
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        if True in matches:
            return authorized_images[matches.index(True)]
    return None  # No match.


def configure_global_logger():
    """ Configures global logger. """
    logger_format = ('%(asctime)s - %(threadName)s - %(funcName)s '
                     '- %(levelname)s - %(message)s')
    logging.basicConfig(
        format=logger_format,
        level=logging.INFO)


def parse_arguments():
    """ Parses command line arguments. """
    parser = argparse.ArgumentParser()
    parser.add_argument('--button-file', type=str, default='.button')
    parser.add_argument('--video-num', type=int, default=0)
    parser.add_argument('--capture-delay', type=float, default=1.0)
    return parser.parse_args()


def main():
    options = parse_arguments()

    configure_global_logger()

    logging.info('Init webcam.')
    webcam = Webcam(options.video_num)

    button_file = os.path.abspath(options.button_file)
    logging.info(f'Button file: {button_file}')

    logging.info('Register button.')
    pins.register_button(button_file)
        
    # If you would like to add an authorized user,
    # create Image instance and add it to authorized_images list.
    
    logging.info('Read images.')
    authorized = Image(name='Kamil Janiec', path='./images/janiec.jpg')
    authorized_images = [
        authorized
    ]

    while True:
        if os.path.exists(button_file):
            logging.info('Taking a picture.')
            rgb_frame = webcam.capture_frame()

            logging.info('Scanning a picture.')
            face_encodings = scan_picture(rgb_frame)

            logging.info(f'Found #{len(face_encodings)} faces.')

            if face_encodings:
                logging.info('Comparing with database.')
                matched = match_faces(authorized_images, face_encodings)

                if matched:
                    logging.info(f'Match found: {matched.name}')
                    pins.open_the_door(interval=4)
                else:
                    logging.info(f'Unknown user.')
                    turn_red_led(interval=1)
        logging.info('Button is not pressed.')
        time.sleep(options.capture_delay)


if __name__ == '__main__':
    main()
import os
import cv2
import numpy as np
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Path:
    folders: str = 'images'


class Click(object):

    def __init__(self):
        self.image = None
        self.image_hsv = None
        self.positive = []
        self.negative = []

    def _get_coord(self, array: List, x: int, y: int):
        array.append([x, y])

    def _get_color(self, array: List, x: int, y: int):
        h = self.image_hsv[y, x, 0]
        s = self.image_hsv[y, x, 1]
        v = self.image_hsv[y, x, 2]
        array.append([h, s, v])
        cv2.circle(self.image, (x, y), 2, (0, 0, 255), -1)

    def _set_up_click(self, array: List, x: int, y: int, color: Tuple[int, int, int]):
        self._get_coord(array, x, y)
        self._get_color(array, x, y)
        cv2.circle(self.image, (x, y), 3, color, -1)
        cv2.imshow("image", self.image)

    def click_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self._set_up_click(self.positive, x, y, color=(0, 255, 0))

        elif event == cv2.EVENT_RBUTTONDOWN:
            self._set_up_click(self.negative, x, y, color=(0, 0, 255))

    def _write_file(self, name: str, array: List[List]):
        """ Record: x, y, h, s, v"""
        with open(name, 'a') as file:
            for idx in range(0, len(array), 2):
                record = f'{array[idx]}, {array[idx + 1]}'.replace('[', '').replace(']', '')
                print(record)
                file.write(record + '\n')

    def run(self):
        files = os.listdir(Path.folders)
        for file in files:
            self.positive = []
            self.negative = []

            self.image = cv2.imread(f'{Path.folders}/{file}')
            self.image_hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

            cv2.imshow("image", self.image)
            cv2.setMouseCallback("image", self.click_event)

            if cv2.waitKey(0) == ord('q'): break
            cv2.destroyAllWindows()

            self._write_file('positive.txt', self.positive)
            self._write_file('negative.txt', self.negative)


if __name__ == '__main__':
    Click().run()

import cv2
import numpy as np
import matplotlib.pyplot as plt
scale = 1
from psd_tools import PSDImage
import logging
import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
Image.MAXBLOCK = 2**20

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

class ImagePoint(object):
    def __init__(self, largeimg, smallimg):
        try:
            if self.file_extension(largeimg) in self.photoshopfile():
                img = np.array(PSDImage.open(largeimg).composite())
            else:
                img = cv2.imread(largeimg)
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGRA)
            self.largeimgsize = img.shape[:2]
            self.smallimgname = smallimg
            template = cv2.imread(smallimg)
            template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
            template_size = template.shape[:2]
            self.smallimagesize = template_size
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            template_ = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(img_gray, template_, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(result >= threshold)
            point = ()
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img, pt, (pt[0] + template_size[1], pt[1] + + template_size[0]), (7, 249, 151), 2)
                point = pt
            self.img = img
            self.x = int(point[0])
            self.y = int(point[1])
            logger.info(point)
        except IOError as e:
            logger.error(e)

    def getNewSaveFileName(self):
        return os.path.splitext(self.smallimgname)

    def setEnlargePixel(self,pixel):
        self.pixel = pixel

    def enlarge(self):
        try:
            point = self.getPoint()
            xmin = point[0]
            xmax = point[0] + self.smallimagesize[1]
            ymin = point[1]
            ymax = point[1] + self.smallimagesize[0]

            new_box = self.reValue(self.largeimgsize,
                                   self.pixel,
                                   xmin,
                                   xmax,
                                   ymin,
                                   ymax
                                   )
            imageobject = self.getPILImage()
            cropImg = imageobject.crop(new_box)
            cropImg = cropImg.convert('RGB')
            fileprefix = "expand_"

            cropImg.save(fileprefix +
                         self.getNewSaveFileName()[0] +
                         self.getNewSaveFileName()[1],
                         format="jpeg")
        except Exception as e:
            print(e)
            print('enlarge pixel is None,please use setEnlargePixel(pixel) to set the pixels to enlarge')

    def reValue(self, img_size, x_1000_chazhi, txmin, txmax, tymin, tymax):
        txmin_1 = txmin - x_1000_chazhi
        txmax_1 = txmax + x_1000_chazhi
        tymin_1 = tymin - x_1000_chazhi
        tymax_1 = tymax + x_1000_chazhi
        txmin_2 = txmin - x_1000_chazhi
        txmax_2 = txmax + x_1000_chazhi
        tymin_2 = tymin - x_1000_chazhi
        tymax_2 = tymax + x_1000_chazhi
        if txmin - x_1000_chazhi < 0:
            txmax_2 = txmax_1 + abs(txmin_1)
            txmin_2 = 0
        if txmax + x_1000_chazhi > img_size[0]:
            txmin_2 = txmin_1 - abs(txmax_1 - img_size[0])
            txmax_2 = img_size[0]
        if tymin - x_1000_chazhi < 0:
            tymax_2 = tymax_1 + abs(tymin_1)
            tymin_2 = 0
        if tymax + x_1000_chazhi > img_size[1]:
            tymin_2 = tymin_1 - abs(tymax_1 - img_size[1])
            tymax_2 = abs(img_size[1])
        if txmin_2 < 0: txmin_2 = 0
        if txmax_2 > img_size[0]: txmax_2 = img_size[0]
        if tymin_2 < 0: tymin_2 = 0
        if tymax_2 > img_size[1]: tymax_2 = img_size[1]
        new_box = (txmin_2, tymin_2, txmax_2, tymax_2)
        return new_box

    def file_extension(self, path):
        return os.path.splitext(path)[1].lower()

    def photoshopfile(self):
        return ['.psd', '.psb']

    def getPoint(self):
        return self.x, self.y

    def getPILImage(self):
        return Image.fromarray(np.uint8(self.img))

    def show(self):
        plt.figure()
        plt.imshow(self.img, animated=True)
        plt.show()

"""验证码处理模块"""
from random import randint

import numpy as np
from cv2 import cv2

from .file import File


class SliderCaptcha:
    """滑块验证码处理模块"""

    @classmethod
    def get_x(cls, png_file):
        """获取滑块中心点的x轴坐标

        :param png_file: 图片路径
        :return: 滑块中心点的x轴坐标
        """
        # 1. 图片剪切
        cropped_img = cv2.imread(png_file)[622:914, 166:914]  # 裁剪坐标为[y0:y1, x0:x1]
        cv2.imwrite(File(png_file).dirPathAndFName + '_cropped.png', cropped_img)
        # 2. 阴影提取
        shadowImg = np.where(np.sum(cropped_img, axis=2) < 250, np.std(cropped_img), 255)
        shadowPng = File(png_file).dirPathAndFName + '_shadow.png'
        cv2.imwrite(shadowPng, shadowImg.astype(np.uint8))
        # 3. 灰色部分提取
        image = cv2.imread(shadowPng)
        hsvImg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsvImg, lowerb=np.array([0, 0, 46]), upperb=np.array([180, 43, 220]))
        # 4. 图像腐蚀。消除图像边缘小的部分
        # 设置kernel卷积核为 3*3 正方形，8位uchar型，全1结构元素
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # 原型为：dst=cv2.erode(src表示原图像,kernel表示卷积核,iterations表示迭代次数)
        mask = cv2.erode(mask, kernel, 15)
        # 5. 查找轮廓。
        contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        # 6. 轮廓值排序
        lengths = [cv2.arcLength(i, True) for i in contours]
        lengths.sort(reverse=True)
        # 7. 筛选出轮廓最长和次长项
        contours = [i for i in contours if cv2.arcLength(i, True) >= lengths[1]]
        # 8. 输出x
        x = cv2.minAreaRect(contours[randint(0, 1)])[0][0]
        print('8. x is', x)
        return x

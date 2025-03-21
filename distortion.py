from PIL import Image, ImageDraw, ImageFont, ImageTransform
import numpy as np
import random

string = "Jhh8856"
font = "./Noto_Sans/NotoSans-Bold.ttf"
stringsize = 64
size = (480, 160)
random.seed = 0

def noise_dots(im, size, count_w, count_l, count):
        dr = ImageDraw.Draw(im)
        #選兩個圖片邊邊上的點畫線
        while count_w:
            dr.line([(0, random.randint(0, size[1])), (size[0], random.randint(0, size[1]))],
                    fill=(0, 0, 0), width=random.randint(1,3))
            count_w -= 1

        while count_l:
            dr.line([(random.randint(0, size[0]), 0), (random.randint(0, size[0]), size[1])],
                    fill=(0, 0, 0), width=random.randint(1,3))
            count_l -= 1

        #選圖上任一點畫僅一個像素長的線
        while count:
            x, y = random.randint(0, size[0]), random.randint(0, size[1])
            dr.line(((x, y), (x-1, y-1)), fill=(0, 0, 0), width=3)
            count -= 1

        return im
def noise_curve(im, size, count):
        dr = ImageDraw.Draw(im)
        #選擇離圖片邊緣1/3邊長長的長方形作為弧度
        x1 = random.randint(0, int(size[0] / 3))
        x2 = random.randint(int(2*size[0] / 3), size[0])
        y1 = random.randint(int(size[1] / 3), int(2 * size[1] / 3))
        y2 = random.randint(y1, int(2 * size[1] / 3))
        #畫弧線
        while count:
            dr.arc([x1, y1, x2, y2],
                size[0]/20,
                9*size[1]/10,
                fill=(0, 0, 0))
            count -= 1

        return im

def noise_ground(im, size, count):
        dr = ImageDraw.Draw(im)

        while count:
            #選擇兩個焦點
            ex, ey = random.randint(0, int(19*size[0]/20)), random.randint(0, int(19*size[1]/20))
            #隨機選顏色
            r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            #畫橢圓
            dr.ellipse([(ex, ey), (random.randint(ex, size[0]), random.randint(ey, size[1]))],
                   fill=(r, g, b), width=random.randint(5, 10))
            count -= 1

        return im

def draw_text(im, size, txt, font, txtsize):
        a_float = random.randint(0, 30) * -1
        b_float = random.randint(0, 30) * -1
        #字型
        f = ImageFont.truetype(font, txtsize)
        dr = ImageDraw.Draw(im)
        #自動尋找適合大小的文字方塊
        left, top, right, bottom = dr.multiline_textbbox((1, 1), txt, font=f)
        #空出一定的行距
        center = (int(size[0]/2), int(size[1]/2))
        dx = right-center[0]
        dy = bottom-center[1]
        imtsize = (right+dx, bottom+dy)

        imt = Image.new('RGB', imtsize, color=(255, 255, 255))
        #先打底
        noise_ground(imt, imtsize, 15)
        #再寫字
        ImageDraw.Draw(imt).text((dx, dy), txt, font=f, fill=(0, 0, 0))
        #旋轉字體
        imt = imt.crop(imt.getbbox())
        imt = imt.rotate(random.uniform(a_float, b_float), Image.Resampling.BILINEAR, expand=True, fillcolor=(255, 255, 255))

        #找出平行四邊形變換的八個參考點，左上點移動(x1, y1)，左下點移動(-x1, -y1)，右上點移動(x2, y2)，右下點移動(-x2, -y2)
        dx2 = right * random.uniform(0.1, 0.3)
        dy2 = bottom * random.uniform(0.1, 0.3)
        x1 = int(random.uniform(-dx2, dx2))
        y1 = int(random.uniform(-dy2, dy2))
        x2 = int(random.uniform(-dx2, dx2))
        y2 = int(random.uniform(-dy2, dy2))
        w2 = right + abs(x1) + abs(x2)
        h2 = bottom + abs(y1) + abs(y2)

        data = (
            x1, y1,
            -x1, h2 - y2,
            w2 + x2, h2 + y2,
            w2 - x1, -y2,
        )
        imt = imt.resize((w2, h2))
        #將原本的矩形文字映射到另一四邊形
        imt = imt.transform((right, bottom), Image.Transform.QUAD, data=data, fillcolor=(255, 255, 255))
        imt = imt.resize(size)
        #已空出行距，自動向左上方對齊
        im.paste(imt)
        #count = 0
        #while count <= 6:
        #    dr.text(
        #        (random.randint(int(count*size[0]/7), int((count+1)*size[0]/7)),
        #         random.randint(int(4*size[1]/10), int(6*size[1]/10))),
        #        text=txt[count], anchor="mm", fill=(0, 0, 0), font=font)
        #    count+=1
        #string_temp.crop(string_temp.getbbox())
        #string_temp = string_temp.rotate(random.uniform(a_float, b_float), Image.Resampling.BILINEAR, expand=True)
        #im.paste(string_temp)

        return im

def color_invert(im):
        #反補色不傷眼
        imi = im.point(lambda p: 255 - p)
        return imi

def croping(im, size):
        #暫棄
        img_temp1 = im.crop(box=(0, 0, size[0], 6*size[1]/10))
        img_temp1 = img_temp1.rotate(random.choice([-1, 1]) * random.randrange(4, 7), resample=Image.Resampling.BILINEAR,
                                     fillcolor=(255, 255, 255))

        img_temp2 = im.crop(box=(0, 4*size[1]/10, size[0], size[1]))
        img_temp2 = img_temp2.rotate(random.choice([-1, 1]) * random.randrange(4, 7), resample=Image.Resampling.BILINEAR,
                              fillcolor=(255, 255, 255))

        im.paste(img_temp2, box=(0, int(4*size[1]/10)))
        im.paste(img_temp1)

        return im

def generator(size, txt):
        im = Image.new('RGB', size=size, color=(255, 255, 255))
        im = draw_text(im, size, txt, font, stringsize)
        im = noise_dots(im, size, 5, 5, 100)
        im = noise_curve(im, size, 5)
        #Lagacy
        #dr = ImageDraw.Draw(im)
        #for i in range(random.randint(8, 15)):
        #        r = random.randint(0, 255)
        #        g = random.randint(0, 255)
        #        b = random.randint(0, 255)
        #        ex = random.randint(0, size[0] - 10)
        #        ey = random.randint(0, size[1] - 10)
        #        dr.ellipse([(ex, ey), (random.randint(ex, size[0]), random.randint(ey, size[1]))],
        #                   fill=(r, g, b), width=random.randint(1, 10))

        #        dr.line([(0, random.randint(0, size[1])), (size[0], random.randint(0, size[1]))],
        #                fill=(0, 0, 0), width=random.randint(1,3))
        #        dr.line([(random.randint(0, size[0]), 0), (random.randint(0, size[0]), size[1])],
        #                fill=(0, 0, 0), width=random.randint(1,3))
        #font = ImageFont.truetype("./Noto_Sans/NotoSans-Bold.ttf", 64)
        #dr.text((random.randint(4 * size[0] / 10,  6 * size[0] / 10), random.randint(4 * size[1] / 10, 6*size[1] / 10)),
        #        text=string, anchor="mm", fill=(0, 0, 0), font=font)

        return im

def blending(size, txt, alpha):
        #多圖交疊
        img_temp1 = generator(size, txt)
        img_temp2 = generator(size, txt)
        im = Image.blend(img_temp1, img_temp2, alpha=alpha)

        return im


#color = random_color(10, 200, random.randint(220, 255))
#img = generator(size, string)
img = blending(size, string, alpha=0.6)

imgnew = Image.new("RGB", size=size, color=(255, 255, 255))
#imgnew = croping(img, size)
imgnew = color_invert(img)
#imgnew = color_invert(imgnew)
imgnew.save("distorted.png")
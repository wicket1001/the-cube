import unittest

SEGMENTS = 26
redColors = [255, 255, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
greenColors = [0, 200, 255, 255, 255, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 0, 0, 0, 0, 0, 0, 0, 0]
blueColors = [255, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

values = {16711935: [255, 0, 255], 16762880: [255, 200, 0], 65535: [0, 255, 255], 16711680: [255, 0, 0]}
colors = {'Pink': [255, 0, 255], 'Orange': [255, 200, 0], 'Cyan': [0, 255, 255], 'Rot': [255, 0, 0]}

numLEDS = [5, 7, 35, 34, 36, 9, 9, 6, 9, 9, 6, 9, 9, 6, 9, 9, 16, 8, 7, 6, 3, 20, 7, 20, 8, 20]
firstIndices = [0, 11, 46, 47, 116, 125, 126, 140, 149, 150, 164, 173, 174, 188, 197, 198, 222, 223, 231, 238, 244, 247, 267, 274, 292, 300]
currentIndices = [0, 11, 46, 47, 116, 125, 126, 140, 149, 150, 164, 173, 174, 188, 197, 198, 222, 223, 231, 238, 244, 247, 267, 274, 292, 300]
directions = [1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


def hsv_to_rgb(h, s, v):
    pass


def rgb_to_hsv(r, g, b):
    # print(r, g, b)
    rr = r / 255
    gg = g / 255
    bb = b / 255
    cmax = max(rr, gg, bb)
    cmin = min(rr, gg, bb)
    delta = cmax - cmin
    if delta == 0:
        h = 0
    elif cmax == rr:
        h = 60 * (((gg - bb) / delta) % 6)
    elif cmax == gg:
        h = 60 * (((bb - rr) / delta) + 2)
    elif cmax == bb:
        h = 60 * (((gg - rr) / delta) + 4)
    else:
        raise NotImplementedError('Bob')
    if cmax == 0:
        s = 0
    else:
        s = delta / cmax
    v = cmax
    return h, s, v


class TestComponents(unittest.TestCase):
    def test_distinct(self):
        print()
        print('⬛')
        distinct = {}
        for i in range(SEGMENTS):
            color = redColors[i] << 16 | greenColors[i] << 8 | blueColors[i]
            value = list(values.keys())
            names = list(colors.keys())
            k = value.index(color)
            print(names[k], rgb_to_hsv(redColors[k], greenColors[k], blueColors[k]))
            if color not in distinct:
                distinct[color] = [redColors[i], greenColors[i], blueColors[i]]
        print(distinct)

    def test_colors(self):
        for color in colors:
            print(color, rgb_to_hsv(*colors[color]))

    def test_indices(self):
        for i in range(SEGMENTS):
            print(firstIndices[i], numLEDS[i], directions[i])
            self.assertTrue(firstIndices[i] == currentIndices[i])


if __name__ == '__main__':
    unittest.main()



def get_paper_format(width_mm=0, height_mm=0):
    if width_mm <= 0 or height_mm <= 0:
        return None
    # available paper formats
    PAPER_FORMATS_MM = {
        'B5': (176.5, 250), 'A4': (210, 297), 'A4E': (236, 323), 'B4': (250, 350),
        'A3': (297, 420),  'A3E': (323, 446), 'B3': (350, 500),  'A2': (420, 594),
        'A2E': (445, 619), 'B2': (500, 700), 'B2E': (525, 725), 'A1': (594, 840),
        'A1E': (619, 865), 'B1': (700, 1000), 'B1E': (725, 1025), 'MAX': (920, 1058)
    }
    # calculate area in mm (squared)
    formats = [{'format': x[0], 's1':x[1][0], 's2':x[1][1], 'area':x[1][0]*x[1][1]}
               for x in PAPER_FORMATS_MM.items()
               if (width_mm <= x[1][0] and height_mm <= x[1][1])or(width_mm <= x[1][1] and height_mm <= x[1][0])
               ]
    # sorted from smallest to biggest area
    formats = sorted(formats, key=lambda x: x.get('area'), reverse=False)
    if len(formats):
        return formats[0].get('format')  # get the first (the smallest format)
    else:
        return None


if __name__ == "__main__":
    '''
        Run test if ran as main program
    '''
    assert get_paper_format(210, 297) == 'A4'
    assert get_paper_format(212, 297) == 'A4E'
    assert get_paper_format(500, 700) == 'B2'
    assert get_paper_format(450, 700) == 'B2'
    assert get_paper_format(400, 400) == 'A2'
    assert get_paper_format(100, 100) == 'B5'
    assert get_paper_format(1000, 700) == 'B1'
    assert get_paper_format(999, 699) == 'B1'
    assert get_paper_format(700, 999) == 'B1'
    assert get_paper_format(701, 999) == 'B1E'
    assert get_paper_format(10, 99999) == None
    assert get_paper_format(-30, -10) == None

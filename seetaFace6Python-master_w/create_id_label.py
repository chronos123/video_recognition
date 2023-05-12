id_list = ['B18231008', 'B19231210', 'B19231217', 'B19374340', 'B19376210', 'BY2202120', 'BY2202204', 'BY2241110',
           'SY2202107', 'SY2202122', 'SY2202423', 'SY2202510', 'SY2207619', 'SY2217105', 'SY2217314', 'SY2241105',
           'SY2241126', 'SY2241204', 'SY2243309', 'teacher', 'ZB2202252', 'ZF2241102', 'ZF2241103', 'ZY2102122',
           'ZY2202205', 'ZY2202402', 'ZY2202417', 'ZY2202418', 'ZY2202513', 'ZY2202521', 'ZY2243304', 'ZY2243310',
           'ZY2243311']


def get_id_from_label(label):
    return id_list[label]


def get_label_from_id(student_id):
    if student_id == 'wengp' or student_id == 'weng':
        return id_list.index('B19374340')
    else:
        return id_list.index(student_id)


if __name__ == '__main__':
    print(get_label_from_id('B19374340'))
    print(get_id_from_label(3))
    print('done')

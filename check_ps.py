#!/usr/bin/python3
import sys
import os
import math
from paper_format import get_paper_format
import zipfile
import zlib
import argparse
from config import zip_password


path_file_ps = ''
path_file_zip = ''


def mark_file_as_invalid(path_filename, new_extension):
    '''Mark file as invalid -> change extension to ".invalid"
    '''
    os.rename(path_filename, path_filename+new_extension)


def read_file_as_list(path_filename):
    content = []
    try:
        with open(path_filename, encoding='UTF-8') as file:
            try:
                content = [line.rstrip('\n') for line in file]
            except UnicodeDecodeError:
                sys.exit('ERROR: I cannot recognize encoding this file. Sorry')
            except:
                sys.exit('ERROR: I cannot read this file.')
    except FileNotFoundError:
        sys.exit('File not found.')
    except:
        sys.exit('Can''t open this file')

    return content


def get_values_from(file_content, line):
    lines = [l[len(line):].strip(':').split()
             for l in file_content
             if l[:len(line)] == line]
    return lines[0] if lines else []  # return only first line (if found more)


def get_page_dimensions(file_content):
    values = get_values_from(file_content, r'%%PageBoundingBox:')
    if len(values) != 4:
        values = get_values_from(file_content, r'%%BoundingBox:')
    if len(values) != 4:
        return {}
    else:
        divider = 72 / 25.4  # 72 points / inch[mm]
        return {
            'width_mm': math.floor((int(values[2])-int(values[0])) / divider),
            'height_mm': math.floor((int(values[3])-int(values[1])) / divider)
        }


def create_output_filename(path_file_ps, paper_format='', width_mm=0, height_mm=0):
    if width_mm > 0 and height_mm > 0:
        filename = "{}_{}x{}mm_{}.zip".format(
            '.'.join(path_file_ps.split('.')[:-1]),
            round(width_mm),
            round(height_mm),
            paper_format or '')
    else:
        filename = f"{path_file_ps}.zip"
    return filename


def marker_eof_exists(file_content):
    return len([l for l in file_content if l.strip() == r'%%EOF']) == 1


def main(path_file_ps):

    print(f"[---] Loading file: {path_file_ps}")
    file_content = read_file_as_list(path_file_ps)

    # new file name will have dimensions in mm (if found)
    dimensions = get_page_dimensions(file_content)
    path_file_zip = create_output_filename(
        args.path_file_ps, get_paper_format(**dimensions), **dimensions)

    if path_file_ps:
        if marker_eof_exists(file_content):
            print('[---] The file is correct.')
            print('[---] Compressing, wait a moment...')
            with zipfile.ZipFile(path_file_zip, 'w',
                                 compression=zipfile.ZIP_DEFLATED
                                 ) as zip_file:
                zip_file.write(
                    path_file_ps,
                    arcname=os.path.basename(path_file_ps))
                zip_file.close()
            if os.path.isfile(path_file_zip):
                print('[---] Deleting old file ps')
                os.remove(path_file_ps)
        else:
            print('[ERROR] <> No matching ending word. File PS may be corrupted.')
            mark_file_as_invalid(path_file_ps, '.invalid')  # change file name
    else:
        print('[ERROR] <> Incorrect file names. Please check.')
        print(f"PS file name: {path_file_ps}")
        print(f"Output file name: {path_file_zip}")
        sys.exit(1)


if __name__ == "__main__":
    print('Hello, this is a check post-script file compresser (made in 2019)')
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        'path_file_ps',
        help='filename input postscript file (.PS)')
    args = parser.parse_args()

    # check import file exists
    if not os.path.isfile(args.path_file_ps):
        sys.exit(f"[ERROR] <> File not exist: {path_file_ps}", 1)

    main(args.path_file_ps)

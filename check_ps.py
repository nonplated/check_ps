#!/usr/bin/python3
import sys
import os
import math
from paper_format import get_paper_format

path_file_ps = ''
path_file_zip = ''

# change your path to archive program
path_absolute_7z = r"D:\Aplikacje\7-Zip\7z"


def mark_file_as_invalid(path_filename, new_extension):
    os.rename(path_filename, path_filename+new_extension)


def read_file_as_list(path_filename):
    content = []
    with open(path_filename) as file:
        content = [line.rstrip('\n') for line in file]
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
    # return file_content[-2] == r'%%EOF'
    return len([l for l in file_content if l.strip() == r'%%EOF']) == 1


if __name__ == "__main__":
    print("Hello, now we will check post-script file (made in 2019)\n")
    print(sys.argv)
    if len(sys.argv) > 1 and len(sys.argv[1]) > 0:
        path_file_ps = os.path.abspath(sys.argv[1])
        if not os.path.exists(path_file_ps):
            sys.exit(f"ERROR: File not exist: {path_file_ps}")
    else:
        print('Usage:                             ')
        print('          check_ps.py [filename.ps]')
        sys.exit(0)

    print(f"Loading file: {path_file_ps}")
    file_content = read_file_as_list(path_file_ps)

    # new file name will have dimensions in mm (if found)
    dimensions = get_page_dimensions(file_content)
    path_file_zip = create_output_filename(
        path_file_ps, get_paper_format(**dimensions), **dimensions)

    if path_file_ps and path_file_zip and path_absolute_7z:
        if marker_eof_exists(file_content):
            print('File is correct.')
            zip_exec_command = f"{path_absolute_7z} a \"{path_file_zip}\" \"{path_file_ps}\" -sdel"
            # used options for 7z:
            #    a      --- add files to archive
            #    -sdel  --- delete source file after success compressing
            os.system(zip_exec_command)
        else:
            print('ERROR: No matching ending word. File PS may be corrupted.')
            mark_file_as_invalid(path_file_ps, '.invalid')  # change file name
    else:
        print('Incorrect file names. Please check.')
        print(f"PS file name: {path_file_ps}")
        print(f"Output file name: {path_file_zip}")
        print(f"Path to 7z app: {path_absolute_7z}")
        sys.exit(1)

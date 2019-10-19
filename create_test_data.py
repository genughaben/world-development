import os
from tqdm import tqdm

line_copy_offset = 2000
copy_state = False
chunk_size = 20

copy_count = 0

original_file_path = 'commodity_trade_statistics_data.csv'

#file_name = os.path.basename(original_file_path)
#base = os.path.splitext(file_name)[0]
#ext = os.path.splitext(file_name)[1]

test_filename = f'data/test/{original_file_path}'

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

num_lines = file_len(f'data/{original_file_path}')

with open(f'{original_file_path}') as original_file:
    test_file = open(test_filename, "w+")
    for idx, line in enumerate(tqdm(original_file, total=num_lines)):
        if idx % line_copy_offset == 0:
            copy_state = True
        if copy_state:
            test_file.write(line)
            copy_count = copy_count + 1
            if copy_count % chunk_size == 0:
                copy_state = False

test_file.close()
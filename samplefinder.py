import json
import argparse
import subprocess
import os
import numpy as np
from pathlib import Path
import pandas as pd
from tqdm import tqdm
from audio_offset_finder.audio_offset_finder import find_offset_between_files

parser = argparse.ArgumentParser(
                    prog='Sample Finder',
                    description='Compares mp3 with a set of mp3s and finds offsets between them')
parser.add_argument('-d', '--dir', help='Name of directory where the mp3s are stored (and downloaded if needed)', required=True)
parser.add_argument('-c', '--channel', help='Channel name to download from')
parser.add_argument('--download', help='Download all videos from a channel', action='store_true')
args = parser.parse_args()

RESULTS = []
DIRECTORY = args.dir

curr_dir = Path().absolute()
mp3s_dir = curr_dir / DIRECTORY

if args.download and args.channel:
    mp3s_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(f'yt-dlp -x --audio-format mp3 --audio-quality 0 -f best -N 5 -o {str(mp3s_dir)}{os.sep}%\(title\)s.%\(ext\)s --verbose https://www.youtube.com/@{args.channel}', shell=True, check=True)

# constructing dict
for file in tqdm(list(mp3s_dir.rglob('*.mp3'))):
    result = find_offset_between_files('ekt.mp3', str(file))
    filename_stripped = file.name

    result_dict = {
        "file": filename_stripped,
        "offset": result["time_offset"],
        "standard_score": 0 if np.isnan(result['standard_score']) else result['standard_score']
    }
    print(result_dict)
    RESULTS.append(result_dict)

# sorting by standard_score descending
RESULTS = sorted(RESULTS, key=lambda x: x["standard_score"], reverse=True)

with open(f'{DIRECTORY}.json', 'w', encoding='UTF-8') as f:
    json.dump(RESULTS, f)

# constructing dataframe for Excel table (A1 is filename, B1 B2 are values, C1 C2 are labels etc)
df = pd.DataFrame(RESULTS)
reshaped_data = []
for i, row in df.iterrows():
    reshaped_data.append([row['file'], row['offset'], 'offset'])
    reshaped_data.append([None, row['standard_score'], 'standard_score'])

reshaped_df = pd.DataFrame(reshaped_data, columns=['A', 'B', 'C'])
reshaped_df.to_excel(f'{DIRECTORY}.xlsx', index=False, header=False)

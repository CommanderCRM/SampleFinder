import json
import argparse
import os
from pathlib import Path
from yt_dlp import YoutubeDL
import numpy as np
import pandas as pd
from tqdm import tqdm
from audio_offset_finder.audio_offset_finder import find_offset_between_files

class ArgParser:
    """Parsing arguments passed to the script"""
    def __init__(self):
        self.parser = argparse.ArgumentParser(
                            prog='Sample Finder',
                            description='Compares mp3 with a set of mp3s and finds offsets between them')
        self.parser.add_argument('-d', '--dir', help='Name of directory where the mp3s are stored (and downloaded if needed)', required=True)
        self.parser.add_argument('-c', '--channel', help='Channel name to download from')
        self.parser.add_argument('--download', help='Download all videos from a channel', action='store_true')
        self.args = self.parser.parse_args()

class SampleFinder:
    """Finding sample of one mp3 in multiple others"""
    def __init__(self, args):
        self.results = []
        self.directory = args.dir
        self.curr_dir = Path().absolute()
        self.mp3s_dir = self.curr_dir / self.directory
        self.json_path = self.mp3s_dir / f'{self.directory}.json'
        self.excel_path = self.mp3s_dir / f'{self.directory}.xlsx'
        self.args = args

    def download(self):
        """Downloads all videos from youtube channel"""
        if self.args.download and self.args.channel:
            self.mp3s_dir.mkdir(parents=True, exist_ok=True)
            with YoutubeDL({
                                'format': 'bestaudio/best',
                                'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '320',
                                }],
                                'outtmpl': f'{self.mp3s_dir}{os.sep}%(title)s.%(ext)s',
                                'quiet': False}) as ydl:
                ydl.download([f'https://www.youtube.com/@{self.args.channel}'])

    def find_offsets(self):
        """Finds offset of one mp3 file in multiple others"""
        mp3s_in_dir = list(self.mp3s_dir.rglob('*.mp3'))
        for file in tqdm(mp3s_in_dir, desc="Comparing sample to mp3s", dynamic_ncols=True, ascii=" ="):
            result = find_offset_between_files('ekt.mp3', str(file))
            filename_stripped = file.name

            result_dict = {
                "file": filename_stripped,
                "offset": result["time_offset"],
                "standard_score": 0 if np.isnan(result['standard_score']) else result['standard_score']
            }

            self.results.append(result_dict)

        # sorting by standard_score descending
        self.results = sorted(self.results, key=lambda x: x["standard_score"], reverse=True)

    def write_results(self):
        """Writes results to JSON and XLSX files"""
        with open(self.json_path, 'w', encoding='UTF-8') as f:
            json.dump(self.results, f)

        df = pd.DataFrame(self.results)
        reshaped_data = []
        for i, row in df.iterrows():
            reshaped_data.append([row['file'], row['offset'], 'offset'])
            reshaped_data.append([None, row['standard_score'], 'standard_score'])

        reshaped_df = pd.DataFrame(reshaped_data, columns=['A', 'B', 'C'])
        reshaped_df.to_excel(self.excel_path, index=False, header=False)

arg_parser = ArgParser()
sample_finder = SampleFinder(arg_parser.args)
sample_finder.download()
sample_finder.find_offsets()
sample_finder.write_results()

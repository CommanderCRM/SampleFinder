# SampleFinder
Python tool for finding offset of an mp3 file within another mp3 files. Supports downloading mp3s from YT channel

## Main dependencies
* tqdm
* pandas
* openpyxl
* audio-offset-finder (more about it [here](https://github.com/bbc/audio-offset-finder))
* yt-dlp (more about it [here](https://github.com/yt-dlp/yt-dlp))

It is recommended not to use Python >3.11.\
You may install them "as is": ```pip install tqdm pandas openpyxl audio-offset-finder yt-dlp```.\
If it's problematic, use fixed versions from ```requirements.txt```: ```pip install -r requirements.txt```.\

## Features
* Downloading all videos from YT channel and converting them to .mp3s
* Finding offsets between one .mp3 file and numerous others (either downloaded or stored)
* Outputting results to JSON and XLSX

## Usage
```python3 samplefinder.py *arguments*```

```
options:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Name of directory where the mp3s are stored (and downloaded if needed)
  -c CHANNEL, --channel CHANNEL
                        Channel name to download from
  --download            Download all videos from a channel
```

-d argument, followed by directory name, is required. To download videos, use --download combined with -c or --channel, followed by channel name.

```python3 samplefinder.py -d dominik500``` - without download, use .mp3s stored in "dominik500" folder.\
```python3 samplefinder.py -d my_dir --download -c dominik500``` - download everything from "dominik500" channel and use .mp3s stored in "my_dir".

## Notes
The .mp3 file is hardcoded for now as ekt.mp3 - [found](https://en.wikipedia.org/wiki/Ulterior_Motives_(song))!

import os
from sys import argv
import pvleopard as tts

ACCESS_KEY = "Cf67X8JSJ4XwOPRt7GAg4m9m/lLPZua2gayxsPXaEYyq508C10ytnQ=="
DIR = os.path.dirname(os.path.abspath(__file__))
dir_change = lambda loc: fr'{DIR}/{loc}' if "txt" in loc else fr'{DIR}/{loc}.txt'
TEMPLATE = dir_change('template.txt')
OUTPUT = dir_change('out.txt')
INPUT = dir_change('lyrics.txt')
TTS = None

def __init__():
    arg_len = len(argv)

    if arg_len > 1: INPUT == dir_change(argv[1])
    if arg_len > 2: OUTPUT == dir_change(argv[2])
    if arg_len > 3: TEMPLATE == dir_change(argv[3])
    if arg_len > 4:
        TTS == fr'{DIR}/{argv[4]}'
        create_transcript(TTS)

    with open(INPUT, 'r') as readfile:
        lines = readfile.readlines()

    lyric = capitalize_lines(lines)
    lyric = truncate_lines(lyric)
    parsed_out = parse_lyrics(lyric)
    write_template(TEMPLATE, OUTPUT, parsed_out)

    print("Usage: python arduino-script.py [input.txt] [output.txt] [temp.txt] [tts.mp3]")

def create_transcript(audio_file):
    ttsObj = tts.create(access_key=ACCESS_KEY)
    transcript, words = ttsObj.process_file(audio_file)
    return transcript, words


def truncate_lines(lyrics):
    new_lines = []
    curr_length = 0
    line = [line.split(" ") for line in lyrics]
    temp_line = ""

    for words in line:
        for word in words:
            curr_length += len(word) + 1
            if curr_length > 16:
                new_lines.append(temp_line)
                curr_length = len(word) + 1
                temp_line = word + " "
            else:
                temp_line += word + " "
        if "\n" in temp_line:
            temp_line = temp_line[:-2]
        new_lines.append(temp_line)
        temp_line = ""
        curr_length = 0
    index = 0
    for new_line in new_lines:
        new_line += "\n"
        new_lines[index] = new_line
        index += 1
    return new_lines

def parse_lyrics(lyrics):
    parsed_output = []
    line_len = 0
    for line in lyrics:
        if line[0].isupper():
            code_block = "\n\tlcd.clear();"
        else:
            code_block = ""
        line = line[:-1]
        if line_len == 0 or line[0].isupper():
            code_block += "\n\tlcd.setCursor(0, 0);"
            line_len = 1
        else:
            code_block += "\n\tlcd.setCursor(0, 1);"
            line_len = 0
        
        code_block += f'\n\tlcd.print("{line}");'
        code_block += "\n\tdelay(1000);"

        if line_len == 1:
            code_block += "\n"
        else:
            code_block += "\n\tlcd.clear();\n"
        
        parsed_output.append(code_block)
    return parsed_output

def write_template(temp, out, parsed):
    final_output = []
    with open(temp, 'r') as read_template:
       template = read_template.readlines()
    for line in template:
        final_output.append(line)
        if "!@#$%^" in line:
            final_output.extend(parsed)
    with open(out, 'w') as write_template:
        write_template.writelines(final_output)

def capitalize_lines(lyrics):
    # capitalize the lines
    cap = []
    for line in lyrics:
        line = line.lstrip()
        if line[0].isalpha():
            first_letter = line[0].upper()
            line = first_letter + line[1:]
            cap.append(line)
        
    return cap

if __name__ == '__main__':
    __init__()
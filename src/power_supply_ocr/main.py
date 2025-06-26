from power_supply_ocr.data import create_output_dir, create_excel, save_excel
from power_supply_ocr.video import get_video, open_video, loop_video, clear_video

import tkinter as tk

def main():
    filename, filepath = get_video()
    video, fps, total_frames = open_video(filename, filepath)
    create_output_dir()
    excel, sheet = create_excel() 
    loop_video(video, fps, total_frames, sheet)
    save_excel(excel, filename)
    clear_video(video)
    return 

if __name__ == "__main__":
    # part of the import if you are not using other tkinter functions
    tk.Tk().withdraw()
    main()
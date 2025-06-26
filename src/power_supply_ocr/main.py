from power_supply_ocr.data import create_output_dir, create_excel, save_excel
from power_supply_ocr.video import open_video, loop_video, clear_video

def main():
    filename, cap, fps = open_video()
    create_output_dir()
    excel, sheet = create_excel() 
    loop_video(cap, fps, sheet)
    save_excel(excel, filename)
    clear_video(cap)
    return 

if __name__ == "__main__":
    main()
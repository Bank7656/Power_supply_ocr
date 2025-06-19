from power_supply_ocr.video import open_video, loop_video, clear_video

def main():
    cap = open_video()
    loop_video(cap)
    clear_video(cap)
    return 

if __name__ == "__main__":
    main()
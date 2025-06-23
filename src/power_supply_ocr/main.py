from power_supply_ocr.video import open_video, loop_video, clear_video

def main():
    cap, fps = open_video()
    loop_video(cap, fps)
    clear_video(cap)
    return 

if __name__ == "__main__":
    main()
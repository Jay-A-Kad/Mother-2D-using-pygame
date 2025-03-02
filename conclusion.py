from ffpyplayer.player import MediaPlayer
import json
import cv2

def play_video_with_audio(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: {video_path}")
        return


    player = MediaPlayer(video_path, ff_opts={'sync': 'video'})
    screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cv2.namedWindow("Conclusion Video", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Conclusion Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

     
        screen_res = (screen_width, screen_height)
        frame = cv2.resize(frame, screen_res)
        cv2.imshow("Conclusion Video", frame)
        audio_frame, val = player.get_frame()
        if val != 'eof' and audio_frame:
            img, t = audio_frame
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    player.close_player()
    cv2.destroyAllWindows()

def main():
    
    with open("choice.json", "r") as file:
        choice_data = json.load(file)
    
    choice = choice_data.get("choice")
    if choice == "1":
        play_video_with_audio("assets/artwork/Final-conclusion-2.mp4")
    elif choice == "2":
        play_video_with_audio("assets/artwork/Final-conclusion-3.mp4")
    elif choice == "3":
        play_video_with_audio("assets/artwork/Final-conclusion-1.mp4")

if __name__ == "__main__":
    main()

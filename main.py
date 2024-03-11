import cv2, requests, datetime, m3u8, tempfile

file = open('temp.m3u8', 'r')

m3u8_file = m3u8.M3U8(file.read())

while timecode := input("timecode [00:00]: "):

    timecode_to_int = datetime.datetime.strptime(timecode, "%M:%S").time().minute * 60 + datetime.datetime.strptime(timecode, "%M:%S").time().second

    current_length = 0

    for f in m3u8_file.data['segments']:
        current_length += f.get('duration', 0)

        if current_length >= timecode_to_int:
            data = requests.get(f.get('uri')).content

            # Сохранение во временный файл на диск
            temp_video_path = tempfile.NamedTemporaryFile(delete=False, suffix='.ts')
            temp_video_path.write(data)
            temp_video_path.close()

            break

    print("DEBUG: " + str(current_length))

    video_capture = cv2.VideoCapture(temp_video_path.name)

    video_capture.set(cv2.CAP_PROP_POS_MSEC, (current_length - timecode_to_int) * 1000)

    print("DEBUG: " + str(video_capture.get(cv2.CAP_PROP_POS_MSEC)))

    success, image = video_capture.read()
    if success:
        cv2.imwrite(f'{timecode}.jpg', image)
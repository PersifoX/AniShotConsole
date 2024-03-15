import cv2, requests, datetime, tempfile, requests

from m3u8 import M3U8

from prompt_toolkit import PromptSession, print_formatted_text as print

from prompt_toolkit.styles import Style

from prompt_toolkit.formatted_text import FormattedText, HTML

from pyfiglet import Figlet



logo = Figlet(font="5lineoblique", width=250)

print(HTML(f'<style color="#e11d48">{logo.renderText("AniShot")}</style>'))
print(HTML(f'<bold>By persifox</bold> | <style color="#60a5fa">github.com/PersifoX/AniShot</style>\n'))

style = Style(
    [
        ('pl', '#454545 italic'),
        ('error', '#e11d48 bold'),
        ('warning', '#f59e0b bold'),
        ('success', '#00b76e bold'),    
    ]
)


session = PromptSession(tempfile="history", style=style, enable_history_search=True, enable_system_prompt=True, erase_when_done=True)

try:
    while url := session.prompt(f"url to m3u file: ", placeholder=FormattedText([("class:pl", "https://example.com/temp.m3u8")])):
        
        try:
            data = requests.get(url).content
        except:
            print(FormattedText([("class:error", "error: Can't get data from url")]), style=style)
            continue

        temp_m3u_path = tempfile.NamedTemporaryFile(delete=False, suffix='.ts')
        temp_m3u_path.write(data)
        temp_m3u_path.close()

        file = open(temp_m3u_path.name, 'r')

        m3u8_file = M3U8(file.read())

        while timecode := session.prompt(f"timecode: ", placeholder=FormattedText([("class:pl", "00:00")])):

            timecode_to_int = datetime.datetime.strptime(timecode, "%M:%S").time().minute * 60 + datetime.datetime.strptime(timecode, "%M:%S").time().second

            current_length = duration = 0

            for f in m3u8_file.data['segments']:
                duration = f.get('duration', 0)

                current_length += duration

                if current_length >= timecode_to_int:
                    data = requests.get(f.get('uri')).content

                    # Сохранение во временный файл на диск
                    temp_video_path = tempfile.NamedTemporaryFile(delete=False, suffix='.ts')
                    temp_video_path.write(data)
                    temp_video_path.close()

                    break

            # print("DEBUG: " + str(current_length))

            video_capture = cv2.VideoCapture(temp_video_path.name)

            video_capture.set(cv2.CAP_PROP_POS_MSEC, (duration - (current_length - timecode_to_int)) * 1000)

            # print("DEBUG: " + str(video_capture.get(cv2.CAP_PROP_POS_MSEC)) + " " + str(duration - (current_length - timecode_to_int)* 1000))

            success, image = video_capture.read()

            if success:
                cv2.imwrite(f'{session.prompt("name of image: ", placeholder=FormattedText([("class:pl", "image"), ("", ".jpg")]))}.jpg', image)

except KeyboardInterrupt:
    print(HTML('\n<style color="#f59e0b">Woah! Some screenshots can be lost, but you can always try again.</style>'), style=style)

finally:
    print(HTML('\n<style color="#60a5fa">Have a nice day!</style>'), style=style)
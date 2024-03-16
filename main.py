import cv2, requests, datetime, tempfile

from m3u8 import M3U8

from prompt_toolkit import PromptSession, print_formatted_text as print
from prompt_toolkit.formatted_text import FormattedText, HTML
from prompt_toolkit.styles import Style

from classes.autocomlete import *
from classes.objects import *
from classes.validation import *

from pyfiglet import Figlet



logo = Figlet(font="5lineoblique", width=250)

print(HTML(f'<style color="#e11d48">{logo.renderText("AniShot Console")}</style>'))
print(HTML(f'<bold>By persifox</bold> | <style color="#e11d48">github.com/PersifoX/AniShotConsole</style>\n'))
print(HTML(f'<bold>RIGHT CLICK</bold> <style color="#60a5fa">для вставки из буфера</style>'))
print(HTML(f'<bold>CTRL + C</bold>    <style color="#60a5fa">для возврата назад</style>\n'))

style = Style(
    [
        ('pl', '#454545 italic'),
        ('error', '#e11d48 bold'),
        ('warning', '#f59e0b bold'),
        ('success', '#00b76e bold'),
        ('primary', '#e11d48')
    ]
)

session = PromptSession(
    tempfile="history", 
    style=style,
    erase_when_done=True, 
    complete_in_thread=True, 
    complete_while_typing=True,
    validate_while_typing=True
)

try:
    while True:

        # set validation and complition for switching profile
        session.completer=AnilibriaSearcher()
        session.validator=AnilibriaValidator()

        # main loop
        anime_id = session.prompt(
                HTML('<bold>Начните писать название аниме: </bold>'), 
                placeholder=FormattedText([("class:pl", "Sousou no Frieren")]), 
            )

        # searching anime from api
        anime = Anime(int(anime_id[3:])).from_api()

        print(HTML(f'<style fg="#e11d48">[AniShot]</style> Выбран профиль для <bold>{anime.names.ru}</bold>'))

        # unset completer
        session.completer = None


        try:
            # series loop
            while serie_number := session.prompt(
                HTML('<bold>Номер серии: </bold>'), 
                        placeholder=FormattedText([("class:pl", "12")]),  
                        validator=SerieValidator(anime),
            ):

                anime.catch_serie(int(serie_number))
                
                m3u8_content = requests.get(anime.get_serie_uri()).text

                # Parsing m3u8
                m3u8_file = M3U8(m3u8_content)

                session.completer = None


                try:
                    # timecode loop
                    while timecode := session.prompt(
                            f"таймкод: ", 
                            placeholder=FormattedText([("class:pl", "00:00")]), 
                            validator=TimecodeValidator()
                        ):

                        # Timecode to seconds
                        timecode_to_int = datetime.datetime.strptime(timecode, "%M:%S").time().minute * 60 + datetime.datetime.strptime(timecode, "%M:%S").time().second

                        current_length = duration = 0

                        # Reading segments
                        for f in m3u8_file.data['segments']:
                            duration = f.get('duration', 0)

                            current_length += duration

                            # If timecode is in this segment
                            if current_length >= timecode_to_int:

                                # Save segment
                                temp_video_path = tempfile.NamedTemporaryFile(delete=False, suffix='.ts')
                                temp_video_path.write(requests.get(f.get('uri')).content)
                                temp_video_path.close()

                                break

                        # Parsing video
                        video_capture = cv2.VideoCapture(temp_video_path.name)

                        # Set position
                        video_capture.set(cv2.CAP_PROP_POS_MSEC, (duration - (current_length - timecode_to_int)) * 1000)

                        success, image = video_capture.read()

                        # Save image
                        if success:
                            default = anime.code

                            session.validator = NameValidator()
                            session.completer = None

                            filename = session.prompt(
                                    "Название изображения: ",
                                    placeholder=FormattedText([("class:pl", default), ("", ".jpg")])
                                ) or default
                            

                            # write image
                            cv2.imwrite(f"{filename}.jpg", image)

                            print(HTML(f'<style fg="#e11d48">[AniShot]</style> Скриншот сохранен как <bold>{filename}.jpg</bold>'))

                            #cv2.imshow("screenshot", image)

                        # clearing memory
                        video_capture.release()


                except KeyboardInterrupt:
                    print(HTML('\n<bold>[CTRL + C]</bold> <style color="#f59e0b">Замена серии...</style>'), style=style)


        except KeyboardInterrupt:
            print(HTML('\n<bold>[CTRL + C]</bold> <style color="#f59e0b">Замена профиля аниме...</style>'), style=style)




except KeyboardInterrupt:
    print(HTML('\n<bold>[CTRL + C]</bold> <style color="#f59e0b">Все скриншоты сохранены в эту папку, завершение работы.</style>'), style=style)

finally:
    print(HTML(f'<style color="#e11d48">{logo.renderText("See next time...")}</style>'))
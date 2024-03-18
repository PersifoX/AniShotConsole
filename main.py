import cv2, requests, datetime, tempfile, os, time

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
print(HTML(f'<bold>CTRL + C</bold>    <style color="#60a5fa">для возврата назад</style>'))
print(HTML(f'<bold>P</bold>           <style color="#60a5fa">поставить реплей на паузу</style>'))
# print(HTML(f'<bold>Q</bold>           <style color="#60a5fa">выйти из реплея</style>\n'))

style = Style(
    [
        ('pl', '#454545 italic'),
        ('error', '#e11d48 bold'),
        ('warning', '#f59e0b bold'),
        ('success', '#00b76e bold'),
        ('primary', '#e11d48')
    ]
)

font = cv2.FONT_HERSHEY_DUPLEX
bottomLeftCornerOfText = (10, 50)
fontScale = 1
fontColor = (255, 255, 255)
lineType = 1

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
                            placeholder=FormattedText([("class:pl", "00:00 или ~00:00")]), 
                            validator=TimecodeValidator()
                        ):

                        replay = False

                        if timecode.startswith('~'):

                            replay = True
                            timecode = timecode[1:]


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

                        # If timecode is not in this segment
                        if current_length < timecode_to_int:
                            print(HTML(f'<style fg="#e11d48">[AniShot]</style> Таймкод <bold>{timecode}</bold> не найден'))
                            continue

                        # Parsing video
                        video_capture = cv2.VideoCapture(temp_video_path.name)

                        if not replay:
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

                        else:
                            print(HTML(f'<style fg="#e11d48">[AniShot]</style> Быстрый реплей отрывка <bold>{timecode}</bold> через 1 секунду...'))

                            time.sleep(1)

                            while True:
                                ret, frame = video_capture.read()

                                if not ret:
                                    break

                                #rescaling image
                                reescaled_frame = frame

                                for i in range(1):
                                    reescaled_frame = cv2.pyrDown(reescaled_frame)

                                #timecode
                                source = current_length - duration + int(video_capture.get(cv2.CAP_PROP_POS_MSEC) / 1000)

                                timecode = datetime.datetime.fromtimestamp(source).strftime('%M:%S')


                                cv2.putText(reescaled_frame, timecode, bottomLeftCornerOfText, font, fontScale, fontColor, lineType)

                                cv2.imshow('Replay', reescaled_frame)

                                # If 'q' key is pressed, exit the loop
                                if cv2.waitKey(25) & 0xFF in (ord('q'), ord('Q'), ord('й'), ord('Й')):
                                    break


                            cv2.destroyWindow('Replay')


                        # clearing memory
                        video_capture.release()

                        os.remove(temp_video_path.name)



                except KeyboardInterrupt:
                    print(HTML('\n<bold>[CTRL + C]</bold> <style color="#f59e0b">Замена серии...</style>'), style=style)


        except KeyboardInterrupt:
            print(HTML('\n<bold>[CTRL + C]</bold> <style color="#f59e0b">Замена профиля аниме...</style>'), style=style)




except KeyboardInterrupt:
    print(HTML('\n<bold>[CTRL + C]</bold> <style color="#f59e0b">Все скриншоты сохранены в эту папку, завершение работы.</style>'), style=style)

except Exception as e:
    print(HTML(f'<style fg="#e11d48">[AniShot]</style> К сожалению, AniShot не смог сделать скриншот\n[Source] <bold>{e}</bold>'), style=style)

finally:
    print(HTML(f'<style color="#e11d48">{logo.renderText("See next time...")}</style>'))
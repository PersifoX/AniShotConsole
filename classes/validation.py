import datetime

from prompt_toolkit.validation import Validator, ValidationError

from classes.objects import Anime



class AnilibriaValidator(Validator):
    def validate(self, document):
        if not document.text.startswith('id:'):
            raise ValidationError(message='Выберите аниме из списка')
            

class SerieValidator(Validator):
    def __init__(self, anime: Anime):
        self.anime = anime

    def validate(self, document):
        if not document.text.isdigit():
            raise ValidationError(message='Номер серии должен быть числом')
        
        if not(int(document.text) in range(1, self.anime.player.series_count + 1)):
            raise ValidationError(message='Такой серии нет в аниме')
        

class TimecodeValidator(Validator):
    def validate(self, document):

        text = document.text.replace('~', '')

        try:
            datetime.datetime.strptime(text, "%M:%S")

        except:
            raise ValidationError(message='Таймкод должен быть в формате MM:SS или ~MM:SS (для просмотра отрывка)')


class NameValidator(Validator):
    def validate(self, document):
        if not document.text.isalpha() and document.text:
            raise ValidationError(message='Название может содержать только латинские буквы без символов')
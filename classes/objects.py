import requests

from typing import List, Optional, Any, Literal



class Anime:
    """Base class for animes"""

    def __init__(self, id: int):
        self.id = id

        self.current_serie = 1
        self.timecode = '00:00'


    def from_api(self):
        """Get anime info from API"""

        request = requests.get('https://api.anilibria.tv/v2/getTitle', params={'id': self.id})

        if request.status_code != 200:
            return

        self.info = request.json()

        self.code: str = self.info.get('code')

        self.names: Names = Names.from_dict(self.info.get('names', {}))

        self.player: Player = Player.from_dict(self.info.get('player', {}))

        return self
    

    def catch_serie(self, serie_number: int) -> Any:
        """Return serie"""
        self.current_serie = serie_number

        return self.player.series[self.current_serie - 1]
    
    def get_serie_uri(self, resolution: Literal['sd', 'hd', 'fhd'] = 'fhd') -> str:
        """Return uri of serie"""
        return self.player.serie_uri(self.current_serie, resolution)



class Names:
    """Names for anime"""
    def __init__(self, ru: str, en: str):

        self.ru = ru
        self.en = en


    def from_dict(names: dict):
        """Return names class from dict"""
        return Names(names.get('ru'), names.get('en'))
    

class Player:
    """Base class for player"""

    def __init__(self, host: str, series_count: int, series: List[Any]):

        self.host = host
        self.series_count = series_count
        self.series = series


    def serie_uri(self, number: int, resolution: Literal['sd', 'hd', 'fhd'] = 'fhd') -> str:
        """Return uri of serie"""
        return f'https://{self.host}{getattr(self.series[number - 1].hls, resolution)}'

    
    def from_dict(player: dict):
        """Return names class from dict"""

        series = []

        for index in range(player['series']['last']):
            index += 1

            series.append(Serie.from_dict(player['playlist'].get(f'{index}')))

        return Player(player['host'], player['series']['last'], series)


class Hls:
    """Base class for hls"""

    def __init__(
            self, 
            sd: Optional[str] = None, 
            hd: Optional[str] = None, 
            fhd: Optional[str] = None
        ):

        self.sd = sd
        self.hd = hd
        self.fhd = fhd


    def from_dict(hls: dict):
        """Return hls class from dict"""

        return Hls(hls.get('sd'), hls.get('hd'), hls.get('fhd'))
    

class Serie:
    """Base class for serie of anime"""

    def __init__(
            self, 
            pos: int, 
            hls: Hls, 
            preview: str | None = None, 
            opening: Optional[List[int]] = None, 
            ending: Optional[List[int]] = None,
            resolution: Literal['sd', 'hd', 'fhd'] = 'fhd'
        ) -> None:

        self.pos = pos
        self.hls = hls
        self.preview = preview
        self.opening = opening
        self.ending = ending
        self.resolution = resolution

    def from_dict(serie: dict):
        """Return serie class from dict"""

        return Serie(serie.get('serie'), Hls.from_dict(serie.get('hls')), serie.get('preview'), serie['skips'].get('opening'), serie['skips'].get('ending'))
    


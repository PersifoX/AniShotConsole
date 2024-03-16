import requests

from prompt_toolkit.completion import Completer, Completion



class AnilibriaSearcher(Completer):
    def get_completions(self, document, complete_event):
        
        request = requests.get(
                'https://api.anilibria.tv/v2/searchTitles', 
                params={'id': document.text[3:]} if document.text.startswith('id:') else {'search': document.text}
            )

        if request.status_code != 200:
            return
        
        titles = request.json()

        for item in titles:
            yield Completion(
                    f"id:{item['id']}",
                    start_position=-len(document.text),
                    display=item['names'].get('ru'),
                    style='bg:#e11d48 fg:#c9cbcf',
                    selected_style='bg:#c3183d fg:#c9cbcf'
                )
            
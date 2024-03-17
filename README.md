<a name="readme-top"></a>

<div align="center">

  <a style="color: #e11d48;" href="https://github.com/PersifoX/AniShotConsole">
    <bold><h1>AniShot Console</h1></bold>
  </a>
  <p align="center">
    Консольное приложение для создания скриншотов по таймкоду и названиям из Anilibria
    <br />
    <br />
  </p>
</div>

## Начало

  

Приложение требует `python` версии `3.10` и выше, а также зависимости,

описанные в `requirements.txt`. Далее - подробный гайд с установкой.
  

> Данный мануал установки является упрощенным, для тех, кто мало работал
в терминале или вовсе не знает, что это такое. Расширенная версия будет позже.

  

### Подготовка

  

Установите python на свой компьютер. Сделать это можно через [microsoft store](https://www.microsoft.com/store/productId/9PJPW5LDXLZ5?ocid=pdpshare),

Или с официального сайта, если у вас `Windows`. В случае с `Linux` хороший гайд по установке можно найти [тут](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server).

  

Убедитесь, что python корректно установлен на компьютер, нажмите правой кнопкой мыши на `windows`

и откройте `Windows PowerShell`. Впишите команду `python -V`.
Примерный вариант ответа (цифры могут отличаться в вашем случае):

  
```sh
PS C:\Users\Кефир> python -V
Python 3.11.8
```

  

### Установка

  

1. Создайте папку в любом удобном месте, мы это сделаем на рабочем столе.

2. Скачайте архив по [этой ссылке](https://github.com/PersifoX/AniShotConsole/releases/download/0.1.0/AniShotConsole.zip), или исходный код в `Realises`.

3. Распакуйте архив в вашу папку.

4. Теперь нам нужно перейти в терминале в нашу папку.
    Введем команду в раннее открытый терминал (пример, если папка названа `AniShot`):

*sh
```sh
PS C:\Users\Кефир> cd Desktop/AniShot
```

5. Установим все зависимости. Просто скопируйте команду

`python -m pip install -r requirements.txt` в терминал:

```sh
 PS C:\Users\Кефир\Desktop\AniShot> python -m pip install -r requirements.txt
```

6. Если в терминале не появилось красного текста, процесс установки можно считать успешным.

  

## Использование

Для запуска используем команду `python main.py`:

```sh
 PS C:\Users\Кефир\Desktop\AniShot> python main.py
```

Нас встретит меню, где описаны основные клавиши взаимодействия:

> **Правый клик** - вставить текст из буфера обмена
**CTRL C** - аналогично "назад"

> Выбирать из списка нужно с помощью стрелочек *вверх* и *вниз*.
Чтобы подтвердить выбор, нажмите **Enter**.

Начните вводить название и немного подождите - AniShot предложит вам варианты.
Выберите нужный стрелочками и нажмите enter.

```sh
By persifox | github.com/PersifoX/AniShotConsole

RIGHT CLICK для вставки из буфера
CTRL + C    для возврата назад

Начните писать название аниме: Sousou
                                    > Провожающая в последний путь Фрирен  
                                      Сумасшедшая столица                  
                                      Бредовый ежемесячный журнал          
```

Далее нужно выбрать серию. Напишите ее номер и также нажмите **enter**.

```sh
[AniShot] Выбран профиль для Провожающая в последний путь Фрирен
Номер серии: 12
```

После этого AniShot попросит вас написать таймкод момента, который вы хотите сохранить.
!В некоторых моментах AniShot может не сохранить момент, будет исправлено в следующей
версии.

```sh
[AniShot] Выбран профиль для Провожающая в последний путь Фрирен
таймкод: 12:48
```

После этого AniShot попросит название для новой картинки. Вы можете просто нажать enter, в таком случае скриншот сохранится в предложенном названии:

```sh
[AniShot] Выбран профиль для Провожающая в последний путь Фрирен
[h264 @ 000002512dd41b40] co located POCs unavailable
[h264 @ 000002512dca9180] mmco: unref short failure  
Название изображения: sousou-no-frieren.jpg
```

Далее Anishot будет снова просить таймкод этой серии до того момента, пока вы не нажмете **CTRL C**. В таком случае вас попросят снова выбрать серию:

```sh
[CTRL + C] Замена серии...
Номер серии: 12
```

Нажмите **CTRL C** еще раз и AniShot предложит сменить профиль аниме:

```sh
[CTRL + C] Замена серии...

[CTRL + C] Замена профиля аниме...
Начните писать название аниме: Sousou no Frieren
```

После того, как вы сделали все скриншоты, снова нажмите **CTRL C** и AniShot завершит свою работу:

```sh
[CTRL + C] Замена серии...

[CTRL + C] Замена профиля аниме...

[CTRL + C] Все скриншоты сохранены в эту папку, завершение работы.
```

Все изображения будут расположены в той же папке, что и сама программа.
### Скриншоты работы

![[Pasted image 20240317122321.png]]

![[Pasted image 20240317122353.png]]

![[Pasted image 20240317122407.png]]

## Ошибки 

### Название аниме

> Название аниме всегда нужно выбрать из списка. Если AniShot слишком долго ищет,
> Вы можете удалить последний символ и ввести его снова.

### Номер серии

> Номер серии должен быть в аниме, это логично. Значения больше последней серии 
> AniShot попросту не примет.

### Таймкод

> Таймкоды также должны быть в правильном формате MM:SS (фильмы пока что не поддерживаются, исправлю в новой версии).

### Если не предлагает ввести имя изображения

> Значит, что не получилось создать скриншот на этом моменте. Попробуйте ввести таймкод 
> на секунду раньше / позже.
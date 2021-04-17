# BC pure python CSV test api

Тестовое API для поиска в *.csv-файле

### Dependencies

* python 3.8+
* *.csv-файл определённого формата

### CSV format

API разработано для работы с *.csv-файлами следующего формата:

|Product   |Related Product|Rank |
|:--------:|:-------------:|:---:|
|JasdjiwM54|kmMsad772Z     |0.9  |
|Clsadj5Aqw|cA54Qee23d     |0.4  |
|5askdS85Ac|sdjU00ASdc     |0.7  |

### Local certificate for https

Для создания собственного сертификата необходимо выполнить команду:

```
openssl req -newkey rsa:4096 -x509 -sha256 -days 3650 -nodes -out cert.pem -keyout key.pem
```

В ОС Windows для удобства можно выполнить команду в Git Bash.  
Путь до сгенерированных файлов необходимо указать в константах `_KEY_FILE_PATH` и `_CERT_FILE_PATH` модуля `web_api.py`.

### Предобработка исходных данных

* поместить *.csv файл в папку tmp рядом с проектом
    * Если исходный файл находится в другой директории необходимо изменить значение переменной `init_csv_path` в
      модуле `pre_treatment_csv.py`
    * Если необходимо изменить пути к результирующим файлам предобработки, то необходимо изменить значения
      переменных `sorted_csv_path` и `separated_csv_path` в модуле `pre_treatment_csv.py`.  
      __Важно!__ Значение константы `_CSV_DIR_PATH` в модуле `web_api.py` должно соответствовать значению
      переменной `separated_csv_path` в модуле `pre_treatment_csv.py`
* выполнить `python -m pre_treatment_csv.py`

### Инструкция

* запустить `python -m web_api.py`
* сделать запрос к API. Например: `https://localhost:443/product?sku=WP260qJAo6&rank=0.9`  
  _Примечание: браузер может выдать предупреждение "Ваше подключение не является закрытым". Такое поведение является
  следствием использования собственного сертификата._

### Дополнительная информация

В модуле `pre_treatment_csv.py` не ведётся контроль используемой оперативной памяти.
# Хакатон "Цифровой прорыв" 2024, международный этап
# Кейс: Система классификации электрокортикограмм
# Команда: WGHAck

## Бекенд
Для установки необходимо прописать: 
```bash
poetry install
```
Если poetry не установлен, то сначала установите его:
```bash
pip install poetry
```
Рядом с main создать папку models и поместить 
туда файлы моделей с названиями "end_model.joblib" и "start_model.joblib".
Ссылка на веса: \
[Ссылка на веса](https://drive.google.com/drive/folders/1Ms7Gu2PjV4SnxYKZ_-ckaPcMm32903tI?usp=sharing)\
После чего запустить main:
```bash
python main.py
```

Ссылка на основной репозиторий проекта:\
[Ссылка на репозиторий](https://github.com/duny-explorer/Electrocorticogram-classification-system)

Отдельным подмодулем находится фронтенд на Flutter, который работает как десктопное приложение. 

Для бекенда использовались версии Python и библиотек, которые поддерживаются на Windows 7.

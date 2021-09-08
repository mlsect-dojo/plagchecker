# plagchecker

Сервис для проверки исходного кода лабораторных на списывание. Сохраняет сданные лабораторные, сравнивает новые с имеющимися при помощи DL алгоритмов


## Структура проекта

--------------
    ├── api/                <- Webserver methods code
    ├── data/               <- The final, canonical data sets for modeling.
    ├── docs/               <- Specifications and papers
    ├── models/             <- Trained and serialized models, model sources
    ├── tests/              <- Models tests
    ├── Pipfile             <- Pipfile for the web server
    ├── LICENSE
    ├── README.md           <- The top-level README for developers using this project.
    ├── server.py           <- Web server
--------------


## Статьи про плагиат кода

- [[1]](https://arxiv.org/pdf/1902.02407.pdf) Ссылка на датасет с java кодом и 3 метода плагиата с метриками точности
- [[2]](https://arxiv.org/pdf/2102.03997.pdf) Обзор мер схожести кода, методов проверки плагиата, методов обхода проверки. Упор на "udergraduated computer science students", так что весьма related. Акцент на устойчивости алгоритмов выявления. Написали симулятор бестолкового студента - рандомно применяет методы плагиата, на созданных таким образом синтетических данных измеряли эффективность существующих алгоритмов

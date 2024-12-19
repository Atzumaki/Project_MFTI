# Project_MFTI
Основная страница сайта
![image](https://github.com/user-attachments/assets/c83843f7-0a03-47a4-8b8e-2c28c5611a0c)
Основная логика:
Изначально происходит парсинг сайта https://utv.ru/ufa с использованием библиотек requests и BeautifulSoup
Библиотека selenium нужна буквально для получения расширенной версии страницы новостей
Получаем название статьи, ссылку на её основную информацию, автора, небольшая информация о новости, дата.
Создаём базу даных и добавляем в неё всё
Далее передаём всё на сайт, заполняя его
Функционал:
Можно найти новость по заголовку
![image](https://github.com/user-attachments/assets/4cb4be05-06d2-4186-b23d-a3f055049c95)
Чтобы вернуться, можно просто задать пустую строку и нажать кнопку найти
Функционал отличный от оригинального сайта - поиск новостей по авторам:
![image](https://github.com/user-attachments/assets/82d4a8e4-b67e-4825-a97e-dc0b4e21ea46)
При нажатии кнопки читать далее переместимся в полную статью:
![image](https://github.com/user-attachments/assets/057dd3d6-815e-49c1-bf92-f6ba70ec1f5b)
Запуск проекта
1 Копировать репозиторй
git clone https://github.com/Atzumaki/Project_MFTI.git
cd Project_MFTI
2. Сделайте checkout для актульной ветки
git checkout dev
3. Запустите контейнеры с помощью файла bash скрипта build.sh(Команду писать внутри папки с проектом!)
./build.sh
4.После запуска перейдите ппо ссылке
http://localhost:5252

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict, Any
import random
import time
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

QUESTIONS = [
    {"id": 1, "text": "Для создания новой таблицы в существующей базе данных используют команду:", "options": ["NEW TABLE", "CREATE TABLE", "MAKE TABLE", "CREATE NEW TABLE"], "correct": 2},
    {"id": 2, "text": "Как расшифровывается SQL?", "options": ["structure query language", "strict question line", "strong question language", "structured query language"], "correct": 4},
    {"id": 3, "text": "Запрос для выборки всех значений из таблицы «Persons» имеет вид:", "options": ["SELECT ALL Persons", "SELECT * FROM Persons", "SELECT . [ Persons ]", "SELECT Persons.*"], "correct": 2},
    {"id": 4, "text": "Какое выражение используется для возврата только разных значений?", "options": ["SELECT DISCINCT", "SELECT DIFFERENT", "SELECT UNIQUE", "SELECT DISTINCT"], "correct": 4},
    {"id": 5, "text": "Для подсчета количества записей в таблице «Persons» используется команда:", "options": ["COUNT ROW IN Persons", "SELECT COUNT(*) FROM Persons", "SELECT ROWS FROM Persons", "GET COUNT FROM Persons"], "correct": 2},
    {"id": 6, "text": "Наиболее распространенным является тип объединения:", "options": ["INNER JOIN", "FULL JOIN", "LEFT JOIN", "RIGHT JOIN"], "correct": 1},
    {"id": 7, "text": "Что возвращает запрос SELECT * FROM Students ?", "options": ["Все записи из таблицы «Students»", "Рассчитанное суммарное количество записей в таблице «Students»", "Внутреннюю структуру таблицы «Students»", "Только первые 10 записей"], "correct": 1},
    {"id": 8, "text": "Какая агрегатная функция используется для расчета суммы?", "options": ["SUM", "AVG", "COUNT", "MAX"], "correct": 1},
    {"id": 9, "text": "Запрос для выборки первых 14 записей из таблицы «Users» имеет вид:", "options": ["SELECT Top 14 Id_Users FROM Users", "SELECT * LIMIT 14 FROM Users", "SELECT * FROM USERS", "SELECT FIRST 14 FROM Users"], "correct": 1},
    {"id": 10, "text": "Запрос, возвращающий все значения из таблицы «Countries», за исключением страны с ID=8, имеет вид:", "options": ["SELECT * FROM Countries EXP ID=8", "SELECT * FROM Countries WHERE ID!=8", "SELECT ALL FROM Countries LIMIT 8", "SELECT * FROM Countries EXCEPT ID=8"], "correct": 2},
    {"id": 11, "text": "Какой оператор используется для выборки значений в пределах заданного диапазона?", "options": ["IN", "BETWEEN", "FROM", "ORDER BY"], "correct": 2},
    {"id": 12, "text": "Для чего в SQL используется оператор ORDER BY ?", "options": ["ДЛЯ ГРУППИРОВКИ", "ДЛЯ ФИЛЬТРАЦИИ", "ДЛЯ СОРТИРОВКИ", "ДЛЯ ОБЪЕДИНЕНИЯ"], "correct": 3},
    {"id": 13, "text": "Как НЕ обозначается комментарий в SQL?", "options": ["#", "/*", "--", "//"], "correct": 4},
    {"id": 14, "text": "Сортировка по убыванию обозначается ...", "options": ["ASC", "DESC", "DOWN", "REVERSE"], "correct": 2},
    {"id": 15, "text": "Какое из следующих описаний типов является неправильным?", "options": ["NUMERIC(7,7)", "NUMERIC(3,4)", "NUMERIC(11,2)", "NUMERIC(65,34)"], "correct": 2},
    {"id": 16, "text": "Какое из следующих чисел можно внести в поле, описанное как NUMERIC(5,3)?", "options": ["16.245", "123.42", "-145.34", "1678.9"], "correct": 1},
    {"id": 17, "text": "Для определения идентификационного номера налогоплательщика (ИНН) больше всего подойдет следующее описание:", "options": ["INN CHAR(12)", "INN VARCHAR(20)", "ИНН CHAR(12)", "INN INT"], "correct": 1},
    {"id": 18, "text": "Какие данные мы получим из этого запроса? select id, date, customer_name from Orders", "options": ["Никакие, запрос составлен неверно", "Номера и даты заказов с именами заказчиков, отсортированные по 1 колонке", "Неотсортированные номера и даты всех заказов с именами заказчиков", "Номера, даты всех заказов с именами заказчиков, отсортированные по колонкам"], "correct": 3},
    {"id": 19, "text": "Есть ли ошибка в запросе? select id, date, customer_name from Orders where customer_name = Mike", "options": ["Запрос составлен правильно", "Нужно убрать лишние поля из запроса", "Строчку с where поменять местами с from", "Mike необходимо записать в кавычках 'Mike'"], "correct": 4},
    {"id": 20, "text": "Что покажет следующий запрос: select * from Orders where date between '2017-01-01' and '2017-12-31'", "options": ["Все данные по заказам, совершенным за 2017 год, за исключением 01.01.2017", "Все данные по заказам, совершенным за 2017 год, за исключением 31.12.2017", "Все данные по заказам, совершенным за 2017 год", "Ничего, запрос составлен неверно"], "correct": 3},
    {"id": 21, "text": "Порядок выполнения операторов AND и OR следующий:", "options": ["Сначала выполняется OR, а затем AND", "Сначала выполняется AND, а затем OR", "Порядок выполнения операторов AND и OR зависит от того, какой из них стоит 1", "Операторы AND и OR выполняются одновременно"], "correct": 2},
    {"id": 22, "text": "Что покажет следующий запрос: select id from Orders where year(date) > 2018", "options": ["номера заказов, сделанных до 2018 года", "номера заказов, сделанных в 2018 году", "номера заказов, сделанных после 2018 года", "уникальные номера заказов"], "correct": 3},
    {"id": 23, "text": "Выберите пример правильно составленного запроса с использованием агрегирующей функции SUM", "options": ["select sum(price) from Orders", "select sum(price), customer_name from Orders", "select * from Orders where price=sum()", "select sum() from Orders group by price desc"], "correct": 1},
    {"id": 24, "text": "Выберите корректно составленный запрос с функцией GROUP BY", "options": ["select count(*) from Orders GROUP seller_id", "select seller_id, count(*) from Orders GROUP seller_id", "select seller_id, count(*) from Orders GROUP BY seller_id", "select count(*) from Orders GROUP ON seller_id"], "correct": 3},
    {"id": 25, "text": "Что такое JOIN?", "options": ["операция группировки", "операция объединения", "операция суммирования", "операция создания"], "correct": 2},
    {"id": 26, "text": "Какого строкового типа данных нет в SQL:", "options": ["VARCHAR", "STRING", "CHAR", "TEXT"], "correct": 2},
    {"id": 27, "text": "Что такое конкатинация?", "options": ["группировка", "присоединение значений друг к другу", "вычисляемое поле", "объединение таблиц"], "correct": 2},
    {"id": 28, "text": "Какой из операторов фильтрует строки?", "options": ["HAVING", "WHERE", "GROUP BY", "SELECT"], "correct": 2},
    {"id": 29, "text": "Какой из операторов фильтрует группы?", "options": ["HAVING", "WHERE", "GROUP BY", "SELECT"], "correct": 1},
    {"id": 30, "text": "Какой из операторов используется только с GROUP BY?", "options": ["HAVING", "WHERE", "GROUP BY", "SELECT"], "correct": 1},
    {"id": 31, "text": "Что означает выражение GROUP BY 2,1 ?", "options": ["сортировку по второму извлекаемому столбцу, а затем по первому", "группировку по второму извлекаемому столбцу, а затем по первому", "сортировку по второй извлекаемой строке, а затем по первой", "группировка по второй извлекаемой строке, а затем по первой"], "correct": 2},
    {"id": 32, "text": "Выберите правильный порядок следования предложений в инструкции SELECT", "options": ["SELECT, WHERE, FROM", "SELECT, FROM, WHERE", "FROM, SELECT, WHERE", "WHERE, GROUP BY, FROM"], "correct": 2},
    {"id": 33, "text": "Сколько столбцов может возвращать инструкция SELECT в подзапросах?", "options": ["1", "2", "3", "4"], "correct": 1},
    {"id": 34, "text": "Выберите корректно написанный запрос с использованием подзапроса, который выводит инфу о заказе с самой дорогой стоимостью", "options": ["select * from Orders where price = (select big(price) from Orders)", "select * from Orders where price = max", "select * from Orders where price = (select max(price) from Orders)", "select count(*) from Orders"], "correct": 3},
    {"id": 35, "text": "Выберите правильный пример запроса с использованием UNION", "options": ["select id, city from Orders order by id union select id, city from Sellers", "select id, city, seller_id from Orders and select city, id from Sellers ord", "Все запросы верные", "select id, city from Orders union select id, city from Sellers order by id"], "correct": 4},
    {"id": 36, "text": "Чем отличается CHAR и VARCHAR?", "options": ["Это одно и то же", "VARCHAR не существует", "CHAR - это тип данных, а VARCHAR - подтип", "CHAR дополняет строку пробелами, а VARCHAR тратит память на хранение значения"], "correct": 4},
    {"id": 37, "text": "Как получить значение текущего года в SQL?", "options": ["select now();", "select year();", "select year(now());", "select year from Date;"], "correct": 3},
    {"id": 38, "text": "Какая функция используется для получения текущей даты в SSMS?", "options": ["CURDATE", "SYSDATE", "GETDATE", "DATE"], "correct": 3},
    {"id": 39, "text": "Функция RTRIM выполняет", "options": ["удаляет пробелы в правой части строки", "удаляет пробелы в левой части строки", "преобразует строку в верхний регистр", "возвращает символы из правой части строки"], "correct": 1},
    {"id": 40, "text": "Как правильно добавить строку в таблицу? Какой запрос верный?", "options": ["INSERT INTO `SimpleTable` (`some_text`) VALUES (\"my text\");", "INSERT INTO `SimpleTable` SET `some_text`=\"my text\";", "SET INTO `SimpleTable` VALUE `some_text`=\"my text\";", "UPDATE INTO `SimpleTable` SET `some_text`=\"my text\";"], "correct": 1},
    {"id": 41, "text": "Какие поля из таблицы обязательно перечислять в INSERT для вставки данных?", "options": ["Конечно все", "Только те, у которых нет DEFAULT значения", "Те, у которых нет DEFAULT значения и которые не имеют атрибут auto_increment", "Все поля имеют негласное DEFAULT значения, обязательных полей в SQL нет"], "correct": 3},
    {"id": 42, "text": "Как сделать несколько записей в таблицу за один запрос?", "options": ["Использовать MULTI INSERT INTO вместо INSERT INTO", "Использовать подзапрос", "Перечислить через запятую все наборы значений после VALUES", "Никак, расходимся по домам"], "correct": 3},
    {"id": 43, "text": "Зачем существует команда UPDATE, если можно сначала удалить запись, а потом добавить новую, исправленную.", "options": ["Именно так и делаю, UPDATE не использую", "Удалять записи в SQL нельзя, поэтому используется UPDATE с NULL для полей", "Так меньше нагрузки на базу, ведь команда одна, а не две", "в записи могут быть автоматически проставляемые поля"], "correct": 4},
    {"id": 44, "text": "Можно ли поменять тип данных поля в уже существующей таблице?", "options": ["Да, достаточно сделать INSERT с новым типом данных", "Да, при помощи команды ALTER", "Нет, только пересоздать таблицу", "Тип бывает только у таблицы, а не у поля таблицы"], "correct": 2},
    {"id": 45, "text": "Какие метасимволы НЕ используются в SSMS?", "options": ["*", "%", "_", "[ ]"], "correct": 1},
    {"id": 46, "text": "Что показывает функция COUNT?", "options": ["среднее значение по столбцу", "число столбцов в таблице", "наибольшее значение в столбце", "число строк в столбце"], "correct": 4},
    {"id": 47, "text": "Аргумент DISTINCT применяется для...", "options": ["вывода строк со значением NULL", "вывода уникальных строк", "вывода ключевых полей", "игнорирования пустых строк"], "correct": 2},
    {"id": 48, "text": "Инструкция INSERT INTO выполняет", "options": ["импорт данных", "экспорт данных"], "correct": 1},
    {"id": 49, "text": "Инструкция SELECT INTO выполняет", "options": ["импорт данных", "экспорт данных"], "correct": 2},
    {"id": 50, "text": "Как изменить значение \"Hansen\" на \"Nilsen\" в колонке \"LastName\", таблицы Persons?", "options": ["MODIFY Persons SET LastName='Hansen' INTO LastName='Nilsen'", "UPDATE Persons SET LastName='Nilsen' WHERE LastName='Hansen'", "MODIFY Persons SET LastName='Nilsen' WHERE LastName='Hansen'", "UPDATE Persons SET LastName='Hansen' INTO LastName='Nilsen'"], "correct": 2},
    {"id": 51, "text": "Что выполняет команда Drop Table?", "options": ["Удаляет только пустую таблицу базы данных", "Создают пустую таблицу", "Удаляет любую таблицу базы данных", "Удаляет только структуру таблицы"], "correct": 3},
    {"id": 52, "text": "Банк данных – это…", "options": ["Разновидность информационной системы", "Разновидность базы данных", "Разновидность системы управления базами данных", "Разновидность объекта данных"], "correct": 1},
    {"id": 53, "text": "Начальная стадия проектирования системы базы данных заключается в построении", "options": ["Инфологической модели данных", "Датологической модели данных", "Физической модели данных", "Логической модели"], "correct": 1},
    {"id": 54, "text": "Компонентом банка данных НЕ является…", "options": ["База данных", "Вычислительная система", "Информационная система", "Администратор банка данных"], "correct": 3},
    {"id": 55, "text": "Комплекс языковых и программных средств, предназначенный для создания, ведения и использования…", "options": ["Информационная система", "Система управления базами данных", "Система поддержки принятия решений", "Система управления базами данных, относящаяся к серверам баз данных"], "correct": 2},
    {"id": 56, "text": "Значение выражения 0,7-3>2 относится к следующему типу данных:", "options": ["числовому", "логическому", "символьному", "текстовому"], "correct": 2},
    {"id": 57, "text": "К символьному типу данных относится атрибут…", "options": ["Адрес", "Фотография", "Количество товара", "Дата рождения"], "correct": 1},
    {"id": 58, "text": "К двоичному типу данных относится атрибут…", "options": ["Наличие автомобиля", "Образец росписи", "Количество порций", "Название альбома"], "correct": 2},
    {"id": 59, "text": "К структурированному типу данных относится:", "options": ["Запись", "Дата-Время", "Символьный переменной длины", "Числовой целый"], "correct": 1},
    {"id": 60, "text": "Формой представления иерархической модели данных является:", "options": ["Таблица", "Дерево", "Сеть", "Схема"], "correct": 2},
    {"id": 61, "text": "Примером иерархической базы данных является:", "options": ["страница классного журнала", "каталог файлов, хранимых на диске", "расписание поездов", "электронная таблица"], "correct": 2},
    {"id": 62, "text": "Формой представления реляционной модели данных является", "options": ["Гиперкуб", "Дерево", "Таблица", "Сеть"], "correct": 3},
    {"id": 63, "text": "Система управления базами данных MS SQL Server работает с моделью данных…", "options": ["иерархической", "постреляционной", "Объектно-ориентированной", "Реляционной"], "correct": 4},
    {"id": 64, "text": "В записи реляционной базы данных может содержаться:", "options": ["неоднородная информация (данные разных типов)", "исключительно однородная информация (данные только одного типа)", "только текстовая информация", "исключительно числовая информация"], "correct": 1},
    {"id": 65, "text": "В поле реляционной базы данных могут быть записаны:", "options": ["только номера записей", "как числовые, так и текстовые данные одновременно", "данные только одного типа", "только время создания записей"], "correct": 3},
    {"id": 66, "text": "В реляционной модели данных строка в таблице:", "options": ["Атрибут", "Схема отношения", "Значение атрибута", "Кортеж"], "correct": 4},
    {"id": 67, "text": "В реляционной модели данных столбец в таблице:", "options": ["Поле", "Схема отношения", "Отношение", "Кортеж"], "correct": 1},
    {"id": 68, "text": "Доменом называется…", "options": ["множество всех возможных значений определенного атрибута отношения", "тип данных определенного атрибута отношения", "содержимое ячейки в отношении", "заголовок столбца в отношении"], "correct": 1},
    {"id": 69, "text": "Реляционная модель данных НЕ допускает…", "options": ["Размещения однотипных данных в таблице", "Повторяющихся значений в неключевых атрибутах", "Дублирования столбцов", "Внесения изменений в названия атрибутов"], "correct": 3},
    {"id": 70, "text": "Даны таблицы. Внешним ключом является…", "options": ["Код предмета в таблице ПРЕДМЕТ", "Код экзамена в таблице ЭКЗАМЕН", "Код предмета в таблице ЭКЗАМЕН", "Предмет в таблице ПРЕДМЕТ"], "correct": 3},
    {"id": 71, "text": "Даны таблицы. Внешним ключом является…", "options": ["Номер детского сада в таблице ДЕТСКИЙ САД", "Св-во о рождении в таблице РЕБЕНОК", "Телефон в таблице ДЕТСКИЙ САД", "Номер детского сада в таблице РЕБЕНОК"], "correct": 4},
    {"id": 72, "text": "Видом связи между таблицами, когда одной записи основной таблицы соответствует несколько записей подчиненной является…", "options": ["1:1", "1:М", "М:М"], "correct": 2},
    {"id": 73, "text": "Связь между таблицами, когда нескольким записям основной таблицы соответствует несколько записей подчиненной называется…", "options": ["1:1", "1:М", "М:М"], "correct": 3},
    {"id": 74, "text": "Дана таблица. Первичным ключом таблицы является …", "options": ["Цена товара", "Код заказанного товара", "Фирма заказчик + Код заказанного товара", "Фирма заказчик + Цена товара"], "correct": 3},
    {"id": 75, "text": "Дана таблица. Первичным ключом таблицы является …", "options": ["№ квартиры", "№ квартиры + Вид заказанных работ", "Вид заказанных работ", "Дата выполнения + Цена работы"], "correct": 2},
    {"id": 76, "text": "Определите роль языка SQL в создании информационных систем.", "options": ["Разработка структуры БД", "Организация пользовательского интерфейса", "Обеспечение различных представлений данных", "Преобразование данных"], "correct": 1}
]

QUESTIONS += [
    # 77. Оконные функции
    {"id": 77, "text": "Какая оконная функция присваивает уникальные номера строкам в партиции БЕЗ пропусков при одинаковых значениях ORDER BY?", "options": ["ROW_NUMBER()", "RANK()", "DENSE_RANK()", "NTILE(4)"], "correct": 3},
    
    # 78. Рекурсивные CTE
    {"id": 78, "text": "Какой синтаксис используется для создания рекурсивного CTE в PostgreSQL?", "options": ["WITH RECURSIVE cte AS (...)", "RECURSIVE CTE (...)", "CTE RECURSIVE (...)", "WITH cte RECURSIVE (...)"], "correct": 1},
    
    # 79. Уровни изоляции
    {"id": 79, "text": "Какой уровень изоляции в PostgreSQL предотвращает 'фантомные чтения'?", "options": ["READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE", "READ UNCOMMITTED"], "correct": 3},
    
    # 80. Индексы
    {"id": 80, "text": "Для запроса WHERE status = 'active' AND created_at > '2023-01-01' оптимальный составной индекс:", "options": ["(status, created_at)", "(created_at, status)", "(status)", "(created_at)"], "correct": 1},
    
    # 81. EXPLAIN ANALYZE
    {"id": 81, "text": "Что означает 'Bitmap Heap Scan' в плане выполнения PostgreSQL?", "options": ["Последовательное чтение таблицы", "Чтение данных через битовую карту индексов", "Соединение по хешу", "Сортировка результатов"], "correct": 2},
    
    # 82. JSON в SQL
    {"id": 82, "text": "Как извлечь значение как текст из JSON-поля 'data' по ключу 'name' в PostgreSQL?", "options": ["data->'name'", "data->>'name'", "JSON_EXTRACT(data, '$.name')", "data#>>'{name}'"], "correct": 2},
    
    # 83. Полнотекстовый поиск
    {"id": 83, "text": "Какой оператор используется для поиска похожих слов в полнотекстовом поиске PostgreSQL?", "options": ["@", "!!", "<->", ":*"], "correct": 4},
    
    # 84. Безопасность
    {"id": 84, "text": "Что делает команда REVOKE SELECT ON orders FROM analyst;", "options": ["Запрещает пользователю analyst читать таблицу orders", "Удаляет права на выполнение SELECT для всех", "Создает новую роль analyst без прав", "Отзывает права на удаление записей"], "correct": 1},
    
    # 85. Временные ряды
    {"id": 85, "text": "Какая функция TimescaleDB оптимизирована для анализа временных рядов?", "options": ["time_bucket()", "date_trunc()", "generate_series()", "window_frame()"], "correct": 1},
    
    # 86. Обработка NULL
    {"id": 86, "text": "Какая функция вернет первое ненулевое значение из списка (NULL, 10, 20)?", "options": ["NULLIF(10,20)", "COALESCE(NULL,10,20)", "ISNULL(10,NULL)", "NVL2(NULL,10,20)"], "correct": 2},
    
    # 87. PIVOT
    {"id": 87, "text": "Как в T-SQL транспонировать строки в столбцы для агрегации продаж по регионам?", "options": ["Использовать оператор PIVOT", "CASE WHEN с группировкой", "CROSS APPLY", "STRING_AGG"], "correct": 1},
    
    # 88. Материализованные представления
    {"id": 88, "text": "Как обновить данные в материализованном представлении PostgreSQL?", "options": ["REFRESH MATERIALIZED VIEW sales_summary", "UPDATE VIEW sales_summary", "REBUILD VIEW sales_summary", "RECREATE MATERIALIZED VIEW sales_summary"], "correct": 1},
    
    # 89. FDW (Foreign Data Wrapper)
    {"id": 89, "text": "Какой механизм PostgreSQL позволяет запросить данные из удаленной базы MySQL?", "options": ["pg_dump", "dblink", "postgres_fdw", "mysql_fdw"], "correct": 4},
    
    # 90. PostGIS
    {"id": 90, "text": "Какая функция PostGIS вычисляет расстояние между двумя точками в метрах?", "options": ["ST_Distance()", "ST_Length()", "ST_Distance_Sphere()", "ST_Meters()"], "correct": 3},
    
    # 91. Системные представления
    {"id": 91, "text": "Как получить список активных сессий в PostgreSQL через системные таблицы?", "options": ["SELECT * FROM pg_stat_activity", "SHOW PROCESSLIST", "SELECT * FROM information_schema.processes", "pg_active_sessions()"], "correct": 1},
    
    # 92. Стринговые функции
    {"id": 92, "text": "Как объединить имена пользователей в одну строку через запятую в группе?", "options": ["STRING_AGG(username, ',')", "GROUP_CONCAT(username)", "CONCAT_WS(',', username)", "ARRAY_TO_STRING(ARRAY_AGG(username), ',')"], "correct": 1},
    
    # 93. Обработка ошибок
    {"id": 93, "text": "Как в PL/pgSQL перехватить ошибку при делении на ноль?", "options": ["EXCEPTION WHEN division_by_zero THEN", "TRY...CATCH", "BEGIN...EXCEPTION division_by_zero", "ON ERROR CONTINUE"], "correct": 1},
    
    # 94. CTE
    {"id": 94, "text": "Может ли рекурсивный CTE ссылаться на самого себя в нескольких частях запроса?", "options": ["Нет, только в одном месте", "Да, в любом количестве", "Только через UNION ALL", "Только в подзапросах"], "correct": 3},
    
    # 95. Триггеры
    {"id": 95, "text": "Какой тип триггера сработает ПОСЛЕ изменения данных, но ДО фиксации транзакции?", "options": ["BEFORE", "AFTER", "INSTEAD OF", "DEFERRABLE"], "correct": 2},
    
    # 96. Партиционирование
    {"id": 96, "text": "Какой тип партиционирования оптимален для таблицы логов с временной меткой?", "options": ["LIST", "RANGE", "HASH", "COMPOSITE"], "correct": 2},
    
    # 97. Хранимые процедуры
    {"id": 97, "text": "Как передать OUT-параметр в хранимой процедуре PostgreSQL?", "options": ["CREATE PROCEDURE p(OUT result INT)", "CREATE FUNCTION p() RETURNS INT", "CALL p(result => ?)", "Использовать RETURN"], "correct": 1},
    
    # 98. Транзакции
    {"id": 98, "text": "Что произойдет при выполнении ROLLBACK в транзакции с уровнем изоляции SERIALIZABLE?", "options": ["Все изменения отменятся", "Только часть изменений отменится", "Транзакция перезапустится автоматически", "Произойдет взаимная блокировка"], "correct": 1},
    
    # 99. Оконные функции (продвинутый)
    {"id": 99, "text": "Как вычислить скользящее среднее за последние 3 дня с использованием оконной функции?", "options": ["AVG(sales) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)", "SUM(sales) OVER (PARTITION BY date)", "ROLLING_AVG(sales, 3)", "MEAN(sales, 3) OVER date"], "correct": 1},
    
    # 100. Индексы (продвинутый)
    {"id": 100, "text": "Для запроса WHERE category = 'books' AND price BETWEEN 10 AND 50 какой частичный индекс будет эффективен?", "options": ["CREATE INDEX idx ON products (price) WHERE category = 'books'", "CREATE INDEX idx ON products (category, price)", "CREATE INDEX idx ON products (price)", "CREATE INDEX idx ON products (category)"], "correct": 1}
]

# Хранилище активных сессий
active_test = {}

@app.get("/", response_class=HTMLResponse)
def start_page(request: Request):
    return templates.TemplateResponse("start.html", {"request": request})

@app.post("/start")
def start_test():
    selected = random.sample(QUESTIONS, 30)
    test_id = str(int(time.time()))
    active_test[test_id] = {
        "questions": selected,
        "start_time": time.time(),
        "answers": {}
    }
    return RedirectResponse(url=f"/test/{test_id}", status_code=303)

@app.get("/test/{test_id}", response_class=HTMLResponse)
def show_test(request: Request, test_id: str):
    if test_id not in active_test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    session = active_test[test_id]
    elapsed = time.time() - session["start_time"]
    if elapsed > 600:  # 10 минут = 600 сек
        return RedirectResponse(url=f"/result/{test_id}", status_code=303)
    return templates.TemplateResponse("test.html", {
        "request": request,
        "test_id": test_id,
        "questions": session["questions"],
        "time_left": max(0, 600 - int(elapsed))
    })

# ОБРАБОТЧИК ДЛЯ ФОРМЫ
@app.post("/submit/{test_id}")
async def submit_test(test_id: str, request: Request):
    if test_id not in active_test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    
    # Получаем данные формы напрямую
    form_data = await request.form()
    answers = {}
    for key, value in form_data.items():
        if key.isdigit() and value.isdigit():
            answers[int(key)] = int(value)
    
    session = active_test[test_id]
    session["answers"] = answers
    return RedirectResponse(url=f"/result/{test_id}", status_code=303)

@app.get("/result/{test_id}", response_class=HTMLResponse)
def show_result(request: Request, test_id: str):
    if test_id not in active_test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    session = active_test[test_id]
    questions = session["questions"]
    user_answers = session.get("answers", {})
    results = []
    correct_count = 0
    
    for q in questions:
        qid = q["id"]
        user_ans = user_answers.get(qid, None)
        correct_ans = q["correct"]
        is_correct = (user_ans == correct_ans)
        
        if is_correct:
            correct_count += 1
            
        results.append({
            "question": q["text"],
            "options": q["options"],
            "user_answer": user_ans,
            "correct_answer": correct_ans,
            "is_correct": is_correct
        })
    
    score = round(correct_count / len(questions) * 100, 1)
    return templates.TemplateResponse("result.html", {
        "request": request,
        "results": results,
        "score": score,
        "total": len(questions),
        "correct": correct_count,
        "test_id": test_id
    })

@app.post("/restart")
def restart():
    return RedirectResponse(url="/", status_code=303)
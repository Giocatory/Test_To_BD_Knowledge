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

QUESTIONS += [
    # 101. Параллельное выполнение запросов
    {"id": 101, "text": "Как в PostgreSQL включить параллельное выполнение для агрегатных функций?", "options": ["SET max_parallel_workers_per_gather = 4;", "ENABLE PARALLEL QUERY;", "ALTER SYSTEM SET parallel_aggregate = true;", "Использовать PARALLEL HINT"], "correct": 1},
    
    # 102. Гипертаблицы TimescaleDB
    {"id": 102, "text": "Что такое chunk в гипертаблице TimescaleDB?", "options": ["Отдельная таблица для каждого интервала времени", "Индекс для временных данных", "Раздел партиции по хешу", "Кэш для агрегатов"], "correct": 1},
    
    # 103. Репликация
    {"id": 103, "text": "Какой тип репликации в PostgreSQL позволяет читать данные с реплики?", "options": ["Логическая репликация", "Физическая репликация", "Синхронная репликация", "Асинхронная репликация"], "correct": 2},
    
    # 104. Хранимые процедуры
    {"id": 104, "text": "Как вернуть табличный результат из хранимой процедуры в PostgreSQL?", "options": ["RETURNS TABLE", "OUT параметры", "RETURN QUERY", "SETOF record"], "correct": 3},
    
    # 105. Миграции
    {"id": 105, "text": "Что делает миграция с idempotent = true в Flyway?", "options": ["Запускается только один раз", "Можно запускать многократно без ошибок", "Откатывается автоматически при ошибке", "Не влияет на данные"], "correct": 2},
    
    # 106. Безопасность
    {"id": 106, "text": "Как защититься от атаки 'time-based SQL injection'?", "options": ["Использовать параметризованные запросы", "Ограничить время выполнения запроса", "Отключить UNION операторы", "Включить strict mode"], "correct": 2},
    
    # 107. OLAP-функции
    {"id": 107, "text": "Как вычислить процентное изменение продаж относительно предыдущего периода?", "options": ["(sales - LAG(sales) OVER (ORDER BY date)) / LAG(sales) OVER (ORDER BY date)", "PERCENT_CHANGE(sales)", "sales / PREV(sales) - 1", "Использовать PCT_CHANGE()"], "correct": 1},
    
    # 108. Индексы
    {"id": 108, "text": "Для какого случая оптимален BRIN-индекс в PostgreSQL?", "options": ["Маленькие таблицы с частыми обновлениями", "Большие таблицы с упорядоченными данными (временные ряды)", "Таблицы с высокой кардинальностью", "JSONB-колонки"], "correct": 2},
    
    # 109. JSON
    {"id": 109, "text": "Как в MySQL создать виртуальный генерируемый столбец для JSON-поля 'data' -> '$.price'?", "options": ["ALTER TABLE orders ADD price INT AS (JSON_UNQUOTE(JSON_EXTRACT(data, '$.price'))) VIRTUAL;", "CREATE INDEX idx_price ON orders (data->'$.price');", "ADD COLUMN price GENERATED ALWAYS AS (data->'$.price')", "Использовать JSON_TABLE()"], "correct": 1},
    
    # 110. Блокировки
    {"id": 110, "text": "Какой тип блокировки возникает при SELECT FOR UPDATE в REPEATABLE READ?", "options": ["ROW SHARE", "ROW EXCLUSIVE", "SHARE UPDATE EXCLUSIVE", "ACCESS EXCLUSIVE"], "correct": 2},
    
    # 111. Системные представления
    {"id": 111, "text": "Как найти неиспользуемые индексы в PostgreSQL?", "options": ["SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;", "pg_unused_indexes()", "EXPLAIN ANALYZE без использования индекса", "pg_stat_reset()"], "correct": 1},
    
    # 112. Репликация данных
    {"id": 112, "text": "Что такое WAL в контексте PostgreSQL?", "options": ["Write-Ahead Logging", "Web Application Layer", "Weighted Average Load", "Windows Authentication Library"], "correct": 1},
    
    # 113. Оконные функции
    {"id": 113, "text": "Какое поведение у RANGE vs ROWS в оконных функциях?", "options": ["RANGE использует значения, ROWS - физические строки", "ROWS работает только с датами", "RANGE не поддерживает PRECEDING", "Нет разницы"], "correct": 1},
    
    # 114. Триггеры
    {"id": 114, "text": "Какой триггер сработает при выполнении UPDATE только если изменилось поле 'price'?", "options": ["WHEN (OLD.price IS DISTINCT FROM NEW.price)", "IF UPDATE(price) THEN", "ON CHANGE OF price", "WHEN (price CHANGED)"], "correct": 1},
    
    # 115. Полнотекстовый поиск
    {"id": 115, "text": "Как в PostgreSQL настроить веса для разных полей в полнотекстовом поиске?", "options": ["setweight(to_tsvector('english', title), 'A') || setweight(to_tsvector('english', body), 'B')", "CONFIGURE WEIGHTS (title=0.7, body=0.3)", "USING WEIGHT(title, 1.0) + WEIGHT(body, 0.5)", "Веса настраиваются в конфигурации словаря"], "correct": 1},
    
    # 116. Оптимизация
    {"id": 116, "text": "Какой хинт в Oracle принудительно использует индекс для таблицы?", "options": ["/*+ INDEX(orders idx_orders_date) */", "FORCE INDEX idx_orders_date", "USE INDEX(idx_orders_date)", "HINT INDEX = idx_orders_date"], "correct": 1},
    
    # 117. Геоданные
    {"id": 117, "text": "Как найти все точки в радиусе 10 км от заданных координат в PostGIS?", "options": ["ST_DWithin(location, ST_Point(37.6,55.7)::geography, 10000)", "ST_Buffer(ST_Point(37.6,55.7), 10)", "ST_Distance(location, ST_Point(37.6,55.7)) < 10", "ST_Contains(ST_Buffer(...), location)"], "correct": 1},
    
    # 118. Распределенные транзакции
    {"id": 118, "text": "Что такое двухфазный коммит (2PC)?", "options": ["Протокол для распределенных транзакций", "Метод репликации данных", "Тип блокировки в БД", "Алгоритм сжатия WAL"], "correct": 1},
    
    # 119. Материализованные представления
    {"id": 119, "text": "Как часто обновлять материализованное представление для отчетов в реальном времени?", "options": ["Каждые 5 минут через cron", "При каждом изменении исходных данных через триггеры", "Использовать Continuous Aggregates в TimescaleDB", "Только вручную"], "correct": 3},
    
    # 120. Шардинг
    {"id": 120, "text": "Какой ключ шардирования оптимален для таблицы пользователей с глобальным распределением?", "options": ["user_id (хеш)", "country_code (лист)", "created_at (диапазон)", "email_domain (хеш)"], "correct": 1},
    
    # 121. Сравнение СУБД
    {"id": 121, "text": "Какая СУБД поддерживает нативные JSON-документы с индексацией вложенных полей?", "options": ["MongoDB", "MySQL 8.0+", "PostgreSQL с jsonb", "Все перечисленные"], "correct": 4},
    
    # 122. Временные таблицы
    {"id": 122, "text": "Чем отличается TEMPORARY TABLE от UNLOGGED TABLE в PostgreSQL?", "options": ["TEMP таблицы существуют только в сессии, UNLOGGED - постоянно но без WAL", "UNLOGGED работает быстрее, но данные теряются при сбое", "TEMP таблицы видны только в транзакции", "Нет разницы"], "correct": 1},
    
    # 123. Аудит
    {"id": 123, "text": "Как отследить все DELETE операции в таблице без триггеров?", "options": ["pgAudit расширение", "Включить лог минимума", "Использовать логический декодинг", "Все варианты верны"], "correct": 4},
    
    # 124. Производительность
    {"id": 124, "text": "Что означает 'Seq Scan' в EXPLAIN ANALYZE?", "options": ["Последовательное чтение таблицы", "Сканирование по индексу", "Соединение по последовательности", "Сортировка результатов"], "correct": 1},
    
    # 125. Работа с NULL
    {"id": 125, "text": "Какой результат: SELECT 1 WHERE NULL = NULL?", "options": ["0 строк", "1 строка", "Ошибка", "Зависит от настроек ANSI_NULLS"], "correct": 1},
    
    # 126. Параметризованные запросы
    {"id": 126, "text": "Почему параметризованные запросы защищают от SQL-инъекций?", "options": ["Данные передаются отдельно от команд", "Экранируют все спецсимволы", "Проверяют типы данных", "Ограничивают длину ввода"], "correct": 1},
    
    # 127. Миграции схемы
    {"id": 127, "text": "Как безопасно добавить NOT NULL столбец в большую таблицу?", "options": ["Добавить с DEFAULT значением, затем убрать DEFAULT", "Использовать ONLINE DDL в MySQL", "Создать новую таблицу и перенести данные", "Все варианты верны"], "correct": 4},
    
    # 128. Системные функции
    {"id": 128, "text": "Как получить информацию о блокировках в PostgreSQL?", "options": ["SELECT * FROM pg_locks;", "pg_blocking_pids()", "SHOW LOCKS;", "pg_stat_activity с wait_event_type = 'Lock'"], "correct": 4},
    
    # 129. CTE
    {"id": 129, "text": "Может ли CTE быть материализован в PostgreSQL?", "options": ["Да, при использовании материализованного представления", "Нет, всегда переписывается в подзапрос", "Да, если используется несколько раз в запросе", "Только в Oracle"], "correct": 3},
    
    # 130. Сравнение данных
    {"id": 130, "text": "Как проверить идентичность данных в двух таблицах с одинаковой структурой?", "options": ["EXCEPT оператор", "FULL OUTER JOIN с фильтром на различия", "Хеширование всех строк", "Все варианты верны"], "correct": 4},
    
    # 131. Оконные функции
    {"id": 131, "text": "Какая функция возвращает значение из следующей строки в окне?", "options": ["LEAD()", "LAG()", "FIRST_VALUE()", "NTH_VALUE()"], "correct": 1},
    
    # 132. Индексы
    {"id": 132, "text": "Для запроса с ILIKE '%text%' какой индекс будет эффективен в PostgreSQL?", "options": ["GIN с pg_trgm", "BTREE с lowercase()", "SP-GiST", "Ни один индекс не поможет"], "correct": 1},
    
    # 133. Репликация
    {"id": 133, "text": "Что такое 'логический декодинг' в PostgreSQL?", "options": ["Преобразование WAL в логические изменения", "Шифрование WAL", "Декодирование бинарных данных", "Компиляция PL/pgSQL функций"], "correct": 1},
    
    # 134. Безопасность
    {"id": 134, "text": "Как ограничить доступ к столбцу 'salary' только для HR-менеджеров?", "options": ["Row-Level Security (RLS)", "Создать представление без этого столбца", "GRANT SELECT на столбец конкретной роли", "Все варианты верны"], "correct": 4},
    
    # 135. JSON
    {"id": 135, "text": "Как эффективно искать по массиву тегов в JSONB поле?", "options": ["GIN индекс с оператором @>", "BTREE индекс на jsonb_array_elements()", "FULLTEXT поиск по тегам", "Нормализовать данные в отдельную таблицу"], "correct": 1},
    
    # 136. Партиционирование
    {"id": 136, "text": "Как добавить новую партицию для диапазона дат в PostgreSQL 12+?", "options": ["CREATE TABLE partition ... PARTITION OF table;", "ALTER TABLE table ADD PARTITION ...", "pg_partman расширение", "Невозможно после создания таблицы"], "correct": 1},
    
    # 137. Хранимые процедуры
    {"id": 137, "text": "Что такое 'procedural code' в контексте СУБД?", "options": ["Хранимые процедуры и функции", "DDL скрипты", "ETL процессы", "Прикладной код приложения"], "correct": 1},
    
    # 138. Оптимизация
    {"id": 138, "text": "Как избежать N+1 проблемы в ORM?", "options": ["Eager loading связанных данных", "Использовать JOIN в запросе", "Кэширование результатов", "Все варианты верны"], "correct": 4},
    
    # 139. Временные зоны
    {"id": 139, "text": "Как сохранить timestamp с часовым поясом в PostgreSQL?", "options": ["TIMESTAMPTZ", "TIMESTAMP WITH TIME ZONE", "CONVERT TO UTC при вставке", "Хранить как BIGINT (Unix timestamp)"], "correct": 1},
    
    # 140. Сравнение СУБД
    {"id": 140, "text": "Какая СУБД поддерживает автоматическое управление партициями (AUTOMATIC PARTITIONING)?", "options": ["Oracle 19c", "PostgreSQL 15", "MySQL 8.0", "SQL Server 2022"], "correct": 1},
    
    # 141. Бекапы
    {"id": 141, "text": "Что такое PITR (Point-in-Time Recovery)?", "options": ["Восстановление к конкретному моменту времени через WAL", "Создание снапшотов на лету", "Резервное копирование только измененных блоков", "Репликация только изменений"], "correct": 1},
    
    # 142. Геопространственные данные
    {"id": 142, "text": "Какой тип данных в PostGIS используется для хранения маршрута?", "options": ["LINESTRING", "POLYGON", "MULTIPOINT", "GEOMETRYCOLLECTION"], "correct": 1},
    
    # 143. Оконные функции
    {"id": 143, "text": "Как вычислить накопительную сумму продаж по месяцам?", "options": ["SUM(sales) OVER (ORDER BY month ROWS UNBOUNDED PRECEDING)", "CUMULATIVE_SUM(sales)", "RUNNING TOTAL sales", "SUM(sales) OVER (PARTITION BY month)"], "correct": 1},
    
    # 144. Триггеры
    {"id": 144, "text": "Какой тип триггера вызывается вместо операции INSERT?", "options": ["INSTEAD OF INSERT", "BEFORE INSERT", "AFTER INSERT", "FOR EACH ROW"], "correct": 1},
    
    # 145. Индексы
    {"id": 145, "text": "Что такое 'partial index' в PostgreSQL?", "options": ["Индекс с условием WHERE", "Индекс только на часть данных", "Неполный индекс при ошибке создания", "Индекс на выражение"], "correct": 1},
    
    # 146. Безопасность
    {"id": 146, "text": "Как включить сквозное шифрование (TLS) для подключений к PostgreSQL?", "options": ["ssl = on в postgresql.conf", "Использовать sslmode=require в строке подключения", "Создать SSL сертификаты", "Все варианты верны"], "correct": 4},
    
    # 147. Материализованные представления
    {"id": 147, "text": "Что происходит при REFRESH MATERIALIZED VIEW CONCURRENTLY?", "options": ["Обновление без блокировки чтения", "Полная блокировка таблицы", "Только добавление новых данных", "Асинхронное обновление в фоне"], "correct": 1},
    
    # 148. JSON
    {"id": 148, "text": "Как объединить несколько JSON-объектов в один в PostgreSQL?", "options": ["JSONB_OBJECT_AGG()", "JSON_BUILD_OBJECT()", "JSON_MERGE()", "ARRAY_TO_JSON(ARRAY_AGG(...))"], "correct": 1},
    
    # 149. Системные представления
    {"id": 149, "text": "Как найти самые тяжелые запросы по времени выполнения в PostgreSQL?", "options": ["pg_stat_statements расширение", "pg_stat_activity с state = 'active'", "EXPLAIN ANALYZE для всех запросов", "slow_query_log"], "correct": 1},
    
    # 150. Репликация
    {"id": 150, "text": "Что такое 'логический срез' (logical slot) в PostgreSQL репликации?", "options": ["Канал для передачи логических изменений", "Слот для хранения WAL файлов", "Логическое разделение данных", "Слот для подключения реплик"], "correct": 1},
    
    # 151. Оптимизация
    {"id": 151, "text": "Какой параметр PostgreSQL управляет размером shared_buffers?", "options": ["shared_buffers", "work_mem", "maintenance_work_mem", "effective_cache_size"], "correct": 1},
    
    # 152. Временные таблицы
    {"id": 152, "text": "Когда использовать UNLOGGED TABLE вместо обычной?", "options": ["Для временных данных, которые можно потерять при сбое", "Для ускорения вставки в 3-5 раз", "Для данных сессии пользователя", "Все варианты верны"], "correct": 4},
    
    # 153. Аудит
    {"id": 153, "text": "Как отследить все изменения в таблице 'users' в течение недели?", "options": ["pgAudit + WAL архивация", "Триггеры на INSERT/UPDATE/DELETE", "Создать историческую таблицу", "Все варианты верны"], "correct": 4},
    
    # 154. Сравнение СУБД
    {"id": 154, "text": "Какая СУБД имеет встроенную поддержку векторных вычислений для аналитики?", "options": ["ClickHouse", "PostgreSQL", "MySQL", "SQLite"], "correct": 1},
    
    # 155. Полнотекстовый поиск
    {"id": 155, "text": "Как настроить поиск по ошибочным написаниям (fuzzy search) в PostgreSQL?", "options": ["pg_trgm расширение + gin_trgm_ops", "pg_similarity", "Использовать SOUNDEX()", "Включить full_text_fuzzy = on"], "correct": 1},
    
    # 156. Оконные функции
    {"id": 156, "text": "Как разделить данные на 4 равные группы по продажам?", "options": ["NTILE(4) OVER (ORDER BY sales)", "RANK() / 4", "PERCENT_RANK() * 4", "WIDTH_BUCKET(sales, 4)"], "correct": 1},
    
    # 157. Индексы
    {"id": 157, "text": "Для какого запроса оптимален GiST-индекс в PostGIS?", "options": ["Поиск точек в прямоугольнике", "Сортировка по времени", "Точные совпадения координат", "Агрегация по районам"], "correct": 1},
    
    # 158. Безопасность
    {"id": 158, "text": "Что такое 'row-level security' (RLS) в SQL Server?", "options": ["Политики доступа на уровне строк", "Шифрование отдельных строк", "Репликация только определенных строк", "Аудит изменений на уровне строк"], "correct": 1},
    
    # 159. JSON
    {"id": 159, "text": "Как в MySQL выполнить запрос к JSON-массиву в поле 'tags'?", "options": ["SELECT * FROM products WHERE JSON_CONTAINS(tags, '\"electronics\"')", "tags @> 'electronics'", "tags::jsonb ? 'electronics'", "JSON_QUERY(tags, '$[*] ? (@ == \"electronics\")')"], "correct": 1},
    
    # 160. Партиционирование
    {"id": 160, "text": "Какой тип партиционирования лучше для таблицы событий с равномерным распределением по времени?", "options": ["RANGE по дате", "LIST по типу события", "HASH по event_id", "COMPOSITE (дата + тип)"], "correct": 1},
    
    # 161. Хранимые процедуры
    {"id": 161, "text": "Как вызвать хранимую процедуру из приложения на Python?", "options": ["cursor.callproc('proc_name', [params])", "EXECUTE proc_name", "CALL proc_name()", "Все варианты верны в зависимости от драйвера"], "correct": 4},
    
    # 162. Системные функции
    {"id": 162, "text": "Как получить размер таблицы в PostgreSQL?", "options": ["pg_total_relation_size('table_name')", "SELECT size FROM pg_tables WHERE tablename='table_name'", "SHOW TABLE SIZE 'table_name'", "TABLESIZE('table_name')"], "correct": 1},
    
    # 163. Репликация
    {"id": 163, "text": "Что такое 'switchover' в контексте отказоустойчивости?", "options": ["Плановая замена основного сервера", "Автоматическое переключение при падении", "Синхронизация реплик", "Ручное восстановление после сбоя"], "correct": 1},
    
    # 164. Оптимизация
    {"id": 164, "text": "Какой уровень изоляции позволяет избежать 'write skew'?", "options": ["SERIALIZABLE", "REPEATABLE READ", "READ COMMITTED", "SNAPSHOT ISOLATION"], "correct": 1},
    
    # 165. Временные зоны
    {"id": 165, "text": "Как конвертировать локальное время в UTC в PostgreSQL?", "options": ["AT TIME ZONE 'UTC'", "CONVERT_TZ(local_time, 'Europe/Moscow', 'UTC')", "SET timezone = 'UTC'", "TO_UTC(local_time)"], "correct": 1},
    
    # 166. Геопространственные данные
    {"id": 166, "text": "Как рассчитать площадь полигона в квадратных километрах в PostGIS?", "options": ["ST_Area(geom::geography) / 1000000", "ST_Area(geom) * 0.000001", "ST_Area_KM2(geom)", "Использовать проекцию EPSG:3857"], "correct": 1},
    
    # 167. CTE
    {"id": 167, "text": "Может ли CTE ссылаться на сам себя несколько раз в рекурсивном запросе?", "options": ["Да, через UNION ALL", "Нет, только один раз", "Только в Oracle", "Только через материализованное представление"], "correct": 1},
    
    # 168. Индексы
    {"id": 168, "text": "Что такое 'covering index' в SQL Server?", "options": ["Индекс, включающий все столбцы запроса", "Индекс для покрытия партиций", "Индекс для материализованных представлений", "Индекс с INCLUDE колонками"], "correct": 4},
    
    # 169. Безопасность
    {"id": 169, "text": "Как ограничить количество одновременных подключений для роли?", "options": ["ALTER ROLE ... CONNECTION LIMIT", "max_connections_per_user", "pgbouncer ограничения", "Нельзя ограничить на уровне СУБД"], "correct": 1},
    
    # 170. JSON
    {"id": 170, "text": "Как удалить поле из JSONB объекта в PostgreSQL?", "options": ["jsonb_set(data, '{field}', 'null', true) - 'field'", "JSON_REMOVE(data, '$.field')", "data::jsonb - 'field'", "UPDATE data SET field = NULL WHERE ..."], "correct": 3},
    
    # 171. Миграции
    {"id": 171, "text": "Что такое 'schema migration'?", "options": ["Изменение структуры БД с контролем версий", "Перенос данных между СУБД", "Обновление PostgreSQL до новой версии", "Миграция данных в облако"], "correct": 1},
    
    # 172. Системные представления
    {"id": 172, "text": "Как найти 'висячие' транзакции в PostgreSQL?", "options": ["pg_stat_activity с state = 'idle in transaction'", "SELECT * FROM pg_locks WHERE granted = false", "pg_blocking_pids()", "Все варианты верны"], "correct": 4},
    
    # 173. Репликация
    {"id": 173, "text": "Что такое 'каскадная репликация'?", "options": ["Реплика может быть мастером для других реплик", "Автоматическое масштабирование реплик", "Репликация только критических данных", "Синхронизация через промежуточный сервер"], "correct": 1},
    
    # 174. Оконные функции
    {"id": 174, "text": "Как вычислить отношение продаж текущего дня к среднему за месяц?", "options": ["sales / AVG(sales) OVER (PARTITION BY EXTRACT(MONTH FROM date))", "sales / MONTHLY_AVG(sales)", "RATIO_TO_REPORT(sales) OVER (PARTITION BY month)", "sales / (SELECT AVG(sales) FROM ...)"], "correct": 1},
    
    # 175. Индексы
    {"id": 175, "text": "Для какого случая оптимален SP-GiST индекс?", "options": ["Деревья решений и несбалансированные данные", "Точные совпадения строк", "Диапазонные запросы по числам", "Полнотекстовый поиск"], "correct": 1},
    
    # 176. Безопасность
    {"id": 176, "text": "Что такое 'dynamic data masking' в SQL Server?", "options": ["Маскировка данных для неавторизованных пользователей", "Шифрование данных на лету", "Анонимизация в тестовых средах", "Скрытие системных таблиц"], "correct": 1},
    
    # 177. Временные таблицы
    {"id": 177, "text": "Когда использовать табличные переменные вместо временных таблиц в T-SQL?", "options": ["Для небольших наборов данных (<1000 строк)", "Когда не нужна статистика", "Для упрощения кода", "Все варианты верны"], "correct": 4},
    
    # 178. JSON
    {"id": 178, "text": "Как преобразовать реляционную таблицу в JSON-массив в PostgreSQL?", "options": ["json_agg(row_to_json(t))", "TO_JSON(array_agg(*))", "JSON_BUILD_ARRAY(*)", "Использовать FOR JSON AUTO"], "correct": 1},
    
    # 179. Партиционирование
    {"id": 179, "text": "Как автоматизировать создание новых партиций при партиционировании по дате?", "options": ["pg_partman расширение", "CRON задача для создания партиций", "Триггер BEFORE INSERT", "Вручную перед началом нового периода"], "correct": 1},
    
    # 180. Геопространственные данные
    {"id": 180, "text": "Как проверить пересечение двух геометрий в PostGIS?", "options": ["ST_Intersects(geom1, geom2)", "geom1 && geom2", "ST_Contains(geom1, geom2)", "ST_Overlaps(geom1, geom2)"], "correct": 1},
    
    # 181. Оптимизация
    {"id": 181, "text": "Что такое 'index-only scan'?", "options": ["Чтение данных только из индекса без обращения к таблице", "Сканирование только части индекса", "Использование индекса для сортировки", "Оптимизация через покрывающий индекс"], "correct": 1},
    
    # 182. Триггеры
    {"id": 182, "text": "Как избежать рекурсивного вызова триггера при обновлении в нем же таблицы?", "options": ["pg_trigger_depth() = 0", "SET session_replication_role = replica", "CREATE TRIGGER ... WHEN (NOT pg_trigger_depth() > 0)", "Нельзя избежать"], "correct": 1},
    
    # 183. Сравнение СУБД
    {"id": 183, "text": "Какая СУБД поддерживает 'временные таблицы' (system-versioned tables)?", "options": ["SQL Server 2016+", "PostgreSQL 13+", "MySQL 8.0+", "Oracle 12c+"], "correct": 1},
    
    # 184. Безопасность
    {"id": 184, "text": "Как включить аудит всех DDL операций в PostgreSQL?", "options": ["pgAudit + log_statement = 'ddl'", "CREATE TRIGGER audit_ddl ON DATABASE", "log_min_messages = ddl", "Невозможно без расширений"], "correct": 1},
    
    # 185. JSON
    {"id": 185, "text": "Как искать по шаблону в JSON-строке в PostgreSQL?", "options": ["data->>'name' ILIKE '%john%'", "jsonb_path_exists(data, '$.name ? (@ like_regex \"john\")')", "JSON_SEARCH(data, 'all', '%john%')", "Все варианты верны"], "correct": 2},
    
    # 186. Системные функции
    {"id": 186, "text": "Как получить список всех индексов таблицы в PostgreSQL?", "options": ["\\d table_name", "SELECT * FROM pg_indexes WHERE tablename = 'table_name'", "SHOW INDEXES FROM table_name", "pg_catalog.pg_class JOIN pg_index"], "correct": 2},
    
    # 187. Репликация
    {"id": 187, "text": "Что такое 'логическая репликация' в PostgreSQL?", "options": ["Репликация на уровне таблиц и строк", "Репликация бинарных WAL файлов", "Синхронизация только изменений", "Репликация только для чтения"], "correct": 1},
    
    # 188. Оконные функции
    {"id": 188, "text": "Как вычислить процентиль 90 для продаж по регионам?", "options": ["PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY sales) OVER (PARTITION BY region)", "PERCENTILE(90) OVER (region)", "NTILE(90) OVER (ORDER BY sales)", "APPROX_PERCENTILE(sales, 0.9)"], "correct": 1},
    
    # 189. Индексы
    {"id": 189, "text": "Для запроса WHERE category = 'books' AND rating > 4 какой составной индекс оптимален?", "options": ["(category, rating)", "(rating, category)", "Отдельные индексы на category и rating", "GIN индекс на оба поля"], "correct": 1},
    
    # 190. Безопасность
    {"id": 190, "text": "Что такое 'privilege escalation' в контексте безопасности БД?", "options": ["Получение прав выше текущих через уязвимость", "Автоматическое повышение прав при длительном сеансе", "Ошибка в управлении ролями", "Уязвимость в механизме аутентификации"], "correct": 1},
    
    # 191. Временные таблицы
    {"id": 191, "text": "Что происходит с TEMPORARY TABLE после COMMIT в PostgreSQL?", "options": ["Таблица сохраняется до конца сессии", "Удаляется автоматически", "Очищается, но структура остается", "Зависит от параметра temp_table_on_commit"], "correct": 1},
    
    # 192. JSON
    {"id": 192, "text": "Как обновить вложенный объект в JSONB поле?", "options": ["jsonb_set(data, '{address,city}', '\"London\"')", "data->'address'->'city' = 'London'", "JSON_MODIFY(data, '$.address.city', 'London')", "UPDATE data SET address.city = 'London' WHERE ..."], "correct": 1},
    
    # 193. Геопространственные данные
    {"id": 193, "text": "Как преобразовать координаты из EPSG:4326 в EPSG:3857 в PostGIS?", "options": ["ST_Transform(geom, 3857)", "ST_SetSRID(geom, 3857)", "CONVERT_SRID(geom, 4326, 3857)", "PROJ4_TRANSFORM(geom)"], "correct": 1},
    
    # 194. Оптимизация
    {"id": 194, "text": "Что делает параметр work_mem в PostgreSQL?", "options": ["Определяет память для сортировок и хеш-соединений", "Размер буфера для записи WAL", "Память для обработки запросов", "Кэш для индексов"], "correct": 1},
    
    # 195. Триггеры
    {"id": 195, "text": "Какой тип события не поддерживается в триггерах PostgreSQL?", "options": ["BEFORE TRUNCATE", "AFTER CREATE TABLE", "INSTEAD OF UPDATE на представлении", "BEFORE INSERT OR UPDATE"], "correct": 2},
    
    # 196. Сравнение СУБД
    {"id": 196, "text": "Какая СУБД имеет встроенную поддержку машинного обучения (ML) внутри запросов?", "options": ["SQL Server 2019+", "PostgreSQL с расширениями", "Oracle 20c", "Все перечисленные"], "correct": 4},
    
    # 197. Безопасность
    {"id": 197, "text": "Как включить Transparent Data Encryption (TDE) в SQL Server?", "options": ["CREATE DATABASE ENCRYPTION KEY", "ALTER DATABASE ... SET ENCRYPTION ON", "Включить в настройках сервера", "Использовать Always Encrypted"], "correct": 2},
    
    # 198. JSON
    {"id": 198, "text": "Как в MySQL создать индекс на JSON-поле 'data->'$.price'?", "options": ["ALTER TABLE products ADD INDEX idx_price ((CAST(data->'$.price' AS UNSIGNED)))", "CREATE INDEX idx_price ON products (data->'$.price')", "GIN индекс на JSON поле", "Нельзя создать индекс на JSON поле"], "correct": 1},
    
    # 199. Системные представления
    {"id": 199, "text": "Как найти запросы, блокирующие другие запросы в PostgreSQL?", "options": ["pg_blocking_pids()", "SELECT * FROM pg_locks WHERE granted = false", "pg_stat_activity с wait_event_type = 'Lock'", "Все варианты верны"], "correct": 4},
    
    # 200. Репликация
    {"id": 200, "text": "Что такое 'synchronous_commit' в PostgreSQL?", "options": ["Гарантирует запись WAL на реплику перед подтверждением", "Синхронизирует транзакции между репликами", "Режим ожидания синхронизации", "Подтверждение транзакции после записи в память"], "correct": 1}
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
Входная точка gunicorn - engine:engine в директории application.
# Зависимости
_______
_______
- dynaconf 3.1.7
- Jinja2 3.0.3

# Настройки
_______
_______
Настройки проекта должны быть описаны в файле ``settings.toml``. Синтаксис обязывает на каждой строке прописывать пары 
настроек в виде 'ключ = значение' при том, что значение обязано быть строкой, числом, либо списком. Поддерживаются следующие настройки:

- ``DEBUG`` определяет работает ли программа в дебаг-режиме.
- ``TEMPLATES_DIR`` определяет название директории в корне проекта в которой будет осуществляться поиск шаблонов.
- ``GLOBAL_TEMPLATES_DIR`` определяет название директории которая является директорией по умолчанию для поиска шаблонов (см. пример в разделе"Шаблоны")
- ``LOGGING`` значение ``"True"`` включит всю систему логирования.
- ``LOGGER_STDOUT`` определяет, куда будет осуществляться вывод сообщений лога, варианта три: 
``"console"`` - в этом случае вывод будет производиться в консоль,
``"file"`` - в этом случае вывод будет производиться в файл. Директория и название файла необходимо указать в соответствующих настройках.
``"both"`` - выведет сообщения и в консоль, и запишет в файл.
- ``LOG_FILE`` определяет название файла с логами. Фреймворк дополнит название файла припиской с датой записи лога.
- ``LOG_FILE_DIR`` определяет название папки в корне проекта, где необходимо создавать файлы логов. Должна быть создана в ручную.
- ``DEFAULT_LOGGER`` значение ``"True"`` включит стандартный встроенный логгер фреймворка.
- ``DEFAULT_LOGGER_EXCLUDE`` это значение определяет, какой тип логов не будет выводиться, если включен стандартный логгер.
Если необходимо, чтобы выводились все типы сообщений, укажите ``[]``, в противном случае укажите, какие стандартные типы логов 
следует отключить ``["Debug", "CRITICAL"]``. Также, если необходимо отключить все стандартные типы логов, то вместо списка
можно указать строку ``"all"``.
- ``SITE_ADR`` ip-адрес сервера.
- ``SITE_PORT`` порт сервера.

В случае, если какая-то из необходимых фреймворку настроек указана не будет, произойдет исключение ``NoSettingDefinedError``.

# Контроллеры
_______
_______
В директории controllers в файле custom_controllers.py создаются контроллеры. Все они создаются в виде классов,
которые наследуются от ``master_controllers.BasicController``. Для их минимальной работы необходимо вызвать
``super().__init__()``, задать атрибут экземпляра ``self.template`` (путь к шаблону) и ``self.context`` (аргументы для jinja2)
в виде словаря. Все контроллеры, созданные таким образом, поддерживают метод GET и POST.


# Шаблоны
_______
_______
Шаблоны должны быть организованы так: в корневом каталоге программы должна лежать папка templates, в ней
уже находится папка global_templates, но пользователи могут создавать собственные папки в templates
для хранения шаблонов под разные логические части приложения. Более глубокую вложенность делать нельзя. В случае, если
будет невозможно найти указанный шаблон, произойдет исключение ``NoTemplateError``.

#### Пример:
```
application
    |
    |-templates
        |
        |-global_templates
        |-your_directory_with_templates
```
В каждой крайней директории хранятся сами шаблоны. Поэтому атрибут при контроллере следует задавать так:
```self.template = "mytmpldir/template.html"```
Или так:
```self.template = "template.html"```
Во втором случае, шаблон должен находиться в папке ``global_templates``.

## Шаблонные теги
_______
При написании шаблонов можно использовать следующие шаблонные теги, помимо тегов предусмотренных jinja2:

- ### Тег "[# childof 'your_template_path' #]".
    Этот тег реализует наследование шаблонов. Он ставится вверху дочернего шаблона, чтобы указать его зависимость
    от родительского шаблона. Вместо ``your_template_path`` следует указать путь к шаблону. Он должен быть представлен
    в том же виде, как при указании шаблона в контроллерах (см. раздел "Шаблоны"), например: ``mytmpldir/template.html``.

#### Пример:
``[# childof 'mytmpldir/template.html' #]``

- ### Тег "[# section your_section_name #]".
    Этот тег парный и состоит из нескольких тегов, а именно: ``[# section your_section_name #]`` и ``[# endsection #]``.
    Тег используется только при реализации наследования шаблонов. В родительском шаблоне с его помощью обозначаются
    логические блоки шаблона. В дальнейшем они соотносятся с блоками с аналогичным названием в дочернем шаблоне.
    В дочернем шаблоне, после указания шаблона как дочернего с помощью тега "``childof``", необходимо внутри парного
    тега "``section``" указать тот html-код, который необходимо поместить в блок "``section``" в родительском шаблоне
    с тем же названием. Таких блоков может быть несколько в одном шаблоне, но их имена должны быть уникальными,
    в противном случае фреймворк выдаст исключение ``SectionTagNameDuplicationError``. Фрйемфорк также выдает исключение
    ``NoParentTemplateError``, если не удалось найти родительский шаблон.

    #### Пример:
Родительский шаблон:
```
<body>
    <div>Im patent template</div>
    [# section myname #]
    [# endsection #]
</body>
```
Дочерний шаблон:
```
[# childof 'mytmpldir/my_parent_template.html' #]
[# section myname #]
    <div>Im child template</div>
[# endsection #]
```
Результат:
```
<body>
    <div>Im patent template</div>
    <div>Im child template</div>
</body>
```
- ### Тег "[# insert 'your_template_path' #]".
    Тег позволяет осуществлять вставку одного шаблона в другой. Тот шаблон, в котором определен этот тег, в месте
    определения последнего, будет дополнен содержимым того шаблона, который будет указан вместо ``your_template_path``.
    Указывать `your_template_path`` следует по тому же принципу, что и в случае с тегом ``[# childof 'your_template_path' #]``, тоесть как в контроллерах.

    #### Пример:
Шаблон-реципиент:
```
<body>
    <div>Im recipient template</div>
    [# insert 'your_template_path' #]
</body>
```
Шаблон-донор:
```
<div>
    <div>Im donor template</div>
</div>
```
Результат:
```
<body>
    <div>Im recipient template</div>
    <div>
        <div>Im donor template</div>
    </div>
</body>
```
# Пути
_______
_______
В документе ``page_urls.py`` в директории ``urls`` определена переменная ``registered_urls``, которая является списком, хранящим списки. Последние состоят из двух элементов: подключаемого url'а и ответственного за его обработку
контроллера в виде класса, который импортируется из документов папки `controllers``, в которой пользователь
может создавать свои контроллеры. 
>Важно! 
>>Пути не должны оканчиваться на "``/``".

# Логирование
_______
_______
## Настройка
_______
Чтобы включить логирование проекта, необходимо в первую очередь указать настройку ``LOGGING = "True"``. Далее необходимо
определить все настройки логгера. У настроек есть зависимости друг от друга:
- Настройка ``LOGGING = "True"`` обязывает определить настройки ``LOGGER_STDOUT`` и ``DEFAULT_LOGGER``. 
- Если ``LOGGER_STDOUT`` равен ``file`` или ``both``, то необходимо определить настройки ``LOG_FILE`` и ``LOG_FILE_DIR``.
- Если ``DEFAULT_LOGGER = "True"``, то необходимо указать настройку ``DEFAULT_LOGGER_EXCLUDE``.

Если в каком-то из вариантов зависимая настройка не определена, то будет выброшено исключение ``NoSettingDefinedError``.

## Покрытие логами
Если необходимо в каком-либо месте приложения осуществить логирвоание, то для реализации этого, сначала импортируйте
логгер: ``from wsgi_framework.framework_logger import Logger``. Затем вызовите его, определив результат в переменную.
``my_var = Logger()``. 

>Обратите внимание, что ``Logger`` - Singleton. Не рекомендуется манипулировать его настройками
на месте, осуществляйте это в соответствующем для этого файле (см. раздел "Пользовательский логгер").

Теперь инициализировать процедуру вывода лога в модуле можно так: 

``my_var["Debug"]("Message which i want to be logged")``

#### Пример:
```
from wsgi_framework.framework_logger import Logger
my_var = Logger()

...some code...
my_var["Debug"]("Debug message which i want to be logged")
...some code...
my_var["ERROR"]("Error message which i want to be logged")
...some code...
```
>Если вы указали название типа логов, которе не было зарегистрировано в логгере ``my_var["Im not registered"]("my_message")``, то произойдет исключение ``LogTypeNotRegisteredError``.
Также в случае, если по каким-то причинам фреймворк не сможет исполнить запись лога в файл, при условии включенной настройки,
то будет вызвано исключение ``NoLogFileError``.
## Стандартный логгер
В стандартном логере определены следующие типы логов:
- ``"Info"``
- ``"Debug"``
- ``"ERROR"``
- ``"CRITICAL"``

>Стандартный логгер, помимо указанного пользователем логирования, будет выводить лог части жизненного цикла самого
фреймворка. Поэтому, обратив на это внимание, подумайте о необходимости отключения стандартного вывода логов с помощью 
настройки ``DEFAULT_LOGGER_EXCLUDE``.

## Пользовательский логгер
Есть возможность создать логгер с собственными настройками. Для этой цели существует файл 
``application/logging/custom_logger.py``, в котором определена функция ``setup_custom_logger``. В ее теле уже заданы
обязательные настройки для кастомного логгера и импортированы модули:
```
from wsgi_framework.framework_logger import Logger
from config import settings


def setup_custom_logger():
	LOG = Logger()
	LOG.set_file_path(settings.APP_LOG_DIR_PATH)
	LOG.set_output_mode(settings.LOGGER_STDOUT)
	
	# Create your custom logger here
```
>Если есть необходимость, смените название переменной ``LOG``, но тогда, не забудьте сменить ее название и в обращениях.

Чтобы создать свой собственный тип лога, необходимо импортировать ``LogType`` - ``from wsgi_framework.framework_logger import LogType``.
``LogType`` принимает два позиционных аргумента, где первый, это название типа лога, а второй - escape-последовательность,
обозначающая цвет. Это цвет, которым будет выводиться название типа лога в консоль.
```
from wsgi_framework.framework_logger import LogType

my_var = LogType("My_log_type_name", some_escape_sequence)
```
### Цвета
Вы можете вместо escape-последовательности воспользоваться стандартным набором цветов. Для этого импортируйте
``LogColors`` - ``from wsgi_framework.framework_logger import LogColors``. 
>LogColors - Singleton, имейте это в виду.

Теперь можно создать экземпляр ``LogColors`` и, при обращении к нему через точечную нотацию с указанием соответствующего
цвета, получить его escape-последовательность.

#### Пример:
```
from wsgi_framework.framework_logger import LogColors

colors = LogColors()

print(colors.red)
print(colors.green)
```
Стандартный набор цветов: bright_white,	red, green, yellow, blue, red_background.

Вы не обязаны пользоваться только стандартным набором цветов. Можно зарегистрировать собственный цвет, чтобы в дальнейшем
обращаться к нему через точку, а не писать некрасивые escape-последовательности. Это можно сделать с помощью вызова 
``add_color()``. В качестве позиционных аргументов, передайте ему имя и escape-последовательность.

#### Пример:
```
from wsgi_framework.framework_logger import LogColors

colors = LogColors()
colors.add_color("my_own_color", "\033[96m")

print(colors.my_own_color)
```
### Регистрация типа логов
Чтобы получить доступ к созданным типам логов в программе, необходимо их зарегистрировать. Для этого используются 
функции-регистраторы экземпляра ``Logger``: ``register_logtype`` и ``register_logtypes``. Вы можете зарегистрировать свой
одиночный тип логера с помощью ``register_logtype``, передав ему в качестве аргумента экземпляр ``LogType``. 
>В этот момент, если у логгера был неверно настроен режим вывода логов, произойдет исключение ``OutputModeError``.

С помощью ``register_logtypes`` можно зарегистрировать сразу несколько пользовательских типов логов. Типы логов необходимо
передать функции в виде списка в именованный аргумент ``types_list``.
> Не следует вызывать ``register_logtypes`` более одного раза, так как она при вызове стирает все ранее установленные типы логов.
#### Пример:
``LOG.register_logtypes(types_list=[my_type_1, my_type_2])``

У ``register_logtypes`` есть дополнительный функционал. C помощью дополнительного именованного аргумента ``exclude``,
можно указать какие из стандартных типов логов необходимо отключить. Значение этого аргумента должно быть создано также,
как в файле настроек в ``DEFAULT_LOGGER_EXCLUDE`` (см. раздел "Настройки").
> Важно!
>> Если при создании своего логгера функция-регистратор ``register_logtypes`` не была вызвана, то никакие стандартные
> типы логов созданы НЕ БУДУТ.

Как бы вы не регистрировали свои типы логов, дублирование их имен в логгере вызовет ошибку ``LogTypeNameDuplicationError``.
### Отключение типа логов
С помощью функции ``disable_logtype`` можно отключить ранее установленный тип логов. Для этого передайте имя типа в функцию,
например: ``LOG.disable_logtype("my_logtype_name")``.

### Проверка наличия типа логов
Есть возможность проверить, зарегестрирован ли в данный момент в логгере тот или иной тип лога. Для этого существует функция
``is_type_enabled()`` класса ``Logger``. Она вернет ``True`` в случае наличия типа логов, или ``False`` в случае отсудствия.

#### Пример:
```
if LOG.is_type_enabled("Info"):
  LOG["Info"]("My info message.")
```

#### Итоговый пример:
```
from wsgi_framework.framework_logger import Logger, LogType, LogColors
from config import settings


def setup_custom_logger():
	LOG = Logger()
	LOG.set_file_path(settings.APP_LOG_DIR_PATH)
	LOG.set_output_mode(settings.LOGGER_STDOUT)
	
	# Create your custom logger here
	
	colors = LogColors()
	colors.add_color("my_color", "\033[96m")

	my_logtypes_list = [
		LogType("My_Logtype_1", colors.my_color),
		LogType("My_Logtype_2", colors.red),
		LogType("My_Logtype_3", colors.blue),
	]

	LOG.register_logtypes(my_logtypes_list, exclude=["Debug"])

	LOG.disable_logtype("My_Logtype_2")

	LOG["My_Logtype_1"]("My logger types are ready!")
```
# Авторизация
_______
_______
В фреймворке реализована система авторизации типа Base-authorization. Есть, как модуль авторизации из коробки, так и 
возможность создать пользовательский класс авторизации.

## Стандартная авторизация
Отключить стандартную авторизацию фреймворка можно удалив ``wsgi_framework.middleware.default_authorization`` из
списка настройки ``MIDDLEWARE`` в ``settings.toml``. Стандартная авторизация сверяет пароль и имя пользователя, и
авторизует, в зависимости от результатов сравнения.

## Пользовательская авторизация
Для пользовательской авторизации в файле ``application/authorization/custom_authorization`` реализован класс
``CustomAuthorizator``:
```
from wsgi_framework.framework_authorization import AbstractAuthorizator


class CustomAuthorizator(AbstractAuthorizator):
	def __init__(self, user, environ):
		self.user = user
		self.environ = environ

	def authorize(self):
		pass
```
В этом классе доступен объект пользователя ``user``, а также ``environ``, присылаемый wsgi-сервером. Осуществлять 
кастомную авторизацию следует в функции ``authorize``:
#### Пример:
```
def authorize(self):
    print("My custom authorizator in action!")
    if 1 == 1:
        self.user.auth()
```
### Объект User
Этот объект содержит данные о пользователе:
- ``username`` содержит имя пользователя.
- ``password`` содержит пароль в не зашифрованном виде.
- ``is_auth`` булево, флаг отмечающий прошел ли пользователь авторизацию.
Также в объекте есть функция ``auth()``. Ее следует использовать, чтобы сменить флаг на ``True``.

### Не явные атрибуты BasicController'a
``master_controllers.BasicController`` обладает несколькими полезными атрибутами связанными с авторизацией:
- ``user`` - объект пользователя доступен и в контроллере, а не только в классе авторизации. 
- ``need_auth`` - булево, флаг отмечающий требуется ли user'у, для исполнения этого контроллера, быть авторизованым.

### Функция pre_execute
В созданных пользовательских контроллерах можно переопределять функцию ``pre_execute``. Она ни за что не отвечает,
но исполнится перед тем, как проверка авторизации будет проведена. Это удобно использовать, чтобы, к примеру, создать 
дополнительную точку авторизации.
#### Пример:
```
def pre_execute(self):
  if self.user.username == "Alex":
      self.user.auth()
```
>Это будет работать, даже если все остальные способы авторизации отключены.

Также эта функция подходит для того, чтобы динамически переключать необходимость авторизации для разного вида запросов
или условий.
#### Пример:
```
def pre_execute(self):
  if self.method.lower() == "post":
      self.need_auth = True
```
# Middleware
_______
_______
### Настройка
Middleware оформлен в виде списка из строк в параметре ``MIDDLEWARE`` в ``settings.toml``.
> Порядок имеет значение! Middleware будут исполняться именно в том порядке, в каком расположены в списке. А в случае,
> если middleware не будет найден, то произойдет исключение ``NoMiddlewareFoundError``.
### Создание Middleware
Middleware создаются в файле ``application/middleware/custom_middleware.py``. Они будут загружены при старте приложения,
наряду с middleware по-умолчанию. Оформлены они должны быть в виде функций, принимающих один позиционный параметр - ``environ``.
#### Пример:
```
def print_environ(environ):
	for key, val in environ.items():
		print(f"{key}: {val}")
```
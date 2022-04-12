import inspect
import sqlite3
import os
import importlib.util
import sys

from config import settings
from wsgi_framework.exceptions import OrmException


def get_obj_attrs(obj):
	result = []
	for i in inspect.getmembers(obj):
		if not i[0].startswith("_"):
			if not inspect.ismethod(i[1]) and not inspect.isfunction(i[1]):
				if i[0] not in ["connection", "cursor", "db_conn_obj"]:
					result.append(i)
	return result


class OrmInitializer:
	def __init__(self):
		self.user_models = []

	def initialize_tables(self):
		self.collect_models()
		self.create_tables()

	def collect_models(self):
		models_dir = os.path.join(settings.APP_DIR_PATH, "models")

		sys.path.append(models_dir)

		user_models_module = importlib.import_module("custom_models")
		for name, cls in inspect.getmembers(user_models_module, inspect.isclass):
			if Table in cls.__bases__:
				self.user_models.append(cls)

	def create_tables(self):
		for model in self.user_models:
			model.create_table(model)


class OrmCache:
	cached_objects = {}

	@staticmethod
	def to_cache(table_name, entry_object):
		if table_name not in OrmCache.cached_objects.keys():
			OrmCache.cached_objects[table_name] = {entry_object.id: entry_object}
		else:
			if entry_object.id not in OrmCache.cached_objects[table_name].keys():
				OrmCache.cached_objects[table_name][entry_object.id] = entry_object

	@staticmethod
	def from_cache(table_name, search_id):
		if table_name in OrmCache.cached_objects.keys():
			if search_id in OrmCache.cached_objects[table_name].keys():
				return OrmCache.cached_objects[table_name][search_id]


class DatabaseConnection:
	def __new__(cls):
		if not hasattr(cls, 'instance'):
			cls.instance = super(DatabaseConnection, cls).__new__(cls)
		return cls.instance

	def __init__(self):
		self.connection = sqlite3.connect(settings.DATABASE_NAME)
		self.cursor = self.connection.cursor()

	def __del__(self):
		self.connection.close()

	def get_cursor(self):
		return self.cursor

	def get_connection(self):
		return self.connection


class Table:
	db_conn_obj = DatabaseConnection()
	connection = db_conn_obj.get_connection()
	cursor = db_conn_obj.get_cursor()

	def __init__(self, **kwargs):
		if kwargs:
			for key, val in kwargs.items():
				self.__setattr__(key, val)

	def insert_expression(self):
		table_name = self.__class__.__name__
		attr_dict = self.__dict__.items()
		col_names = [i[0] for i in attr_dict]
		col_values = [i[1] for i in attr_dict]
		full_expression = f"""INSERT INTO {table_name}({', '.join([f"'{i}'" for i in col_names])}) VALUES({', '.join(['?' for _ in range(len(col_names))])})"""
		if settings.PRINT_QUERIES:
			print(full_expression, col_values)
		return [full_expression, col_values]

	def add_row(self):
		Table.cursor.execute(*self.insert_expression())
		Table.connection.commit()

	def select_where_expression(self, **kwargs):
		table_name = self.__class__.__name__
		full_expression = f"""SELECT * FROM {table_name} WHERE {", ".join([f"{key} = '{val}'" for key, val in kwargs.items()])};"""
		if settings.PRINT_QUERIES:
			print(full_expression)
		return full_expression

	def filter(self, **kwargs):
		result = Table.cursor.execute(self.select_where_expression(**kwargs)).fetchall()
		result_list = [self.convert_to_object(db_data) for db_data in result]
		for obj in result_list:
			OrmCache.to_cache(self.__class__.__name__, obj)
		return result_list

	def find_by_id(self, id):
		if cache_result := OrmCache.from_cache(self.__class__.__name__, id):
			result_obj = cache_result
			print("loaded from cache")
		else:
			result = Table.cursor.execute(self.select_where_expression(id=id)).fetchall()[0]
			result_obj = self.convert_to_object(result)
			OrmCache.to_cache(self.__class__.__name__, result_obj)
		return result_obj

	def find_all(self):
		table_name = self.__class__.__name__
		full_expression = f"SELECT * FROM {table_name};"
		result = Table.cursor.execute(full_expression).fetchall()
		result_list = [self.convert_to_object(db_data) for db_data in result]
		for obj in result_list:
			OrmCache.to_cache(table_name, obj)
		return result_list

	def update_expression(self, **kwargs):
		table_name = self.__class__.__name__
		full_expression = f"""UPDATE {table_name} SET {", ".join([f"{key} = {val}" for key, val in kwargs.items()])} WHERE {" AND ".join([f"{key} = '{val}'" for key, val in self.__dict__.items()])};"""
		if settings.PRINT_QUERIES:
			print(full_expression)
		return full_expression

	def update(self, **kwargs):
		Table.cursor.execute(self.update_expression(**kwargs))
		Table.connection.commit()

	def delete_expression(self):
		table_name = self.__class__.__name__
		full_expression = f"""DELETE FROM {table_name} WHERE {" AND ".join([f"{key} = '{val}'" for key, val in self.__dict__.items()])};"""
		if settings.PRINT_QUERIES:
			print(full_expression)
		return full_expression

	def delete(self):
		Table.cursor.execute(self.delete_expression())
		Table.connection.commit()

	def convert_to_object(self, data):
		result_obj = self.__class__()
		attributes = ["id"]
		attributes.extend([i[0] for i in get_obj_attrs(self)])
		combined = zip(attributes, data)
		for attr, value in combined:
			result_obj.__setattr__(attr, value)
		return result_obj

	def reset_attrs(self, obj):
		for attr, value in obj.__dict__:
			self.__setattr__(attr, value)

	@staticmethod
	def create_table_expression(class_obj):
		table_name = class_obj.__name__
		table_items = get_obj_attrs(class_obj)
		full_expression = f"CREATE TABLE IF NOT EXISTS {table_name} (id integer PRIMARY KEY, "
		full_expression += ", ".join([f"{name} {setting.get_expression()}" for name, setting in table_items]) + ");"
		print(full_expression)
		return full_expression

	@staticmethod
	def create_table(class_obj):
		Table.cursor.execute(Table.create_table_expression(class_obj))


class Column:
	def __init__(self, type_name, **kwargs):
		self.sql_expression = f"{type_name}"
		keys = kwargs.keys()
		if "max_length" in keys:
			self.sql_expression += f"({kwargs['max_length']})"
		if "not_null" in keys and kwargs["not_null"]:
			self.sql_expression += " NOT NULL"
		if "unique" in keys and kwargs["unique"]:
			self.sql_expression += " UNIQUE"
		if "default" in keys:
			self.sql_expression += f" DEFAULT '{kwargs['default']}'"

	def get_expression(self):
		return self.sql_expression

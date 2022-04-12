from wsgi_framework.framework_orm import Table, Column


class Good(Table):
	name = Column("varchar", max_length=225, unique=True)
	description = Column("text", max_length=229, not_null=True)
	price = Column("integer", not_null=True, default=0)


# table = Good
#
# table.cursor.execute("DROP TABLE IF EXISTS Good")
# table.create_table(Good)
#
# good = Good(description="very good", name="Fridge")
# good2 = Good(price=100, description="very very good", name="Toaster")
# good3 = Good(price=100, description="not good", name="Oven")
# all_goods = [good, good2, good3]
# for i in all_goods:
# 	i.add_row()

# result = Good().find_all()
# print(result)
# for i in result:
# 	print(i.price)

# result_2 = Good().filter(price=100)
# for i in result_2:
# 	print(i.name)

# print(Good().find_by_id(1).name)
# print(Good().find_by_id(2).name)
# print(Good().find_by_id(3).name)

# print(list(globals().values()))
# for val in list(globals().values()):
# 	if hasattr(val, "connection") and Table in val.__bases__:
# 		print(val)





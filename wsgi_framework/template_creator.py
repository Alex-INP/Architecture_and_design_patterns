from jinja2 import Template
import os

global variables
import variables as vrb

def get_template_path_data(path):
	templates_segment, name = os.path.split(path)
	if templates_segment:
		path_body = os.path.join(vrb.TEMPLATE_DIR, templates_segment)
	else:
		path_body = os.path.join(vrb.TEMPLATE_DIR, vrb.GLOBAL_TEMPLATE_DIR)
	template_dir = os.path.join(path_body, name)
	return {"template_dir": template_dir, "template_name": name, "template_path": path_body}


def render_template(path, **kwargs):
	# templates_segment, name = os.path.split(path)
	# if templates_segment:
	# 	path_body = os.path.join(vrb.TEMPLATE_DIR, templates_segment)
	# else:
	# 	path_body = os.path.join(vrb.TEMPLATE_DIR, vrb.GLOBAL_TEMPLATE_DIR)
	# template_dir = os.path.join(path_body, name)
	path_data = get_template_path_data(path)

	try:
		with open(path_data["template_dir"], "r", encoding="utf-8") as file:
			template_body = Template(file.read())
	except FileNotFoundError:
		print(f"Not found: No '{path_data['name']}' template found in '{path_data['path_body']}'.")
		return

	return bytes(template_body.render(**kwargs), "utf-8")

	# return template_body.render(**kwargs)

if __name__ == "__main__":
	result = render_template("index.html", names=["Alex", "Bill", "Kate"])
	print(result)


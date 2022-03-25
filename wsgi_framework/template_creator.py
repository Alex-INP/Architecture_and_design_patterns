import os
import re

from jinja2 import Template
from config import settings

from wsgi_framework.exceptions import SectionTagNameDuplicationError, TemplateException, NoParentTemplateError
from wsgi_framework.framework_logger import Logger

LOG = Logger()

def render_template(path, **kwargs):
	try:
		template_body = load_template_body(path)
		tags_count = get_tags_count(template_body)
		for _ in range(tags_count):
			template_body = process_special_tags(template_body)

		template_body = Template(template_body)
	except:
		raise TemplateException(template=path)

	return bytes(template_body.render(**kwargs), "utf-8")


def process_special_tags(template_body):
	special_tags = {"childof": insert_child_template, "insert": add_dependant_template}

	if search_result := re.search(r"\[#\s(.+)\s#]", template_body):
		search_result = search_result.group(1).split(" ")
		if search_result[0] in special_tags.keys():
			template_body = special_tags[search_result[0]](template_body, search_result[1].strip("'"))
	return template_body


def add_dependant_template(main_template, dep_template_path):
	dep_template_body = load_template_body(dep_template_path)
	tag = re.search(fr"\[#\sinsert\s'{dep_template_path}'\s#]", main_template)
	insert_tag_data = [tag.start(), tag.end()]
	main_template = main_template.replace(
		main_template[insert_tag_data[0]:insert_tag_data[1]],
		dep_template_body
	)
	return main_template


def insert_child_template(child_template, parent_template_path):
	parent_template_body = load_template_body(parent_template_path)
	parent_sections_names = parse_template_sections(parent_template_body)
	child_sections_names = parse_template_sections(child_template)

	for section_name in parent_sections_names:
		parent_section_data = get_section_data(section_name, parent_template_body)
		if section_name in child_sections_names:
			child_section_data = get_section_data(section_name, child_template)
			parent_template_body = parent_template_body.replace(
				parent_template_body[parent_section_data[0]:parent_section_data[1]],
				child_section_data[2]
			)
		else:
			parent_template_body = parent_template_body.replace(
				parent_template_body[parent_section_data[0]:parent_section_data[1]],
				""
			)
	return parent_template_body


def parse_template_sections(template):
	sections = re.findall(re.compile(r"\[#\ssection\s.*?endsection\s#]", re.DOTALL), template)
	sections_data = []
	for section in sections:
		section_header_len = len(re.search(re.compile(r"\[#.*?#]", re.DOTALL), section).group(0))
		section_name = section[:section_header_len].split(" ")[2]

		# !!! в будущем, при создании функционала проверки синтаксиса шаблонов, эту проверку необходимо будет переместить
		if section_name not in sections_data:
			sections_data.append(section_name)
		else:
			raise SectionTagNameDuplicationError(section_name)
	return sections_data


def get_section_data(section_name, template):
	section = re.search(re.compile(fr"\[#\ssection\s{section_name}\s#].*?\[#\sendsection\s#]", re.DOTALL), template)
	section_header_len = len(re.search(re.compile(r"\[#.*?#]", re.DOTALL), section.group(0)).group(0))
	return [section.start(), section.end(), section.group(0)[section_header_len:-16].strip("\n")]


def load_template_body(path):
	template_path = get_template_path_data(path)
	try:
		with open(template_path["template_dir"], "r", encoding="utf-8") as file:
			template_body = file.read()
	except FileNotFoundError:
		raise NoParentTemplateError(path)
	return template_body


def get_template_path_data(path):
	templates_segment, name = os.path.split(path)
	if templates_segment:
		path_body = os.path.join(settings.TEMPLATES_DIR, templates_segment)
	else:
		path_body = os.path.join(settings.TEMPLATES_DIR, settings.GLOBAL_TEMPLATES_DIR)
	template_dir = os.path.join(path_body, name)
	return {"template_dir": template_dir, "template_name": name, "template_path": path_body}


def get_tags_count(template_body):
	exception_tags = ["[# endsection #]"]
	all_matches = re.findall(re.compile(r"\[#.+?#]", re.DOTALL), template_body)
	for exc in exception_tags:
		all_matches = list(filter(lambda x: x != exc, all_matches))
	return len(all_matches)


if __name__ == "__main__":
	result = render_template("index.html", names=["Alex", "Bill", "Kate"])
	print(result)

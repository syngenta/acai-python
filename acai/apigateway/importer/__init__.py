import os
import glob


class Importer:

	def __init__(self, **kwargs):
		self.__mode = kwargs['mode']
		self.__handlers = Importer.clean_path(kwargs['handlers'])
		self.__file_tree = {}

	@staticmethod
	def clean_path(dirty_path):
		return dirty_path.strip(os.sep)

	def get_absolute_handler_path(self):
		path = os.path.normpath(self.__handlers)
		handler_root = path.split(os.sep)[0]
		project_root = os.getcwd().split(handler_root)[0]
		return project_root + self.__handlers

	def get_glob_pattern(self):
		abs_path = self.get_absolute_handler_path()
		if self.__mode == 'directory':
			return abs_path + os.sep + '**' + os.sep + '*.py'
		if self.__mode == 'pattern':
			return abs_path

	def list_files_in_handler_path(self):
		glob_pattern = self.get_glob_pattern()
		return glob.glob(glob_pattern, recursive=True)

	def get_file_tree(self):
		if not self.__file_tree:
			file_paths = self.list_files_in_handler_path()
			for file_path in file_paths:
				sections = file_path.split(os.sep)
				self.__recurse_section(self.__file_tree, sections, 0)
		return self.__file_tree

	def __recurse_section(self, file_leaf, sections, index):
		if index >= len(sections):
			return
		section = sections[index]
		if not section:
			self.__recurse_section(file_leaf, sections, index+1)
		if section not in file_leaf:
			file_leaf[section] = {} if index+1 < len(sections) else '*'
		if type(file_leaf[section]) is dict and '__has_init' not in file_leaf[section]:
			file_leaf[section]['__has_init'] = False
			file_leaf[section]['__dynamic_file_count'] = set()
		self.__recurse_section(file_leaf[section], sections, index+1)


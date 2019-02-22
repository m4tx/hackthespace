import os
import re

from django.core.management.base import BaseCommand, CommandError

TEMPLATE_CONTENT = '''{% extends 'base.html' %}


{% block content %}
    <div class="container">
        <p class="text-grey text-spacey">
            This is a new puzzle.
        </p>
    </div>
{% endblock %}
'''

PUZZLE_PY_CONTENT = '''from django.views.generic import TemplateView


class {title_name}PuzzleView(TemplateView):
    template_name = 'puzzles/{name}.html'
'''

URL_REGEX = r'^(\nurlpatterns = \[.+)\]$'
URL_SUBST = (
    'from game.puzzles.{name}.puzzle import {title_name}PuzzleView\n'
    '\\1'
    '    path(\'{name}/\', {title_name}PuzzleView.as_view(), '
    'name=\'{name}\'),\n]')

SETTINGS_REGEX = r'^(PUZZLE_ORDER = \[.+?)\]'
SETTINGS_SUBST = '\\1    \'{name}\',\\n]'


class Command(BaseCommand):
    help = 'Create new puzzle with given name'

    def add_arguments(self, parser):
        parser.add_argument(
            'name', help='underscore case name of the puzzle to add', type=str)

    def handle(self, *args, **options):
        name: str = options.pop('name').lower()
        title_name = name.title().replace('_', '')

        self.__create_files(name, title_name)
        self.__add_to_urls(name, title_name)
        self.__add_to_order(name, title_name)

    @staticmethod
    def __get_app_root():
        return os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))

    def __create_files(self, name, title_name):
        app_root = self.__get_app_root()
        templates_root = os.path.join(app_root, 'templates', 'puzzles')
        puzzles_root = os.path.join(app_root, 'puzzles')
        puzzle_path = os.path.join(puzzles_root, name)

        self.__create_puzzle_dir(puzzle_path)
        self.__create_puzzle_files(puzzle_path, name, title_name)
        self.__create_template_file(templates_root, name)

    @staticmethod
    def __create_puzzle_dir(puzzle_path):
        try:
            os.makedirs(puzzle_path)
        except FileExistsError:
            raise CommandError('Puzzle with this name already exists!')

    @staticmethod
    def __create_puzzle_files(puzzle_path, name, title_name):
        init_py_path = os.path.join(puzzle_path, '__init__.py')
        with open(init_py_path, 'w'):
            pass
        puzzle_py_path = os.path.join(puzzle_path, 'puzzle.py')
        with open(puzzle_py_path, 'w') as f:
            f.write(PUZZLE_PY_CONTENT.format(name=name, title_name=title_name))

    @staticmethod
    def __create_template_file(templates_root, name):
        template_path = os.path.join(templates_root, '{}.html'.format(name))
        with open(template_path, 'w') as f:
            f.write(TEMPLATE_CONTENT)

    @staticmethod
    def __apply_regex_to_file(path, regex, subst, name, title_name):
        subst = subst.format(name=name, title_name=title_name)
        with open(path, 'r+') as f:
            content = f.read()
            new_contents = re.sub(regex, subst, content, 1,
                                  re.MULTILINE | re.DOTALL)
            f.seek(0)
            f.write(new_contents)

    def __add_to_urls(self, name, title_name):
        urls_path = os.path.join(self.__get_app_root(), 'puzzles', 'urls.py')
        self.__apply_regex_to_file(urls_path, URL_REGEX, URL_SUBST,
                                   name, title_name)

    def __add_to_order(self, name, title_name):
        urls_path = os.path.join(self.__get_app_root(),
                                 '..', 'stronghold', 'settings', 'base.py')
        self.__apply_regex_to_file(urls_path, SETTINGS_REGEX, SETTINGS_SUBST,
                                   name, title_name)

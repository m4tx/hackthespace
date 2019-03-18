import os
import re
from django.core.management import call_command

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

VIEWS_PY_CONTENT = '''from django.views.generic import TemplateView


class {title_name}PuzzleView(TemplateView):
    template_name = '{name}/puzzle.html'
'''

URLS_PY_CONTENT = '''from django.urls import path

from {name}.views import {title_name}PuzzleView

urlpatterns = [
    path('{name}/', {title_name}PuzzleView.as_view(), name='{name}'),
]
'''

SETTINGS_REGEX = r'^(PUZZLE_ORDER = \[.+?)\]'
SETTINGS_SUBST = '\\1    \'{name}\',\\n]'


class Command(BaseCommand):
    help = 'Create new puzzle with given name'

    def add_arguments(self, parser):
        parser.add_argument(
            'name', help='underscore case name of the puzzle to add', type=str)

    def handle(self, *args, **options):
        name = options.pop('name').lower()
        title_name = name.title().replace('_', '')

        call_command('startapp', name)
        self.__create_files(name, title_name)
        self.__add_to_order(name, title_name)

    @staticmethod
    def __get_project_root():
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))))

    def __get_app_root(self, name: str):
        return os.path.join(self.__get_project_root(), name)

    def __create_files(self, name, title_name):
        app_root = self.__get_app_root(name)
        templates_root = os.path.join(app_root, 'templates', name)
        os.makedirs(templates_root)

        self.__create_views_file(app_root, name, title_name)
        self.__create_template_file(templates_root)
        self.__create_urls_file(app_root, name, title_name)

    @staticmethod
    def __create_views_file(puzzle_path, name, title_name):
        puzzle_py_path = os.path.join(puzzle_path, 'views.py')
        with open(puzzle_py_path, 'w') as f:
            f.write(VIEWS_PY_CONTENT.format(name=name, title_name=title_name))

    @staticmethod
    def __create_template_file(templates_root):
        template_path = os.path.join(templates_root, 'puzzle.html')
        with open(template_path, 'w') as f:
            f.write(TEMPLATE_CONTENT)

    @staticmethod
    def __create_urls_file(templates_root, name, title_name):
        urls_path = os.path.join(templates_root, 'urls.py')
        with open(urls_path, 'w') as f:
            f.write(URLS_PY_CONTENT.format(name=name, title_name=title_name))

    @staticmethod
    def __apply_regex_to_file(path, regex, subst, name, title_name):
        subst = subst.format(name=name, title_name=title_name)
        with open(path, 'r+') as f:
            content = f.read()
            new_contents = re.sub(regex, subst, content, 1,
                                  re.MULTILINE | re.DOTALL)
            f.seek(0)
            f.write(new_contents)

    def __add_to_order(self, name, title_name):
        urls_path = os.path.join(self.__get_project_root(),
                                 'hackthespace', 'settings', 'base.py')
        self.__apply_regex_to_file(urls_path, SETTINGS_REGEX, SETTINGS_SUBST,
                                   name, title_name)

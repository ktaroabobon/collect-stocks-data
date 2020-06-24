import os
import string

import termcolor


def get_temp_dir_path(dir_name) -> str:
    """To Research and Return the path of the directory you choose.

    Returns: The dir path.
    """
    dir_path = None

    if not dir_path:
        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        dir_path = os.path.join(base_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

    return dir_path


class NoTemplateError(Exception):
    """No template file"""


def find_template(temp_file):
    """Find for template file in the given location.

    Returns:
        str: The template file path

    Raises:
        NoTemplateError: If the file does not exists.
    """
    template_dir_path = get_temp_dir_path("templates")
    temp_file_path = os.path.join(template_dir_path, temp_file)
    if not os.path.exists(temp_file_path):
        raise NoTemplateError('Could not find {}'.format(temp_file))
    return temp_file_path


def get_template(template_file_path, color=None):
    """Return the path of the template.

    Args:
        template_file_path (str): The template file path
        color: (str): Color formatting for output in terminal
            See in more details: https://pypi.python.org/pypi/termcolor


    Returns:
        string.Template: Return templates with characters in templates.
    """
    template = find_template(template_file_path)
    with open(template, 'r', encoding='utf-8') as template_file:
        contents = template_file.read()
        contents = contents.rstrip(os.linesep)
        contents = '{splitter}{sep}{contents}{sep}{splitter}{sep}'.format(
            contents=contents, splitter="=" * 60, sep=os.linesep)
        contents = termcolor.colored(contents, color)
        return string.Template(contents)

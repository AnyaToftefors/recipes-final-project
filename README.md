# Example project of the Applied Object-Oriented Programming course<!-- omit in toc -->

This repository contains an example project meant to be used as a guide for the development of a [Flask](https://flask.palletsprojects.com/) project using [VSCode](https://code.visualstudio.com/) and best practices of software development.

## Features

This project has the following features:

- [VSCode configuration](.vscode/settings.json) that uses Python-focused code quality tools and formatters
  - Static type checker: [Mypy](https://mypy.readthedocs.io/)
  - [Black](https://black.readthedocs.io/), the uncompromising code formatter
  - [isort](https://pycqa.github.io/isort/) for sorting and categorizing your imports
  - [Flake8](https://flake8.pycqa.org/) for style guide enforcement
  - [Pylint](https://pylint.pycqa.org/) for removing *code smells*
- Integration with [GitHub Actions](https://github.com/features/actions) for a CI/CD pipeline ready to be integrated with [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)
- Code coverage assessment and requirement such that the CI/CD pipeline only continues if 100% of the code is covered
- Functional tests using [selenium](https://selenium-python.readthedocs.io/)
- Implementation of an HTML validator based on the [Nu Html Checker (v.Nu)](https://validator.github.io/validator/)

# Table of Contents<!-- omit in toc -->

- [Installation procedures](#installation-procedures)
  - [Configurations for production](#configurations-for-production)
  - [CI/CD configuration with Heroku](#cicd-configuration-with-heroku)
- [Useful Commands](#useful-commands)
  - [During development](#during-development)
    - [Initializing the database](#initializing-the-database)
    - [Running the site in development mode](#running-the-site-in-development-mode)
    - [Running unit tests](#running-unit-tests)
    - [Running the functional tests](#running-the-functional-tests)
    - [Checking code formatting](#checking-code-formatting)
  - [Validate the entire project](#validate-the-entire-project)
- [Code snippets](#code-snippets)
  - [Python](#python)
    - [New test class](#new-test-class)
  - [HTML](#html)
    - [New navbar item](#new-navbar-item)
    - [New details page](#new-details-page)
    - [New form page](#new-form-page)
    - [General form fields](#general-form-fields)
- [Files that you MUST NOT change](#files-that-you-must-not-change)
- [Suggestion for improvements](#suggestion-for-improvements)
- [Contact](#contact)

# Installation procedures

If you are following the course, please check the *software installation instructions* page on canvas.

If not, this project requires/has been tested the following software:
- Python 3.9
- pip-tools
- [VSCode extension package](https://marketplace.visualstudio.com/items?itemName=CarlosNatalino.chalmers-applied-object-oriented-programming)
- (recommended) use a virtual environment

Once you have these software installed, you can compile the `requirements.txt` for development with:

`pip-compile --output-file requirements.txt requirements.in requirements-dev.in`

Then, you can install all the required packages with:

`pip install --upgrade -r requirements.txt`

## Configurations for production

This project expects the variables `DATABASE_URL` and `FLASK_SECRET_KEY` to be set in the production environment.
The guide on how to do it will be published in the course page.

## CI/CD configuration with Heroku

If you want to use the CD pipeline to deploy it to Heroku, you need to configure the following GitHub secrets:
- HEROKU_API_KEY
- HEROKU_APP_NAME
- HEROKU_EMAIL

# Useful Commands

Here are some useful commands to use during development and project validation.

## During development

### Initializing the database

To create or re-create the database, run:

```
python manage.py initdb
```

### Running the site in development mode

In the terminal, run:

```python manage.py run```

If you get an error saying that `"Address already in use"`, you can specify a port number (for instance, `5005` in the example below):

```python manage.py run --port 5005```

### Running unit tests

To run the unit tests and stop at the first failed test, in the terminal, run the following command:

```pytest -sxk 'not functional'```

### Running the functional tests

To run the functional tests and stop at the first failed test, use the following commands.

In MS Windows, use:

```powershell
$Env:WAIT="True"
pytest --log-cli-level="INFO" -sxk functional
```

In macOS, use:

```shell
export WAIT="True"
pytest --log-cli-level="INFO" -sxk functional
```

### Checking code formatting

To check if the imports are sorted correctly, run:

```isort . --check --diff```

To fix any issues, run:

```isort .```

To check code formatting, run:

```black . --check```

## Validate the entire project

To validate the entire project, run the following commands in the terminal.

If you are using MS Windows, run:

```.\validate.ps1```

If you are using macOS or Linux, run:

```./validate.sh```

# Code snippets

## Python

### New test class

If you want to create a new test class, create a file with the name `test_<objective>.py` within the `codeapp/tests` folder, and start the file with the following content.

```python
import logging

from .utils import TestCase


class Test<Feature>(TestCase):
    def test_<case_1>(self) -> None:
        pass

    def test_<case_2>(self) -> None:
        pass


if __name__ == "__main__":
    logging.fatal("This file cannot be run directly. Run `pytest` instead.")
```

## HTML

### New navbar item

```html
<!-- menu list definition -->
<ul class="navbar-nav me-auto mb-2 mb-md-0">

<!-- here you insert your new menu item -->
<li class="nav-item">
  <a
    {% set class="nav-link" %}
    {% if request.url_rule.endpoint == "<< endpoint >>" %}
    {% set class = class ~ " active" %}
    {% endif %}
    class="{{ class }}" 
    aria-current="page" 
    href="{{ url_for('<< endpoint >>') }}">
    <i class="bi bi-app"></i>
    << nav item title >>
  </a>
</li>
<!-- end of your new menu item -->

<!-- closing the list definition -->
</ul>
```

### New details page

```html
{% extends "base.html" %}
{% block content %}
<h2>!PAGE TITLE!</h2>
<div class="container">
    <!-- each info gets one row -->
    <div class="row">
        <div class="col-3"><p class="text-end">!INFO TITLE!</p></div>
        <div class="col-9"><b>!INFO VALUE!</b></div>
    </div>
    <!-- other infos -->
</div>
{% endblock content %}
```

Reference for the layout can be found here: https://getbootstrap.com/docs/5.1/layout/columns/

### New form page

To create a new page that contains a form, you can use the following structure.
Make sure to replace `!FORM TITLE!` by the title you want.
Also make sure to replace the name `form` if needed.

References for forms:
- WTForms fields: https://wtforms.readthedocs.io/en/3.0.x/fields/
- WTForms validators: https://wtforms.readthedocs.io/en/3.0.x/validators/

```html
{% extends "base.html" %}
{% block content %}
<form method="POST">
    {{ form.csrf_token }}
    <fieldset>
        <legend class="border-bottom mb-4">!FORM TITLE!</legend>
        
        <!-- your form fields here -->
        
    </fieldset>
    {{ form.submit(class="btn btn-outline-info") }}
    **<button type="reset" class="btn btn-secondary">Reset</button>**
</form>
{% endblock content %}
```

### General form fields

This snippet below works for most of the form fields, except checkboxes and radio buttons.

Replace the name `form` if needed.

Replace `!fieldname!` and `!PLACEHOLDER!` by the name of the field.

```html
<div class="mb-3">
    {{ form.!fieldname!.label(class="form-label") }}
    {% if form.!fieldname!.errors %}
        {{ form.!fieldname!(class="form-control is-invalid", placeholder="!PLACEHOLDER!") }}
        <div class="invalid-feedback">
            {% for error in form.!fieldname!.errors %}
                <span>{{ error }}</span>
            {% endfor %}
        </div>
    {% else %}
        {{ form.!fieldname!(class="form-control", placeholder="!PLACEHOLDER!") }}
    {% endif %}
</div>
```

References for form fields: https://wtforms.readthedocs.io/en/3.0.x/fields/

# Files that you MUST NOT change

There are some files within this project that are not meant for you to change.
During the project grading, the original files (from the skeleton repository) will be used.
If you change one of these files, your project will not run.

If you find some issue with one of these files, please open a discussion in the course discussion forum.

List of files/folders that MUST NOT be changed:
- .github/
- manage.py
- Procfile
- pyproject.toml
- runtime.txt
- setup.cfg
- validate.ps1
- validate.sh

Some specific files within the `codeapp` folder also MUST NOT be changed:
- \_ \_init\_ \_.py
- config.py
- tests/utils.py

# Suggestion for improvements

If you are planning to develop a mid/large scale project, I recommend you split the Python files within the `codeapp` folder into modules, each one with their own `routes.py` and `forms.py` files. The same would be done for the files within the `templates` folder.

# Contact

Original repository URL: https://github.com/carlosnatalino/

For questions and improvements, feel free to file issues in the GitHub repository. Please discuss any improvement suggestion in an issue before submitting pull requests.

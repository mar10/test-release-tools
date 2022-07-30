# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "yabs_test"
copyright = "2020, Martin Wendt"
author = "Martin Wendt"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinxcontrib.mermaid",
]

templates_path = ["_templates"]
exclude_patterns = []

source_suffix = {
    ".rst": "restructuredtext",
    # '.txt': 'markdown',
    ".md": "markdown",
}

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}
html_theme_options = {
    # "logo": "favicon-32x32.png",
    # "logo_text_align": "left",
    "show_powered_by": False,
    "github_user": "mar10",
    "github_repo": "yabs-test",
    "github_banner": True,
    "github_button": True,
    "github_type": "star",
    # "github_size": "small",
    "github_count": "true",
    # "travis_button": True,
    # "codecov_button": True,
    "show_related": False,
    "note_bg": "#FFF59C",
}

html_static_path = ["_static"]

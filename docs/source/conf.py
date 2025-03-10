# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "crimsonslate-portfolio"
copyright = "2024, crimsonslate"
author = "crimsonslate"
release = "1.3.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx_rtd_theme", "sphinx.ext.intersphinx"]

templates_path = ["_templates"]
exclude_patterns = []
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "django": (
        "http://docs.djangoproject.com/en/5.1/",
        "http://docs.djangoproject.com/en/5.1/_objects/",
    ),
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

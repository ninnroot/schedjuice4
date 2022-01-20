from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("jinja2_stuff"),
    autoescape=select_autoescape()
)

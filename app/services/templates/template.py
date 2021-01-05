from app.core import config

import jinja2

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(f"{config.BASEDIR}/server/templates/"),
    autoescape=jinja2.select_autoescape(['html'])
)


def render_to_string(template_name: str, *args, **kwargs):
    template = env.get_template(template_name)
    return template.render(*args, **kwargs)

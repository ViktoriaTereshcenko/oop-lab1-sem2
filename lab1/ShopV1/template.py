from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('views/templates'))

def render_template(template_name, context=None):
    if context is None:
        context = {}
    template = env.get_template(template_name)
    return template.render(context)

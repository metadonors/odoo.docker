import yaml
from jinja2 import Environment
from jinja2 import FileSystemLoader
import click
import os

ENV = Environment(loader=FileSystemLoader('./'))


@click.command()
@click.option('--template', help='Template file to use')
@click.option('--config', help='Config file to use')
def generate_odoo_conf(template, config):
    with open(config, 'r') as config_file:
        config = yaml.load(config_file)
        template = ENV.get_template(template)
        print(template.render(cfg=config, env=os.environ))


if __name__ == '__main__':
    generate_odoo_conf()

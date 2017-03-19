import datetime
import json
import click
import re
import requests
from bs4 import BeautifulSoup


@click.group(chain=True)
def cli():
    pass

def validate_url(ctx, param, value):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if regex.match(value):
        return value
    else:
        raise click.BadParameter('URL is not valid')

@cli.command()
@click.option('--url', callback=validate_url)
@click.option('--tags', default = None)
@click.option('--label', default = "")
@click.option('--name', default = None)
@click.option('--date', default = None)
def new_link(url, tags, label, name, date):
    if tags is None:
        tags = []
    else:
        tags = tags.split(",")
    if name is None:
        name = BeautifulSoup(requests.get(url).content, "html.parser").title.string
    if date is None:
        date = str(datetime.datetime.now()).split(".")[0]
    with open('content/shared_links.json') as data_file:
        links = json.load(data_file)
    links.append({"date":date, "name":name, "url": url, "label": label, "tags":tags})
    with open('content/shared_links.json', 'w') as data_file:
        json.dump(links, data_file)



if __name__ == '__main__':
    cli()


from pelican.generators import Generator
from pelican import signals
import json


class ShareLinkGenerator(Generator):
    def __init__(self, context, settings, path, theme, output_path, readers_cache_name='', **kwargs):
        super().__init__(context, settings, path, theme, output_path, readers_cache_name, **kwargs)
        self.links = []

    def generate_context(self):
        with open(self.context['PATH']+'/shared_links.json') as data_file:
            self.links = json.load(data_file)[::-1]

    def write_file(self, writer, dest, links, pagination_info):
        writer.write_file(dest, self.env.get_template("shared_links.html"), self.context, links=links,
                          pagination_info=pagination_info)

    def generate_output(self, writer):
        current_page_links = []
        pagination_info = {'nb_per_page': 5, 'cur_page': 1, 'nb': len(self.links)}
        pagination_info['nb_page'] = int((pagination_info['nb']-1)/pagination_info['nb_per_page'])+1
        for link in self.links:
            current_page_links.append(link)
            if len(current_page_links) == pagination_info['nb_per_page']:
                self.write_file(writer, "shared_links_{}.html".format(pagination_info['cur_page']), current_page_links,
                                pagination_info)
                if pagination_info['cur_page'] == 1:
                    self.write_file(writer, "shared_links.html".format(pagination_info['cur_page']), current_page_links,
                                    pagination_info)
                current_page_links = []
                pagination_info['cur_page'] += 1
        if len(current_page_links) > 0:
            self.write_file(writer, "shared_links_{}.html".format(pagination_info['cur_page']), current_page_links,
                            pagination_info)
            if pagination_info['cur_page'] == 1:
                self.write_file(writer, "shared_links.html".format(pagination_info['cur_page']), current_page_links,
                                pagination_info)


def get_generator(o):
    return ShareLinkGenerator


def add_laste_shared_link(generators):
    with open(generators[0].context['PATH'] + '/shared_links.json') as data_file:
        links = json.load(data_file)
    for generator in generators:
        generator.context['last_shared_link'] = links[-1]


def register():
    signals.get_generators.connect(get_generator)
    signals.all_generators_finalized.connect(add_laste_shared_link)


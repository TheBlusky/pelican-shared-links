from pelican.generators import Generator
from pelican import signals
import json
import os


class ShareLinkGenerator(Generator):
    def __init__(self, *args, **kwargs):
        super(ShareLinkGenerator, self).__init__(*args, **kwargs)
        self.links = []

    def generate_context(self):
        with open(os.path.join(self.context['PATH'], 'shared_links.json')) as data_file:
            self.links = json.load(data_file)[::-1]
        self.context['last_shared_link'] = self.links[0]

    def write_file(self, writer, dest, links, pagination_info):
        writer.write_file(dest, self.env.get_template("shared_links.html"), self.context, links=links,
                          pagination_info=pagination_info)

    def generate_output(self, writer):
        current_page_links = []
        pagination_info = {
            'nb_per_page': self.settings.get('SHARED_LINKS_PAGINATION', 5),
            'cur_page': 1,
            'nb': len(self.links)}
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


def register():
    signals.get_generators.connect(get_generator)


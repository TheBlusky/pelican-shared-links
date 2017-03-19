# pelican-shared-links
Sharing links (Shaarli Clone) plugin for Pelican

## Installation 
- Add `shared_links.py` in your plugin directory
- Add `shared_links.json` in your content directory
- Rename `shared_links.template-example.html` into `shared_links.html` in your template directoy, in change its content accorded to your template
- Change your `pelican` configuration so `shared_links` plugin is added, example:
```
PLUGIN_PATHS = ["plugins", "./plugins"]
PLUGINS = ["plugins.shared_links"]
```

## Usage
### Add links to your site
#### Using provided tool
- Put `tool.py` in your pelican root directory (you can rename it if you want)
- usage: `./tool.py new_link [OPTIONS]`, options :
  - `--url http://website.com` : The link you want to share
  - `--tags tag1,tag2` : (optional) tags to add to the link, coma separated (default, empty)
  - `--label label` : (optional) a short description of the link (default, empty)
  - `--name name` : (optional) name of the link (default, Website `<title>` info)
  - `--date date` : (optional) date of the sharing (default, now())

#### Manually
You can edit the `content/shared_links.json` file, it is a simple JSON file, with an array of dictionary using the following information, example :
```
[
  {
    "label": "Awesome website",
    "tags": ["website", "fun"],
    "name": "Site #1",
    "date": "2017-03-19 15:06:01",
    "url": "http://website1.com/"
  },
  {
    "label": "Another awesome website",
    "tags": ["website", "fun"],
    "name": "Site #2",
    "date": "2017-03-19 15:06:01",
    "url": "http://website2.com/"
  }
]
```

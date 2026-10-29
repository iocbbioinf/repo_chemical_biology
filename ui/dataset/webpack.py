from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    ".",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "dataset_search": "./js/dataset/search/index.js",
                "dataset_deposit_form": "./js/dataset/forms/index.js",
            },
            dependencies={
                # map in the geolocation field of the deposit form
                "leaflet": "^1.9.4",
            },
            devDependencies={},
            aliases={
                "@js/dataset": "./js/dataset"
            },
        )
    },
)

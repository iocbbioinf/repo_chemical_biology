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
            dependencies={},
            devDependencies={},
            aliases={
                "@js/dataset": "./js/dataset"
            },
        )
    },
)

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    ".",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "metabolomics_dataset_search": "./js/metabolomics_dataset/search/index.js",
                "metabolomics_dataset_deposit_form": "./js/metabolomics_dataset/forms/index.js",
            },
            dependencies={},
            devDependencies={},
            aliases={
                "@js/metabolomics_dataset": "./js/metabolomics_dataset"
            },
        )
    },
)

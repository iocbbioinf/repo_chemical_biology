from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    ".",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "proteomics_dataset_search": "./js/proteomics_dataset/search/index.js",
                "proteomics_dataset_deposit_form": "./js/proteomics_dataset/forms/index.js",
            },
            dependencies={},
            devDependencies={},
            aliases={
                "@js/proteomics_dataset": "./js/proteomics_dataset"
            },
        )
    },
)

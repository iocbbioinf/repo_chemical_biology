from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    ".",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "spectrum_search": "./js/spectrum/search/index.js",
                "spectrum_deposit_form": "./js/spectrum/forms/index.js",
            },
            dependencies={},
            devDependencies={},
            aliases={
                "@js/spectrum": "./js/spectrum"
            },
        )
    },
)

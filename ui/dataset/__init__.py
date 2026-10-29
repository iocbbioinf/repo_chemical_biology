from babel import Locale
from ccmm_invenio.ui.config import CCMMRecordsUIResourceConfig
from ccmm_invenio.ui.resource import CCMMRecordsUIResource
from oarepo_ui.utils import can_view_deposit_page
from flask_menu import current_menu
from invenio_i18n import lazy_gettext as _
from oarepo_ui.overrides import UIComponent
from oarepo_ui.overrides.components import UIComponentImportMode
from oarepo_ui.proxies import current_oarepo_ui


class DatasetUIResourceConfig(CCMMRecordsUIResourceConfig):
    template_folder = "templates"
    url_prefix = "/dataset"
    blueprint_name = "dataset_ui"
    model_name = "dataset"
    search_component = UIComponent(
        "DatasetResultsListItem",
        "@js/dataset/search/ResultsListItem",
        UIComponentImportMode.DEFAULT
    )

    components = [
        *CCMMRecordsUIResourceConfig.components,
    ]

    application_id = "dataset"


class DatasetUIResource(CCMMRecordsUIResource):
    pass

def ui_overrides(app):
    """Register UI overrides."""
    ui_resource_config = DatasetUIResourceConfig()

    if (
        current_oarepo_ui is not None
        and ui_resource_config.model
        and ui_resource_config.model.record_json_schema
        and ui_resource_config.search_component
    ):
        current_oarepo_ui.register_result_list_item(
            ui_resource_config.model.record_json_schema, ui_resource_config.search_component
        )


def init_menu(app):
    """Initialize menu before first request."""
    ui_resource_config = DatasetUIResourceConfig()

    with app.app_context():
        current_menu.submenu("plus.create_dataset").register(
            f"{ui_resource_config.blueprint_name}.deposit_create",
            _("New Dataset"),
            order=1,
            visible_when=can_view_deposit_page,
        )

def finalize_app(app):
    """Finalize app"""
    init_menu(app)
    ui_overrides(app)

def country_name(code):
    """English name of an ISO 3166-1 alpha-2 country code (e.g. "CZ" -> "Czechia")."""
    return Locale("en").territories.get(code, code) if code else ""


def create_blueprint(app):
    """Register blueprint for this resource."""
    blueprint = DatasetUIResource(DatasetUIResourceConfig()).as_blueprint()
    blueprint.add_app_template_filter(country_name, "country_name")
    return blueprint

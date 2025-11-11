"""
Person Update Page

Updates existing persons in Poool CRM via API using the generic entity update component.
"""

from src.components.crm import (
    render_entity_update_page,
    create_person_update_config
)

# Create person update configuration
config = create_person_update_config()

# Render the update page with person-specific configuration
render_entity_update_page(
    config=config,
    page_title="Personen-Aktualisierung",
    page_icon="👤"
)

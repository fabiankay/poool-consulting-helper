"""
CRM Company Update Page

Updates existing companies in Poool CRM via API using the generic entity update component.
"""

from src.components.crm import (
    render_entity_update_page,
    create_company_update_config
)

# Create company update configuration
config = create_company_update_config()

# Render the update page with company-specific configuration
render_entity_update_page(
    config=config,
    page_title="CRM Aktualisierung",
    page_icon="🔄"
)

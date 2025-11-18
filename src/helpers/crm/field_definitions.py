"""
Field definition functions for CRM operations.

Provides functions that return lists of required and optional fields
for companies, persons, clients, and suppliers.
"""

from typing import List, Dict


def get_required_company_fields() -> List[str]:
    """Return list of fields that are typically required for company creation."""
    return ["name"]


def get_optional_company_fields() -> List[str]:
    """Return list of optional fields for company creation."""
    return [
        # Core company info
        "name_legal", "name_token", "uid", "commercial_register", "jurisdiction",
        "management", "data_privacy_number",

        # Person fields (for company contacts)
        "salutation", "title", "firstname", "middlename", "lastname", "nickname",
        "position", "function", "department", "birthday", "gender",

        # Additional info
        "note", "is_operator",

        # Relationship flags
        "is_client", "is_supplier",

        # Client-specific fields
        "customer_number_client", "payment_time_day_num_client", "comment_client",
        "send_bill_to_email_to", "reference_number_required", "dunning_blocked",
        "client_number", "datev_account_client",

        # Supplier-specific fields
        "supplier_number", "comment_supplier", "comment_internal", "discount_day_num", "discount_percentage",
        "customer_number_supplier", "payment_time_day_num_supplier", "datev_account_supplier",

        # German/EU specific fields
        "leitweg_id", "datev_is_client_collection",

        # Tags
        "tags",

        # Complex fields (create nested objects)
        "address_street", "address_house_number", "address_zip", "address_city", "address_country", "address_title",
        "contact_phone", "contact_email", "contact_website"
    ]


def get_required_person_fields() -> List[str]:
    """Return list of fields that are typically required for person creation."""
    return ["firstname", "lastname"]


def get_optional_person_fields() -> List[str]:
    """Return list of optional fields for person creation."""
    return [
        "company", "company_id", "company_subsidiary_id", "email", "phone",
        "salutation", "title", "middlename", "middle_name", "nickname",
        "position", "function", "department",
        "tags", "contacts"
    ]


def get_client_fields() -> List[str]:
    """Return list of fields that belong to the client endpoint."""
    return [
        'customer_number_client', 'payment_time_day_num_client', 'dunning_blocked', 'dunning_document_blocked',
        'reference_number_required', 'datev_account_client', 'leitweg_id', 'datev_is_client_collection',
        'send_bill_to_email_to', 'send_bill_to_email_cc', 'send_bill_to_email_bcc',
        'send_by_email', 'send_by_mail', 'client_number', 'number_unique'
    ]


def get_supplier_fields() -> List[str]:
    """Return list of fields that belong to the supplier endpoint."""
    return [
        'supplier_number', 'customer_number_supplier', 'payment_time_day_num_supplier',
        'discount_day_num', 'discount_percentage',
        'comment_supplier', 'comment_internal', 'datev_account_supplier'
    ]


def get_field_api_name_mapping() -> Dict[str, str]:
    """
    Return mapping of internal field names to actual API field names.

    This allows us to have separate fields for client vs supplier endpoints
    that map to the same API field name but go to different endpoints.
    """
    return {
        # Client-specific mappings
        'customer_number_client': 'customer_number',
        'payment_time_day_num_client': 'payment_time_day_num',
        'datev_account_client': 'datev_account',
        'client_number': 'number',

        # Supplier-specific mappings
        'supplier_number': 'number',
        'customer_number_supplier': 'customer_number',
        'payment_time_day_num_supplier': 'payment_time_day_num',
        'datev_account_supplier': 'datev_account',
    }


def get_company_field_labels() -> Dict[str, str]:
    """Return mapping of API field names to human-readable German labels for companies."""
    return {
        # Core company info
        "name": "Firmenname",
        "name_legal": "Rechtlicher Firmenname",
        "name_token": "Kurzname",
        "uid": "UID-Nummer",
        "commercial_register": "Handelsregisternummer",
        "jurisdiction": "Gerichtsstand",
        "management": "Geschäftsführung",
        "data_privacy_number": "Datenschutznummer",

        # Person fields (for company contacts)
        "salutation": "Anrede",
        "title": "Titel",
        "firstname": "Vorname",
        "middlename": "Zweiter Vorname",
        "lastname": "Nachname",
        "nickname": "Spitzname",
        "position": "Position",
        "function": "Funktion",
        "department": "Abteilung",
        "birthday": "Geburtstag",
        "gender": "Geschlecht",

        # Additional info
        "note": "Notiz",
        "is_operator": "Ist Betreiber",

        # Relationship flags
        "is_client": "Ist Kunde",
        "is_supplier": "Ist Lieferant",

        # Client-specific fields
        "customer_number_client": "Kundennummer (Kunde)",
        "payment_time_day_num_client": "Zahlungsziel Tage (Kunde)",
        "comment_client": "Kommentar (Kunde)",
        "send_bill_to_email_to": "Rechnung per E-Mail an",
        "reference_number_required": "Referenznummer erforderlich",
        "dunning_blocked": "Mahnung gesperrt",
        "dunning_document_blocked": "Mahndokument gesperrt",
        "send_bill_to_email_cc": "Rechnung CC",
        "send_bill_to_email_bcc": "Rechnung BCC",
        "send_by_email": "Versand per E-Mail",
        "send_by_mail": "Versand per Post",
        "number_unique": "Eindeutige Nummer",
        "client_number": "Kundennummer",
        "datev_account_client": "DATEV-Konto (Kunde)",

        # Supplier-specific fields
        "supplier_number": "Lieferantennummer",
        "customer_number_supplier": "Kundennummer (Lieferant)",
        "payment_time_day_num_supplier": "Zahlungsziel Tage (Lieferant)",
        "comment_supplier": "Kommentar (Lieferant)",
        "comment_internal": "Interner Kommentar",
        "discount_day_num": "Skonto-Tage",
        "discount_percentage": "Skonto-Prozentsatz",
        "datev_account_supplier": "DATEV-Konto (Lieferant)",

        # German/EU specific fields
        "leitweg_id": "Leitweg-ID",
        "datev_is_client_collection": "DATEV Sammelkonto",

        # Tags
        "tags": "Tags",

        # Address fields
        "address_street": "Straße",
        "address_house_number": "Hausnummer",
        "address_zip": "PLZ",
        "address_city": "Stadt",
        "address_country": "Land",
        "address_title": "Adress-Titel",

        # Contact fields
        "contact_phone": "Telefon",
        "contact_email": "E-Mail",
        "contact_website": "Webseite"
    }


def get_person_field_labels() -> Dict[str, str]:
    """Return mapping of API field names to human-readable German labels for persons."""
    return {
        # Core person info
        "firstname": "Vorname",
        "lastname": "Nachname",
        "email": "E-Mail",
        "phone": "Telefon",
        "company": "Firma (Name)",

        # Details
        "salutation": "Anrede",
        "title": "Titel",
        "middlename": "Zweiter Vorname",
        "middle_name": "Zweiter Vorname",
        "nickname": "Spitzname",
        "position": "Position",
        "function": "Funktion",
        "department": "Abteilung",

        # Company relationship
        "company_id": "Firma (ID)",
        "company_subsidiary_id": "Niederlassung (ID)",

        # Additional
        "tags": "Tags",
        "contacts": "Kontakte"
    }


def get_company_field_tabs() -> Dict[str, List[str]]:
    """Return field organization for company tabs."""
    return {
        "Stammdaten": [
            "name", "name_legal", "name_token", "note",
            "is_client", "is_supplier"
        ],
        "Personendaten (EPUs)": [
            "salutation", "title", "firstname", "middlename",
            "lastname", "nickname", "position", "function",
            "department", "birthday", "gender"
        ],
        "Adresse": [
            "address_street", "address_house_number", "address_zip",
            "address_city", "address_country", "address_title"
        ],
        "Kontakt": [
            "contact_phone", "contact_email", "contact_website"
        ],
        "Kunde": [
            "customer_number_client", "client_number", "datev_account_client", "leitweg_id",
            "payment_time_day_num_client", "comment_client",
            "send_bill_to_email_to", "reference_number_required", "dunning_blocked"
        ],
        "Lieferant": [
            "supplier_number", "customer_number_supplier", "datev_account_supplier",
            "payment_time_day_num_supplier", "comment_supplier", "comment_internal",
            "discount_day_num", "discount_percentage"
        ],
        "Erweitert": [
            "uid", "commercial_register", "jurisdiction", "management", "data_privacy_number"
        ]
    }


def get_person_field_tabs() -> Dict[str, List[str]]:
    """Return field organization for person tabs."""
    return {
        "Stammdaten": [
            "firstname", "lastname", "email", "phone", "company"
        ],
        "Details": [
            "salutation", "title", "middlename", "nickname",
            "position", "function", "department"
        ],
        "Firma": [
            "company_id", "company_subsidiary_id"
        ],
        "Zusätzlich": [
            "tags"
        ]
    }

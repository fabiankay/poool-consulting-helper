Hello, it's me!
GET
https://app.poool.cc/api/2/hello_its_me
requires authentication
This basic test confirms you can access the Poool API with your Token.
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Authorization
:
Bearer  
Content-Type
:

Accept
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/hello_its_me" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "message": "Hello YOUR USERNAME! Welcome to Poool API for INSTANCE NAME.",
        "domain_id": "Your domain ID",
        "instance_id": "Your Instance ID"
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
20 CRM
Access company address book data
Company

Search companies
POST
https://app.poool.cc/api/2/companies/search
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Body Parameters
page
integer
Current page in paginated responses.
Example:
1

scopes
object[]

filters
object[]

sorts
object[]
Authorization
:
Bearer  
Content-Type
:

Accept
:

{
    "page": 1,
    "scopes": [
        {
            "name": "is_operator",
            "parameters": null
        }
    ],
    "filters": [
        {
            "field": "contacts.contact_type_id",
            "group": [
                {
                    "field": "firstname",
                    "logic": "and",
                    "operator": "=",
                    "value": "et"
                }
            ],
            "logic": "and",
            "operator": "in",
            "value": "quas"
        }
    ],
    "sorts": [
        {
            "field": "name_aggregated",
            "direction": "asc"
        }
    ]
}
Send Request 💥
curl --request POST \
    "https://app.poool.cc/api/2/companies/search" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"page\": 1,
    \"scopes\": [
        {
            \"name\": \"is_operator\"
        }
    ],
    \"filters\": [
        {
            \"field\": \"contacts.contact_type_id\",
            \"logic\": \"and\",
            \"operator\": \"in\",
            \"value\": \"quas\",
            \"group\": [
                {
                    \"field\": \"firstname\",
                    \"logic\": \"and\",
                    \"operator\": \"=\",
                    \"value\": \"et\"
                }
            ]
        }
    ],
    \"sorts\": [
        {
            \"field\": \"name_aggregated\",
            \"direction\": \"asc\"
        }
    ]
}"
{
    "data": [
        {
            "generic_field_id": 1,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 1,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 2,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        },
        {
            "generic_field_id": 2,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 3,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 4,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        }
    ],
    "links": {
        "first": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
        "last": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
        "prev": null,
        "next": "https://app.poool-dev.cc/api/2/endpoint/action?page=2"
    },
    "meta": {
        "current_page": 1,
        "from": 1,
        "last_page": 4,
        "links": [
            {
                "url": null,
                "label": "&laquo; Previous",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "2",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=3",
                "label": "3",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
                "label": "4",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "Next &raquo;",
                "active": false
            }
        ],
        "path": "https://app.poool-dev.cc/api/2/endpoint/action",
        "per_page": 50,
        "to": 50,
        "total": 167
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
New company structure
GET
https://app.poool.cc/api/2/companies/new
requires authentication
Generates an empty item structure with default values. Does not create/store data.
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Authorization
:
Bearer  
Content-Type
:

Accept
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/companies/new" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
List companies
GET
https://app.poool.cc/api/2/companies
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Query Parameters
page
integer
Current page in paginated responses.
Example:
1
scopes
string
Use a combination of any of the following scopes, limit scopes by "," (colon).
Must be one of:
is_client
is_operator
is_supplier
Example:
is_client,is_operator,is_supplier
sorts
string
Use a combination of any of the following sortable fields, descending sorting by prepending a "-" (minus), limit fields by "," (colon).
Must be one of:
id
name_aggregated
created_at
updated_at
Example:
id,-name_aggregated,created_at,updated_at
Authorization
:
Bearer  
Content-Type
:

Accept
:

page
:

scopes
:

sorts
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/companies?page=1&scopes=is_client%2Cis_operator%2Cis_supplier&sorts=id%2C-name_aggregated%2Ccreated_at%2Cupdated_at" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": [
        {
            "generic_field_id": 1,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 1,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 2,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        },
        {
            "generic_field_id": 2,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 3,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 4,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        }
    ],
    "links": {
        "first": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
        "last": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
        "prev": null,
        "next": "https://app.poool-dev.cc/api/2/endpoint/action?page=2"
    },
    "meta": {
        "current_page": 1,
        "from": 1,
        "last_page": 4,
        "links": [
            {
                "url": null,
                "label": "&laquo; Previous",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "2",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=3",
                "label": "3",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
                "label": "4",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "Next &raquo;",
                "active": false
            }
        ],
        "path": "https://app.poool-dev.cc/api/2/endpoint/action",
        "per_page": 50,
        "to": 50,
        "total": 167
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Create company
POST
https://app.poool.cc/api/2/companies
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

{
    "data": {
        "company_group_id": 2,
        "name": "ktjeumrdmnnfeqfwhabnll",
        "name_legal": "cuswm",
        "name_token": "ABC123",
        "type": "company",
        "uid": "xhpe",
        "management": "lx",
        "jurisdiction": "hhrvtxxbnjpoxotn",
        "commercial_register": "ybrubkyzkhhbrpiq",
        "data_privacy_number": "urcffkbvgttofiile",
        "salutation": "zpkguo",
        "title": "qymwtdogqezos",
        "firstname": "qwudvnzfssxq",
        "middlename": "vqtmewuqtqpich",
        "lastname": "mirvwyzgtdh",
        "nickname": "zytkjwuonwoe",
        "position": "habcrvqbhobytgt",
        "function": "wwykjqvbyobvk",
        "department": "tqjkkvppqvwkjdezptuohr",
        "maiden_name": "ksaibcvttvqaz",
        "birthday": "1970-01-01",
        "gender": "m",
        "addresses": [
            {
                "country_id": 8,
                "is_preferred": true,
                "title": "cgatecdummmqxpqmjil",
                "recipient_1": "iwnigwio",
                "recipient_2": "wbjxgqtqrurexszaaehklsye",
                "recipient_3": "ctlkbkf",
                "street_name": "yqvedhh",
                "street_number": "xkjxvyupbvhxbdulrzfplzpd",
                "street_additional": "ljdk",
                "zip": "aytpfaaidgpupfpeszebzkzm",
                "location": "aofoazar",
                "state": "qizpfcfblz",
                "pos": 18
            }
        ],
        "contacts": [
            {
                "contact_type_id": 13,
                "is_preferred": false,
                "title": "psjpxrqtyhvjk",
                "value": "suyxtwcsgrlldgakncf",
                "pos": 20
            }
        ],
        "tags": [
            {
                "id": 12
            }
        ]
    }
}
Send Request 💥
curl --request POST \
    "https://app.poool.cc/api/2/companies" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"company_group_id\": 2,
        \"name\": \"ktjeumrdmnnfeqfwhabnll\",
        \"name_legal\": \"cuswm\",
        \"name_token\": \"ABC123\",
        \"type\": \"company\",
        \"uid\": \"xhpe\",
        \"management\": \"lx\",
        \"jurisdiction\": \"hhrvtxxbnjpoxotn\",
        \"commercial_register\": \"ybrubkyzkhhbrpiq\",
        \"data_privacy_number\": \"urcffkbvgttofiile\",
        \"salutation\": \"zpkguo\",
        \"title\": \"qymwtdogqezos\",
        \"firstname\": \"qwudvnzfssxq\",
        \"middlename\": \"vqtmewuqtqpich\",
        \"lastname\": \"mirvwyzgtdh\",
        \"nickname\": \"zytkjwuonwoe\",
        \"position\": \"habcrvqbhobytgt\",
        \"function\": \"wwykjqvbyobvk\",
        \"department\": \"tqjkkvppqvwkjdezptuohr\",
        \"maiden_name\": \"ksaibcvttvqaz\",
        \"birthday\": \"1970-01-01\",
        \"gender\": \"m\",
        \"addresses\": [
            {
                \"country_id\": 8,
                \"is_preferred\": true,
                \"title\": \"cgatecdummmqxpqmjil\",
                \"recipient_1\": \"iwnigwio\",
                \"recipient_2\": \"wbjxgqtqrurexszaaehklsye\",
                \"recipient_3\": \"ctlkbkf\",
                \"street_name\": \"yqvedhh\",
                \"street_number\": \"xkjxvyupbvhxbdulrzfplzpd\",
                \"street_additional\": \"ljdk\",
                \"zip\": \"aytpfaaidgpupfpeszebzkzm\",
                \"location\": \"aofoazar\",
                \"state\": \"qizpfcfblz\",
                \"pos\": 18
            }
        ],
        \"contacts\": [
            {
                \"contact_type_id\": 13,
                \"is_preferred\": false,
                \"title\": \"psjpxrqtyhvjk\",
                \"value\": \"suyxtwcsgrlldgakncf\",
                \"pos\": 20
            }
        ],
        \"tags\": [
            {
                \"id\": 12
            }
        ]
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Show company
GET
https://app.poool.cc/api/2/companies/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
18
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/companies/18" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Update company
PUT
PATCH
https://app.poool.cc/api/2/companies/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
16
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

{
    "data": {
        "company_group_id": 10,
        "name": "vuuefmrepcul",
        "name_legal": "htzbebquzyjf",
        "name_token": "ABC123",
        "type": "company",
        "uid": "szhjadlsaatocchsvro",
        "management": "ijfthqvdfaxxzprildlcu",
        "jurisdiction": "qpwxtkresozzhhgv",
        "commercial_register": "xragmrmiykrmvlosggnw",
        "data_privacy_number": "stut",
        "salutation": "crrklxlab",
        "title": "myarsxwxashmof",
        "firstname": "brjjmildxcan",
        "middlename": "pnyqf",
        "lastname": "cwzgoazmzgjhrolnyiajbnjtq",
        "nickname": "mbf",
        "position": "mhkyuwnlqenbusho",
        "function": "boygglaghknrp",
        "department": "raqgaffrzuvgpjxnqvhtezcy",
        "maiden_name": "nzeaqmwdhsjxcmpipllamtblb",
        "birthday": "1970-01-01",
        "gender": "m",
        "addresses": [
            {
                "country_id": 14,
                "is_preferred": true,
                "title": "rkesrkwrtpodkehxmvaczvo",
                "recipient_1": "wkeemwgvbbaepl",
                "recipient_2": "bdfeijsodeejetjyqov",
                "recipient_3": "yseseeyccycawsgsfiks",
                "street_name": "rhwrtwtaaf",
                "street_number": "mljdptxnpexdsofdx",
                "street_additional": "ivkfixssyngqo",
                "zip": "lmnpnacfmxqzbpn",
                "location": "ehhucqocprgiswxgwxkzt",
                "state": "hfhzfzubfikk",
                "pos": 3
            }
        ],
        "contacts": [
            {
                "contact_type_id": 4,
                "is_preferred": true,
                "title": "ttegidv",
                "value": "gkdtnnptamfuliufet",
                "pos": 9
            }
        ],
        "tags": [
            {
                "id": 8
            }
        ]
    }
}
Send Request 💥
curl --request PUT \
    "https://app.poool.cc/api/2/companies/16" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"company_group_id\": 10,
        \"name\": \"vuuefmrepcul\",
        \"name_legal\": \"htzbebquzyjf\",
        \"name_token\": \"ABC123\",
        \"type\": \"company\",
        \"uid\": \"szhjadlsaatocchsvro\",
        \"management\": \"ijfthqvdfaxxzprildlcu\",
        \"jurisdiction\": \"qpwxtkresozzhhgv\",
        \"commercial_register\": \"xragmrmiykrmvlosggnw\",
        \"data_privacy_number\": \"stut\",
        \"salutation\": \"crrklxlab\",
        \"title\": \"myarsxwxashmof\",
        \"firstname\": \"brjjmildxcan\",
        \"middlename\": \"pnyqf\",
        \"lastname\": \"cwzgoazmzgjhrolnyiajbnjtq\",
        \"nickname\": \"mbf\",
        \"position\": \"mhkyuwnlqenbusho\",
        \"function\": \"boygglaghknrp\",
        \"department\": \"raqgaffrzuvgpjxnqvhtezcy\",
        \"maiden_name\": \"nzeaqmwdhsjxcmpipllamtblb\",
        \"birthday\": \"1970-01-01\",
        \"gender\": \"m\",
        \"addresses\": [
            {
                \"country_id\": 14,
                \"is_preferred\": true,
                \"title\": \"rkesrkwrtpodkehxmvaczvo\",
                \"recipient_1\": \"wkeemwgvbbaepl\",
                \"recipient_2\": \"bdfeijsodeejetjyqov\",
                \"recipient_3\": \"yseseeyccycawsgsfiks\",
                \"street_name\": \"rhwrtwtaaf\",
                \"street_number\": \"mljdptxnpexdsofdx\",
                \"street_additional\": \"ivkfixssyngqo\",
                \"zip\": \"lmnpnacfmxqzbpn\",
                \"location\": \"ehhucqocprgiswxgwxkzt\",
                \"state\": \"hfhzfzubfikk\",
                \"pos\": 3
            }
        ],
        \"contacts\": [
            {
                \"contact_type_id\": 4,
                \"is_preferred\": true,
                \"title\": \"ttegidv\",
                \"value\": \"gkdtnnptamfuliufet\",
                \"pos\": 9
            }
        ],
        \"tags\": [
            {
                \"id\": 8
            }
        ]
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Delete company
DELETE
https://app.poool.cc/api/2/companies/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
4
Query Parameters
app_version_override
boolean
Delete data set regardless of a failed version check.
Example:
false
app_version
integer
The version number of the the data set to be deleted. Must match current data set version.
Example:
42
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

app_version_override
:

app_version
:

Send Request 💥
curl --request DELETE \
    "https://app.poool.cc/api/2/companies/4?app_version_override=&app_version=42" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null,
        "action": "destroyed"
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Person

Search persons
POST
https://app.poool.cc/api/2/persons/search
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Body Parameters
page
integer
Current page in paginated responses.
Example:
1

scopes
object[]

filters
object[]

sorts
object[]
Authorization
:
Bearer  
Content-Type
:

Accept
:

{
    "page": 1,
    "scopes": [
        {
            "name": "is_external_user",
            "parameters": null
        }
    ],
    "filters": [
        {
            "field": "birthday",
            "group": [
                {
                    "field": "title",
                    "logic": "and",
                    "operator": "=",
                    "value": "distinctio"
                }
            ],
            "logic": "and",
            "operator": ">",
            "value": "quaerat"
        }
    ],
    "sorts": [
        {
            "field": "created_at",
            "direction": "desc"
        }
    ]
}
Send Request 💥
curl --request POST \
    "https://app.poool.cc/api/2/persons/search" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"page\": 1,
    \"scopes\": [
        {
            \"name\": \"is_external_user\"
        }
    ],
    \"filters\": [
        {
            \"field\": \"birthday\",
            \"logic\": \"and\",
            \"operator\": \">\",
            \"value\": \"quaerat\",
            \"group\": [
                {
                    \"field\": \"title\",
                    \"logic\": \"and\",
                    \"operator\": \"=\",
                    \"value\": \"distinctio\"
                }
            ]
        }
    ],
    \"sorts\": [
        {
            \"field\": \"created_at\",
            \"direction\": \"desc\"
        }
    ]
}"
{
    "data": [
        {
            "generic_field_id": 1,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 1,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 2,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        },
        {
            "generic_field_id": 2,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 3,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 4,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        }
    ],
    "links": {
        "first": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
        "last": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
        "prev": null,
        "next": "https://app.poool-dev.cc/api/2/endpoint/action?page=2"
    },
    "meta": {
        "current_page": 1,
        "from": 1,
        "last_page": 4,
        "links": [
            {
                "url": null,
                "label": "&laquo; Previous",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "2",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=3",
                "label": "3",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
                "label": "4",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "Next &raquo;",
                "active": false
            }
        ],
        "path": "https://app.poool-dev.cc/api/2/endpoint/action",
        "per_page": 50,
        "to": 50,
        "total": 167
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
New person structure
GET
https://app.poool.cc/api/2/persons/new
requires authentication
Generates an empty item structure with default values. Does not create/store data.
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Authorization
:
Bearer  
Content-Type
:

Accept
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/persons/new" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
List persons
GET
https://app.poool.cc/api/2/persons
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Query Parameters
page
integer
Current page in paginated responses.
Example:
1
scopes
string
Use a combination of any of the following scopes, limit scopes by "," (colon).
Must be one of:
is_staff
is_active_user
is_external_user
is_regular_user
Example:
is_staff,is_active_user,is_external_user,is_regular_user
sorts
string
Use a combination of any of the following sortable fields, descending sorting by prepending a "-" (minus), limit fields by "," (colon).
Must be one of:
id
firstname
lastname
created_at
updated_at
Example:
id,-firstname,lastname,created_at,updated_at
Authorization
:
Bearer  
Content-Type
:

Accept
:

page
:

scopes
:

sorts
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/persons?page=1&scopes=is_staff%2Cis_active_user%2Cis_external_user%2Cis_regular_user&sorts=id%2C-firstname%2Clastname%2Ccreated_at%2Cupdated_at" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": [
        {
            "generic_field_id": 1,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 1,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 2,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        },
        {
            "generic_field_id": 2,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 3,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 4,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        }
    ],
    "links": {
        "first": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
        "last": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
        "prev": null,
        "next": "https://app.poool-dev.cc/api/2/endpoint/action?page=2"
    },
    "meta": {
        "current_page": 1,
        "from": 1,
        "last_page": 4,
        "links": [
            {
                "url": null,
                "label": "&laquo; Previous",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "2",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=3",
                "label": "3",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
                "label": "4",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "Next &raquo;",
                "active": false
            }
        ],
        "path": "https://app.poool-dev.cc/api/2/endpoint/action",
        "per_page": 50,
        "to": 50,
        "total": 167
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Create person
POST
https://app.poool.cc/api/2/persons
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

{
    "data": {
        "company_id": 8,
        "company_subsidiary_id": 13,
        "salutation": "jhmtthqyhb",
        "title": "itjl",
        "firstname": "zinprnvdjzzmxmbwbmgc",
        "middlename": "rfli",
        "lastname": "wyfdwcoyfri",
        "nickname": "xeajgdcdogoyzmf",
        "position": "kpyaegrgs",
        "function": "smtoyuemjsxmhp",
        "department": "f",
        "maiden_name": "gwsxdkznaqpvzvyinpeytld",
        "birthday": "2025-09-09T13:11:47",
        "gender": "m",
        "addresses": [
            {
                "country_id": 7,
                "is_preferred": true,
                "title": "o",
                "recipient_1": "imvfjabwebfgnrewhmgqm",
                "recipient_2": "dnhjpmfwex",
                "recipient_3": "swvztuwgfdywabfxdrph",
                "street_name": "rjiwnagwbvhqadhmpxzgzhd",
                "street_number": "fngdlazgfwfmpzrg",
                "street_additional": "r",
                "zip": "sanrbsrdtytjpgqalppsixhge",
                "location": "subsjjzintwhrd",
                "state": "ieyww",
                "pos": 19
            }
        ],
        "contacts": [
            {
                "contact_type_id": 19,
                "is_preferred": false,
                "title": "lnilwgignb",
                "value": "vm",
                "pos": 17
            }
        ],
        "tags": [
            {
                "id": 20
            }
        ]
    }
}
Send Request 💥
curl --request POST \
    "https://app.poool.cc/api/2/persons" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"company_id\": 8,
        \"company_subsidiary_id\": 13,
        \"salutation\": \"jhmtthqyhb\",
        \"title\": \"itjl\",
        \"firstname\": \"zinprnvdjzzmxmbwbmgc\",
        \"middlename\": \"rfli\",
        \"lastname\": \"wyfdwcoyfri\",
        \"nickname\": \"xeajgdcdogoyzmf\",
        \"position\": \"kpyaegrgs\",
        \"function\": \"smtoyuemjsxmhp\",
        \"department\": \"f\",
        \"maiden_name\": \"gwsxdkznaqpvzvyinpeytld\",
        \"birthday\": \"2025-09-09T13:11:47\",
        \"gender\": \"m\",
        \"addresses\": [
            {
                \"country_id\": 7,
                \"is_preferred\": true,
                \"title\": \"o\",
                \"recipient_1\": \"imvfjabwebfgnrewhmgqm\",
                \"recipient_2\": \"dnhjpmfwex\",
                \"recipient_3\": \"swvztuwgfdywabfxdrph\",
                \"street_name\": \"rjiwnagwbvhqadhmpxzgzhd\",
                \"street_number\": \"fngdlazgfwfmpzrg\",
                \"street_additional\": \"r\",
                \"zip\": \"sanrbsrdtytjpgqalppsixhge\",
                \"location\": \"subsjjzintwhrd\",
                \"state\": \"ieyww\",
                \"pos\": 19
            }
        ],
        \"contacts\": [
            {
                \"contact_type_id\": 19,
                \"is_preferred\": false,
                \"title\": \"lnilwgignb\",
                \"value\": \"vm\",
                \"pos\": 17
            }
        ],
        \"tags\": [
            {
                \"id\": 20
            }
        ]
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Show person
GET
https://app.poool.cc/api/2/persons/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
7
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/persons/7" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Update person
PUT
PATCH
https://app.poool.cc/api/2/persons/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
10
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

{
    "data": {
        "company_id": 4,
        "company_subsidiary_id": 17,
        "salutation": "ijlvxpesoif",
        "title": "qanlzafvmuedugd",
        "firstname": "ksoendrohcwevkvtln",
        "middlename": "eqcurarkhqpfmseiecxixr",
        "lastname": "sphcfbwskwmdjei",
        "nickname": "cboqwncaonanxliqwbf",
        "position": "lcx",
        "function": "tvobdfctcmrlnbviqqw",
        "department": "baldiuwipxpohymmogxlbcheq",
        "maiden_name": "dxveorgmpqehydnl",
        "birthday": "2025-09-09T13:11:47",
        "gender": "f",
        "addresses": [
            {
                "country_id": 1,
                "is_preferred": true,
                "title": "fbxx",
                "recipient_1": "ohsccvtmsqtluxe",
                "recipient_2": "myccjyygmxssok",
                "recipient_3": "ueudqdhkgizfrnrmrlvv",
                "street_name": "lgeanhhfch",
                "street_number": "zkljpfxfcgzu",
                "street_additional": "vobggzbzag",
                "zip": "gwtrpndkrgwaob",
                "location": "xizlpwucddrwfbznemtti",
                "state": "tabvrxftoqmbd",
                "pos": 1
            }
        ],
        "contacts": [
            {
                "contact_type_id": 7,
                "is_preferred": false,
                "title": "rrdrwkw",
                "value": "qcnliomb",
                "pos": 8
            }
        ],
        "tags": [
            {
                "id": 19
            }
        ]
    }
}
Send Request 💥
curl --request PUT \
    "https://app.poool.cc/api/2/persons/10" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"company_id\": 4,
        \"company_subsidiary_id\": 17,
        \"salutation\": \"ijlvxpesoif\",
        \"title\": \"qanlzafvmuedugd\",
        \"firstname\": \"ksoendrohcwevkvtln\",
        \"middlename\": \"eqcurarkhqpfmseiecxixr\",
        \"lastname\": \"sphcfbwskwmdjei\",
        \"nickname\": \"cboqwncaonanxliqwbf\",
        \"position\": \"lcx\",
        \"function\": \"tvobdfctcmrlnbviqqw\",
        \"department\": \"baldiuwipxpohymmogxlbcheq\",
        \"maiden_name\": \"dxveorgmpqehydnl\",
        \"birthday\": \"2025-09-09T13:11:47\",
        \"gender\": \"f\",
        \"addresses\": [
            {
                \"country_id\": 1,
                \"is_preferred\": true,
                \"title\": \"fbxx\",
                \"recipient_1\": \"ohsccvtmsqtluxe\",
                \"recipient_2\": \"myccjyygmxssok\",
                \"recipient_3\": \"ueudqdhkgizfrnrmrlvv\",
                \"street_name\": \"lgeanhhfch\",
                \"street_number\": \"zkljpfxfcgzu\",
                \"street_additional\": \"vobggzbzag\",
                \"zip\": \"gwtrpndkrgwaob\",
                \"location\": \"xizlpwucddrwfbznemtti\",
                \"state\": \"tabvrxftoqmbd\",
                \"pos\": 1
            }
        ],
        \"contacts\": [
            {
                \"contact_type_id\": 7,
                \"is_preferred\": false,
                \"title\": \"rrdrwkw\",
                \"value\": \"qcnliomb\",
                \"pos\": 8
            }
        ],
        \"tags\": [
            {
                \"id\": 19
            }
        ]
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Delete person
DELETE
https://app.poool.cc/api/2/persons/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
2
Query Parameters
app_version_override
boolean
Delete data set regardless of a failed version check.
Example:
false
app_version
integer
The version number of the the data set to be deleted. Must match current data set version.
Example:
42
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

app_version_override
:

app_version
:

Send Request 💥
curl --request DELETE \
    "https://app.poool.cc/api/2/persons/2?app_version_override=&app_version=42" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null,
        "action": "destroyed"
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
CompanySubsidiary

New company subsidiary structure
GET
https://app.poool.cc/api/2/company_subsidiaries/new
requires authentication
Generates an empty item structure with default values. Does not create/store data.
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Authorization
:
Bearer  
Content-Type
:

Accept
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/company_subsidiaries/new" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
List company subsidiaries
GET
https://app.poool.cc/api/2/company_subsidiaries
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Query Parameters
page
integer
Current page in paginated responses.
Example:
1
scopes
string
No scopes available.
sorts
string
No sorts available.
Authorization
:
Bearer  
Content-Type
:

Accept
:

page
:

scopes
:

sorts
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/company_subsidiaries?page=1" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": [
        {
            "generic_field_id": 1,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 1,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 2,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        },
        {
            "generic_field_id": 2,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 3,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 4,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        }
    ],
    "links": {
        "first": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
        "last": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
        "prev": null,
        "next": "https://app.poool-dev.cc/api/2/endpoint/action?page=2"
    },
    "meta": {
        "current_page": 1,
        "from": 1,
        "last_page": 4,
        "links": [
            {
                "url": null,
                "label": "&laquo; Previous",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "2",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=3",
                "label": "3",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
                "label": "4",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "Next &raquo;",
                "active": false
            }
        ],
        "path": "https://app.poool-dev.cc/api/2/endpoint/action",
        "per_page": 50,
        "to": 50,
        "total": 167
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Create company subsidiary
POST
https://app.poool.cc/api/2/company_subsidiaries
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

{
    "data": {
        "company_id": 10,
        "name_location": "kvonxctqclwhummcyut",
        "name": "ohzeml",
        "name_legal": "lx",
        "name_token": "cutfzhqhqoqgknbagilcitmld",
        "uid": "sazgknynlvgkyxasqaxeowfip",
        "tags": [
            {
                "id": 5
            }
        ]
    }
}
Send Request 💥
curl --request POST \
    "https://app.poool.cc/api/2/company_subsidiaries" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"company_id\": 10,
        \"name_location\": \"kvonxctqclwhummcyut\",
        \"name\": \"ohzeml\",
        \"name_legal\": \"lx\",
        \"name_token\": \"cutfzhqhqoqgknbagilcitmld\",
        \"uid\": \"sazgknynlvgkyxasqaxeowfip\",
        \"tags\": [
            {
                \"id\": 5
            }
        ]
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Show company subsidiary
GET
https://app.poool.cc/api/2/company_subsidiaries/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
15
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/company_subsidiaries/15" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Update company subsidiary
PUT
PATCH
https://app.poool.cc/api/2/company_subsidiaries/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
20
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

{
    "data": {
        "company_id": 8,
        "name_location": "atrffkgbpealisxbwhcachuz",
        "name": "skbwtzqyacixgziiriex",
        "name_legal": "fvwmlqvjalmbj",
        "name_token": "tjqkfckpmjdfzrpeerllawa",
        "uid": "kqpoqkvqsuhq",
        "tags": [
            {
                "id": 15
            }
        ]
    }
}
Send Request 💥
curl --request PUT \
    "https://app.poool.cc/api/2/company_subsidiaries/20" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"company_id\": 8,
        \"name_location\": \"atrffkgbpealisxbwhcachuz\",
        \"name\": \"skbwtzqyacixgziiriex\",
        \"name_legal\": \"fvwmlqvjalmbj\",
        \"name_token\": \"tjqkfckpmjdfzrpeerllawa\",
        \"uid\": \"kqpoqkvqsuhq\",
        \"tags\": [
            {
                \"id\": 15
            }
        ]
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Delete company subsidiary
DELETE
https://app.poool.cc/api/2/company_subsidiaries/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
20
Query Parameters
app_version_override
boolean
Delete data set regardless of a failed version check.
Example:
false
app_version
integer
The version number of the the data set to be deleted. Must match current data set version.
Example:
42
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

app_version_override
:

app_version
:

Send Request 💥
curl --request DELETE \
    "https://app.poool.cc/api/2/company_subsidiaries/20?app_version_override=&app_version=42" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null,
        "action": "destroyed"
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
CompanyGroup

New company group structure
GET
https://app.poool.cc/api/2/company_groups/new
requires authentication
Generates an empty item structure with default values. Does not create/store data.
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Authorization
:
Bearer  
Content-Type
:

Accept
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/company_groups/new" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
List company groups
GET
https://app.poool.cc/api/2/company_groups
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Query Parameters
page
integer
Current page in paginated responses.
Example:
1
scopes
string
No scopes available.
sorts
string
Use a combination of any of the following sortable fields, descending sorting by prepending a "-" (minus), limit fields by "," (colon).
Must be one of:
id
name
name_legal
name_token
created_at
updated_at
Example:
id,-name,name_legal,name_token,created_at
Authorization
:
Bearer  
Content-Type
:

Accept
:

page
:

scopes
:

sorts
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/company_groups?page=1&sorts=id%2C-name%2Cname_legal%2Cname_token%2Ccreated_at" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": [
        {
            "generic_field_id": 1,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 1,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 2,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        },
        {
            "generic_field_id": 2,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 3,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 4,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        }
    ],
    "links": {
        "first": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
        "last": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
        "prev": null,
        "next": "https://app.poool-dev.cc/api/2/endpoint/action?page=2"
    },
    "meta": {
        "current_page": 1,
        "from": 1,
        "last_page": 4,
        "links": [
            {
                "url": null,
                "label": "&laquo; Previous",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "2",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=3",
                "label": "3",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
                "label": "4",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "Next &raquo;",
                "active": false
            }
        ],
        "path": "https://app.poool-dev.cc/api/2/endpoint/action",
        "per_page": 50,
        "to": 50,
        "total": 167
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Create company group
POST
https://app.poool.cc/api/2/company_groups
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

{
    "data": {
        "name": "tjpyiymwhvbn",
        "name_legal": "veqpqjwvkxpxzli",
        "name_token": "erlzmjtfgu"
    }
}
Send Request 💥
curl --request POST \
    "https://app.poool.cc/api/2/company_groups" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"name\": \"tjpyiymwhvbn\",
        \"name_legal\": \"veqpqjwvkxpxzli\",
        \"name_token\": \"erlzmjtfgu\"
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Show company group
GET
https://app.poool.cc/api/2/company_groups/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
11
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/company_groups/11" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Update company group
PUT
PATCH
https://app.poool.cc/api/2/company_groups/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
19
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

{
    "data": {
        "name": "aogyblkjewlwqqyaleyxja",
        "name_legal": "ortsnxmoukroneqqmjvjcl",
        "name_token": "ejfbftse"
    }
}
Send Request 💥
curl --request PUT \
    "https://app.poool.cc/api/2/company_groups/19" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"name\": \"aogyblkjewlwqqyaleyxja\",
        \"name_legal\": \"ortsnxmoukroneqqmjvjcl\",
        \"name_token\": \"ejfbftse\"
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Delete company group
DELETE
https://app.poool.cc/api/2/company_groups/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
16
Query Parameters
app_version_override
boolean
Delete data set regardless of a failed version check.
Example:
false
app_version
integer
The version number of the the data set to be deleted. Must match current data set version.
Example:
42
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

app_version_override
:

app_version
:

Send Request 💥
curl --request DELETE \
    "https://app.poool.cc/api/2/company_groups/16?app_version_override=&app_version=42" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null,
        "action": "destroyed"
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
ContactType

New contact type structure
GET
https://app.poool.cc/api/2/contact_types/new
requires authentication
Generates an empty item structure with default values. Does not create/store data.
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Authorization
:
Bearer  
Content-Type
:

Accept
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/contact_types/new" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
List contact types
GET
https://app.poool.cc/api/2/contact_types
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Query Parameters
page
integer
Current page in paginated responses.
Example:
1
scopes
string
No scopes available.
sorts
string
No sorts available.
Authorization
:
Bearer  
Content-Type
:

Accept
:

page
:

scopes
:

sorts
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/contact_types?page=1" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": [
        {
            "generic_field_id": 1,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 1,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 2,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        },
        {
            "generic_field_id": 2,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 3,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 4,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        }
    ],
    "links": {
        "first": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
        "last": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
        "prev": null,
        "next": "https://app.poool-dev.cc/api/2/endpoint/action?page=2"
    },
    "meta": {
        "current_page": 1,
        "from": 1,
        "last_page": 4,
        "links": [
            {
                "url": null,
                "label": "&laquo; Previous",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "2",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=3",
                "label": "3",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
                "label": "4",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "Next &raquo;",
                "active": false
            }
        ],
        "path": "https://app.poool-dev.cc/api/2/endpoint/action",
        "per_page": 50,
        "to": 50,
        "total": 167
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Create contact type
POST
https://app.poool.cc/api/2/contact_types
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

{
    "data": {
        "title": "covmppbqjdgqwa"
    }
}
Send Request 💥
curl --request POST \
    "https://app.poool.cc/api/2/contact_types" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"title\": \"covmppbqjdgqwa\"
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Show contact type
GET
https://app.poool.cc/api/2/contact_types/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
16
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/contact_types/16" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Update contact type
PUT
PATCH
https://app.poool.cc/api/2/contact_types/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
1
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

{
    "data": {
        "title": "lkgbq"
    }
}
Send Request 💥
curl --request PUT \
    "https://app.poool.cc/api/2/contact_types/1" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"title\": \"lkgbq\"
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Delete contact type
DELETE
https://app.poool.cc/api/2/contact_types/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
14
Query Parameters
app_version_override
boolean
Delete data set regardless of a failed version check.
Example:
false
app_version
integer
The version number of the the data set to be deleted. Must match current data set version.
Example:
42
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

app_version_override
:

app_version
:

Send Request 💥
curl --request DELETE \
    "https://app.poool.cc/api/2/contact_types/14?app_version_override=&app_version=42" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null,
        "action": "destroyed"
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Country

New country structure
GET
https://app.poool.cc/api/2/countries/new
requires authentication
Generates an empty item structure with default values. Does not create/store data.
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Authorization
:
Bearer  
Content-Type
:

Accept
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/countries/new" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
List countries
GET
https://app.poool.cc/api/2/countries
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Query Parameters
page
integer
Current page in paginated responses.
Example:
1
scopes
string
No scopes available.
sorts
string
No sorts available.
Authorization
:
Bearer  
Content-Type
:

Accept
:

page
:

scopes
:

sorts
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/countries?page=1" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": [
        {
            "generic_field_id": 1,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 1,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 2,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        },
        {
            "generic_field_id": 2,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 3,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 4,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        }
    ],
    "links": {
        "first": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
        "last": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
        "prev": null,
        "next": "https://app.poool-dev.cc/api/2/endpoint/action?page=2"
    },
    "meta": {
        "current_page": 1,
        "from": 1,
        "last_page": 4,
        "links": [
            {
                "url": null,
                "label": "&laquo; Previous",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "2",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=3",
                "label": "3",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
                "label": "4",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "Next &raquo;",
                "active": false
            }
        ],
        "path": "https://app.poool-dev.cc/api/2/endpoint/action",
        "per_page": 50,
        "to": 50,
        "total": 167
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Create country
POST
https://app.poool.cc/api/2/countries
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

{
    "data": {
        "iso_3166_alpha2": "wn",
        "iso_3166_alpha3": "bk",
        "name_german": "oerrfiy",
        "name_local": "gmcqeltpxcfykiszywthx",
        "name_international": "wozn",
        "is_eu_member": true,
        "phone_prefix": 1,
        "top_level_domain": "qzujyfbwwuzwg"
    }
}
Send Request 💥
curl --request POST \
    "https://app.poool.cc/api/2/countries" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"iso_3166_alpha2\": \"wn\",
        \"iso_3166_alpha3\": \"bk\",
        \"name_german\": \"oerrfiy\",
        \"name_local\": \"gmcqeltpxcfykiszywthx\",
        \"name_international\": \"wozn\",
        \"is_eu_member\": true,
        \"phone_prefix\": 1,
        \"top_level_domain\": \"qzujyfbwwuzwg\"
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Show country
GET
https://app.poool.cc/api/2/countries/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
1
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/countries/1" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Update country
PUT
PATCH
https://app.poool.cc/api/2/countries/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
1
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

{
    "data": {
        "iso_3166_alpha2": "y",
        "iso_3166_alpha3": "vy",
        "name_german": "rvvqemmimfztjuvjori",
        "name_local": "xypkeheewuiizxf",
        "name_international": "xevkvcu",
        "is_eu_member": true,
        "phone_prefix": 14,
        "top_level_domain": "dbfdwb"
    }
}
Send Request 💥
curl --request PUT \
    "https://app.poool.cc/api/2/countries/1" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"iso_3166_alpha2\": \"y\",
        \"iso_3166_alpha3\": \"vy\",
        \"name_german\": \"rvvqemmimfztjuvjori\",
        \"name_local\": \"xypkeheewuiizxf\",
        \"name_international\": \"xevkvcu\",
        \"is_eu_member\": true,
        \"phone_prefix\": 14,
        \"top_level_domain\": \"dbfdwb\"
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Delete country
DELETE
https://app.poool.cc/api/2/countries/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
5
Query Parameters
app_version_override
boolean
Delete data set regardless of a failed version check.
Example:
false
app_version
integer
The version number of the the data set to be deleted. Must match current data set version.
Example:
42
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

app_version_override
:

app_version
:

Send Request 💥
curl --request DELETE \
    "https://app.poool.cc/api/2/countries/5?app_version_override=&app_version=42" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null,
        "action": "destroyed"
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Client

Search clients
POST
https://app.poool.cc/api/2/clients/search
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Body Parameters
page
integer
Current page in paginated responses.
Example:
1

scopes
object[]

filters
object[]

sorts
object[]
Authorization
:
Bearer  
Content-Type
:

Accept
:

{
    "page": 1,
    "scopes": [
        {
            "name": "history",
            "parameters": null
        }
    ],
    "filters": [
        {
            "field": "company_id",
            "group": [
                {
                    "field": "company_id",
                    "logic": "and",
                    "operator": "<=",
                    "value": "a"
                }
            ],
            "logic": "or",
            "operator": "like",
            "value": "repellendus"
        }
    ],
    "sorts": [
        {
            "field": "id",
            "direction": "asc"
        }
    ]
}
Send Request 💥
curl --request POST \
    "https://app.poool.cc/api/2/clients/search" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"page\": 1,
    \"scopes\": [
        {
            \"name\": \"history\"
        }
    ],
    \"filters\": [
        {
            \"field\": \"company_id\",
            \"logic\": \"or\",
            \"operator\": \"like\",
            \"value\": \"repellendus\",
            \"group\": [
                {
                    \"field\": \"company_id\",
                    \"logic\": \"and\",
                    \"operator\": \"<=\",
                    \"value\": \"a\"
                }
            ]
        }
    ],
    \"sorts\": [
        {
            \"field\": \"id\",
            \"direction\": \"asc\"
        }
    ]
}"
{
    "data": [
        {
            "generic_field_id": 1,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 1,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 2,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        },
        {
            "generic_field_id": 2,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 3,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 4,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        }
    ],
    "links": {
        "first": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
        "last": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
        "prev": null,
        "next": "https://app.poool-dev.cc/api/2/endpoint/action?page=2"
    },
    "meta": {
        "current_page": 1,
        "from": 1,
        "last_page": 4,
        "links": [
            {
                "url": null,
                "label": "&laquo; Previous",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "2",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=3",
                "label": "3",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
                "label": "4",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "Next &raquo;",
                "active": false
            }
        ],
        "path": "https://app.poool-dev.cc/api/2/endpoint/action",
        "per_page": 50,
        "to": 50,
        "total": 167
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
New client structure
GET
https://app.poool.cc/api/2/clients/new
requires authentication
Generates an empty item structure with default values. Does not create/store data.
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Authorization
:
Bearer  
Content-Type
:

Accept
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/clients/new" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
List clients
GET
https://app.poool.cc/api/2/clients
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Query Parameters
page
integer
Current page in paginated responses.
Example:
1
scopes
string
Use a combination of any of the following scopes, limit scopes by "," (colon).
Must be one of:
favorites
history
Example:
favorites,history
sorts
string
Use a combination of any of the following sortable fields, descending sorting by prepending a "-" (minus), limit fields by "," (colon).
Must be one of:
id
Example:
id
Authorization
:
Bearer  
Content-Type
:

Accept
:

page
:

scopes
:

sorts
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/clients?page=1&scopes=favorites%2Chistory&sorts=id" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": [
        {
            "generic_field_id": 1,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 1,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 2,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        },
        {
            "generic_field_id": 2,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 3,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 4,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        }
    ],
    "links": {
        "first": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
        "last": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
        "prev": null,
        "next": "https://app.poool-dev.cc/api/2/endpoint/action?page=2"
    },
    "meta": {
        "current_page": 1,
        "from": 1,
        "last_page": 4,
        "links": [
            {
                "url": null,
                "label": "&laquo; Previous",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "2",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=3",
                "label": "3",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
                "label": "4",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "Next &raquo;",
                "active": false
            }
        ],
        "path": "https://app.poool-dev.cc/api/2/endpoint/action",
        "per_page": 50,
        "to": 50,
        "total": 167
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Create client
POST
https://app.poool.cc/api/2/clients
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

{
    "data": {
        "company_id": 5,
        "custom_activity_cost_set_id": 15,
        "number_range_id": 2,
        "person_responsible_id": 14,
        "number": "lkz",
        "number_unique": "uqfhvu",
        "payment_time_day_num": 7,
        "dunning_blocked": "0",
        "dunning_document_blocked": "1",
        "reference_number_required": "1",
        "default_tax_id": 8,
        "comment_client": null,
        "comment_internal": null,
        "datev_account": "qdrtcmkihmwdkayjkrtmj",
        "leitweg_id": "lmg",
        "supplier_number": "bfovkolqhtsigsol",
        "datev_is_client_collection": "0",
        "oob_document_template_order_default_id": 2,
        "oob_document_template_offer_default_id": 9,
        "oob_document_template_bill_default_id": 1,
        "oob_email_template_order_default_id": 16,
        "oob_email_template_offer_default_id": 2,
        "oob_email_template_bill_default_id": 1,
        "send_bill_to_email_to": "rswjjvwvgrgkzfyaums",
        "send_bill_to_email_cc": "fvzvafhilndrnsipogbsllawn",
        "send_bill_to_email_bcc": "vh",
        "send_by_email": "0",
        "send_by_mail": "1"
    }
}
Send Request 💥
curl --request POST \
    "https://app.poool.cc/api/2/clients" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"company_id\": 5,
        \"custom_activity_cost_set_id\": 15,
        \"number_range_id\": 2,
        \"person_responsible_id\": 14,
        \"number\": \"lkz\",
        \"number_unique\": \"uqfhvu\",
        \"payment_time_day_num\": 7,
        \"dunning_blocked\": \"0\",
        \"dunning_document_blocked\": \"1\",
        \"reference_number_required\": \"1\",
        \"default_tax_id\": 8,
        \"datev_account\": \"qdrtcmkihmwdkayjkrtmj\",
        \"leitweg_id\": \"lmg\",
        \"supplier_number\": \"bfovkolqhtsigsol\",
        \"datev_is_client_collection\": \"0\",
        \"oob_document_template_order_default_id\": 2,
        \"oob_document_template_offer_default_id\": 9,
        \"oob_document_template_bill_default_id\": 1,
        \"oob_email_template_order_default_id\": 16,
        \"oob_email_template_offer_default_id\": 2,
        \"oob_email_template_bill_default_id\": 1,
        \"send_bill_to_email_to\": \"rswjjvwvgrgkzfyaums\",
        \"send_bill_to_email_cc\": \"fvzvafhilndrnsipogbsllawn\",
        \"send_bill_to_email_bcc\": \"vh\",
        \"send_by_email\": \"0\",
        \"send_by_mail\": \"1\"
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Show client
GET
https://app.poool.cc/api/2/clients/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
12
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/clients/12" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Update client
PUT
PATCH
https://app.poool.cc/api/2/clients/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
16
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

{
    "data": {
        "company_id": 15,
        "custom_activity_cost_set_id": 12,
        "number_range_id": 2,
        "person_responsible_id": 2,
        "number": "wbuv",
        "number_unique": "ftdvdo",
        "payment_time_day_num": 11,
        "dunning_blocked": "0",
        "dunning_document_blocked": "0",
        "reference_number_required": "1",
        "default_tax_id": 12,
        "comment_client": null,
        "comment_internal": null,
        "datev_account": "mymftjqnjsrgiohstlm",
        "leitweg_id": "fosxfnc",
        "supplier_number": "lksvemmpibylrkaavlkist",
        "datev_is_client_collection": "0",
        "oob_document_template_order_default_id": 6,
        "oob_document_template_offer_default_id": 20,
        "oob_document_template_bill_default_id": 11,
        "oob_email_template_order_default_id": 7,
        "oob_email_template_offer_default_id": 4,
        "oob_email_template_bill_default_id": 5,
        "send_bill_to_email_to": "qlfpffzre",
        "send_bill_to_email_cc": "kpfecoxiegiviimxtehkrch",
        "send_bill_to_email_bcc": "j",
        "send_by_email": "0",
        "send_by_mail": "1"
    }
}
Send Request 💥
curl --request PUT \
    "https://app.poool.cc/api/2/clients/16" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"company_id\": 15,
        \"custom_activity_cost_set_id\": 12,
        \"number_range_id\": 2,
        \"person_responsible_id\": 2,
        \"number\": \"wbuv\",
        \"number_unique\": \"ftdvdo\",
        \"payment_time_day_num\": 11,
        \"dunning_blocked\": \"0\",
        \"dunning_document_blocked\": \"0\",
        \"reference_number_required\": \"1\",
        \"default_tax_id\": 12,
        \"datev_account\": \"mymftjqnjsrgiohstlm\",
        \"leitweg_id\": \"fosxfnc\",
        \"supplier_number\": \"lksvemmpibylrkaavlkist\",
        \"datev_is_client_collection\": \"0\",
        \"oob_document_template_order_default_id\": 6,
        \"oob_document_template_offer_default_id\": 20,
        \"oob_document_template_bill_default_id\": 11,
        \"oob_email_template_order_default_id\": 7,
        \"oob_email_template_offer_default_id\": 4,
        \"oob_email_template_bill_default_id\": 5,
        \"send_bill_to_email_to\": \"qlfpffzre\",
        \"send_bill_to_email_cc\": \"kpfecoxiegiviimxtehkrch\",
        \"send_bill_to_email_bcc\": \"j\",
        \"send_by_email\": \"0\",
        \"send_by_mail\": \"1\"
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Delete client
DELETE
https://app.poool.cc/api/2/clients/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
16
Query Parameters
app_version_override
boolean
Delete data set regardless of a failed version check.
Example:
false
app_version
integer
The version number of the the data set to be deleted. Must match current data set version.
Example:
42
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

app_version_override
:

app_version
:

Send Request 💥
curl --request DELETE \
    "https://app.poool.cc/api/2/clients/16?app_version_override=&app_version=42" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null,
        "action": "destroyed"
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Supplier

Search suppliers
POST
https://app.poool.cc/api/2/suppliers/search
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Body Parameters
page
integer
Current page in paginated responses.
Example:
1
scopes
object
No scopes available.
filters
object
No filters available.
sorts
object
No sorts available.
Authorization
:
Bearer  
Content-Type
:

Accept
:

{
    "page": 1,
    "scopes": null,
    "filters": null,
    "sorts": null
}
Send Request 💥
curl --request POST \
    "https://app.poool.cc/api/2/suppliers/search" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"page\": 1
}"
{
    "data": [
        {
            "generic_field_id": 1,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 1,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 2,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        },
        {
            "generic_field_id": 2,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 3,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 4,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        }
    ],
    "links": {
        "first": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
        "last": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
        "prev": null,
        "next": "https://app.poool-dev.cc/api/2/endpoint/action?page=2"
    },
    "meta": {
        "current_page": 1,
        "from": 1,
        "last_page": 4,
        "links": [
            {
                "url": null,
                "label": "&laquo; Previous",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "2",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=3",
                "label": "3",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
                "label": "4",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "Next &raquo;",
                "active": false
            }
        ],
        "path": "https://app.poool-dev.cc/api/2/endpoint/action",
        "per_page": 50,
        "to": 50,
        "total": 167
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
New supplier structure
GET
https://app.poool.cc/api/2/suppliers/new
requires authentication
Generates an empty item structure with default values. Does not create/store data.
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Authorization
:
Bearer  
Content-Type
:

Accept
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/suppliers/new" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
List suppliers
GET
https://app.poool.cc/api/2/suppliers
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Query Parameters
page
integer
Current page in paginated responses.
Example:
1
scopes
string
No scopes available.
sorts
string
No sorts available.
Authorization
:
Bearer  
Content-Type
:

Accept
:

page
:

scopes
:

sorts
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/suppliers?page=1" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": [
        {
            "generic_field_id": 1,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 1,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 2,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        },
        {
            "generic_field_id": 2,
            "generic_field_bool": true,
            "generic_field_nullable": null,
            "generic_field_string": "",
            "generic_nested_relation": [
                {
                    "nested_relation_id": 3,
                    "nested_relation_a1": "value",
                    "nested_relation_a2": "value",
                    "nested_relation_a3": "value"
                },
                {
                    "nested_relation_id": 4,
                    "nested_relation_b1": "value",
                    "nested_relation_b2": "value",
                    "nested_relation_b3": "value"
                }
            ],
            "_meta": {
                "_comment": "Read-Only",
                "additional_information_a": "value",
                "additional_information_b": "value",
                "additional_information_c": "value",
                "created_at": "2024-12-06T10:49:37+01:00",
                "updated_at": "2024-12-06T10:50:12+01:00"
            }
        }
    ],
    "links": {
        "first": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
        "last": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
        "prev": null,
        "next": "https://app.poool-dev.cc/api/2/endpoint/action?page=2"
    },
    "meta": {
        "current_page": 1,
        "from": 1,
        "last_page": 4,
        "links": [
            {
                "url": null,
                "label": "&laquo; Previous",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=1",
                "label": "1",
                "active": true
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "2",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=3",
                "label": "3",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=4",
                "label": "4",
                "active": false
            },
            {
                "url": "https://app.poool-dev.cc/api/2/endpoint/action?page=2",
                "label": "Next &raquo;",
                "active": false
            }
        ],
        "path": "https://app.poool-dev.cc/api/2/endpoint/action",
        "per_page": 50,
        "to": 50,
        "total": 167
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Create supplier
POST
https://app.poool.cc/api/2/suppliers
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

{
    "data": {
        "company_id": 10,
        "number_range_id": 16,
        "number": "k",
        "customer_number": "tkjz",
        "payment_time_day_num": 5,
        "discount_day_num": 14,
        "discount_percentage": 2340.6001781,
        "company_payment_account_id": 13,
        "comment_supplier": "nam",
        "comment_internal": "dolores",
        "datev_account": "jiqhfkegujz",
        "is_active_expense_position": "1",
        "is_default_mileage_allowance": "0",
        "is_default_daily_allowance": "1"
    }
}
Send Request 💥
curl --request POST \
    "https://app.poool.cc/api/2/suppliers" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"company_id\": 10,
        \"number_range_id\": 16,
        \"number\": \"k\",
        \"customer_number\": \"tkjz\",
        \"payment_time_day_num\": 5,
        \"discount_day_num\": 14,
        \"discount_percentage\": 2340.6001781,
        \"company_payment_account_id\": 13,
        \"comment_supplier\": \"nam\",
        \"comment_internal\": \"dolores\",
        \"datev_account\": \"jiqhfkegujz\",
        \"is_active_expense_position\": \"1\",
        \"is_default_mileage_allowance\": \"0\",
        \"is_default_daily_allowance\": \"1\"
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Show supplier
GET
https://app.poool.cc/api/2/suppliers/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
7
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

Send Request 💥
curl --request GET \
    --get "https://app.poool.cc/api/2/suppliers/7" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Update supplier
PUT
PATCH
https://app.poool.cc/api/2/suppliers/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
8
Body Parameters

data
object
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

{
    "data": {
        "company_id": 5,
        "number_range_id": 2,
        "number": "yu",
        "customer_number": "bmupjcexwkq",
        "payment_time_day_num": 9,
        "discount_day_num": 2,
        "discount_percentage": 2904.629183,
        "company_payment_account_id": 2,
        "comment_supplier": "tenetur",
        "comment_internal": "odit",
        "datev_account": "zgt",
        "is_active_expense_position": "1",
        "is_default_mileage_allowance": "0",
        "is_default_daily_allowance": "1"
    }
}
Send Request 💥
curl --request PUT \
    "https://app.poool.cc/api/2/suppliers/8" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "{
    \"data\": {
        \"company_id\": 5,
        \"number_range_id\": 2,
        \"number\": \"yu\",
        \"customer_number\": \"bmupjcexwkq\",
        \"payment_time_day_num\": 9,
        \"discount_day_num\": 2,
        \"discount_percentage\": 2904.629183,
        \"company_payment_account_id\": 2,
        \"comment_supplier\": \"tenetur\",
        \"comment_internal\": \"odit\",
        \"datev_account\": \"zgt\",
        \"is_active_expense_position\": \"1\",
        \"is_default_mileage_allowance\": \"0\",
        \"is_default_daily_allowance\": \"1\"
    }
}"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1,
        "generic_field_bool": true,
        "generic_field_nullable": null,
        "generic_field_string": "value",
        "generic_nested_relation": [
            {
                "_comment": "id is set. Updates existing relation.",
                "nested_relation_id": 1,
                "nested_relation_a1": "value",
                "nested_relation_a2": "value",
                "nested_relation_a3": "value"
            },
            {
                "_comment": "id is not set. Creates new relation.",
                "nested_relation_b1": "value",
                "nested_relation_b2": "value",
                "nested_relation_b3": "value"
            }
        ],
        "_meta": {
            "_comment": "Read-Only",
            "additional_information_a": "value",
            "additional_information_b": "value",
            "additional_information_c": "value",
            "created_at": "2024-12-06T10:49:37+01:00",
            "updated_at": "2024-12-06T10:50:12+01:00"
        }
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}
Delete supplier
DELETE
https://app.poool.cc/api/2/suppliers/{id}
requires authentication
Headers
Authorization
Example:
Bearer {YOUR_AUTH_TOKEN}
Content-Type
Example:
application/json
Accept
Example:
application/json
URL Parameters
id
integer
required
Example:
12
Query Parameters
app_version_override
boolean
Delete data set regardless of a failed version check.
Example:
false
app_version
integer
The version number of the the data set to be deleted. Must match current data set version.
Example:
42
Authorization
:
Bearer  
Content-Type
:

Accept
:

id
:

app_version_override
:

app_version
:

Send Request 💥
curl --request DELETE \
    "https://app.poool.cc/api/2/suppliers/12?app_version_override=&app_version=42" \
    --header "Authorization: Bearer {YOUR_AUTH_TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json"
{
    "data": {
        "_comment": "API standard response structure. Generate API call to get individual examples.",
        "generic_field_id": 1
    },
    "meta": {
        "_comment": "Optional: The top level meta field can provide additional information to the response, most likely data generated by the request that is not strictly endpoint related/embedded.",
        "response": null,
        "action": "destroyed"
    },
    "api": {
        "generation": 2,
        "label": "YYYY-MM-DD-beta|prod|alpha",
        "version": "2.X.Y",
        "served": "https://app.poool.cc/api/2/endpoint/action",
        "served_by": "www",
        "served_at": "2024-12-06T10:49:37+00:00"
    }
}

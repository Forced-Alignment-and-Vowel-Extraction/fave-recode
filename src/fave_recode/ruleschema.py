from cerberus import Validator

def attribute_check(field, value, error):
    aligned_textgrid_properities = [
        'fol',
        'prev',
        'label',
        'super_instance',
        'inword',
        'sub_labels',
        'first',
        'last',
        'within'
    ]
    value_components = value.split(".")
    value_valid = [x in aligned_textgrid_properities for x in value_components]
    if not all(value_valid):
        error(field, f"invalid attribute '{value}'")


rule_schema = {
    'rule' : {
        'type': 'string',
        'required': True
    },
    'conditions' : {
        'type': 'list',
        'required': True
    },
    'return': {
        'type': 'string',
        'required': True
    },
    'updates': {
        'type': 'string',
        'required': False
    }
}

condition_schema = {
    'attribute': {
        'type': 'string',
        'required': True,
        'check_with': attribute_check
    },
    'relation': {
        'type': 'string',
        'allowed': [
            "in",
            "not in",
            "contains",
            "excludes",
            "==",
            "!=",
            "rematches",
            "reunmatches"
        ],
        'required': True
    },
    'set': {
        'type': ['list', 'string'],
        'required': True
    }
}

label_parser_schema = {
    "parser": {
        "type": "string",
        "required": True
    },
    "properties": {
        "type": "list",
        "required": True
    }
}

parser_property_schema = {
    "name": {
        "type": "string",
        "required": True
    },
    "updates": {
        "type": "string",
        "required": True
    },
    "default": {
        "type": "string",
        "required": True
    },
    "rules": {
        "type": "list",
        "required": True
    }
}



rule_validator = Validator(rule_schema)
condition_validator = Validator(condition_schema)
label_parser_validator = Validator(label_parser_schema)
parser_property_validator = Validator(parser_property_schema)
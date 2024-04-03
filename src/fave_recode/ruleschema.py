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

rule_validator = Validator(rule_schema)
condition_validator = Validator(condition_schema)
from cerberus import Validator

def attribute_check(field, value, error):
    """_internal attribute check_
    """
    aligned_textgrid_properities = [
        'fol',
        'prev',
        'label',
        'super_instance',
        'inword',
        'subset_list'
    ]
    value_components = value.split(".")
    value_valid = [x in aligned_textgrid_properities for x in value_components]
    if not all(value_valid):
        error(field, f"invalid attribute '{value}'")


rule_schema = {
    'rule' : {
        'type': 'string'
    },
    'conditions' : {
        'type': 'list'
    },
    'return': {
        'type': 'string'
    }
}

condition_schema = {
    'attribute': {
        'type': 'string'
    },
    'relation': {
        'type': 'string',
        'allowed': [
            "==",
            "in",
            "!="
        ]
    },
    'set': {
        'type': ['list', 'string']
    }
}

rule_validator = Validator(rule_schema)
condition_validator = Validator(condition_schema)
import pprint

output_dict = {}


def flat(x, input):
    global output_dict
    for i in x:
        if not isinstance(x.get(i), dict):
            this_key = (input+'.'+i).split('.',1)[1]
            val = x.get(i)
            output_dict[this_key] = {
                                "last_key_type": type(i),
                                "value": val,
                                "value_type": type(val)
                                }
        else:
            flat(x.get(i), input+'.'+i)


def flatten(input_dict):
    """
    sample input:
        y = {'a':
                {
                    'e': 1,
                    'f': {'i': 2, 'j': 3, 'k': 4}
                },
            'b': 5,
            'c': {
                    'g': {'l': 6, 'm': 7}
                }
            }
    sample output:
        {
            'a.e': {'last_key_type': <class 'str'>,
                'value': 1,
                'value_type': <class 'int'>},
            'a.f.i': {'last_key_type': <class 'str'>,
                    'value': 2,
                    'value_type': <class 'int'>},
            'a.f.j': {'last_key_type': <class 'str'>,
                    'value': 3,
                    'value_type': <class 'int'>},
            'a.f.k': {'last_key_type': <class 'str'>,
                    'value': 4,
                    'value_type': <class 'int'>},
            'b': {'last_key_type': <class 'str'>, 'value': 5, 'value_type': <class 'int'>},
            'c.g.l': {'last_key_type': <class 'str'>,
                    'value': 6,
                    'value_type': <class 'int'>},
            'c.g.m': {'last_key_type': <class 'str'>,
                    'value': 7,
                    'value_type': <class 'int'>}
        }
    """
    flat(input_dict, "")
    pprint.pprint(output_dict)
    return output_dict

# flatten({'a':
#                 {
#                     'e': 1,
#                     'f': {'i': 2, 'j': 3, 'k': 4}
#                 },
#             'b': 5,
#             'c': {
#                     'g': {'l': 6, 'm': 7}
#                 }
#             })
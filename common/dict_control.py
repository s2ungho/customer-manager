def valid_key(dict_body, key, required=False, default=None):
    if key in dict_body:
        return dict_body[key]
    if required:
        raise ValueError('invalid key error[{}]'.format(key))
    return default


def safe_dict_builder(input_body, output, key, default=None, required=False, output_prefix=None):
    if output_prefix:
        output_key = output_prefix + '.' + key
    else:
        output_key = key

    if key in input_body:
        output[output_key] = input_body[key]
    else:
        if required:
            raise ValueError('safe_dict_builder - invalid key error[{}]'.format(key))
        else:
            if default is not None:
                output[output_key] = default

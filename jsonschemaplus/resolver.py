from copy import deepcopy
from jsonschemaplus.helpers import array, object_, string, uri
from jsonschemaplus.parsers import url
from jsonschemaplus.requests import get
from jsonschemaplus.errors import SchemaError


def resolve(schema, copy=False):
    """Resolve schema references.
    :param schema: The schema to resolve.
    :return: The resolved schema.
    """
    from jsonschemaplus.schemas import metaschema
    from jsonschemaplus.schemas import hyperschema
    
    _substitutions = {'%25': '%', '~1': '/', '~0': '~'}

    def _resolve_refs(schema, root=None, id_acc=None):
        """Resolve schema references and modify supplied
        schema as a side effect.
        If function parses value that equals schema's root,
        _resolve_refs early exits because references have
        already been resolved.
        :param schema: The schema to resolve.
        :param root: The root of the schema.
        :side effect: Modifies schema.
        :return: None
        :TODO: resolve all http ref values
        """
        if root is None:
            root = schema

        ref = '$ref'
        id_ = 'id'
        if object_(schema):
            value = schema.get(id_)
            if value and string(value):
                if uri(value):
                    id_acc = value
                else:
                    if id_acc is None:
                        raise SchemaError('Error resolving schema with id: %s' % value)
                    else:
                        id_acc += value
                        if not uri(id_acc):
                            raise SchemaError('Error resolving schema with id: %s' % value)
            value = schema.get(ref)
            if value and string(value):
                if uri(value):
                    schema.pop(ref)
                    if (value == 'http://json-schema.org/draft-04/schema#'
                        and root != metaschema):
                        schema.update(deepcopy(metaschema))
                    # elif (value == 'http://json-schema.org/draft-04/hyper-schema#'
                    #     and root != hyperschema):
                    #     schema.update(deepcopy(hyperschema))
                    else:
                        try:
                            (url_, path_) = url(value)
                            data = resolve(get(url_))
                            schema.update(_path(data, path_))
                        except:
                            raise SchemaError('Error resolving schema with $ref: %s' % value)
                    _resolve_refs(schema, root, id_acc)
                elif value[0] == '#':
                    schema.pop(ref)
                    subschema = _path(root, value)
                    if object_(subschema) and ref in subschema and string(subschema[ref]):
                        _resolve_refs(subschema, root, id_acc)
                        subschema = _path(root, value)
                    schema.update(subschema)
                elif value.find('.json') != -1:
                    schema.pop(ref)
                    (url_, path_) = url(id_acc + value)
                    data = resolve(get(url_))
                    schema.update(_path(data, path_))
                    _resolve_refs(schema, root, id_acc)
                else:
                    raise SchemaError('Error resolving schema with $ref: %s' % value)
            for k, v in schema.items():
                if k != ref and k != id_ and v != root:
                    _resolve_refs(v, root, id_acc)
        elif array(schema):
            for item in schema:
                if item != root:
                    _resolve_refs(item, root, id_acc)


    def _path(schema, path):
        components = path[1:].split('/')[1:]
        subschema = schema
        for c in components:
            for k, v in _substitutions.items():
                if k in c:
                    c = c.replace(k, v)
            if array(subschema):
                try:
                    index = int(c)
                    subschema = subschema[index]
                except:
                    raise SchemaError('Invalid path %s' % path)
            elif object_(subschema):
                subschema = subschema.get(c)
            else:
                raise SchemaError('Invalid path %s' % path)
        return subschema

    resolve.resolve_refs = _resolve_refs
    resolve.path = _path

    if copy:
        schema_ = deepcopy(schema)
    else:
        schema_ = schema

    _resolve_refs(schema_)
    return schema_

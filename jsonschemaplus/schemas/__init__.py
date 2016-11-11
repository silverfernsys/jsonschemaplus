from jsonschemaplus.resolver import resolve

from jsonschemaplus.schemas._hyperschema import hyperschema
from jsonschemaplus.schemas._metaschema import metaschema

metaschema = resolve(metaschema)
# hyperschema = resolve(hyperschema)

import os

def get_params():
    """
    Extracts metadata from process environment parameters into dictionary. It will extract content metadata and custom
    metadata and return a tuple. Each value is a dictionary. Key is always uppercase, value is case sensitive.
    """
    content_metadata = {}  # content metadata - DATATYPE, MIMETYPE, CHARSET, CONTENTTYPE (HTTP header value)
    custom_metadata = {}  # custom metadata

    for key, value in os.environ.items():
        if key.startswith('P_C_') and len(key) > 4:
            custom_metadata[key[4:]] = value
        elif key.startswith('P_') and len(key) > 2:
            content_metadata[key[2:]] = value

    return content_metadata, custom_metadata

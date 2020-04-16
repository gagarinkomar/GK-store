from flask_restful import abort


api_key = "676B5F7365637265745F6170695F6B6579"


def abort_if_invalid_api_key(key):
    if not api_key == key:
        abort(403, message='Invalid key')

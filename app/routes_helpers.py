from flask import abort, make_response

def validate_model(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{id} was invalid"}, 400))

    model = cls.query.get(id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} with id {id} not found"}, 404))

    return model
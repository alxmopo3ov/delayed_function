import inspect


def get_nearest_class(target_class, candidate_classes):
    for cls in inspect.getmro(target_class):
        if cls in candidate_classes:
            return cls
    return object

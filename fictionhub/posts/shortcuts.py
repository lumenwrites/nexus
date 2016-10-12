def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
    

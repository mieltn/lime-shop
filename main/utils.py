def set_filter(request, model, name):
    fltrs = request.GET.getlist(name)
    if not fltrs:
        return model.objects.all()
    return model.objects.filter(name__in=fltrs).all()

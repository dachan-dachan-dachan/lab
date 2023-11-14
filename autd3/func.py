def z_route(now, start, end, velocity, f):
    if start <= end:
        if now < end:
            now += velocity*f
        else:
            now = start
    else:
        if end < now:
            now -= velocity*f
        else:
            now = start
    return now

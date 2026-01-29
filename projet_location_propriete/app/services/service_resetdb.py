from app.data import data_reset


def resetdb():
    fkhan_locations = data_reset.reset()
    return fkhan_locations

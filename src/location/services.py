from location.models import Country, Region, City


def get_countries():
    return Country.query.all()


def get_country_by_id(country_id):
    return Country.query.filter_by(id=country_id).one_or_none()


def get_country_regions(country_id):
    return Region.query.filter_by(country_id=country_id)


def get_region_by_id(region_id):
    return Region.query.filter_by(id=region_id).one_or_none()


def get_region_cities(region_id):
    return City.query.filter_by(region_id=region_id)

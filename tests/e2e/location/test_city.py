from flask import url_for


class TestCityList:

    def test_city_list(self, client, create_country, create_region, create_city):
        countries = []
        for i in range(2):
            countries.append(create_country(name=f'Country{i}'))

        regions = []
        for country in countries:
            for i in range(2):
                regions.append(create_region(country, name=f'Region{i}'))

        cities_count = 5
        for region in regions:
            for i in range(cities_count):
                create_city(region.country, region, name=f'City{i}')

        response = client.get(url_for('location.city_list', country_id=countries[0].id, region_id=regions[0].id))
        assert response.status_code == 200
        assert len(response.json) == cities_count

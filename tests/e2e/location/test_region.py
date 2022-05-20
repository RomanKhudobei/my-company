from flask import url_for


class TestRegionList:

    def test_region_list(self, client, create_country, create_region):
        countries = []
        for i in range(2):
            countries.append(create_country(name=f'Country{i}'))

        regions_count = 5
        for country in countries:
            for i in range(regions_count):
                create_region(country, name=f'Region{i}')

        response = client.get(url_for('location.region_list', country_id=countries[0].id))
        assert response.status_code == 200
        assert len(response.json) == regions_count

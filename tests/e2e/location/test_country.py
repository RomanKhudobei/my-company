from flask import url_for


class TestCountryList:

    def test_country_list(self, client, create_country):
        countries_count = 5
        for i in range(5):
            create_country(name=f'Country{i}')

        response = client.get(url_for('location.country_list'))
        assert response.status_code == 200
        assert len(response.json) == countries_count

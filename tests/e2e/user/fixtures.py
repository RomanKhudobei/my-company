

def get_user_data(**kwargs):
    data = {
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@gmail.com',
        'password': 'testabc123',
        'repeat_password': 'testabc123',
    }
    data.update(**kwargs)
    return data

from flask import render_template


def get_dict():
    ole = {'position': 1, 'name': 'Elon Musk', 'wealth': '326.2B', 'country': 'United States', 'Company': 'Tesla'}
    return render_template('../templates/home/home.html', dict=ole)
get_dict()

from flask import Blueprint, render_template, request
from app.wrapper import WeatherWrapper

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    
    return render_template('home.html')

@routes.route('/alerts', methods=('GET', 'POST'))
def alerts():
    if request.method == 'POST':
        # Access the lists for repeatable inputs
        events_list = request.form.getlist('event') if request.form.getlist('event') != [''] else None
        code_list = request.form.getlist('code') if request.form.getlist('code') != [''] else None
        points_list = request.form.getlist('points') if request.form.getlist('points') != [''] else None
        area_list = request.form.getlist('area') if request.form.getlist('area') != [''] else None
        zone_list = request.form.getlist('zone') if request.form.getlist('zone') != [''] else None

        args = {
            'active': request.form.get('active'),
            'start': request.form.get('start_time'),
            'end': request.form.get('end_time'),
            'status': request.form.get('status'),
            'message_type': request.form.get('message_type'),
            'event': events_list,
            'code': code_list,
            'area': area_list,  # Use the list
            'point': points_list,  # Use the list
            'region': request.form.get('region'),
            'zone': zone_list,  # Use the list
            'urgency': request.form.get('urgency'),
            'severity': request.form.get('severity'),
            'certainty': request.form.get('certainty'),
            'limit': request.form.get('limit'),
            'cursor': request.form.get('cursor')
        }
        print(args)
        wrapper = WeatherWrapper('https://api.weather.gov')
        resps = wrapper.get_alerts(**args)

        return render_template('alerts_parsed.html', resps=resps)
    else:
        return render_template('alerts.html')

@routes.route('/glossary')
def glossary():
    wrapper = WeatherWrapper('https://api.weather.gov')
    resps = wrapper.get_glossary()
    return render_template('glossary.html', resps=resps)
    
@routes.route('/stations')
def stations():
    return render_template('stations.html')
    
    
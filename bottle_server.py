#!/usr/bin/python
from bottle import route, run, template, post, get, request

# country (colors): blue, red, green, yellow, empty(no one)

class AGame(object):
    """docstring for AGame."""

    def __init__(self):
        super(AGame, self).__init__()
        self.cities = {}

    def add_city(self, city_name, peo_num, country_name):
        self.cities[city_name] = {}
        self.cities[city_name]['people'] = int(peo_num)
        self.cities[city_name]['country'] = str(country_name)

    def remove_city(self, city_name):
        if city_name in self.cities:
            del self.cities[city_name]
            return True
        else:
            return False

    def city_add_people(self, city_name, delta_people):
        if city_name in self.cities:
            self.cities[city_name]['people'] += delta_people
            return True
        else:
            return False

    def city_del_people(self, city_name, delta_people):
        if city_name in self.cities:
            self.cities[city_name]['people'] -= delta_people
            return True
        else:
            return False

    def all_city_add(self, delta_people, country_name):
        if country_name == 'ALL':
            for name in self.cities:
                self.cities[name]['people'] += delta_people
        else:
            for name in self.cities:
                if self.cities[name]['country'] == country_name:
                    self.cities[name]['people'] += delta_people

    def all_city_del(self, delta_people, country_name):
        if country_name == 'ALL':
            for name in self.cities:
                self.cities[name]['people'] -= delta_people
        else:
            for name in self.cities:
                if self.cities[name]['country'] == country_name:
                    self.cities[name]['people'] -= delta_people

    def show_peo(self, city_name):
        if city_name in self.cities:
            return self.cities[city_name]
        else:
            return None

    def get_all_city(self):
        return self.cities

n_game = AGame()
n_game.add_city("Land01", 400, 'empty')
n_game.add_city("Land02", 400, 'empty')
n_game.add_city("Land03", 200, 'blue')
n_game.add_city("Land04", 600, 'empty')
n_game.add_city("Land05", 1000, 'blue')
n_game.add_city("Land06", 300, 'blue')
n_game.add_city("Land07", 300, 'empty')
n_game.add_city("Land08", 600, 'empty')
n_game.add_city("Land09", 300, 'red')
n_game.add_city("Land10", 1000, 'red')
n_game.add_city("Land11", 200, 'red')
n_game.add_city("Land12", 400, 'empty')
n_game.add_city("Land13", 600, 'empty')
n_game.add_city("Land14", 300, 'green')
n_game.add_city("Land15", 1000, 'green')
n_game.add_city("Land16", 200, 'green')
n_game.add_city("Land17", 400, 'empty')
n_game.add_city("Land18", 600, 'empty')
n_game.add_city("Land19", 200, 'yellow')
n_game.add_city("Land20", 400, 'empty')
n_game.add_city("Land21", 1000, 'yellow')
n_game.add_city("Land22", 300, 'yellow')
n_game.add_city("Land23", 400, 'empty')
n_game.add_city("Land24", 300, 'empty')
n_game.add_city("Land25", 200, 'empty')

host_ip = '140.113.148.79'

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/object/<id:int>')
def callback(id):
    print("The id is: ", id)
    return template('<b>The id is: {{id}}</b>!', id=id)

@route('/see_city/<city_name>')
def see_city(city_name):
    land = n_game.show_peo(city_name)
    if land is None:
        return template('<p>There is no City <b>{{name}}</b></p>!', name=city_name)
    elif land['country'] == 'empty':
        return template('<p>City <b>{{name}}</b>: <b><font color="red">{{num}}</font></b> people. It does NOT belongs to anyone.</p>', name=city_name, num=land['people'])
    else:
        return template('<p>City <b>{{name}}</b>: <b><font color="red">{{num}}</font></b> people. It belongs to <b><font color="{{country}}">{{country}}</font></b></p>', name=city_name, num=land['people'], country=land['country'])

@route('/see_all_city/yoyodiy')
def see_all_city():
    all_cities = n_game.get_all_city()
    answer_string = ''
    for city in all_cities:
        if all_cities[city]['country'] == 'empty':
            answer_string += '<p>City <b>' + city + '</b>: <b><font color="red">' + str(all_cities[city]['people']) + '</font></b> people. It does NOT belongs to anyone.</p>'
        else:
            answer_string += '<p>City <b>' + city + '</b>: <b><font color="red">' + str(all_cities[city]['people']) + '</font></b> people. It belongs to <b><font color="' + all_cities[city]['country'] + '">' + all_cities[city]['country'] + '</font></b></p>'

    return answer_string

@get('/new_city') # or @route('/login')
def new_city_gui():
    return '''
        <form action="/new_city" method="post">
            Create New City ID: <input name="city_id" type="text" />
            Set People number: <input name="people" type="number" />
            <input value="Submit" type="submit" />
        </form>
    '''

@post('/new_city') # or @route('/login', method='POST')
def do_new_city():
    city_id = request.forms.get('city_id')
    people = request.forms.get('people')
    result = n_game.add_city(city_id, int(people))
    return template('<p>Create City <b>{{id}}</b> with <b><font color="red">{{people}}</font></b> people.</p> Check all city people <a href="http://{{ip}}:8080/see_all_city/yoyodiy">here</a>', id=city_id, people=people, ip=host_ip)


@get('/set_city') # or @route('/login')
def set_city_gui():
    return '''
        <form action="/set_city" method="post">
            City ID: <input name="city_id" type="text" />
            Set People number: <input name="people" type="number" />
            <input value="Submit" type="submit" />
        </form>
    '''

@post('/set_city') # or @route('/login', method='POST')
def do_set_city():
    city_id = request.forms.get('city_id')
    people = request.forms.get('people')
    result = n_game.add_city(city_id, int(people))
    #if city_add_people:
    return template('<p>Set City <b>{{id}}</b> to <b><font color="red">{{people}}</font></b> people.</p> Check all city people <a href="http://{{ip}}:8080/see_all_city/yoyodiy">here</a>', id=city_id, people=people, ip=host_ip)
    #else:
    #    return template('<p>City {{id}} do not exist. Please use <a href="http://{{ip}}:8080/see_all_city/yoyodiy">new city</a> to create new city.', id=city_id, ip=host_ip)

@get('/add_all') # or @route('/login')
def add_all_gui():
    return '''
        <form action="/add_all" method="post">
            How many people do you want to <b><font color="green">ADD</font></b> which country?
            <p></p>
            <input type="radio" name="country" value="ALL" checked> <b>ALL</b><br>
            <input type="radio" name="country" value="blue"> <b><font color="blue">Blue</font></b><br>
            <input type="radio" name="country" value="red"> <b><font color="red">Red</font></b><br>
            <input type="radio" name="country" value="green"> <b><font color="green">Green</font></b><br>
            <input type="radio" name="country" value="yellow"> <b><font color="yellow">Yellow</font></b><br>
            <p></p>
            Number: <input name="people" type="number" />
            <input value="Submit" type="submit" />
        </form>
    '''

@post('/add_all') # or @route('/login', method='POST')
def do_add_all():
    delta_people = request.forms.get('people')
    n_game.all_city_add(int(delta_people))
    if country_name == 'ALL':
        return template('<p> <b><font color="red">DEL</font> {{delta_people}}</b> people to <b>ALL</b> city.</p> Check all city people <a href="http://{{ip}}:8080/see_all_city/yoyodiy">here</a>', delta_people=delta_people, ip=host_ip)
    else:
        return template('<p> <b><font color="red">DEL</font> {{delta_people}}</b> people to cities of <b><font color="{{country}}">{{country}}</font></b>.</p> Check all city people <a href="http://{{ip}}:8080/see_all_city/yoyodiy">here</a>', delta_people=delta_people, country=country_name, ip=host_ip)

@get('/del_all') # or @route('/login')
def add_all_gui():
    return '''
        <form action="/del_all" method="post">
            How many people do you want to <b><font color="red">DEL</font></b> which country?
            <p></p>
            <input type="radio" name="country" value="ALL" checked> <b>ALL</b><br>
            <input type="radio" name="country" value="blue"> <b><font color="blue">Blue</font></b><br>
            <input type="radio" name="country" value="red"> <b><font color="red">Red</font></b><br>
            <input type="radio" name="country" value="green"> <b><font color="green">Green</font></b><br>
            <input type="radio" name="country" value="yellow"> <b><font color="yellow">Yellow</font></b><br>
            <p></p>
            Number: <input name="people" type="number" />
            <input value="Submit" type="submit" />
        </form>
    '''

@post('/del_all') # or @route('/login', method='POST')
def do_add_all():
    delta_people = request.forms.get('people')
    country_name = request.forms.get('country')
    n_game.all_city_del(int(delta_people), str(country_name))
    if country_name == 'ALL':
        return template('<p> <b><font color="red">DEL</font> {{delta_people}}</b> people to <b>ALL</b> city.</p> Check all city people <a href="http://{{ip}}:8080/see_all_city/yoyodiy">here</a>', delta_people=delta_people, ip=host_ip)
    else:
        return template('<p> <b><font color="red">DEL</font> {{delta_people}}</b> people to cities of <b><font color="{{country}}">{{country}}</font></b>.</p> Check all city people <a href="http://{{ip}}:8080/see_all_city/yoyodiy">here</a>', delta_people=delta_people, country=country_name, ip=host_ip)


@get('/add_people') # or @route('/login')
def add_people_gui():
    return '''
        <form action="/add_people" method="post">
            <b><font color="green">ADD</font></b>
            Number: <input name="people" type="number" />
            to <input name="city_id" type="text" /> city?
            <input value="Submit" type="submit" />
        </form>
    '''

@post('/add_people') # or @route('/login', method='POST')
def do_add_people():
    city_id = request.forms.get('city_id')
    people = request.forms.get('people')
    result = n_game.city_add_people(city_id, int(people))
    if result:
        return template('<p>Add <b><font color="red">{{people}}</font></b> people to City <b>{{id}}</b>.</p> Check all city people <a href="http://{{ip}}:8080/see_all_city/yoyodiy">here</a>', id=city_id, people=people, ip=host_ip)
    else:
        return template('<p>City {{id}} do not exist. Please use <a href="http://{{ip}}:8080/new_city">new city</a> to create new city.', id=city_id, ip=host_ip)

@get('/del_people') # or @route('/login')
def add_people_gui():
    return '''
        <form action="/del_people" method="post">
            <b><font color="red">DEL</font></b>
            Number: <input name="people" type="number" />
            to <input name="city_id" type="text" /> city?
            <input value="Submit" type="submit" />
        </form>
    '''

@post('/del_people') # or @route('/login', method='POST')
def do_add_people():
    city_id = request.forms.get('city_id')
    people = request.forms.get('people')
    result = n_game.city_add_people(city_id, int(people))
    if result:
        return template('<p>Add <b><font color="red">{{people}}</font></b> people to City <b>{{id}}</b>.</p> Check all city people <a href="http://{{ip}}:8080/see_all_city/yoyodiy">here</a>', id=city_id, people=people, ip=host_ip)
    else:
        return template('<p>City {{id}} do not exist. Please use <a href="http://{{ip}}:8080/new_city">new city</a> to create new city.', id=city_id, ip=host_ip)

run(server='paste', host=host_ip, port=8080)
# run(server='paste')

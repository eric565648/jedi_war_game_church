#!/usr/bin/python
from bottle import route, run, template, post, get, request
import yaml

# country (colors): blue, red, green, yellow, empty(no one)

class AGame(object):
    """docstring for AGame."""

    def __init__(self):
        super(AGame, self).__init__()
        self.cities = {}

    def save_city(self):
        with open('data/game_data.yaml', 'w') as outfile:
            yaml.dump(self.cities, outfile)

    def add_city(self, city_name, peo_num, country_name):
        self.cities[city_name] = {}
        self.cities[city_name]['people'] = int(peo_num)
        self.cities[city_name]['country'] = str(country_name)
        self.cities[city_name]['status'] = 'Alive'

    def remove_city(self, city_name):
        if city_name in self.cities:
            del self.cities[city_name]
            return True
        else:
            return False

    def city_add_people(self, city_name, delta_people):
        if city_name in self.cities:
            if self.cities[city_name]['status'] != 'Dead':
                self.cities[city_name]['people'] += delta_people
            return True
        else:
            return False

    def city_del_people(self, city_name, delta_people):
        if city_name in self.cities:
            self.cities[city_name]['people'] -= delta_people
            if self.cities[city_name]['people'] <= 0:
                self.cities[city_name]['people'] = 0
                self.cities[city_name]['status'] = 'Dead'
            return True
        else:
            return False

    def all_city_add(self, delta_people, country_name):
        if country_name == 'ALL':
            for name in self.cities:
                if self.cities[name]['status'] != 'Dead':
                    self.cities[name]['people'] += delta_people
        else:
            for name in self.cities:
                if self.cities[name]['country'] == country_name:
                    if self.cities[name]['status'] != 'Dead':
                        self.cities[name]['people'] += delta_people

    def all_city_del(self, delta_people, country_name):
        if country_name == 'ALL':
            for name in self.cities:
                self.cities[name]['people'] -= delta_people
                if self.cities[name]['people'] <= 0:
                    self.cities[name]['people'] = 0
                    self.cities[name]['status'] = 'Dead'
        else:
            for name in self.cities:
                if self.cities[name]['country'] == country_name:
                    self.cities[name]['people'] -= delta_people
                    if self.cities[name]['people'] <= 0:
                        self.cities[name]['people'] = 0
                        self.cities[name]['status'] = 'Dead'

    def change_country(self, city_name, country_name):

        if city_name in self.cities:
            self.cities[city_name]['country'] = country_name
            return True
        else:
            return False

    def city_resurrection(self, city_name):

        if city_name in self.cities:
            self.cities[city_name]['status'] = 'Alive'
            return True
        else:
            return False

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
# host_ip = '192.168.50.113'

import signal
import sys

def signal_handler(signal, frame):
    global n_game
    n_game.save_city()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# @route('/hello/<name>')
# def index(name):
#     return template('<b>Hello {{name}}</b>!', name=name)
#
# @route('/object/<id:int>')
# def callback(id):
#     print("The id is: ", id)
#     return template('<b>The id is: {{id}}</b>!', id=id)

@route('/see_city/<city_name>')
def see_city(city_name):
    land = n_game.show_peo(city_name)
    if land is None:
        return template('<p>There is no City <b>{{name}}</b></p>!', name=city_name)
    elif land['country'] == 'empty':
        return template('<p>City <b>{{name}}</b>: <b><font color="red">{{num}}</font></b> people. It does NOT belongs to anyone.</p>. It is <b>{{status}}</b>.', name=city_name, num=land['people'], status=land['status'])
    else:
        return template('<p>City <b>{{name}}</b>: <b><font color="red">{{num}}</font></b> people. It belongs to <b><font color="{{country}}">{{country}}</font></b></p>. It is <b>{{status}}</b>.', name=city_name, num=land['people'], country=land['country'], status=land['status'])

@route('/see_all_city/yoyodiy')
def see_all_city():
    all_cities = n_game.get_all_city()
    answer_string = ''
    for city in all_cities:
        if all_cities[city]['country'] == 'empty':
            answer_string += '<p>City <b>' + city + '</b>: <b><font color="red">' + str(all_cities[city]['people']) + '</font></b> people. It does NOT belongs to anyone. It is <b>' + all_cities[city]['status'] + '</b>.</p>'
        else:
            answer_string += '<p>City <b>' + city + '</b>: <b><font color="red">' + str(all_cities[city]['people']) + '</font></b> people. It belongs to <b><font color="' + all_cities[city]['country'] + '">' + all_cities[city]['country'] + '</font></b>. It is <b>' + all_cities[city]['status'] + '</b>.</p>'

    return answer_string

# @get('/new_city') # or @route('/login')
# def new_city_gui():
#     return '''
#         <form action="/new_city" method="post">
#             Create New City ID: <input name="city_id" type="text" />
#             Set People number: <input name="people" type="number" />
#             <input value="Submit" type="submit" />
#         </form>
#     '''
#
# @post('/new_city') # or @route('/login', method='POST')
# def do_new_city():
#     city_id = request.forms.get('city_id')
#     people = request.forms.get('people')
#     result = n_game.add_city(city_id, int(people))
#     return template('<p>Create City <b>{{id}}</b> with <b><font color="red">{{people}}</font></b> people.</p> Check all city people <a href="http://{{ip}}:8080/see_all_city/yoyodiy">here</a>', id=city_id, people=people, ip=host_ip)


# @get('/set_city') # or @route('/login')
# def set_city_gui():
#     return '''
#         <form action="/set_city" method="post">
#             City ID: <input name="city_id" type="text" />
#             Set People number: <input name="people" type="number" />
#             <input value="Submit" type="submit" />
#         </form>
#     '''
#
# @post('/set_city') # or @route('/login', method='POST')
# def do_set_city():
#     city_id = request.forms.get('city_id')
#     people = request.forms.get('people')
#     result = n_game.add_city(city_id, int(people))
#     #if city_add_people:
#     return template('<p>Set City <b>{{id}}</b> to <b><font color="red">{{people}}</font></b> people.</p> Check all city people <a href="http://{{ip}}:8080/see_all_city/yoyodiy">here</a>', id=city_id, people=people, ip=host_ip)
#     #else:
#     #    return template('<p>City {{id}} do not exist. Please use <a href="http://{{ip}}:8080/see_all_city/yoyodiy">new city</a> to create new city.', id=city_id, ip=host_ip)

@get('/change_country') # or @route('/login')
def set_city_gui():
    return '''
        <form action="/change_country" method="post">
            Change city:
            <p></p>
            <input type="radio" name="city_id" value="Land01"> <b>Land01</b><br>
            <input type="radio" name="city_id" value="Land02"> <b>Land02</b><br>
            <input type="radio" name="city_id" value="Land03"> <b>Land03</b><br>
            <input type="radio" name="city_id" value="Land04"> <b>Land04</b><br>
            <input type="radio" name="city_id" value="Land05"> <b>Land05</b><br>
            <input type="radio" name="city_id" value="Land06"> <b>Land06</b><br>
            <input type="radio" name="city_id" value="Land07"> <b>Land07</b><br>
            <input type="radio" name="city_id" value="Land08"> <b>Land08</b><br>
            <input type="radio" name="city_id" value="Land09"> <b>Land09</b><br>
            <input type="radio" name="city_id" value="Land10"> <b>Land10</b><br>
            <input type="radio" name="city_id" value="Land11"> <b>Land11</b><br>
            <input type="radio" name="city_id" value="Land12"> <b>Land12</b><br>
            <input type="radio" name="city_id" value="Land13"> <b>Land13</b><br>
            <input type="radio" name="city_id" value="Land14"> <b>Land14</b><br>
            <input type="radio" name="city_id" value="Land15"> <b>Land15</b><br>
            <input type="radio" name="city_id" value="Land16"> <b>Land16</b><br>
            <input type="radio" name="city_id" value="Land17"> <b>Land17</b><br>
            <input type="radio" name="city_id" value="Land18"> <b>Land18</b><br>
            <input type="radio" name="city_id" value="Land19"> <b>Land19</b><br>
            <input type="radio" name="city_id" value="Land20"> <b>Land20</b><br>
            <input type="radio" name="city_id" value="Land21"> <b>Land21</b><br>
            <input type="radio" name="city_id" value="Land22"> <b>Land22</b><br>
            <input type="radio" name="city_id" value="Land23"> <b>Land23</b><br>
            <input type="radio" name="city_id" value="Land24"> <b>Land24</b><br>
            <input type="radio" name="city_id" value="Land25"> <b>Land25</b><br>
            <p></p>
            to country
            <p></p>
            <input type="radio" name="country_name" value="blue"> <b><font color="blue">Blue</font></b><br>
            <input type="radio" name="country_name" value="red"> <b><font color="red">Red</font></b><br>
            <input type="radio" name="country_name" value="green"> <b><font color="green">Green</font></b><br>
            <input type="radio" name="country_name" value="yellow"> <b><font color="yellow">Yellow</font></b><br>
            <input value="Submit" type="submit" />
        </form>
    '''

@post('/change_country') # or @route('/login', method='POST')
def do_set_city():
    city_id = request.forms.get('city_id')
    country_name = request.forms.get('country_name')
    result = n_game.change_country(city_id, country_name)
    #if city_add_people:
    return template('<p>Change city <b>{{id}}</b> to <b><font color="{{country}}">{{country}}</font></b> country.</p> Check all city people <a href="http://{{ip}}:8080/see_all_city/yoyodiy">here</a>', id=city_id, country=country_name, ip=host_ip)
    #else:

@get('/resurrection') # or @route('/login')
def resurrection_gui():
    return '''
        <form action="/resurrection" method="post">
            Which city to <b><font color="cyan">Resurrect</font></b>?:
            <p></p>
            <input type="radio" name="city_id" value="Land01"> <b>Land01</b><br>
            <input type="radio" name="city_id" value="Land02"> <b>Land02</b><br>
            <input type="radio" name="city_id" value="Land03"> <b>Land03</b><br>
            <input type="radio" name="city_id" value="Land04"> <b>Land04</b><br>
            <input type="radio" name="city_id" value="Land05"> <b>Land05</b><br>
            <input type="radio" name="city_id" value="Land06"> <b>Land06</b><br>
            <input type="radio" name="city_id" value="Land07"> <b>Land07</b><br>
            <input type="radio" name="city_id" value="Land08"> <b>Land08</b><br>
            <input type="radio" name="city_id" value="Land09"> <b>Land09</b><br>
            <input type="radio" name="city_id" value="Land10"> <b>Land10</b><br>
            <input type="radio" name="city_id" value="Land11"> <b>Land11</b><br>
            <input type="radio" name="city_id" value="Land12"> <b>Land12</b><br>
            <input type="radio" name="city_id" value="Land13"> <b>Land13</b><br>
            <input type="radio" name="city_id" value="Land14"> <b>Land14</b><br>
            <input type="radio" name="city_id" value="Land15"> <b>Land15</b><br>
            <input type="radio" name="city_id" value="Land16"> <b>Land16</b><br>
            <input type="radio" name="city_id" value="Land17"> <b>Land17</b><br>
            <input type="radio" name="city_id" value="Land18"> <b>Land18</b><br>
            <input type="radio" name="city_id" value="Land19"> <b>Land19</b><br>
            <input type="radio" name="city_id" value="Land20"> <b>Land20</b><br>
            <input type="radio" name="city_id" value="Land21"> <b>Land21</b><br>
            <input type="radio" name="city_id" value="Land22"> <b>Land22</b><br>
            <input type="radio" name="city_id" value="Land23"> <b>Land23</b><br>
            <input type="radio" name="city_id" value="Land24"> <b>Land24</b><br>
            <input type="radio" name="city_id" value="Land25"> <b>Land25</b><br>
            <p></p>
            <input value="Submit" type="submit" />
        </form>
    '''

@post('/resurrection') # or @route('/login', method='POST')
def do_resurrection():
    city_id = request.forms.get('city_id')
    result = n_game.city_resurrection(city_id)
    #if city_add_people:
    return template('<p>City <b>{{id}}</b> is now <b><font color="cyan">Resurrect</font></b>.</p>', id=city_id)
    #else:

@get('/add_all') # or @route('/login')
def add_all_gui():
    return '''
        <form action="/add_all" method="post">
            How many people do you want to <b><font color="green">ADD</font></b> which country?
            <p></p>
            <input type="radio" name="country_name" value="ALL" checked> <b>ALL</b><br>
            <input type="radio" name="country_name" value="blue"> <b><font color="blue">Blue</font></b><br>
            <input type="radio" name="country_name" value="red"> <b><font color="red">Red</font></b><br>
            <input type="radio" name="country_name" value="green"> <b><font color="green">Green</font></b><br>
            <input type="radio" name="country_name" value="yellow"> <b><font color="yellow">Yellow</font></b><br>
            <p></p>
            Number: <input name="people" type="number" />
            <input value="Submit" type="submit" />
        </form>
    '''

@post('/add_all') # or @route('/login', method='POST')
def do_add_all():
    delta_people = request.forms.get('people')
    country_name = request.forms.get('country_name')
    n_game.all_city_add(int(delta_people), str(country_name))
    if country_name == 'ALL':
        return template('<p> <b><font color="green">ADD</font> {{delta_people}}</b> people to <b>ALL</b> city.</p> Check all city people <a href="http://{{ip}}:8080/see_all_city/yoyodiy">here</a>', delta_people=delta_people, ip=host_ip)
    else:
        return template('<p> <b><font color="green">ADD</font> {{delta_people}}</b> people to cities of <b><font color="{{country}}">{{country}}</font></b>.</p> Check all city people <a href="http://{{ip}}:8080/see_all_city/yoyodiy">here</a>', delta_people=delta_people, country=country_name, ip=host_ip)

@get('/del_all') # or @route('/login')
def add_all_gui():
    return '''
        <form action="/del_all" method="post">
            How many people do you want to <b><font color="red">DEL</font></b> which country?
            <p></p>
            <input type="radio" name="country_name" value="ALL" checked> <b>ALL</b><br>
            <input type="radio" name="country_name" value="blue"> <b><font color="blue">Blue</font></b><br>
            <input type="radio" name="country_name" value="red"> <b><font color="red">Red</font></b><br>
            <input type="radio" name="country_name" value="green"> <b><font color="green">Green</font></b><br>
            <input type="radio" name="country_name" value="yellow"> <b><font color="yellow">Yellow</font></b><br>
            <p></p>
            Number: <input name="people" type="number" />
            <input value="Submit" type="submit" />
        </form>
    '''

@post('/del_all') # or @route('/login', method='POST')
def do_add_all():
    delta_people = request.forms.get('people')
    country_name = request.forms.get('country_name')
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
            to
            <p></p>
            <input type="radio" name="city_id" value="Land01"> <b>Land01</b><br>
            <input type="radio" name="city_id" value="Land02"> <b>Land02</b><br>
            <input type="radio" name="city_id" value="Land03"> <b>Land03</b><br>
            <input type="radio" name="city_id" value="Land04"> <b>Land04</b><br>
            <input type="radio" name="city_id" value="Land05"> <b>Land05</b><br>
            <input type="radio" name="city_id" value="Land06"> <b>Land06</b><br>
            <input type="radio" name="city_id" value="Land07"> <b>Land07</b><br>
            <input type="radio" name="city_id" value="Land08"> <b>Land08</b><br>
            <input type="radio" name="city_id" value="Land09"> <b>Land09</b><br>
            <input type="radio" name="city_id" value="Land10"> <b>Land10</b><br>
            <input type="radio" name="city_id" value="Land11"> <b>Land11</b><br>
            <input type="radio" name="city_id" value="Land12"> <b>Land12</b><br>
            <input type="radio" name="city_id" value="Land13"> <b>Land13</b><br>
            <input type="radio" name="city_id" value="Land14"> <b>Land14</b><br>
            <input type="radio" name="city_id" value="Land15"> <b>Land15</b><br>
            <input type="radio" name="city_id" value="Land16"> <b>Land16</b><br>
            <input type="radio" name="city_id" value="Land17"> <b>Land17</b><br>
            <input type="radio" name="city_id" value="Land18"> <b>Land18</b><br>
            <input type="radio" name="city_id" value="Land19"> <b>Land19</b><br>
            <input type="radio" name="city_id" value="Land20"> <b>Land20</b><br>
            <input type="radio" name="city_id" value="Land21"> <b>Land21</b><br>
            <input type="radio" name="city_id" value="Land22"> <b>Land22</b><br>
            <input type="radio" name="city_id" value="Land23"> <b>Land23</b><br>
            <input type="radio" name="city_id" value="Land24"> <b>Land24</b><br>
            <input type="radio" name="city_id" value="Land25"> <b>Land25</b><br>
            <p></p>
            city?
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
            to
            <p></p>
            <input type="radio" name="city_id" value="Land01"> <b>Land01</b><br>
            <input type="radio" name="city_id" value="Land02"> <b>Land02</b><br>
            <input type="radio" name="city_id" value="Land03"> <b>Land03</b><br>
            <input type="radio" name="city_id" value="Land04"> <b>Land04</b><br>
            <input type="radio" name="city_id" value="Land05"> <b>Land05</b><br>
            <input type="radio" name="city_id" value="Land06"> <b>Land06</b><br>
            <input type="radio" name="city_id" value="Land07"> <b>Land07</b><br>
            <input type="radio" name="city_id" value="Land08"> <b>Land08</b><br>
            <input type="radio" name="city_id" value="Land09"> <b>Land09</b><br>
            <input type="radio" name="city_id" value="Land10"> <b>Land10</b><br>
            <input type="radio" name="city_id" value="Land11"> <b>Land11</b><br>
            <input type="radio" name="city_id" value="Land12"> <b>Land12</b><br>
            <input type="radio" name="city_id" value="Land13"> <b>Land13</b><br>
            <input type="radio" name="city_id" value="Land14"> <b>Land14</b><br>
            <input type="radio" name="city_id" value="Land15"> <b>Land15</b><br>
            <input type="radio" name="city_id" value="Land16"> <b>Land16</b><br>
            <input type="radio" name="city_id" value="Land17"> <b>Land17</b><br>
            <input type="radio" name="city_id" value="Land18"> <b>Land18</b><br>
            <input type="radio" name="city_id" value="Land19"> <b>Land19</b><br>
            <input type="radio" name="city_id" value="Land20"> <b>Land20</b><br>
            <input type="radio" name="city_id" value="Land21"> <b>Land21</b><br>
            <input type="radio" name="city_id" value="Land22"> <b>Land22</b><br>
            <input type="radio" name="city_id" value="Land23"> <b>Land23</b><br>
            <input type="radio" name="city_id" value="Land24"> <b>Land24</b><br>
            <input type="radio" name="city_id" value="Land25"> <b>Land25</b><br>
            <p></p>
            city?
            <input value="Submit" type="submit" />
        </form>
    '''

@post('/del_people') # or @route('/login', method='POST')
def do_add_people():
    city_id = request.forms.get('city_id')
    people = request.forms.get('people')
    result = n_game.city_del_people(city_id, int(people))
    if result:
        return template('<p>DEL <b><font color="red">{{people}}</font></b> people to City <b>{{id}}</b>.</p> Check all city people <a href="http://{{ip}}:8080/see_all_city/yoyodiy">here</a>', id=city_id, people=people, ip=host_ip)
    else:
        return template('<p>City {{id}} do not exist. Please use <a href="http://{{ip}}:8080/new_city">new city</a> to create new city.', id=city_id, ip=host_ip)

run(server='paste', host=host_ip, port=8080)
# run(server='paste')

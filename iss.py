#!/usr/bin/env python

__author__ = 'jontaylor224'

import requests
import turtle
from time import ctime


def get_people_api_data():
    astro_req = requests.get('http://api.open-notify.org/astros.json')
    astro_data = astro_req.json()
    people = astro_data["people"]

    print('There are currently {} people in space.'.format(
        str(astro_data["number"])))
    for person in people:
        print('{} is on board {}.'.format(person["name"], person["craft"]))


def get_location_api_data():
    loc_req = requests.get('http://api.open-notify.org/iss-now.json')
    loc_data = loc_req.json()
    location = loc_data['iss_position']
    current_latitude = location['latitude']
    current_longitude = location['longitude']
    return (float(current_latitude), float(current_longitude))


def setup_iss_turtle():
    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.bgpic('map.gif')
    screen.register_shape('iss.gif')

    iss = turtle.Turtle()
    iss.shape('iss.gif')
    iss.setheading(45)
    iss.penup()
    (current_latitude, current_longitude) = get_location_api_data()
    iss.goto(current_longitude, current_latitude)
    setup_indy_turtle()
    screen.exitonclick()


def setup_indy_turtle():
    indy = turtle.Turtle()
    indy.color('yellow')
    indy.shape('circle')
    indy.shapesize(0.5, 0.5)
    indy.penup()
    indy.goto(-86.1, 39.8)
    passovers = find_indy_passover_times()
    next_passover = ctime(passovers[0]['risetime'])
    indy.write(next_passover)


def find_indy_passover_times():
    passing_indy_req = requests.get(
        "http://api.open-notify.org/iss-pass.json?lat=39.8&lon=86.1")
    passing_indy_data = passing_indy_req.json()
    return passing_indy_data['response']


def main():
    get_people_api_data()
    get_location_api_data()
    setup_iss_turtle()
    # setup_indy_turtle()
    find_indy_passover_times()


if __name__ == '__main__':
    main()

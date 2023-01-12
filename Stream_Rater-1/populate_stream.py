#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'Stream_Rater.settings')
import requests
import django
django.setup()
from stream.models import Category, Streamer, Comment, SubComment, User

ClientID = "y4jb83gocuiaz4st31smsd2lgt3ko5"
accessToken = "89gx4l6795zslw3kdn61sl0o7z5b6u"
    
req_head = {
    'Client-ID' : ClientID,
    'Authorization' :  "Bearer " + accessToken
    }

def populate():
    # our data split into categories

    cats = createDataDict()

    # these functions create the categories in the database
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["gameImage"])
        for p in cat_data["streamers"]:
            add_streamer(c, p['name'], p['title'], p["image"], p["views"])

    '''
    for comment, comment_data in comments.items():
        for streamer in Streamer.objects.all():
            if comment_data['streamer'] == streamer.name:
                com = add_comment(comment_data['user_name'], streamer, text=comment_data['text'])
                for sub_comment, sub_comment_data in sub_comments.items():
                    if sub_comment_data['father_comment'] == comment:
                        add_sub_comment(sub_comment_data['user_name'], com, sub_comment_data['text'])
    '''

    for c in Category.objects.all():
        for p in Streamer.objects.filter(category=c):
            print(f'- {c}: {p}')

    for streamer in Streamer.objects.all():
        for comment in Comment.objects.filter(streamer=streamer):
            print(f'{comment}')
            print('people responded:')
            for sub_comment in SubComment.objects.filter(father_comment=comment):
                print(f'{sub_comment}')

# define the methods of information here...


# helper function that adds a page to a category with its url
def add_streamer(cat, name, title, image, views):
    p = Streamer.objects.get_or_create(category=cat, name=name, title=title, image=image,views=views)[0]
    p.save()
    return p


# helper function that creates a category of a given name
def add_cat(name, image):
    c = Category.objects.get_or_create(name=name, image=image)[0]
    c.save()
    return c

#helper function to get the top games
def getTopGames():
    url = "https://api.twitch.tv/helix/games/top?first=20" 
    games_request = requests.get(url, headers = req_head).json()['data']
    return games_request

#helper function to get streamers from each game.Takes game id in string form as  a parameter
def getStreamersGame(game_ID):
    url = "https://api.twitch.tv/helix/streams?game_id=" + game_ID
    streamer_request = requests.get(url, headers = req_head).json()['data']
    return streamer_request

#helper function to get the data of the user that is streaming
def getUserData(users_list):
    url = "https://api.twitch.tv/helix/users?"
    for user in users_list:
        url += ("id=" + user["user_id"] + "&")
    request = requests.get(url, headers = req_head).json()['data']
    return request

#helper function to create the cats nested dictionary
def createDataDict():
    #creates a list of top games
    games = getTopGames()
    games_dict = {}
    #for each game we create a list to add streamers in
    for game in games:
        game_name = game["name"]
        game_id = game["id"]
        game_image = game["box_art_url"].replace("{width}x{height}","188x250")
        game_list = []
        streamers_list = getStreamersGame(game_id)
        users_data = getUserData(streamers_list)
        count=0
        #for each streamer we keep only the necessary bits and add them to the list of the game
        for streamer in streamers_list:
            streamer_dict = {
                "name": streamer["user_name"],
                "title" : streamer["title"],
                "image" : users_data[count]["profile_image_url"].replace("{width}x{height}","188x250"),
                "views" : users_data[count]["view_count"]
                }
            game_list.append(streamer_dict)
            count+=1
        game_dict = {
            "streamers" : game_list,
            "gameImage" : game_image
            }
        games_dict[game_name] = game_dict
    return games_dict


def add_comment(user, streamer, rating=5, text=''):
    com = Comment.objects.get_or_create(user_name=user, streamer=streamer, rating=rating, text=text)[0]
    com.save()
    return com


def add_sub_comment(user, father_comment, text):
    sub_com = SubComment.objects.get_or_create(user_name=user, father_comment=father_comment, text=text)[0]
    sub_com.save()
    return sub_com


# starts execution here
if __name__ == '__main__':
    print('Starting Stream Rater population script...')
    populate()

           
             
    

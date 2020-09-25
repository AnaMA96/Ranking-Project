import requests
from flask import request, Response
import re
from config.database import db
import json
from bson.json_util import dumps
import random
from app import app


@app.route("/lab/create", methods=['POST'])
def createLab():
    '''
    Create a lab to be analyzed
    '''
    lab_prefix = request.args["lab_prefix"]
    query = {"lab_id": lab_prefix}
    if db.Labs.find_one(query):
        data = dumps({"Error": f"Ya existe un lab con ese prefix: {lab_prefix}"})
        return Response(data, status=409, mimetype='application/json')
    
    data = dumps(db.Labs.insert_one({"lab_id": lab_prefix, "pulls_list": []}).inserted_id)
    return Response(data, status=200, mimetype='application/json')


@app.route("/lab/<lab_id>/search")
def searchLab(lab_id):
    '''
    Create resoponse with below fields:
        - Number of open PR
        - Number of closed PR
        - Percentage of completeness (closed vs open)
        - List number of missing pr from students
        - The list of unique memes used for that lab
        - Instructor grade time in hours: (pr_close_time-last_commit_time)
    '''
    lab = db.Labs.find_one({"lab_id": lab_id}, {"_id": False})
    if lab:
        pullRequestList = searchPullRequests(lab["pulls_list"])

        labResponse = {}
        labResponse.update({"lab_id:": lab["lab_id"]})

        open_pr_number = openPullRequestNumber(pullRequestList)
        closed_pr_number = closedPullRequestNumber(pullRequestList)
        labResponse.update({"open_pr_number": open_pr_number})
        labResponse.update({"closed_pr_number": closed_pr_number})
        labResponse.update({"pr_completed_per": (closed_pr_number*100)/len(pullRequestList)})
        labResponse.update({"unique_memes_list": listToUnique(joinMemesLists(pullRequestList))})
        labResponse.update({"user_missing_pr_list": usersMissingPrForLab(lab)})
        return Response(dumps(labResponse), status=200, mimetype='application/json')

    return Response(status=404, mimetype='application/json')

@app.route("/lab/memeranking")
def memeRanking():
    '''
    Purpose: Ranking of the most used memes for datamad0820 divided by labs
    '''
    cursor = db.Labs.find({}, {'_id': False})
    labs = []
    for lab in cursor:
        memes_in_lab = []
        for pr in searchPullRequests(lab["pulls_list"]):
            memes_in_lab += pr["memes_lst"]
        lab["memes_ranking"] = memeRankingList(memes_in_lab)
        labs.append(lab)
    
    return Response(dumps(labs), status=200, mimetype='application/json')

@app.route("/lab/<lab_id>/meme")
def randomMeme(lab_id):
    '''
    Devuelve un meme random, de entre todos los utilizados para este lab.
    '''
    lab = db.Labs.find_one({"lab_id": lab_id}, {"_id": False})
    if lab:
        memes_in_lab = []
        for pr in searchPullRequests(lab["pulls_list"]):
            memes_in_lab += pr["memes_lst"]
        random_meme = random.choice(memes_in_lab)
        return Response(dumps(random_meme), status=200, mimetype='application/json')

    return Response(status=404, mimetype='application/json')

def memeRankingList(memes_list):
    '''
        Devuelve una lista donde cada elemento es un json con el meme y las veces que aparece el meme
        Como parámetro  recibe la lista de memes "memes_list". Vamos a llamar a esta función por cada lab.
    '''
    memes_set = set()
    for meme in memes_list:
        memes_set.add(meme)

    meme_ranking = {}
    for meme in list(memes_set):
        if meme in meme_ranking:
            meme_ranking[meme] = meme_ranking[meme] + 1
        else:
            meme_ranking[meme] = 1

    meme_ranking_list = []
    for meme, count in meme_ranking.items():
        meme_ranking_list.append({"meme": meme, "count": count})

    return meme_ranking_list


def searchPullRequests(pullRequestIdList):
    '''
        Devuelve una lista con el id de las pull requests
    '''
    pullRequestList = []

    for pullId in pullRequestIdList:
        pull = db.Pulls.find_one({"pull_id": pullId}, {"_id": False})
        if pull:
            pullRequestList.append(pull)

    return pullRequestList

def openPullRequestNumber(pullRequestList):
    '''
        Devuelve el número de pull requests abiertas
    '''
    counter = 0
    for pullRequest in pullRequestList:
        if pullRequest["state"] == "open":
            counter += 1
    return counter

def closedPullRequestNumber(pullRequestList):
    '''
        Devuelve el número de pull requests abiertas

    '''
    counter = 0
    for pullRequest in pullRequestList:
        if pullRequest["state"] == "closed":
            counter += 1
    return counter

def joinMemesLists(pullRequestList):
    '''
    Devuelve una lista con todos los memes por cada pull request
    '''
    memesList = []
    for pullRequest in pullRequestList:
        memesList += pullRequest["memes_lst"]
    return memesList

def listToUnique(elements_list):
    '''

    '''
    set_converted = set()
    for element in elements_list:
        set_converted.add(element)
    return list(set_converted)

def usersList():
    '''
        Devuelve la lista de users
    '''
    return db.Users.find({}, {'_id': False})

def usersMissingPrForLab(lab):
    '''
    Devuelve una lista de los labs que faltan a cada usuario
    '''
    user_missed_list = []

    for user in usersList():
        if lab["lab_id"] not in user["labs"]:
            user_missed_list.append(user["name"])
    return user_missed_list
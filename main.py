from fastapi import FastAPI
from mapwithlist import generate_mapwithlist
import pymongo
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

@app.get('/map')
def generate():
    generate_mapwithlist()
    return ""

@app.get('/register/name={name}&email={email}&password={password}')
def register(name:str,email:str,password:str):
    client = pymongo.MongoClient("mongodb+srv://hiimanshu:himanshu@fastlance.fmvuepr.mongodb.net/test")
    mydb = client["ambulance"]
    mycol = mydb["userlogin"]
    data = {"Name":f"{name}","Email":f"{email}","Password":f"{password}"}
    if mycol.insert_one(data):
        return True
    else:
        return False

@app.get('/login/email={email}&password={password}')
def login(email:str,password:str):
    client = pymongo.MongoClient("mongodb+srv://hiimanshu:himanshu@fastlance.fmvuepr.mongodb.net/test")
    mydb = client["ambulance"]
    mycol = mydb["userlogin"]
    user = mycol.find_one({'Email':f"{email}","Password":f"{password}"})
    if user:
        return True
    else:
        return False
    
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
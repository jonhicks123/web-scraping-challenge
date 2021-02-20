from splinter import Browser
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
import pymongo
import requests

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    
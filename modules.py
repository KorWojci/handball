import os
import csv
import re
import requests
import xlsxwriter
import http.client
import json
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date
from datetime import timedelta

today_date = datetime.today().strftime('%Y-%m-%d')
today_date_format = datetime.today().strftime('%d-%m-%Y')

with open('C:\\Users\\kordi\\Documents\\Projekty\\config.txt') as f:
        lines = f.readlines()
        for line in lines:
            split = line.split('=')
            match split[0]:
                case 'prefix':
                    prefix = split[1][:-1]
                case 'file_path':
                    file_path = split[1][:-1]
                case 'key_handball':
                    key_handball = split[1][:-1]
                case 'host_handball':
                    host_handball = split[1][:-1]
                case 'key_football':
                    key_football = split[1][:-1]
                case 'host_football':
                    host_football = split[1]

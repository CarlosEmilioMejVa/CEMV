import requests
import mariadb
import datetime

from connect_mariadb_v0_1_1B4 import *

def get_lastest_commit():
	url = 'https://api.github.com/repos/CarlosEmilioMejVa/CEMV/commits/main'
	response = requests.get(url)
	response.raise_for_status()
	commit_data = response.json()
	return commit_data['sha'], commit_data['commit']['author']['date'].split('T')[0]

def save_last_known_commit_sha(mydb, sha_value, sha_date):
	with mydb.cursor() as cursor:
		query = f"INSERT INTO sha_git VALUES(DEFAULT, '{str(sha_value)}', '{sha_date}');"
		cursor.execute(query)
		mydb.commit()

with connect_to_database() as mydb:
	print(mydb)
import requests
import urllib.request
import pandas as pd
from requests.auth import HTTPBasicAuth
from pandas import json_normalize
from functools import reduce

# https://api.onepeloton.com/api/user/56b285f754024a0dab79417df829d033/workout_history_csv?timezone=America/New_York

class PelotonLoginException(Exception):
    pass

class PelotonWorkouts:
  def __init__(self, username, password):
    self.base_url = 'https://api.onepeloton.com'
    self.s = requests.Session()
    self.headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'pylotoncycle'
    }
    # Initialize a couple of variables that will get reused
    # userid - our userid
    # instructor_id_dict - dictionary that will allow us to cache
    #                      information
    #                      format is: instructor_id : instructor_dict
    self.userid = None

    self.test(username, password)
    #self.login(username, password)
    #self.getFile()

  def test(self, username, password):
      username_user = "CacheCoder"
      peloton_csv_link = "https://api.onepeloton.com/api/user/56b285f754024a0dab79417df829d033/workout_history_csv"
      #Authenticate the user
      s = requests.Session()
      payload = {'username_or_email': username, 'password':password}
      s.post('https://api.onepeloton.com/auth/login', json=payload)
      download_data = s.get(peloton_csv_link, allow_redirects=True)
      csv_file = str(username_user) + ".csv"
      with open(csv_file, "wb") as f:
          f.write(download_data.content)



      #API URL -
      # 56b285f754024a0dab79417df829d033
      #workoutUrl = "https://api.onepeloton.com/api/user/{}/workout_history_csv?timezone=America/New_York".format(*my_id)



  def login(self, username, password):
      auth_login_url = '%s/auth/login' % self.base_url
      auth_payload = {
          'username_or_email': username,
          'password': password
      }
      headers = {
          'Content-Type': 'application/json',
          'User-Agent': 'pyloton'
      }
      resp = self.s.post(
          auth_login_url,
          json=auth_payload, headers=headers, timeout=10).json()

      if (('status' in resp) and (resp['status'] == 401)):
          raise PelotonLoginException(resp['message'] if ('message' in resp)
                else "Login Failed")

      self.userid = resp['user_id']

      url = 'http://somewebsite.org'
      #user, password = 'bob', 'I love cats'
      resp = requests.get(self.workoutUrl, auth=(username, password))
      print(resp.content)
      print("logged in as " + self.userid)

  def getFile(self):
      with open('downloaded_workouts.csv', 'wb') as out_file:
          content = requests.get(self.workoutUrl, stream=True).content
          out_file.write(content)

if __name__ == '__main__':
    username = 'blah'
    password = 'blah'
    conn = PelotonWorkouts(username, password)
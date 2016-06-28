#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# import MySQLdb
import sqlite

# conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="seeds")
conn = sqlite.connect('db.sqlite')
c = conn.cursor()

"""
try:
  c.execute('''CREATE TABLE seeds 
    (`id` int AUTO_INCREMENT PRIMARY KEY, 
      `source` varchar(100), 
      `url` varchar(255) UNIQUE, 
      `priority` int,
      `is_active` BOOLEAN,
      `timestamp` TIMESTAMP);
  ''')
  conn.commit()
except Exception,e:
  print str(e)
  pass
"""

try:
  c.execute('''CREATE TABLE seeds 
    (id int AUTO_INCREMENT PRIMARY KEY, 
      source varchar(100), 
      url varchar(255) UNIQUE, 
      priority int,
      is_active BOOLEAN,
      timestamp TIMESTAMP);
  ''')
  conn.commit()
except Exception,e:
  print str(e)
  pass


DEVELOPER_KEY = "AIzaSyCFiMxz3SilBw2Q9AYkHjxxZPoWkAxWUy8"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results,
    order='date'
  ).execute()


  s =  search_response.get('nextPageToken', None)
  
  while(s != None):
    print s
    search_response = youtube.search().list(
      q=options.q,
      part="id,snippet",
      maxResults=options.max_results,
      pageToken=s, 
      order='date'
    ).execute()
    
    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        videos.append("%s (%s)" % (search_result["snippet"]["title"].encode('utf-8'),
                                   search_result["id"]["videoId"].encode('utf-8')))
        url = 'https://www.youtube.com/watch?v=%s' %(search_result["id"]["videoId"].encode('utf-8'))
      elif search_result["id"]["kind"] == "youtube#channel":
        channels.append("%s (%s)" % (search_result["snippet"]["title"].encode('utf-8'),
                                     search_result["id"]["channelId"].encode('utf-8')))
        url = 'https://www.youtube.com/channel/%s' %(search_result["id"]["channelId"].encode('utf-8'))
      elif search_result["id"]["kind"] == "youtube#playlist":
        playlists.append("%s (%s)" % (search_result["snippet"]["title"].encode('utf-8'),
                                      search_result["id"]["playlistId"].encode('utf-8')))
        url = 'https://www.youtube.com/playlist?list=%s' %(search_result["id"]["playlistId"].encode('utf-8'))

      source = 'youtube'
      priority = 0
      is_active = 0

      try:
        command = 'INSERT INTO seeds (source, url, priority, is_active) VALUES ("%s", "%s", "%s", "%s")'%(source, url, priority, is_active)
        c.execute(command)
        conn.commit()
      except Exception, e:
        print str(e)
        pass
      
    print "Videos:\n", "\n".join(videos), "\n"
    print "Channels:\n", "\n".join(channels), "\n"
    print "Playlists:\n", "\n".join(playlists), "\n"

    s =  search_response.get('nextPageToken', None)

if __name__ == "__main__":
  f = open('colors.txt', 'r')
  h = open('errors.txt', 'w')
  primary_colors  = []

  for i in f:
    primary_colors.append(i.strip())
  
  argparser.add_argument("--q", help="Search term", default='Color')
  argparser.add_argument("--max-results", help="Max results", default=25)
  
  for i in primary_colors:
    args = argparser.parse_args(("--q %s"%(i)).split())
    print args

    try:
      youtube_search(args)
    except HttpError, e:
      print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

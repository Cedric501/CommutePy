# This script downloads top YouTube/Dailymotion/Vimeo videos from a subreddit
# It is designed for repeated cron use, like weekly top documentaries

################################
####### Key Variables ##########
################################

SubReddit = "documentaries" # No /r/ required
Period = "Weekly"  # Hourly, Daily, Weekly, Monthly, Yearly
Episodes = 5

UserAgent = "Cedric501-Commute" # Put name of Redditor + project

DestFolder = "/Users/cedriclendais/Documents/Commute/" # Where you want your files + the history of downloads

################################
######### Libraries ############
################################

#Dependencies: PRAW & Youtube-dl
import csv
import os
import praw
import subprocess

################################
######### Functions ############
################################

def service_ok(url):
# youtube-dl supports lots of other services than Youtube
# full list on http://rg3.github.io/youtube-dl/supportedsites.html

  result = False

  if "vimeo" in url:
  	result = True
  elif "youtube" in url:
  	result = True
  elif "youtu.be" in url:
  	result = True
  elif "dailymotion" in url:
    result = True

  return result

################################
######## Main script ###########
################################

# Connect to Reddit through API
r = praw.Reddit(user_agent=UserAgent)

# Connect to subreddit with right time frame
maxlimit = 3*Episodes

if Period == "Hourly":
  submissions = r.get_subreddit(SubReddit).get_top_from_hour(limit=maxlimit)
elif Period == "Daily":
  submissions = r.get_subreddit(SubReddit).get_top_from_day(limit=maxlimit)
elif Period == "Weekly":
  submissions = r.get_subreddit(SubReddit).get_top_from_week(limit=maxlimit)
elif Period == "Monthly":
  submissions = r.get_subreddit(SubReddit).get_top_from_month(limit=maxlimit)
elif Period == "Yearly":
  submissions = r.get_subreddit(SubReddit).get_top_from_year(limit=maxlimit)
else:
  print "This time limit is not known"
  exit()

# Connect to the list of past links downloaded
pastresults = []

if os.path.exists(DestFolder+"past_results.csv"):
  d = csv.reader(open(DestFolder+"past_results.csv","rU"))
  for row in d:
    pastresults.append(row)
else:
  print "No previous results"
  
# Retrieve all youtube links not already downloaded in the past

links = []

for x in submissions:
  if service_ok(x.url):
    if [x.url] not in pastresults:
      if x.link_flair_text != "Trailer":
        links.append(x.url)

links = links[0:min(Episodes,len(links))]

# Download all the youtube videos
if os.path.exists(DestFolder+"past_results.csv"):
  c = csv.writer(open(DestFolder+"past_results.csv", "a"))
else:
  c = csv.writer(open(DestFolder+"past_results.csv", "wb"))

for url in links:
  cli = 'youtube-dl -q -o "' + DestFolder + '%(title)s.%(ext)s" "'  + url + '"'
  subprocess.call(cli, shell=True)

  # Save results
  c.writerow([url])

# End
print "All done, " + str(len(links)) + " items downloaded"


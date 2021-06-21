from twython import Twython
import os, sys
import time

print("Welcome to the Buffalometer\n")
screen_name = input("Enter a Twitter handle: ")
def start_twython():
	#Collect keys
	APP_KEY = os.environ.get('APP_KEY')
	APP_SECRET = os.environ.get('APP_SECRET')
	OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN')
	OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET')
  #Return twython instance
	return Twython(
                  APP_KEY,
                  APP_SECRET,
                  OAUTH_TOKEN,
                  OAUTH_TOKEN_SECRET
                  )

#create twython object
twython = start_twython()

#Locations possibly meaning Buffalo, NY
bflos = [
	"buffalo",
	"bflo",
	"blo",
	"allentown",
	"black rock",
	"fruit belt",
	"elmwood",
	"first ward",
	"hamlin park",
	"kaisertown",
	"university heights",
	"masten park",
	"humbolt park"
]

followers_query = twython.cursor(twython.get_followers_ids, screen_name=screen_name)
followers = []
try:
	for page in followers_query:
		followers.append(page)
except RuntimeError:
	print(f'Collected IDs for {screen_name}\'s {len(followers)} followers')

follower_prof = []
for follower in followers:
	#For testing purposes
	follower_prof.append(twython.show_user(user_id=follower))
	time.sleep(1)
	print(f'Collected profiles for {len(follower_prof)} followers')
	else:
		break
#Pull location from each follower
locs = [f['location'] for f in follower_prof]

#Multiquery search across list
in_buff = [loc for loc in locs if any(buffs in loc.lower() for buffs in bflos)]

#Users that did not provide locations
no_locs = [loc for loc in locs if loc==""]

locs_provided = len(locs)-len(no_locs)

print(f'Total Followers: {len(locs)}\n')
print(f'Followers in Buffalo: {len(in_buff)} ({round(len(in_buff)/len(locs), 2)}% of all followers)\n')
print(f'Locations Provided: {locs_provided} ({round(len(in_buff)/locs_provided, 2)}% of followers providing locations in Buffalo\n')








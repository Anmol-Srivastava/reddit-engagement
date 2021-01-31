# functions to write to sql database given generators from app.py
# insert only if ID doesn't already exist 
# better than checking for dups in python land (how would u even do that when 
# data is saved to sqlite lol, load it and then check? dumbass)
# btw you might want subreddit name also
# maybe inserter is a sep fn
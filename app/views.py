from facebook import get_user_from_cookie, GraphAPI
from flask import g, render_template, redirect, request, session, url_for

from app import app, db
from models import User

from TweetMiner import mineTweets

from Analyzetext import PostData, TweetData, WeightedData, DecayData, CompositeWk, CompositeAvg

# Facebook app details
FB_APP_ID = '829452593844042'
FB_APP_NAME = 'FriendInNeed'
FB_APP_SECRET = 'e3b54e9cf119f1a4fe31225e72c11919'


@app.route('/')
def index():
    # If a user was set in the get_current_user function before the request,
    # the user is logged in.
    if g.user:
        return render_template('confirmation.html', app_id=FB_APP_ID,
                               app_name=FB_APP_NAME, user=g.user)
    # Otherwise, a user is not logged in.
    return render_template('login.html', app_id=FB_APP_ID, name=FB_APP_NAME)

@app.route('/confirmation', methods = ['GET','POST'])
def confirm():
    graph = GraphAPI(access_token='CAALyYfs2z0oBAGkAVLO8cZAqZAzz5SF9ncMdQunQB2aq1HME3N2DC1iyL2QHtTW2WryHWyxhlih78uNa64kABBCM0Bg5c2C7yEEmjnRHlAibYnV4vqwNcN01VSpORHqBWTfFwXYcP6kLWB5QYsFqe7WvccNZCPkn4UJfujPMwZASeGmF3qthjBa5nYl2672ZB4Q9KpbaVoQZDZD')
    post = graph.get_object('/me/'+'posts',since = "2016-02-20T00:00:00")
    postInfo = post['data'];
    postList = []
    for d in postInfo:
        postList.append((d['message'], d['created_time']))
    tweetList = mineTweets(request.form['twitter_usr'])

    FB_posts = PostData(postList)
    TW_posts = TweetData(tweetList)

    WD_posts = WeightedData(FB_posts, TW_posts)
    Decayed  = DecayData(WD_posts)
    LastWk   = CompositeWk(Decayed)
    DecAvg   = CompositeAvg(Decayed)

    Sent2 = "Our algorithm indicates that you are experiencing significantly negative sentiment. We advise you seek the company of friends or family and discuss factors that may be leading to such tension. If you believe you are at risk for depression, please seek the counsel of a medical professional."
    Sent4 = "Our algorithm indicates that you are experiencing moderately negative sentiment. We advise you seek the company of friends or family, spend some time pursuing your own interests, and consider increasing relaxing activities."
    Sent6 = "Our algorithm indicates that you are experiencing rather neutral sentiment. Consider increasing relaxing activities."
    Sent8 = "Our algorithm indicates you are experiencing rather positive sentiment. We hope you continue enjoying your experiences and pursue other enjoyable activities in the future."
    Sent10 = "Our algorithm indicates that you are experiencing highly positive sentiment! We hope you continue to enjoy your experiences and assist others who may not be as fortunate."

    if (LastWk >= 0 and LastWk <= 2):
        summary = Sent2
    elif (LastWk >2 and LastWk <=4):
        summary = Sent4
    elif (LastWk >4 and LastWk <=6):
        summary = Sent6
    elif (LastWk >6 and LastWk<=8):
        summary = Sent8
    elif (LastWk > 8 and LastWk <=10):
        summary = Sent10
    else:
        summary = "Unable to determine sentiment score."

    return render_template('index.html', app_id=FB_APP_ID,
                           app_name=FB_APP_NAME, user=g.user,
                           fb_values =  FB_posts, tw_values = TW_posts,
                           overall = Decayed, week = LastWk, average = DecAvg,
                           summary = summary)
@app.route('/logout')
def logout():
    """Log out the user from the application.
    Log out the user from the application by removing them from the
    session.  Note: this does not log the user out of Facebook - this is done
    by the JavaScript SDK.
    """
    session.pop('user', None)
    return redirect(url_for('index'))


@app.before_request
def get_current_user():
    """Set g.user to the currently logged in user.
    Called before each request, get_current_user sets the global g.user
    variable to the currently logged in user.  A currently logged in user is
    determined by seeing if it exists in Flask's session dictionary.
    If it is the first time the user is logging into this application it will
    create the user and insert it into the database.  If the user is not logged
    in, None will be set to g.user.
    """

    # Set the user in the session dictionary as a global g.user and bail out
    # of this function early.
    if session.get('user'):
        g.user = session.get('user')
        return

    # Attempt to get the short term access token for the current user.
    result = get_user_from_cookie(cookies=request.cookies, app_id=FB_APP_ID,
                                  app_secret=FB_APP_SECRET)

    # If there is no result, we assume the user is not logged in.
    if result:
        # Check to see if this user is already in our database.
        user = User.query.filter(User.id == result['uid']).first()

        if not user:
            # Not an existing user so get info
            graph = GraphAPI(result['access_token'])
            profile = graph.get_object('me')
            if 'link' not in profile:
                profile['link'] = ""

            # Create the user and insert it into the database
            user = User(id=str(profile['id']), name=profile['name'],
                        profile_url=profile['link'],
                        access_token=result['access_token'])
            db.session.add(user)
        elif user.access_token != result['access_token']:
            # If an existing user, update the access token
            user.access_token = result['access_token']

        # Add the user to the current session
        session['user'] = dict(name=user.name, profile_url=user.profile_url,
                               id=user.id, access_token=user.access_token)

    # Commit changes to the database and set the user as a global g.user
    db.session.commit()
    g.user = session.get('user', None)

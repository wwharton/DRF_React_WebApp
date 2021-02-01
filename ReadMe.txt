This is a dummy directory to highlight a WIP project.

It is built with future iterations in mind, as I hope to use this project as a way to practice feature design
    with github issues and pulls.

WSB_tldr is a dockerized Django/React app which displays a web page featuring either a rocket or a bear,
    reflecting expressed economy sentiment from WallStreetBets users.
The app leverages Reddit's public API to sample recently trending posts and comments from the subreddit.
Using several custom classes  the app can get posts, post text, and comments, of variable quantity.
It uses SQLAlchemy and Pandas' df-to-sql to database the posts, comments, and metadata.
Since it is sampling a lower volume of comments than total, I use a regex to extract comment "body" content from the Reddit returned JSON.
    (Regex is maybe the worst method here, but was a working solution to the complexity of deeply nested JSON responses)
Then it hunts uses keyword frequency to estimate a proportion of bull:bear market sentiment.
It stores meta data of bull:bear frequency in a persistent db table, whereas the posts and comments are wiped on refresh to conserve space.
DRF drives the API, following MVT design.
I used React to create the two possible display webpages/css and an index.js page where I fetch from my Django API to determine what to display.
Static pages are generated from a built version of the react app to allow for Django to static serve the final webpage.
The app is containerized and scheduled to run Reddit API requests and update the metadata (and thus app display page) daily with Cron

The to-do list:
    Rewrite DB generators (I have a band-aid function to apply primary key columns via queries)
    Rewrite the Reddit API tools with PRAW to extract, up to, all possible posts and comments
    Rewrite the Reddit API tools to use DRF to post to the db instead of direct SQLAlchemy queries
    Create or commission cleaner svg images
    Create an About Page
    Create a Calendar of results




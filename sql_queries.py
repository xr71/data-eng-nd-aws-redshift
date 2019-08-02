import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# print(*config["CLUSTER"].values())

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS times"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events (
         eventid integer PRIMARY KEY IDENTITY(0,1)
        ,artist text
        ,auth text
        ,firstName text
        ,gender text
        ,itemInSession text
        ,lastName text
        ,length text
        ,level text
        ,location text
        ,method text
        ,page text
        ,registration text
        ,sessionid text
        ,song text
        ,status text
        ,startTime text
        ,userAgent text
        ,userid text
    )
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs (
         num_songs integer
        ,artist_id text
        ,artist_latitude double precision
        ,artist_longitude double precision
        ,artist_location text
        ,artist_name text
        ,song_id text PRIMARY KEY
        ,title text
        ,duration double precision
        ,year integer
    )
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
         songplayid integer PRIMARY KEY IDENTITY(0,1)
        ,startTime timestamp sortkey
        ,userid text 
        ,level text
        ,songid text
        ,artistid text
        ,sessionid text
        ,location text
        ,userAgent text
    ) 
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
         userid text PRIMARY KEY
        ,firstName text
        ,lastName text
        ,gender text
        ,level text
    ) DISTSTYLE ALL
""")


song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
         songid text PRIMARY KEY
        ,title text
        ,artistid text sortkey
        ,year integer
        ,duration double precision
    ) DISTSTYLE ALL
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
         artistid text PRIMARY KEY
        ,artistName text
        ,artistLocation text
        ,artistLatitude double precision
        ,artistLongitude double precision
    ) DISTSTYLE ALL
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS times (
         startTime timestamp PRIMARY KEY
        ,hour integer
        ,day integer
        ,week integer
        ,month integer
        ,year integer
        ,weekday text
    ) DISTSTYLE ALL
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events
    FROM {}
    CREDENTIALS 'aws_iam_role={}'
    REGION 'us-west-2'
    FORMAT AS JSON {}
""").format(config.get('S3', 'LOG_DATA'), 
            config.get('IAM_ROLE', 'ARN'), 
            config.get('S3', 'LOG_JSONPATH'))

staging_songs_copy = ("""
    COPY staging_songs
    FROM {}
    CREDENTIALS 'aws_iam_role={}'
    REGION 'us-west-2'
    JSON 'auto'
""").format(config.get('S3', 'SONG_DATA'),
            config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays 
    (startTime, userid, level, songid, artistid, sessionid, location, userAgent)
    select TIMESTAMP 'epoch' + starttime/1000*INTERVAL '1 second' as starttime
          ,e.userid
          ,e.level
          ,s.song_id
          ,s.artist_id
          ,e.sessionid
          ,e.location
          ,e.userAgent
    FROM staging_events as e
    JOIN staging_songs as s
        on e.song = s.title
    where e.page = 'NextSong'
""")

user_table_insert = ("""
    INSERT INTO users
    (userid, firstName, lastName, gender, level)
    select distinct userid
          ,firstName
          ,lastName
          ,gender
          ,level
    FROM staging_events 
    where page = 'NextSong'
""")

song_table_insert = ("""
    INSERT INTO songs
    (songid, title, artistid, year, duration)
    select distinct song_id
          ,title
          ,artist_id
          ,year
          ,duration
    from staging_songs 
""")

artist_table_insert = ("""
    INSERT INTO artists
    (artistid, artistName, artistLocation, artistLatitude, artistLongitude)
    select distinct artist_id
          ,artist_name
          ,artist_location
          ,artist_latitude
          ,artist_longitude
    FROM staging_songs
""")

time_table_insert = ("""
    INSERT INTO times
    (starttime, hour, day, week, month, year, weekday)
    select distinct starttime
          ,extract(hr from starttime) as hour
          ,extract(d from starttime) as day
          ,extract(w from starttime) as week
          ,extract(mon from starttime) as month
          ,extract(yr from starttime) as year
          ,extract(weekday from starttime) as weekday
    FROM (
        select distinct 
               TIMESTAMP 'epoch' + starttime/1000*INTERVAL '1 second' as starttime
        from staging_events
    ) as e
""")

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

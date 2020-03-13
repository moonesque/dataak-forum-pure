# Database credentials
CONNECTION_STRING = "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}?charset=utf8".format(
    drivername="mysql",
    user="root",
    passwd="oberyn martel",
    host="localhost",
    port="3306",
    db_name="dataak_forum_pure",
)
# forum links
forum_url = 'http://forum.dataak.com/index.php'
login_url = 'http://forum.dataak.com/member.php'
host = 'forum.dataak.com'

# user credentials
forum_username = 'mahan'
forum_password = '@123456'

# request headers
headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Host": host,
}


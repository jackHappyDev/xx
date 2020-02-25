from sqlalchemy import create_engine,Column,Integer,String,Table,MetaData
import pymysql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BaseUrl = 'http://www.okzy.co/'
BASE_FIRSTURL = 'http://www.okzy.co/index.php'
LocalPath = '/Users/jack/Desktop/123/'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
SimpleSearchUrl = 'http://www.okzy.co//?m=vod-detail-id-24967.html'

engine = create_engine('mysql+pymysql://root:jj123456@127.0.0.1/videoInfoList',echo =False)
DBSession = sessionmaker(bind=engine)

session = DBSession()

Base = declarative_base()

metadata =MetaData(engine)

#创建类目 数据库
MoviesInfo = Table('MoviesInfo',metadata,
                   Column('id',Integer,primary_key=True,autoincrement=True),
                   Column('title',String(10)),
                   Column('href',String(100)),
                   Column('tp',String(20)),
                   )

metadata.create_all(engine)


#创建类目下面的类型 数据库 分类装 类型下面的所有地址
MoviesDetailListInfo =Table('MoviesDetailListInfo',metadata,
                            Column('id',Integer,primary_key=True,autoincrement=True),
                            Column('moveType',String(10)),
                            Column('title',String(100)),
                            Column('link',String(100)),
                            Column('did',Integer),
                            )
metadata.create_all(engine)

#创建播放信息的视频列表
VideoPlayInfo = Table(
    'VideoPlayInfo',metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('videoName',String(100)),
    Column('videoImg',String(100)),
    Column('videoInfoContent',String(10000)),
    Column('videoPlayAdd',String(200)),
)
metadata.create_all(engine)

#创建电影或者电视剧的m3u8的视频地址列表
VideoM3u8List = Table(
    'VideoM3u8List',metadata,
    Column('id',Integer,primary_key=True,autoincrement=True),
    Column('playAdd',String(100)),
    Column('fzid',Integer),
)
metadata.create_all(engine)

TmpList = Table(
    'TmpList',metadata,
    Column('id',Integer,primary_key=True,autoincrement=True),
    Column('msg',String(10)),
)
metadata.create_all(engine)

Chatlist = Table(
    'Chatlist',metadata,
    Column('id',Integer,primary_key=True,autoincrement=True),
    Column('name',String(100)),
    Column('msg',String(1024)),
)
metadata.create_all(engine)



class MoviesInfo(Base):
    __tablename__ = 'moviesInfo'
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(10))
    href =Column(String(200))
    tp = Column(String(20))

class MoviesDetailListInfo(Base):
    __tablename__ = 'moviesDetailListInfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    moveType = Column(String(10))
    title = Column(String(100))
    link = Column(String(200))
    did =Column(Integer)

class VideoPlayInfo(Base):
    __tablename__ = 'videoPlayInfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    videoName = Column(String(100))
    videoImg = Column(String(100))
    videoInfoContent = Column(String(2500))
    videoPlayAdd = Column(String(200))

class VideoM3u8List(Base):
    __tablename__ = 'videoM3u8List'
    id = Column(Integer, primary_key=True, autoincrement=True)
    playAdd = Column(String(100))
    fzid = Column(Integer)

class TmpList(Base):
    __tablename__ = 'tmpList'
    id = Column(Integer,primary_key=True,autoincrement=True)
    msg = Column(String(10))


class Chatlist(Base):
    __tablename__ = 'chatlist'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(100))
    msg = Column(String(1024))
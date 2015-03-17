# -*- coding: utf-8 -*-
import urllib,urllib2,re,os
import xbmcplugin,xbmcgui,xbmcaddon
from stats import *
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP

addon = xbmcaddon.Addon('plugin.video.dmd.streams')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))

__settings__ = xbmcaddon.Addon(id='plugin.video.dmd.streams')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )
file = __settings__.getSetting('xml_file')
if __settings__.getSetting('community_list') == "true":
        if __settings__.getSetting('save_location') == "":
                xbmc.executebuiltin("XBMC.Notification('DMD Streams','Vyber místo s playlisty.',30000,"+icon+")")
                __settings__.openSettings()

def getSoup():
        req = urllib2.Request('http://iamm.xf.cz/ims/xbmc/streams/')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup = BeautifulSoup(link, convertEntities=BeautifulSoup.HTML_ENTITIES)
        print soup
        files = soup('ul')[0]('li')[1:]
        for i in files:
            name = i('a')[0]['href']
            url = 'http://iamm.xf.cz/ims/xbmc/streams/'+name 
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            name = xbmc.makeLegalFilename(os.path.join(__settings__.getSetting('save_location'), '%s') % name)
            try:
                f = open(name,"w")
                f.write(link)
                f.close()
            except:
                print "Nemohu ukládat do zvoleného umístění, vyber jiné." 
        req = urllib2.Request('http://iamm.xf.cz/ims/xbmc/streams/')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        try:
            R = open(REV,"w")
            R.write(link)
            R.close()
        except:
            print "nemohu zapsat revizi do profilu."

def checkForUpdate():
        url = 'http://iamm.xf.cz/ims/xbmc/streams/'
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        revision = re.compile('<html><head><title>(.+?)/trunk</title></head>').findall(link)
        try:
            R = open(REV,"r")
            rev = R.read()
            R.close()
        except:
            getSoup()
            print "neexistuje soubor s revizí."
        try:
            revision_check = re.compile('<html><head><title>(.+?)/trunk</title></head>').findall(rev)
            if revision_check[0] != revision[0]:
                getSoup()
        except:
            getSoup()
            pass
        

if __settings__.getSetting('community_list') == "true":
        checkForUpdate()

def getStreams():
        try:
                response = open(file, 'rb')
        except:
                xbmc.executebuiltin("XBMC.Notification('DMD Streams','Vyber playlist',30000,"+icon+")")
                __settings__.openSettings()
                return
        link=response.read()
        soup = BeautifulStoneSoup(link, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        if len(soup('channels')) > 0:
                channels = soup('channel')
                for channel in channels:
                        name = channel('name')[0].string
                        thumbnail = channel('thumbnail')[0].string
                        url = ''
                        addDir(name,url,2,thumbnail)
        else:
                INDEX()

def getChannels(url):
        response = open(file, 'rb')
        link=response.read()
        soup = BeautifulStoneSoup(file, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        channels = soup('channel')
        for channel in channels:
                name = channel('name')[0].string
                thumbnail = channel('thumbnail')[0].string
                addDir(name,'',2,thumbnail)
        else:
                INDEX()        
                        
def getChannelItems(name):
        response = open(file, 'rb')
        link=response.read()
        soup = BeautifulSOAP(link, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        channel_list = soup.find('channel', attrs={'name' : name})
        items = channel_list('item')
        for channel in channel_list('subchannel'):
                name = channel('name')[0].string
                thumb = channel('thumbnail')[0].string
                addDir(name,'',3,thumb)
        for item in items:
                try:
                        name = item('title')[0].string
                except:
                        pass
                     
                try:
                        if __settings__.getSetting('mirror_link') == "true":
                                try:
                                        url = item('link')[1].string	
                                except:
                                        url = item('link')[0].string
                        if __settings__.getSetting('mirror_link_low') == "true":
                                try:
                                        url = item('link')[2].string	
                                except:
                                        try:
                                                url = item('link')[1].string
                                        except:
                                                url = item('link')[0].string
                        else:
                                url = item('link')[0].string
                except:
                        pass
                        
                try:
                        thumbnail = item('thumbnail')[0].string
                except:
                        thumbnail = ''
                addLink(url,name,thumbnail)

def getSubChannelItems(name):
        response = open(file, 'rb')
        link=response.read()
        soup = BeautifulSOAP(link, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        channel_list = soup.find('subchannel', attrs={'name' : name})
        items = channel_list('subitem')
        for item in items:
                try:
                        name = item('title')[0].string
                except:
                        pass
                     
                try:
                        if __settings__.getSetting('mirror_link') == "true":
                                try:
                                        url = item('link')[1].string	
                                except:
                                        url = item('link')[0].string
                        if __settings__.getSetting('mirror_link_low') == "true":
                                try:
                                        url = item('link')[2].string	
                                except:
                                        try:
                                                url = item('link')[1].string
                                        except:
                                                url = item('link')[0].string
                        else:
                                url = item('link')[0].string
                except:
                        pass
                        
                try:
                        thumbnail = item('thumbnail')[0].string
                except:
                        thumbnail = ''
                addLink(url,name,thumbnail)               


def INDEX():
        response = open(file, 'rb')
        link=response.read()
        soup = BeautifulStoneSoup(link, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        items = soup('item')
        for item in items:
                try:
                        name = item('title')[0].string
                except:
                        pass
                        name = ''
                try:
                        if __settings__.getSetting('mirror_link') == "true":
                                try:
                                        url = item('link')[1].string	
                                except:
                                        url = item('link')[0].string
                        if __settings__.getSetting('mirror_link_low') == "true":
                                try:
                                        url = item('link')[2].string	
                                except:
                                        try:
                                                url = item('link')[1].string
                                        except:
                                                url = item('link')[0].string
                        else:
                                url = item('link')[0].string
                except:
                        pass#url = item('link')[0].string
                try:
                        thumbnail = item('thumbnail')[0].string
                except:
                        thumbnail = ''       
                addLink(url,name,thumbnail)
	


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(url,name,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

            
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        url = ''
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None:
        print ""
        STATS("getStreams", "Function")
        getStreams()

elif mode==1:
        print ""+url
        STATS("getChanels", "Function")
        getChannels()

elif mode==2:
        print ""+url
        STATS(name, "Item")
        getChannelItems(name)

elif mode==3:
        print ""+url
        STATS(name, "Item")
        getSubChannelItems(name)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))

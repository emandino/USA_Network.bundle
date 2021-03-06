SHOW_LIST = "http://feed.theplatform.com/f/OyMl-B/PleQEkKucpUm/categories?&form=json&fields=order,title,fullTitle,label,:smallBannerUrl,:largeBannerUrl&fileFields=duration,url,width,height&sort=order"
EPISODE_FEED = "http://feed.theplatform.com/f/OyMl-B/8IyhuVgUXDd_/?&form=json&fields=guid,title,description,:subtitle,content,thumbnails,categories,:fullEpisode&fileFields=duration,url,width,height,contentType,fileSize,format&byCategories=Series/%s&byCustomValue={fullEpisode}{true}&count=true"
VIDEO_URL = "http://www.usanetwork.com/videos/%s/vid:%s"

ICON = 'icon-default.png'
ART  = 'art-default.jpg'

####################################################################################################
def Start():

	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = 'USA Network'
	DirectoryObject.thumb = R(ICON)

	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.14 (KHTML, like Gecko) Version/6.0.1 Safari/536.26.14'

####################################################################################################
@handler('/video/usanetwork', 'USA Network', art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer()
	show_list = JSON.ObjectFromURL(SHOW_LIST)

	for show in show_list['entries']:
		if "Series/" in show['plcategory$fullTitle']:
			title = show['title']
		else:
			continue

		oc.add(DirectoryObject(key=Callback(EpisodesPage, title=title), title=title))

	oc.objects.sort(key = lambda obj: obj.title)

	return oc

####################################################################################################
@route('/video/usanetwork/episodes')
def EpisodesPage(title):

	oc = ObjectContainer(title2=title)
	episode_list = JSON.ObjectFromURL(EPISODE_FEED % String.Quote(title))

	for episode in episode_list['entries']:
		video_title = episode['title']
		summary = episode['description']
		show = title
		thumbs = SortImages(episode['media$thumbnails'])
		duration = int(float(episode['media$content'][0]['plfile$duration'])*1000)
		video_url = VIDEO_URL % (String.Quote(title), episode['guid'])

		oc.add(EpisodeObject(url=video_url, title=video_title, show=show, summary=summary,
			thumb=Resource.ContentsOfURLWithFallback(url=thumbs, fallback=ICON)))

	if len(oc) == 0:
		return ObjectContainer(header="Empty", message="No episodes found.")

	return oc

####################################################################################################
def SortImages(images=[]):

	sorted_thumbs = sorted(images, key=lambda thumb : int(thumb['plfile$height']), reverse=True)
	thumb_list = []

	for thumb in sorted_thumbs:
		thumb_list.append(thumb['plfile$url'])

	return thumb_list

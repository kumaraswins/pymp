

# Pymp - a python based youtube to mp3 converter for linux #

Pymp is a python based youtube downloader and mp3 converter for linux-based systems. It is a python/qt fronted for the famous python script youtube-dl.

## Intention ##

Pymp is the frontend for and based on the script youtube-dl. youtube-dl is a downloader for videos from certain sites (youtube.com, google video, yahoo video ...). Therefor it is not specialized on one. This program only relies on the availability of the video host. Which is much better than that of the conversion sites. As soon you have the video you can do anything with it.
Pymp extracts the audio cuts the silence at the beginning and the end. It converts it to mp3 and it normalizes the audio. That means setting it to a certain amplitude-level so that every mp3 has the same loudness.

And besides other youtube-dl frontends it can run several downloads/conversions in parallel.
What it does not provide is what the typical youtube-specialized programs do offer - a fancy UI which basically shows a video list for your search query. That can be done within the browser (of either a laptop or the N900).

The reason why this program was made are

  * All online youtube/mp3 converter are not good - they either suffer from to much traffic, or can't convert something from time to time etc. (even though there are fast for stuff they have in their database)
  * Online converters are down from time to time
  * They are mostly specialized for a certain site (youtube)
  * Many of the online converters are bad to use from my mobile (N900) and I guess many others too - there must be a reason for those youtube-apps

## Dependencies ##

Pymp depends on programs that are not delivered with pymp. Those are:

### Must have ###

ffmpeg or mplayer together with lame. At least one of them needs to be available.

### Optional ###

  * sox (cutting silcence at the beginning and the end)
  * normalize (adjusting the output volume)

# Screenshots #

http://sites.google.com/site/markusscharnowski/_/rsrc/1297613600810/pc-software/pymp-youtube-downloader-and-mp3-converter/addingFiles.png?height=250&width=400

http://sites.google.com/site/markusscharnowski/_/rsrc/1297613607102/pc-software/pymp-youtube-downloader-and-mp3-converter/preferences.png?height=222&width=400

http://sites.google.com/site/markusscharnowski/_/rsrc/1297613614090/pc-software/pymp-youtube-downloader-and-mp3-converter/runningDownloads6.png?height=250&width=400

https://sites.google.com/site/markusscharnowski/_/rsrc/1297614696847/pc-software/pymp-youtube-downloader-and-mp3-converter/screenshot01.png?height=240&width=400

http://sites.google.com/site/markusscharnowski/_/rsrc/1297614701144/pc-software/pymp-youtube-downloader-and-mp3-converter/screenshot03.png?height=240&width=400

http://sites.google.com/site/markusscharnowski/_/rsrc/1297614710218/pc-software/pymp-youtube-downloader-and-mp3-converter/screenshot07.png?height=240&width=400
#!/usr/bin/python3
"""
This Script is written by ## THANMAYRAM B R ##

This python program reads youtube links from the file and downloads mp4a files and 
converts them to raw 16bit pcm files with 8khz and 16khz sampling rate 

this program runs with an assumption that 'youtube_dl' and 'ffmpeg' are installed 

To install youtube_dl run $ sudo pip install youtube_dl

To install ffmpeg run $ sudo pip install ffmpeg

this programs accepts only one file as an input 
reads youtube links from links_file
creates 'raw_audio_database_8khz'and 'raw_audio_database_16khz' folder and store the raw_pcm files
processes link by link using for loop
downloads the audio stream into youtube_audio_downloads folder
convert mp4a to 16bit raw pcm with 8khz and 16khz  sampling rate using ffmpeg 
where the codec requirements are given as input to ffmpeg along with input file 
all the processing data for each youtube link are printed on the stdout
this data can be considered as log data of this program 
loads all the raw pcm file into 'raw_audio_database_8khz'and 'raw_audio_database_16khz' folders
deletes the 'youtube_audio_downloads' folder 
"""

import youtube_dl
import subprocess
import sys 


# link list file intake
if (len(sys.argv) < 2):
    print("Argument Error\nHelp syntax :- $ "+sys.argv[0]+" <Links_file_name.txt> \nmake sure to add a links_file as input")
    sys.exit()

# Opening file
try:
    links=open(sys.argv[1],'r')
except Exception as e:
    print("could not open/read file :- "+sys.argv[1])
    print("Exception : %s" %(e))
    sys.exit()

c = 0
subprocess.call(['mkdir', 'raw_audio_database_8khz'])
subprocess.call(['mkdir', 'raw_audio_database_16khz'])

#Iterate through links
for i in links:
    c += 1
    ydl_opts = {'format':'bestaudio/best','outtmpl':'youtube_audio_downloads/'+str(c)+'.%(ext)s',}
    print(str(c)+". "+i)

    # Check for no link
    if i == "\n" :
        print("Error no link \nEmpty line \n\n")
        continue

    yt = i.strip()
    # Filter and select audio stream 
    opted = youtube_dl.YoutubeDL(ydl_opts)

    # Connect and download from youtube
    try:
        opted.download([yt])
    except Exception as e:
        print("Unable to download the video from the link %s" %(i))
        print("%s\n\n" %(e))
        continue

    # Convert mp4a to 16bit raw pcm with 8khz sampling rate
    subprocess.call(['ffmpeg' , '-i',"youtube_audio_downloads/"+str(c)+".m4a" , '-acodec', 'pcm_s16le', '-f' ,'s16le' ,'-ac' ,'1', '-ar' ,'8000' ,"raw_audio_database_8khz/sample"+str(c)+"_8khz.pcm"])
    print('8khz pcm file created\n \n \n')
    
    subprocess.call(['ffmpeg' , '-i',"youtube_audio_downloads/"+str(c)+".m4a" , '-acodec', 'pcm_s16le', '-f' ,'s16le' ,'-ac' ,'1', '-ar' ,'16000' ,"raw_audio_database_16khz/sample"+str(c)+"_16khz.pcm"])
    print('16khz pcm file created\n \n \n')

subprocess.call(['rm', '-r', 'youtube_audio_downloads']) 
print('Task Completed!')
links.close()

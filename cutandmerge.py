import sys
import time
import os
import moviepy.editor
from moviepy.editor import *
import configparser
import csv
from configparser import ConfigParser

def configMovieConcatenate():
	parser = ConfigParser()
	parser.read("CSettings.cfg")

	xheight = int(parser.get('Settings', 'height'))
	xwidth = int(parser.get('Settings', 'width'))
	xfps = int(parser.get('Settings', 'fps'))

	moviesnames = []
	timesnames = []
	outputs=[]

	with open('movies.csv') as f:
		for line in csv.DictReader(f, fieldnames=('v1', 'v2')):
			moviesnames.append(line["v1"])
			timesnames.append(line["v2"])

	StartTime = []

	for i in timesnames:
		StartTime.append(i.split('-')[0])

	EndTime = []

	for i in timesnames:
	    EndTime.append(i.split('-')[1])

	t = len(StartTime)

	for b in range(t):
	    clip = moviepy.editor.VideoFileClip(moviesnames[b]).resize((xwidth, xheight)) 

	    out_clip = clip.subclip(StartTime[b],EndTime[b])

	    outputs.append(out_clip)

	collage = moviepy.editor.concatenate_videoclips(outputs) 
	collage.write_videofile('OutPutVideoMerged.mp4', fps=xfps)
import sys
import KcwikiVoiceClient as KVC

voiceClient = KVC.KcwikiVoiceClient()

if len(sys.argv) == 1:
	voiceClient.downloadVoice()
	voiceClient.removeDuplicatedVoice()
	voiceClient.uploadVoice()
	voiceClient.generateWikiCode()

if len(sys.argv) == 2:
	if sys.argv[1] == 'download' or sys.argv[1] == '-d':
		print '-'*16 + ' download ' + '-'*16
		voiceClient.downloadVoice()
		voiceClient.removeDuplicatedVoice()
	if sys.argv[1] == 'upload' or sys.argv[1] == '-u':
		print '-'*16 + ' upload ' + '-'*16
		voiceClient.uploadVoice()
	if sys.argv[1] == 'genwiki' or sys.argv[1] == '-g':
		print '-'*16 + ' generate wiki code ' + '-'*16
		voiceClient.generateWikiCode()

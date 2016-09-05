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
        print '-'*16 + ' download started ' + '-'*16
        voiceClient.downloadVoice()
        print '-'*16 + ' download finished ' + '-'*16
    if sys.argv[1] == 'remove_duplicated' or sys.argv[1] == '-r':
        print '-'*16 + ' remove duplicated started ' + '-'*16
        voiceClient.removeDuplicatedVoice()
        print '-'*16 + ' remove duplicated finished ' + '-'*16
    if sys.argv[1] == 'upload' or sys.argv[1] == '-u':
        print '-'*16 + ' upload started ' + '-'*16
        voiceClient.uploadVoice()
        print '-'*16 + ' upload finished ' + '-'*16
    if sys.argv[1] == 'genwiki_seasonal' or sys.argv[1] == '-g':
        print '-'*16 + ' generate wiki code started' + '-'*16
        voiceClient.generateWikiCode()
        print '-'*16 + ' generate wiki code finished' + '-'*16

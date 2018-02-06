import sys
import asyncio

from KcwikiVoiceClient import KcwikiVoiceClient

voiceClient = KcwikiVoiceClient()


async def main():
    await voiceClient.reqeustKcdataJson()

    if len(sys.argv) == 1:
        await voiceClient.downloadVoice()
        voiceClient.removeDuplicatedVoice()
        await voiceClient.uploadVoice()
        voiceClient.generateWikiCode()

    elif len(sys.argv) == 2:
        if sys.argv[1] == 'download' or sys.argv[1] == '-d':
            print('-' * 16 + ' download started ' + '-' * 16)
            await voiceClient.downloadVoice()
            print('-' * 16 + ' download finished ' + '-' * 16)
        elif sys.argv[1] == 'upload' or sys.argv[1] == '-u':
            print('-' * 16 + ' upload started ' + '-' * 16)
            voiceClient.removeDuplicatedVoice()
            await voiceClient.uploadVoice()
            print('-' * 16 + ' upload finished ' + '-' * 16)
        elif sys.argv[1] == 'genwiki' or sys.argv[1] == '-g':
            print('-' * 16 + ' generate wiki code started' + '-' * 16)
            voiceClient.generateWikiCode()
            print('-' * 16 + ' generate wiki code finished' + '-' * 16)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

#!/bin/bash
#
# Scrape IPTV m3u8 URLs from iptvcat.com & add to local playlist.
#
# v.1.0

SCRAPE_URL='https://iptvcat.com/s/nautical'
DEST_FILE='/tmp/test.m3u'
CHANNEL_ID='Nautical.Channel.HD.gr'
CHANNEL_NAME='USA | Nautical Channel (custom)'
CHANNEL_LOGO='https://www.pngkey.com/png/detail/420-4205016_nautical-channel-logo.png'
CHANNEL_GROUP_TITLE='"USA",USA | Nautical Channel(custom)'

# Check if VARS empty.
EMPTY_VARS=0
for i in `echo "SCRAPE_URL DEST_FILE CHANNELS_ID CHANNEL_NAME CHANNEL_LOGO CHANNEL_GROUP_TITLE"`; do
        if [ "$i" = "" ]; then
                EMPTY_VARS=1
                echo -e "\n$i is empty. Please set variable inside this script.\n"
        fi
done

if [ "$EMPTY_VARS" == 0 ]; then
        # Grab channels.
        LINKS_TO_ADD=`curl -s $SCRAPE_URL | grep get_vlc | grep -Po 'https:\/\/list\.iptvcat\.com\/my_list\/s\/.*.m3u8'`

        # Add channels.
        for i in `echo  "$LINKS_TO_ADD"`; do echo -e \#EXTINF\:-1 tvg-id\=\"$CHANNEL_ID\" tvg-name\=\"$CHANNEL_NAME\" tvg-logo\=\"$CHANNEL_LOGO\" group-title\=$CHANNEL_GROUP_TITLE\\n$i >> $DEST_FILE; done
fi

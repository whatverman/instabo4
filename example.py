#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
from src import InstaBot
from src.check_status import check_status
from src.feed_scanner import feed_scanner
from src.follow_protocol import follow_protocol
from src.unfollow_protocol import unfollow_protocol

bot = InstaBot(
    login=process.env.login,
    password=process.env.pass,
    like_per_day=process.env.like_per_day,
    comments_per_day=process.env.comments_per_day,
    tag_list=[process.env.tag_list],
    tag_blacklist=[process.env.tag_blacklist],
    user_blacklist={},
    max_like_for_one_tag=process.env.max_like_for_one_tag,
    follow_per_day=process.env.follow_per_day,
    follow_time=1 * 60,
    unfollow_per_day=process.env.unfollow_per_day,
    unfollow_break_min=process.env.unfollow_break_min,
    unfollow_break_max=process.env.unfollow_break_max,
    log_mod=process.env.log_mod,
    proxy=process.env.proxy,
    # List of list of words, each of which will be used to generate comment
    # For example: "This shot feels wow!"
    comment_list=[[process.env.comment_list1],
                  [process.env.comment_list2],
                  [process.env.comment_list3],
                  [process.env.comment_list4],
                  [process.env.comment_list5]],
    # Use unwanted_username_list to block usernames containing a string
    ## Will do partial matches; i.e. 'mozart' will block 'legend_mozart'
    ### 'free_followers' will be blocked because it contains 'free'
    unwanted_username_list=[process.env.unwanted_username_list
    ],
    unfollow_whitelist=[process.env.unfollow_whitelist])
while True:

    #print("# MODE 0 = ORIGINAL MODE BY LEVPASHA")
    #print("## MODE 1 = MODIFIED MODE BY KEMONG")
    #print("### MODE 2 = ORIGINAL MODE + UNFOLLOW WHO DON'T FOLLOW BACK")
    #print("#### MODE 3 = MODIFIED MODE : UNFOLLOW USERS WHO DON'T FOLLOW YOU BASED ON RECENT FEED")
    #print("##### MODE 4 = MODIFIED MODE : FOLLOW USERS BASED ON RECENT FEED ONLY")
    #print("###### MODE 5 = MODIFIED MODE : JUST UNFOLLOW EVERYBODY, EITHER YOUR FOLLOWER OR NOT")

    ################################
    ##  WARNING   ###
    ################################

    # DON'T USE MODE 5 FOR A LONG PERIOD. YOU RISK YOUR ACCOUNT FROM GETTING BANNED
    ## USE MODE 5 IN BURST MODE, USE IT TO UNFOLLOW PEOPLE AS MANY AS YOU WANT IN SHORT TIME PERIOD

    mode = process.env.mode

    #print("You choose mode : %i" %(mode))
    #print("CTRL + C to cancel this operation or wait 30 seconds to start")
    #time.sleep(30)

    if mode == 0:
        bot.new_auto_mod()

    elif mode == 1:
        check_status(bot)
        while bot.self_following - bot.self_follower > 200:
            unfollow_protocol(bot)
            time.sleep(10 * 60)
            check_status(bot)
        while bot.self_following - bot.self_follower < 400:
            while len(bot.user_info_list) < 50:
                feed_scanner(bot)
                time.sleep(5 * 60)
                follow_protocol(bot)
                time.sleep(10 * 60)
                check_status(bot)

    elif mode == 2:
        bot.bot_mode = 1
        bot.new_auto_mod()

    elif mode == 3:
        unfollow_protocol(bot)
        time.sleep(10 * 60)

    elif mode == 4:
        feed_scanner(bot)
        time.sleep(60)
        follow_protocol(bot)
        time.sleep(10 * 60)

    elif mode == 5:
        bot.bot_mode = 2
        unfollow_protocol(bot)

    else:
        print("Wrong mode!")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler,JobQueue
from telegram import Bot
from telegram.error import(BadRequest)
import logging
import cluster
import userbase

#TODO create propper config file!
TOKEN = "402118788:AAHiTndcgv3cTcP6eXUoAtYEHh7bhVJ31n4"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update): #TODO create a TEXTfile with all info texts
    """Starts and resets the bot"""

    update.message.reply_text("""Hi I'm your new DX Bot.\n
Use /add to add new callsigns\nUse /list to list all callsigns\nUse /rm to delete calls""")

    update.message.reply_text(userbase.create_user(update.effective_user.id))

def help(bot, update):
    """Prints out help message"""
    update.message.reply_text("Use:\n/start to reset\n/add to add CALLS\n/list to show all CALLS\n/rm to delete CALLS")

def error(bot, update, error):
    """Update error logger"""
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def addcall(bot, update):
    """Adds new call to callsign list"""
    newcall = userbase.add_call(update.effective_user.id, update.message.text.split(' ', 1)[1])
    update.message.reply_text(newcall)

def deletecall(bot, update):
    """Deletes an old call"""
    deletedcall = userbase.delete_call(update.effective_user.id, update.message.text.split(' ', 1)[1])
    update.message.reply_text(deletedcall)

def listcalls(bot,update):
    """Prints out all calls in users list"""
    update.message.reply_text(userbase.get_calls(update.effective_user.id))

#Passive Commands
def realcluster(bot, jobs):
    """Prints out the matched calls for each user"""
    chatids = userbase.get_all_chats_ids()
    for ids in chatids:
        try:
            bot.send_message(chat_id=ids, text=(cluster.user_cluster(ids)))
        except BadRequest:
            print("Nothing to send")
    cluster.reset_callsignlist()

def main():
    """Main methode, starts all jobs"""
    #Start DX Cluster in background
    cluster.clustersearch()

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)
    jobquere = JobQueue(Bot(TOKEN))
    
    #Register Cluster job
    jobquere.run_repeating(realcluster, 15, 0)
    jobquere.start()
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("add", addcall))
    dp.add_handler(CommandHandler("rm", deletecall))
    dp.add_handler(CommandHandler("list", listcalls))

    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    cluster.clustersearch()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from token import TOKEN

import cluster
import usercommands
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import CallbackQueryHandler, CommandHandler, JobQueue, Updater

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


def start(bot, update):  # TODO create a TEXTfile with all info texts
    """Starts and resets the bot"""

    update.message.reply_text(
        """Hi I'm your new DX Bot.\n
Use /add to add new callsigns\nUse /list to list all callsigns\nUse /rm to delete calls\nUse /adddx to add a new dxcc
Use /listdx to list a dxcc\nWARNING: DXCC feature is not working"""
    )

    update.message.reply_text(usercommands.create_user(update.effective_user.id))


def help(bot, update):
    """Prints out help message"""
    update.message.reply_text(
        "Use:\n/start to reset\n/add to add CALLS\n/list to show all CALLS\n/rm to delete CALLS"
    )


def error(bot, update, error):
    """Update error logger"""
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def menu(bot, update):
    keyboard = [
        [
            InlineKeyboardButton("Add a new Call", callback_data="newcall"),
            InlineKeyboardButton("List all Calls", callback_data="listcalls"),
            InlineKeyboardButton("Delete a Call", callback_data="deletecall"),
        ],
        [
            InlineKeyboardButton("Add a new DXCC", callback_data="newdxcc"),
            InlineKeyboardButton("List all DXCC", callback_data="listdxcc"),
            InlineKeyboardButton("Delete a DXCC", callback_data="deletedxcc"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Please choose: (You can press the Button but you cant type in commands after that :-( )",
        reply_markup=reply_markup,
    )


def button(bot, update):  # TODO fix actions
    """New type of menu for user Input"""
    query = update.callback_query
    choices = {
        "newcall": ("Please enter a valid callsign:", "TEST"),
        "listcalls": ("Here are all callsigns:", "TEST"),
        "deletecall": (
            "Please enter the callsign you want to delete from your list:",
            "TEST",
        ),
        "newdxcc": ("Please enter a valid country/dxcc:", "TEST"),
        "listdxcc": (
            "Here is a complete list of dxcc we are watching for you:",
            "TEST",
        ),
        "deletedxcc": (
            "Please enter a dxcc you want to delete from your list:",
            "TEST",
        ),
    }
    dxoption = choices.get(query.data, "ERROR")[0]
    bot.edit_message_text(
        text=dxoption,
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
    )


def addcall(bot, update):
    """Adds new call to callsign list"""
    newcall = usercommands.add_call(
        update.effective_user.id, update.message.text.split(" ", 1)[1]
    )
    update.message.reply_text(newcall)


def deletecall(bot, update):
    """Deletes an old call"""
    deletedcall = usercommands.delete_call(
        update.effective_user.id, update.message.text.split(" ", 1)[1]
    )
    update.message.reply_text(deletedcall)


def listcalls(bot, update):
    """Prints out all calls in users list"""
    update.message.reply_text(usercommands.get_calls(update.effective_user.id))


def adddxcc(bot, update):
    """Adds new dxcc to dxcc list"""
    new_dxcc = usercommands.add_dxcc(
        update.effective_user.id, update.message.text.split(" ", 1)[1]
    )
    update.message.reply_text(new_dxcc)


def listdxcc(bot, update):
    """Prints out all dxcc in users list"""
    update.message.reply_text(usercommands.get_dxcc(update.effective_user.id))


# Passive Commands
def realcluster(bot, jobs):  # TODO Check max messages per second
    """Prints out the matched calls for each user"""
    chatids = usercommands.get_all_chats_ids()
    for ids in chatids:
        try:
            bot.send_message(chat_id=ids, text=(cluster.user_cluster(ids)))
        except BadRequest:
            print("Nothing to send!")


def main():
    """Main methode, starts all jobs"""
    # Start DX Cluster in background
    cluster.clustersearch()

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)
    jobquere = JobQueue(Bot(TOKEN))

    # Register Cluster job
    jobquere.run_repeating(realcluster, 15, 0)
    jobquere.start()

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("menu", menu))

    # Call Commands
    dp.add_handler(CommandHandler("add", addcall))
    dp.add_handler(CommandHandler("rm", deletecall))
    dp.add_handler(CommandHandler("list", listcalls))

    # DXCC Commands
    dp.add_handler(CommandHandler("adddx", adddxcc))
    dp.add_handler(CommandHandler("listdx", listdxcc))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    cluster.clustersearch()


if __name__ == "__main__":
    main()

import logging
import os
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ---------------------------------------------------------------------------
# Facts. Add your own by adding more lines to this list.
# ---------------------------------------------------------------------------
FACTS = [
    "The fastest goal in World Cup history took just 11 seconds. Hakan Şükür scored it for Turkey against South Korea in 2002.",
    "Brazil is the only country that has played in every single World Cup. They have won it 5 times.",
    "Miroslav Klose of Germany is the all-time top scorer at the World Cup with 16 goals.",
    "Just Fontaine of France scored 13 goals at the 1958 World Cup. No one has scored more in a single tournament.",
    "The first World Cup was played in 1930 in Uruguay, and Uruguay won it.",
    "Pelé was only 17 when he won the World Cup in 1958, the youngest winner ever.",
    "Lionel Messi finally won the World Cup in 2022, when Argentina beat France on penalties after a 3-3 draw.",
    "The 2022 World Cup in Qatar was the first one held in the Middle East, and the first played in November and December.",
    "Cristiano Ronaldo became the first man to score at five different World Cups (2006, 2010, 2014, 2018 and 2022).",
    "Arsenal went a whole Premier League season without losing in 2003-04. Fans call them 'The Invincibles'.",
    "Real Madrid have won the European Cup / Champions League more times than any other club, including 5 in a row from 1956 to 1960.",
    "FIFA, the organisation that runs world football, was founded in 1904 in Paris.",
    "The real World Cup trophy is made of 18-carat gold and weighs about 6 kg.",
    "The penalty kick was invented in 1891. Before that, fouls near the goal had no special punishment.",
    "Yellow and red cards were first used at the 1970 World Cup. The idea came from referee Ken Aston, who thought of it at a traffic light.",
    "Lev Yashin of the Soviet Union is the only goalkeeper to ever win the Ballon d'Or, in 1963.",
    "The highest-scoring World Cup match ever was Austria 7-5 Switzerland in 1954. That is 12 goals!",
    "Hungary scored 10 goals against El Salvador at the 1982 World Cup, the most by one team in a single World Cup match.",
    "In the 1930 World Cup final, the two teams could not agree on a ball. Argentina's ball was used in the first half and Uruguay's in the second.",
    "In 1966 the World Cup trophy was stolen in England. A dog named Pickles found it wrapped in newspaper under a bush.",
    "The Ballon d'Or was first given in 1956, and the winner was Stanley Matthews of England.",
    "Lionel Messi has won the Ballon d'Or 8 times, more than any other player.",
    "A football goal is 7.32 metres wide and 2.44 metres tall.",
    "The word 'hat-trick' comes from cricket, not football. It was used when a bowler took three wickets in a row.",
    "The first Women's World Cup was played in 1991 in China, and the USA won it.",
    "Marta of Brazil is the top scorer in Women's World Cup history with 17 goals.",
    "Sheffield FC, started in 1857 in England, is recognised as the oldest football club in the world.",
    "Neymar's move to Paris Saint-Germain in 2017 cost 222 million euros, still the most expensive transfer ever.",
    "Pelé counted his 1,000th career goal in 1969. It was a penalty at the Maracanã stadium in Rio.",
    "Kylian Mbappé scored a hat-trick in the 2022 World Cup final, the first player to do it since Geoff Hurst in 1966.",
    "Penalty shootouts were first used at a World Cup in 1982, when West Germany beat France.",
    "Goal-line technology was first used at the World Cup in 2014 in Brazil.",
    "Erling Haaland scored 36 goals in the 2022-23 Premier League season, a record for a 38-game season.",
    "Leicester City won the Premier League in 2015-16 after starting the season at 5000-1 odds.",
    "Roger Milla of Cameroon scored at the 1994 World Cup at age 42, the oldest goalscorer in World Cup history.",
    "Morocco became the first African team to reach a World Cup semi-final, in 2022.",
    "Nigeria won the Olympic gold medal in men's football at the 1996 Games in Atlanta.",
    "A standard international football pitch is about 105 metres long and 68 metres wide.",
    "Goal-scoring legend Ferenc Puskás of Hungary scored 84 goals in 85 international matches.",
]

KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔄 Another fact", callback_data="fact:next")]]
)


def format_fact(text):
    return f"⚽ Did you know?\n\n{text}"


def next_fact(context):
    """Pick facts in random order and don't repeat until all have been seen."""
    queue = context.user_data.get("queue")
    last = context.user_data.get("last")
    if not queue:
        queue = list(range(len(FACTS)))
        random.shuffle(queue)
        if len(queue) > 1 and queue[0] == last:
            queue[0], queue[-1] = queue[-1], queue[0]
    idx = queue.pop(0)
    context.user_data["queue"] = queue
    context.user_data["last"] = idx
    return FACTS[idx]


HELP = (
    "⚽ Football Facts Bot\n\n"
    "Fun football facts, one tap at a time.\n\n"
    "/fact - get a random fact\n"
    "/help - show this message"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP)
    await update.message.reply_text(
        format_fact(next_fact(context)), reply_markup=KEYBOARD
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP)


async def fact_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        format_fact(next_fact(context)), reply_markup=KEYBOARD
    )


async def on_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        format_fact(next_fact(context)), reply_markup=KEYBOARD
    )


def main():
    token = os.environ["BOT_TOKEN"]
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("fact", fact_cmd))
    app.add_handler(CallbackQueryHandler(on_next, pattern=r"^fact:next$"))

    logging.info("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

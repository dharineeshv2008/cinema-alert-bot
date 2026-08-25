import asyncio
import random
import requests
from playwright.sync_api import sync_playwright
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

TOKEN = "8736978159:AAHXzdOoAE4O_F6n0229xgNNmpiBJ78vRCI"

users = {}
subscribers = set()

last_not_found_time = 0


# 🎬 SCRAPER
def get_movies():
    movies = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://karurcinemas.com")
            page.wait_for_timeout(5000)

            content = page.content().lower()

            if "toxic" in content:
                movies.append("Toxic")

            if "irumudi" in content:
                movies.append("Irumudi")

            browser.close()

    except:
        pass

    return movies


# 💺 SEAT GENERATOR
def generate_seats():
    rows = ["A", "B", "C"]
    seats = {}

    for r in rows:
        seats[r] = []
        for i in range(1, 11):
            if random.random() < 0.3:
                seats[r].append("X")
            else:
                seats[r].append(f"{r}{i}")

    return seats


# 🧠 BEST SEATS
def best_seats(seats):
    result = []
    for r in seats:
        available = [s for s in seats[r] if s != "X"]
        if available:
            result.append(available[len(available)//2])
    return result[:3]


# 🔔 AUTO ALERT LOOP
async def alert_loop(app):
    global last_not_found_time

    while True:
        movies = get_movies()

        # 🎬 FOUND
        if movies:
            msg = "🔥🎬 MOVIE FOUND 🎬🔥\n\n" + "\n".join(movies)

            for user in subscribers:
                await app.bot.send_message(chat_id=user, text=msg)

        # ❌ NOT FOUND (5 min once)
        else:
            now = asyncio.get_event_loop().time()
            if now - last_not_found_time > 300:
                for user in subscribers:
                    await app.bot.send_message(chat_id=user, text="❌ Movie Not Found")

                last_not_found_time = now

        await asyncio.sleep(60)  # check every 1 min


# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subscribers.add(chat_id)
    users[chat_id] = {}

    await update.message.reply_text("👋 Welcome!\nType 'hi' to start booking")


# 💬 CHATBOT FLOW
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    subscribers.add(chat_id)

    if chat_id not in users:
        users[chat_id] = {}

    user = users[chat_id]

    # 👋 START
    if text.lower() == "hi":
        user["step"] = "movie"

        movies = get_movies()
        if not movies:
            await update.message.reply_text("❌ No movies available")
            return

        keyboard = [[m] for m in movies]

        await update.message.reply_text(
            "🎬 Select Movie:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

    # 🎬 MOVIE
    elif user.get("step") == "movie":
        user["movie"] = text
        user["step"] = "seat"

        seats = generate_seats()
        user["seats"] = seats

        seat_map = ""
        for r in seats:
            seat_map += r + ": " + " ".join(seats[r]) + "\n"

        best = best_seats(seats)

        await update.message.reply_text(
            f"💺 Seat Map:\n{seat_map}\n\n⭐ Best: {', '.join(best)}\n\nEnter seat:"
        )

    # 💺 SEAT
    elif user.get("step") == "seat":
        chosen = text.upper()

        if any(chosen in row for row in user["seats"].values()):
            user["seat"] = chosen
            user["step"] = "confirm"

            await update.message.reply_text(
                f"🎟 Confirm Booking?\nMovie: {user['movie']}\nSeat: {chosen}\n\nYes/No"
            )
        else:
            await update.message.reply_text("❌ Seat not available")

    # ✅ CONFIRM
    elif user.get("step") == "confirm":
        if text.lower() == "yes":
            await update.message.reply_text("💳 Processing...")
            await update.message.reply_text("🎉 Booking Successful!")
        else:
            await update.message.reply_text("❌ Cancelled")

        users[chat_id] = {}


# ▶️ MAIN
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    # 🔔 Start background alert
    asyncio.create_task(alert_loop(app))

    print("🚀 Bot Running...")
    await app.run_polling()


# RUN
asyncio.run(main())
import random
from playwright.sync_api import sync_playwright
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

TOKEN = "8736978159:AAHXzdOoAE4O_F6n0229xgNNmpiBJ78vRCI"

users = {}

# 🎬 REAL SCRAPER USING PLAYWRIGHT
def get_movies_data():
    data = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://karurcinemas.com")

        page.wait_for_timeout(5000)  # wait for JS load

        content = page.content()

        # ⚠️ You MUST adjust selectors after inspecting site
        movies = page.query_selector_all("h3")

        for m in movies:
            name = m.inner_text().strip()

            # Fake screens + timings (until real selectors mapped)
            data[name] = {
                "Screen 1": ["10:00 AM", "1:00 PM"],
                "Screen 2": ["4:00 PM", "7:00 PM"]
            }

        browser.close()

    return data


# 💺 SEAT GENERATOR (AUTO DETECTION SIMULATION)
def generate_seats():
    rows = ["A", "B", "C", "D"]
    seats = {}

    for r in rows:
        seats[r] = []
        for i in range(1, 11):
            # randomly mark seats booked
            if random.random() < 0.3:
                seats[r].append("X")  # booked
            else:
                seats[r].append(f"{r}{i}")

    return seats


# 🧠 SMART BEST SEAT SUGGESTION
def suggest_best_seats(seats):
    best = []

    for row in seats:
        available = [s for s in seats[row] if s != "X"]

        # choose middle seats
        if len(available) >= 3:
            mid = len(available) // 2
            best.append(available[mid])

    return best[:3]


# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    users[chat_id] = {}

    await update.message.reply_text(
        "🎬 Welcome!\nType 'hi' to start booking"
    )


# 💬 MAIN FLOW
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    if chat_id not in users:
        users[chat_id] = {}

    user = users[chat_id]

    # 👋 START
    if text.lower() == "hi":
        user["step"] = "theatre"

        keyboard = [["Karur Cinemas"]]
        await update.message.reply_text(
            "🎭 Choose Theatre:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

    # 🎭 THEATRE
    elif text == "Karur Cinemas":
        user["data"] = get_movies_data()
        user["step"] = "movie"

        keyboard = [[m] for m in user["data"].keys()]

        await update.message.reply_text(
            "🎬 Select Movie:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

    # 🎬 MOVIE
    elif user.get("step") == "movie":
        user["movie"] = text
        user["step"] = "screen"

        screens = list(user["data"][text].keys())
        keyboard = [[s] for s in screens]

        await update.message.reply_text(
            "🎥 Choose Screen:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

    # 🎥 SCREEN
    elif user.get("step") == "screen":
        user["screen"] = text
        user["step"] = "time"

        times = user["data"][user["movie"]][text]
        keyboard = [[t] for t in times]

        await update.message.reply_text(
            "⏰ Choose Timing:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

    # ⏰ TIME
    elif user.get("step") == "time":
        user["time"] = text
        user["step"] = "seat"

        seats = generate_seats()
        user["seats"] = seats

        # show seat map
        seat_map = ""
        for row in seats:
            seat_map += row + " : " + " ".join(seats[row]) + "\n"

        best = suggest_best_seats(seats)

        await update.message.reply_text(
            f"💺 Seat Map:\n{seat_map}\n\n⭐ Best Seats: {', '.join(best)}\n\nEnter seat:"
        )

    # 💺 SEAT
    elif user.get("step") == "seat":
        chosen = text.upper()

        # check availability
        if any(chosen in seats for seats in user["seats"].values()):
            user["seat"] = chosen
            user["step"] = "confirm"

            await update.message.reply_text(
                f"🎟 Confirm Booking?\nMovie: {user['movie']}\nSeat: {chosen}\n\nYes / No"
            )
        else:
            await update.message.reply_text("❌ Seat not available")

    # ✅ CONFIRM
    elif user.get("step") == "confirm":
        if text.lower() == "yes":
            await update.message.reply_text("💳 Processing Payment...")
            await update.message.reply_text("🎉 Booking Successful!")
        else:
            await update.message.reply_text("❌ Cancelled")

        users[chat_id] = {}


# ▶️ RUN BOT
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("🚀 Bot Running...")
app.run_polling()
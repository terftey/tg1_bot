from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import random

# Your real bot token
BOT_TOKEN = "7942972350:AAEvdIsOUbeQYYrorNcRwL-XIWm-B2VrFWw"

# Your Telegram channel username
CHANNEL_USERNAME = "@Kingdomvtruthchannel"

# Bible verses for the guessing game
bible_verses = {
    "Waaqayyo jalqabatti bantiiwwan waaqaa fi lafa uume.": "Uma 1:1",
    "Waaqayyo, akkasitti tokkicha ilma isaa hamma kennuufitti biyya lafaa jaallate; kun immoo isatti kan amanu hundinuu jireenya bara baraa haa qabaatuuf malee, haa baduuf miti!.": "yoh 3:16",
    "Yeroo hundumaa gooftaatti gammadaa! Ammas irra deebi'ee nan jedha, gammadaa!": "Filp 4:4",
    "Waaqayyo tiksee koo ti, ani homaa hin dhabu!": "Far 23:1",
    "Garaa kee guutuu Waaqayyoon amanadhu, hubannaa ofii keetiitti hin hirkatin!": "Fak 3:5",
    "Waaqayyo, ayyaana Kristosiin qajeelotatti lakkaa'amnee, abdiidhaan jireenya bara baraa akka argannuuf kana nuuf godhe.": "Tit 3:7",
    "Foon koo, keessi namummaa koos yoo gad dhuman iyyuu, Waaqayyo garaa koo in jajjabeessa, bara baraanis qooda anaaf in ta'a.": "Far 73:26",
    "Aariin koo tiksoota irratti in boba'a, warra dura-buutotas nan adaba; ani Waaqayyo gooftaan maccaa hoolota koo namoota Yihudaatiif nan dhimma, akka farda lolaas isaan nan jabeessa;": "Zak 10:3",
    "Guyyaan Waaqayyoo dhi'aateeraatii Waaqayyo gooftaa duratti calluma jedhaa! Waaqayyo wanta aarsaa ta'u qopheesseera, warra waames qulqulleesseera.": "Sef 1:7",
    "Egaa amma firdiin, warra Kristos Yesusitti qabamanii jiraatanitti faradamu tokko illee hin jiru.": "Rom 8:1",
    "Kristos inni jireenya nuuf ta'e yommuu mul'atu isinis immoo isaa wajjin ulfinaan mul'achuuf jirtu.": "Qol 3:4",
    "Kana booddee Waaqayyo, 'Kottaa! Akka bifa keenyaatti, akka fakkaattii keenyaattis nama in umnaa! ...' jedhe.": "Uma 1:26",
    "Waaqayyo, 'Bishaanonni tuuta lubbuu qabaatanii munyuuqaniin haa guutan! ...' jedhe.": "Uma 1:20",
    "Amma immoo Waaqayyo, 'Lafti biqila haa baasu! ...' jedhe; innis akkasuma in ta'e.": "Uma 1:11",
    "bishaan isa ani kennuufiif jiru irraa inni dhugu garuu, bara baraan hin dheebotu...": "Yoh 4:14",
    "Dubartittiin immoo deebiftee, 'Masiihiin inni Kristos jedhamu akka dhufu anuu beeka...' jette.": "Yoh 4:25",
    "Jireenya amma biyya lafaa kana irra jiraannu duwwaadhaaf Kristosin abdanna erga ta'ee...": "1Qor 15:19",
    "inni awwaalameera, caaffanni qulqullaa'oon akka jedhanitti guyyaa sadaffaattis du'aa kaafameera.": "1Qor 15:4",
    "Bifa namicha isa biyya lafaa akka fudhanne akkasuma immoo bifa namicha isa waaqa irraa fudhachuuf jirra.": "1Qor 15:49",
    "Waa'ee boriifis hin yaadda'inaa...": "Mat 6:34",
    "Duraan dursitanii yaada keessan mootummaa Waaqayyoo fi qajeelummaa isaa barbaaduutti hidhaa!": "Mat 6:33",
    "Elsaa'in immoo deebisee, 'Warri nuu wajjin jiran, warra isaanii wajjin jiran irra in caaluutii hin sodaatin!' jedheen.": "2Mot 6:16",
    "Egaa Waaqayyo Abrahaamii fi hidda isaatiif abdii kenneera...": "Gal 3:16",
    "Kristos immoo nuuf jedhee abaaramaa ta'uudhaan, abaarsa isa seerichi nutti fidu jalaa nu fureera...": "Gal 3:13",
    "Waaqayyo warra saba isaa hin ta'in amantiidhaan qajeelota gochuuf akka jiru duraan dursee caaffata qulqullaa'aa keessatti dubbachiiseera...": "Gal 3:8",
    "Yeroo ofii jaallatettis warra saba isaa hin ta'in gidduutti isaa wangeela godhee akkan lallabuuf...": "Gal 1:16",
    "Yesus, 'Kana hundumaa dubbii haalaatiin isinitti dubbadheera...": "Yoh 16:25",
    "Isin waan na jaallattaniif, abbaa biraa dhufuu koos waan amantaniif...": "Yoh 16:27",
    "Gaafas isin maqaa kootiin in kadhattu...": "Yoh 16:26",
    "Ani dafee nan dhufa; namni tokko illee gonfoo mo'ichaa isa kan keetii si duraa akka hin fudhannetti...": "Mul 3:11",
    "Nuyi ijoollee Waaqayyoo erga taanee...": "Rom 8:17",
    "Nus isuma labsina; namni hundinuu karaa Kristos nama ga'aa ta'ee...": "Qol 1:28",
    "Kanaanis maqaan Waaqayyo isaaf kenne maqaa ergamootaa irra caalaa beekamaa...": "Ibr 1:4",
    "Itti fufees immoo, akka hin arginetti, gurra isaatiin akka hin dhageenyetti...": "Isa 6:10",
    "Kanaaf inni, 'Gara saba kanaa dhaqiitii...": "Isa 6:9",
    "Warra Waaqayyoof qulqullaa'an gargaaruuf...": "2Qor 8:4",
    "Isaan jaalaluma isaaniitiin hamma humna isaanii...": "2Qor 8:3",
    "Yaa obboloota nana, gochaa ayyaana Waaqayyoo isa waldoota Kristiyaanaa biyya Maqedooniyaatiif raawwatame akka beektan...": "2Qor 8:1",
    "Rakkinni, baay'isee yoo isaan qore iyyuu safara malee gammadanii...": "2Qor 8:2",
    "Yaa michoota ko! Abdii kana erga qabaannee...": "2Qor 7:1",
    "Egaa dhuguman si duratti faara tolaadhaan ilaalame yoon ta'e...": "Bau 33:13",
    "Ayyaanni gooftaa Yesus Kristos, jaalalli Waaqayyoo, tokkummaan hafuura qulqulluus hunduma keessanii wajjin haa ta'u!": "2Qor 13:13",
    "Ani karaa koo waanuman hojjedhuun nama hundumaa gammachiisuu nan yaala...": "1Qor 10:33",
    "Warra Yihudootaatti, warra Yihudoota hin ta'inittis yookiis waldaa kristiyaanaa Waaqayyootti gufuu hin ta'inaa!": "1Qor 10:32",
    "Ani ga'aa koo galateeffadhee yoon fudhadhe...": "1Qor 10:30",
    "Kunis yaada garaa isaa akka hin tuqneef malee...": "1Qor 10:29",
    "Namni tokko, 'Kun qalma aarsaadhaaf dhi'aatee dha' jedhee yoo isinitti hime...": "1Qor 10:28",
    "Namni hin amanne tokko mana isaatti nyaataaf yoo isin waame...": "1Qor 10:27"
}

# Memory to store user's current verse and points
current_verse = {}
user_points = {}

def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎯 Jalqabi", callback_data="play")],
        [
            InlineKeyboardButton("🏆 Dursitoota", callback_data="leaderboard"),
            InlineKeyboardButton("🎖️ Qabxii koo", callback_data="score"),
        ],
        [InlineKeyboardButton("🤝 Namaf Ergii", switch_inline_query="Join this Bible Game Bot!")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if user is a member
    if await is_user_member(context, user_id):
        await update.message.reply_text(
            "🙌 Welcome to the Bible Verse Guessing Game!\n\n"
            "📝 *Hubachisa: Deebii keef gabajee maqaa macaafa fayadami!* (fknf., 'Uma' for 'Uumama', 'Yoh' for 'Yohannis')\n\n"
            "Choose an option below 👇",
            reply_markup=main_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await prompt_join_channel(update)

async def prompt_join_channel(update: Update):
    join_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("👉 Join Channel", url="https://t.me/Kingdomvtruthchannel")],
        [InlineKeyboardButton("✅ I've Joined!", callback_data="check_join")]
    ])
    if update.message:
        await update.message.reply_text(
            "🚫 You must join [Kingdomvtruthchannel](https://t.me/Kingdomvtruthchannel) to play the Bible Game!",
            reply_markup=join_buttons,
            disable_web_page_preview=True,
            parse_mode='Markdown'
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            "🚫 You must join [Kingdomvtruthchannel](https://t.me/Kingdomvtruthchannel) to play the Bible Game!",
            reply_markup=join_buttons,
            disable_web_page_preview=True,
            parse_mode='Markdown'
        )

async def is_user_member(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    verse = random.choice(list(bible_verses.keys()))
    current_verse[user_id] = verse
    await update.callback_query.message.reply_text(f"📖 Guess the reference for this verse:\n\n\"{verse}\"")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_answer = update.message.text
    correct_answer = bible_verses.get(current_verse.get(user_id, ""), "")

    if correct_answer and correct_answer.lower() in user_answer.lower():
        user_points[user_id] = user_points.get(user_id, 0) + 1
        await update.message.reply_text(f"✅ Correct! You earned 1 point! 🎯", reply_markup=main_keyboard())
        current_verse.pop(user_id, None)
    else:
        await update.message.reply_text("❌ Not quite. Try again or pick a new verse!", reply_markup=main_keyboard())

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    points = user_points.get(user_id, 0)
    await update.callback_query.message.reply_text(f"🏆 You have {points} points!", reply_markup=main_keyboard())

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not user_points:
        await update.callback_query.message.reply_text("😢 No one has scored any points yet!", reply_markup=main_keyboard())
        return

    top_users = sorted(user_points.items(), key=lambda x: x[1], reverse=True)[:5]
    message = "👑 Top 5 Players:\n\n"
    for i, (user_id, points) in enumerate(top_users, start=1):
        try:
            user = await context.bot.get_chat(user_id)
            username = user.username if user.username else user.first_name
        except:
            username = "Unknown User"

        message += f"{i}. {username} — {points} points\n"

    await update.callback_query.message.reply_text(message, reply_markup=main_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    if data == "play":
        await play(update, context)
    elif data == "leaderboard":
        await leaderboard(update, context)
    elif data == "score":
        await score(update, context)
    elif data == "check_join":
        if await is_user_member(context, user_id):
            await query.message.reply_text(
                "🙌 Thanks for joining! Now you can play the Bible Game!",
                reply_markup=main_keyboard()
            )
        else:
            await query.message.reply_text(
                "❌ You're still not a member! Please join the channel first.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("👉 Join Channel", url="https://t.me/Kingdomvtruthchannel")],
                    [InlineKeyboardButton("✅ I've Joined!", callback_data="check_join")]
                ])
            )

# ADD HELP COMMAND
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 *How to Play:*\n\n"
        "1. Press 🎯 Play to get a Bible verse.\n"
        "2. Guess the correct book abbreviation and chapter:verse.\n"
        "   Example: 'Uma 1:1', 'Yoh 3:16', etc.\n"
        "3. Earn 1 point for every correct answer!\n\n"
        "📝 *Reminder:* Always use book abbreviations (e.g., Uma, Yoh, Far, Rom, etc.)\n\n"
        "Have fun! 🎉",
        parse_mode="Markdown"
    )

def main():
    app = ApplicationBuilder().token("7942972350:AAEvdIsOUbeQYYrorNcRwL-XIWm-B2VrFWw").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))  # Help command added
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()


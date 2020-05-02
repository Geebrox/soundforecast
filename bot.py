# import config which contains API tokens
import config

# import yahoo weather forecast API handler
from yahoo_weather.weather import YahooWeather
from yahoo_weather.config.units import Unit

# import telegram bot framework
import telebot
from telebot import types
from telebot.types import Message

# import classes from another files to easier handle operations
from users import Users, User
from sounds import Sounds

# Setup weather API handler with configs from config file
weatherHandler = YahooWeather(
    APP_ID=config.WEATHER_APP_ID,
    api_key=config.WEATHER_CONSUMER_KEY,
    api_secret=config.WEATHER_CONSUMER_SECRET)

# Connect to a telegram bot with the telegram bot framework
bot = telebot.TeleBot(config.TOKEN)

# Function that sends error message to the chat
def sendErrMessage(chat_id, message):
    bot.send_message(
        chat_id,
        "<b>Oops!</b>\n\n" + message,
        parse_mode="html")

# Create Users and Sound objects
users = Users()
sounds = Sounds()

# Function that gets forecast for user with id and sends information to chat with chat id
# If user is not found insdie of Users object it adds user to object and requires to type city
def getForecastForUser(user_id, chat_id):
    user = users.findUserById(user_id)
    if user == None:
        userTemp = User(user_id, True)
        users.addUser(userTemp)
        sendErrMessage(
            chat_id,
            "I don't know your city. Please, message me your <b>city</>:")
    else:
        weatherHandler.get_yahoo_weather_by_city(user.location, Unit.celsius)
        try:
            bot.send_message(
                chat_id, "Currently in " + user.location + ": \n"
                + "The condition is <b>" + weatherHandler.condition.text + "</b>\n"
                + "The temperature is <b>" + str(weatherHandler.condition.temperature) + "°C</b>", parse_mode='html')
            bot.send_audio(
                chat_id,
                audio=open(sounds.getSoundForCondition(
                    weatherHandler.condition.code), 'rb'),
                title=' ')
        except Exception:
            users.setUser(user.id, "", True)
            sendErrMessage(
                chat_id,
                "Something went wrong. Seems you mistyped your <b>city</>. Maybe try again?")


#Listen for /start command of the bot and create UI buttons in telegram
#Greet the user with username and send message
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(types.KeyboardButton("Weather forecast"))
    markup.row(types.KeyboardButton("Random sound"))
    markup.row(types.KeyboardButton("Change my city"))

    bot.send_message(
        message.chat.id, "Hello, " + message.from_user.first_name + ". Choose the action:", reply_markup=markup)


#Listen for any text messages that user sends to the bot
#Check if user clicked UI buttons and preform specific actions
#If user typed something that is not familiar to the bot -> send information message
@bot.message_handler(content_types=['text'])
def answer(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text == 'Weather forecast':
        getForecastForUser(user_id, chat_id)
    elif message.text == 'Random sound':
        bot.send_audio(
            chat_id,
            audio=open(sounds.getRandomSound(), 'rb'),
            title=' ',
            reply_to_message_id=message.message_id)
    elif message.text == 'Change my city':
        bot.send_message(
            chat_id, "No problem, just type me your <b>city</b>:", parse_mode="html")
        user = users.findUserById(user_id)
        if user != None:
            users.setUser(user.id, "", True)
            return
        userTemp = User(user_id, True)
        users.addUser(userTemp)

    else:
        user = users.findUserById(user_id)
        if user != None:
            if user.asked_for_location == True:
                users.setUser(user.id, message.text, False)
                bot.send_message(
                    chat_id, "Alright! I saved your city!")
                getForecastForUser(user_id, chat_id)
                return
        sendErrMessage(
            chat_id,
            "I didn't understand you. Maybe you will use my commands?")

#Launch the bot and listen for new message from users
bot.polling(none_stop=True, interval=1, timeout=30)

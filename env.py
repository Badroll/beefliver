sha256_addon_key = "2_)^EPD-l6TD"
app_secret_key = ",%PcRxaPc#-z"
api_key_public_route = "c%SCV$}hRKuH"
telebot_token = "6353387757:AAHarFsMOrHwVg__9dGiEVOnal7_PGpPbuU"
tele_chat_id_me = "751219891"
tele_chat_id_bdmsth_logger_pakdhe = "-4085393710"
tele_chat_id_bdmsth_logger_wablas_hooks = "-4011133592"
wabot = [
    {
        "wabot_1_token" : "CrrwBDFIcUzhyzh1RqfpR9M7Oo3MnCVf3aTRhauidFUdijprYzwePFm81LbHSkJm",
        "wabot_1_no" : "6285173205090"
    }
]
development = "local"
if development == "local":
    runHost = "0.0.0.0"
    runDebug = True
    runPort = 5007
    dbHost = "localhost"
    dbUser = "root"
    dbPassword = ""
    dbDatabase = "kmsbalita"
if development == "vps":
    runHost = "0.0.0.0"
    runDebug = False
    runPort = 5007
    dbHost = "localhost"
    dbUser = "user_1"
    dbPassword = "mySQLuser_1"
    dbDatabase = "kmsbalita"
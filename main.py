import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# Responder mensajes
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text.lower()

    if "hola" in mensaje:
        await update.message.reply_text(
            "💇 ¡Hola! Soy tu asistente del salón."
        )
    else:
        await update.message.reply_text(
            f"Recibí tu mensaje: {mensaje}"
        )

# Iniciar el bot
def main():
    token = os.getenv("TOKEN")

    app = Application.builder().token(token).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, responder)
    )

    print("Bot iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()

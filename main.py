import os
from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# Memoria simple (por ahora en RAM)
ventas = []
gastos = []

def extraer_monto(texto):
    numeros = ''.join(c for c in texto if c.isdigit())
    return int(numeros) if numeros else 0

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ventas, gastos

    mensaje = update.message.text.lower()
    monto = extraer_monto(mensaje)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 💰 VENTAS
    if any(x in mensaje for x in ["corte", "balayage", "tintura", "manicure", "pedicure", "venta"]):
        ventas.append({"texto": mensaje, "monto": monto, "fecha": fecha})

        await update.message.reply_text(
            f"💰 Venta registrada\nMonto: ${monto}\n📅 {fecha}"
        )
        return

    # 💸 GASTOS
    if any(x in mensaje for x in ["compré", "compre", "gasté", "gaste", "pagué", "pague"]):
        gastos.append({"texto": mensaje, "monto": monto, "fecha": fecha})

        await update.message.reply_text(
            f"💸 Gasto registrado\nMonto: ${monto}\n📅 {fecha}"
        )
        return

    # 📊 RESUMEN
    if "resumen" in mensaje:
        total_ventas = sum(v["monto"] for v in ventas)
        total_gastos = sum(g["monto"] for g in gastos)
        ganancia = total_ventas - total_gastos

        await update.message.reply_text(
            f"📊 RESUMEN\n"
            f"💰 Ventas: ${total_ventas}\n"
            f"💸 Gastos: ${total_gastos}\n"
            f"📈 Ganancia: ${ganancia}"
        )
        return

    # 🧴 INVENTARIO (simple por ahora)
    if "stock" in mensaje:
        await update.message.reply_text("🧴 Inventario en desarrollo (próximo paso)")
        return

    await update.message.reply_text(
        "💇 No entendí\nEscribe por ejemplo:\n- Corte varón 7000\n- Compré shampoo 13000\n- Resumen"
    )


def main():
    token = os.getenv("TOKEN")

    app = Application.builder().token(token).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("Bot iniciado...")
    app.run_polling()


if __name__ == "__main__":
    main()

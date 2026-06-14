import os
import re
from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from supabase import create_client

# 🔐 Conexión Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🧠 extraer monto de cualquier texto
def extraer_monto(texto):
    numeros = re.findall(r'\d+', texto)
    return int(numeros[0]) if numeros else 0


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text.lower()
    monto = extraer_monto(mensaje)
    fecha = datetime.now().isoformat()

    # 💰 VENTAS
    if any(p in mensaje for p in [
        "corte", "balayage", "tintura", "manicure", "pedicure", "venta"
    ]):
        supabase.table("ventas").insert({
            "texto": mensaje,
            "monto": monto,
            "fecha": fecha
        }).execute()

        await update.message.reply_text(f"💰 Venta registrada: ${monto}")
        return

    # 💸 GASTOS
    elif any(p in mensaje for p in [
        "compré", "compre", "gasté", "gaste", "pagué", "pague",
        "shampoo", "insumo", "esmalte", "tinte"
    ]):
        supabase.table("gastos").insert({
            "texto": mensaje,
            "monto": monto,
            "fecha": fecha
        }).execute()

        await update.message.reply_text(f"💸 Gasto registrado: ${monto}")
        return

    # 📊 RESUMEN
    if "resumen" in mensaje:
        ventas = supabase.table("ventas").select("*").execute().data
        gastos = supabase.table("gastos").select("*").execute().data

        total_ventas = sum(v["monto"] for v in ventas)
        total_gastos = sum(g["monto"] for g in gastos)
        ganancia = total_ventas - total_gastos

        await update.message.reply_text(
            f"📊 RESUMEN GENERAL\n\n"
            f"💰 Ventas: ${total_ventas}\n"
            f"💸 Gastos: ${total_gastos}\n"
            f"📈 Ganancia: ${ganancia}"
        )
        return

    # 💡 MENSAJE DE AYUDA
    await update.message.reply_text(
        "💇 COMANDOS DEL SALÓN\n\n"
        "💰 Venta: Corte varón 7000\n"
        "💸 Gasto: Compré shampoo 13000\n"
        "📊 Resumen"
    )


def main():
    token = os.getenv("TOKEN")

    if not token:
        print("❌ Falta TOKEN")
        return

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Falta Supabase config")
        return

    app = Application.builder().token(token).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, responder)
    )

    print("💇 Bot del salón activo...")
    app.run_polling()


if __name__ == "__main__":
    main()

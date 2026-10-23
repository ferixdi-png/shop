# Ferixdi AI Shop

Telegram shop bot with a compact product catalog, full descriptions behind a "Подробнее" button, SBP payment instructions, and a handoff to @ferixdiii for receipt submission and manual fulfillment.

## Deploy on Render Free

This project runs as a **Web Service** using Telegram webhooks, so it can use Render's free Web Service plan instead of a paid Background Worker.

1. Create a Telegram bot via [@BotFather](https://t.me/BotFather) with `/newbot`.
2. In Render, open the existing Web Service connected to this repository, or create a new one with **Web Service** and plan **Free**.
3. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
4. Add the secret environment variable `BOT_TOKEN` from BotFather. Never commit the token to GitHub.
5. Render automatically provides `RENDER_EXTERNAL_URL` and `PORT`; the app registers the Telegram webhook on startup.
6. Optional: set `WEBHOOK_SECRET` to a long random value. If omitted, the app generates a secret at startup.
7. Deploy, then open the bot in Telegram and send `/start`.

The service exposes `/` and `/health` for health checks. An external uptime monitor can request `https://YOUR-SERVICE.onrender.com/health` periodically. Render's free web services can sleep after inactivity, so a monitor may reduce sleeping but does not guarantee uninterrupted operation or instant responses.

## Configuration

- `BOT_TOKEN` — required secret from BotFather.
- `WEBHOOK_SECRET` — optional secret for validating incoming Telegram webhook requests; generated on startup if omitted.
- `RENDER_EXTERNAL_URL` — supplied automatically by Render.
- `PORT` — supplied automatically by Render.
- `ADMIN_USERNAME` — Telegram username receiving order messages; default `ferixdiii`.
- `PAYMENT_PHONE` — SBP phone; default `+79935801642`.
- `PAYMENT_BANK` — default `Яндекс Банк`.
- `PAYMENT_NAME` — default `Дмитрий`.

The bot does not verify bank transfers automatically. Buyers send their receipt to the seller, who checks the actual incoming payment and fulfills the order manually. Clicking the payment-confirmation button is not proof of payment.

## Products

All four product descriptions are included in `main.py`; the catalog shows compact summaries and displays full descriptions on request. Product images are intentionally omitted so every item uses the same clean text-card layout.

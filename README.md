# Ferixdi AI Shop

Telegram shop bot with a compact product catalog, full descriptions behind a "Подробнее" button, SBP payment instructions, and a handoff to @ferixdiii for receipt submission and manual fulfillment.

## Deploy on Render

1. Create a Telegram bot via [@BotFather](https://t.me/BotFather) with `/newbot`.
2. Copy the bot token privately.
3. In Render, choose **New + → Blueprint** and connect this repository: https://github.com/ferixdi-png/shop
4. Render reads `render.yaml` and creates a Python Background Worker.
5. Add the secret environment variable `BOT_TOKEN` to the service in Render. Do not commit the token to GitHub.
6. Deploy and open the bot in Telegram, then send `/start`.

## Configuration

- `BOT_TOKEN` — required secret from BotFather.
- `ADMIN_USERNAME` — Telegram username receiving order messages; default `ferixdiii`.
- `PAYMENT_PHONE` — SBP phone; default `+79935801642`.
- `PAYMENT_BANK` — default `Яндекс Банк`.
- `PAYMENT_NAME` — default `Дмитрий`.

The bot does not verify bank transfers automatically. Buyers send their receipt to the seller, who checks the actual incoming payment and fulfills the order manually. Clicking the payment-confirmation button is not proof of payment.

## Products

All four product descriptions are included in `main.py`; the catalog shows compact summaries and displays full descriptions on request. Product images are intentionally omitted so every item uses the same clean text-card layout.

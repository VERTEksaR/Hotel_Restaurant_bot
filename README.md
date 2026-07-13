# Telegram Bot: Hotel & Restaurant Search

## Overview

A Telegram bot that lets users search for hotels and restaurants in cities worldwide. All data is retrieved via the TripAdvisor API (through RapidAPI).

Built with `aiogram`, using a finite state machine (FSM) to manage multi-step user interactions, with persistent request history stored in a database.

## Setup

1. Get a bot token from [BotFather](https://telegram.me/BotFather).
2. Register on [RapidAPI](https://rapidapi.com/hub), search for `Travel Advisor`, and subscribe to a pricing plan.
3. Retrieve your API key from the RapidAPI dashboard (`Apps` → `My Apps` → Authorization).
4. Add your bot token and API key to `.env.template`.

## Features

- `/start` — initialize the bot
- `/help` — list all available commands
- `/low` — search results sorted by lowest price (hotels) or budget-friendly cuisine (restaurants)
- `/high` — search results sorted by popularity (hotels) or high-end cuisine (restaurants)
- `/custom` — user-defined sorting criteria
- `/history` — view the last 10 search requests

## Tech Stack

Python · aiogram · RapidAPI (TripAdvisor) · FSM (Finite State Machine)

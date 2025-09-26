from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from loguru import logger

from app.sheets_client import sheets_client

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.first_name or "User"

    logger.info(f" /start from user {username} (ID: {user_id})")
    #just for now without checking id in list

    if sheets_client.check_user_exists_in_sheets(user_id):
        client_id = sheets_client.get_user_from_sheets(user_id)
        await message.answer(f"Welcome back {username} 👋 Your account is already linked.\n"
                             f"You can type /stats anytime to see your report",
                             parse_mode="Markdown")
    else:
        await message.answer("Hi 👋 Welcome to your PostAd Dashboard.\n"
                             "Please enter your dashboard code to continue",
                             parse_mode="Markdown")



@router.message(F.text.regexp(r'^\d{6,8}$'))
async def process_dash_code(message: Message):
    user_id = message.from_user.id
    username = message.from_user.first_name or "User"
    telegram_username = message.from_user.first_name
    dash_code = message.text.strip()

    logger.info(f'{telegram_username} entered code: {dash_code}')

    checking_msg = await message.answer("Checking your code...")


    #logic for checking
    if sheets_client.check_dash_code_exists(dash_code):

        # checking if user is registered
        if sheets_client.check_user_exists_in_sheets(user_id):
            await checking_msg.edit_text(
                f"❌ Your Telegram account is already linked to the dashboard code.\n\n"
                f"Please contact support at support@postad.io if you need help.",
                parse_mode="Markdown"
            )
            return

        existing_users = sheets_client.get_users_sheet()
        if existing_users:
            records = existing_users.get_all_records()
            for record in records:
                existing_client_id = record.get('client_id') or record.get("Client ID") #depends on google sheets column name
                if existing_client_id and str(existing_client_id) == str(dash_code):
                    await message.answer(f"❌ This company code is already registered by another user.\n\n"
                                         f"Please contact support at support@postad.io to receive your dashboard code.",
                                         parse_mode="Markdown")
                    return


        #saving telegram_id
        success = sheets_client.save_user_to_sheets(
            client_id=int(dash_code),
            telegram_id=user_id,
            first_name=username,
            username=telegram_username
        )

        if success:
            await checking_msg.edit_text(
                f"Thanks {username}! ✅ Your account has been linked!\n"
                f"From now on, just type /stats to see your campaign report.",
                parse_mode="Markdown"
            )
            logger.info(f"{username} confirmed with code {dash_code}")

        else:
            await message.answer(f"Code {dash_code} confirmed but failed to save user data\n"
                                 f"Please contact support at support@example.com to receive your dashboard code.",
                                 parse_mode="Markdown")

    else:
        await message.answer(f"❌ Your account is not found or not active.\n\n"
                             f"Please contact support at support@example.com to receive your dashboard code.",
                             parse_mode="Markdown")



@router.message()
async def unknown_message(message : Message):
    await message.answer(
        "Unkwown command."
    )

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from loguru import logger
import re

from app.sheets_client import sheets_client

router = Router()

@router.message(Command("stats"))
async def stats_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.first_name or 'User'

    logger.info(f'/stats for {username}')

    if not sheets_client.check_user_exists_in_sheets(user_id):
        await message.answer(f"You are not authorized\n"
                             f"Please use /start and enter your dashboard code first",
                             parse_mode="Markdown")
        return

    dash_code  = sheets_client.get_user_from_sheets(user_id)

    if not dash_code:
        await message.answer(f"No campaign found for code {dash_code}")
        return

    campaigns = sheets_client.get_campaigns_by_code(str(dash_code))

    if not campaigns:
        await message.answer(f"No campaigns found for code {dash_code}")
        return

    company_name = campaigns[0].get('Company Name')

    response = (f"Statistics for code: {company_name}\n"
                f"━━━━━━━━━━━━━━━\n\n")

    total_cost = 0
    total_views = 0
    #for each campaign sending info
    for i, campaign in enumerate(campaigns, 1):
        cost_str = str(campaign.get('Cost', '0'))
        views_str = str(campaign.get('Views', '0'))

        #cleaning cost (without currency)
        views_clean = re.sub(r'[^\d]', '', str(views_str))

        cost_str_clean = str(cost_str).replace("₪", "").strip()
        cost_clean = cost_str_clean.replace(",", "")

        try:
            cost = float(cost_clean) if cost_clean else 0
            views = int(views_clean) if views_clean else 0
            total_cost += cost
            total_views += views

        except ValueError:
            cost = 0
            views = 0


        response += f"📊 Campaign Report — {campaign.get('Campaign ID', 'N/A')}\n"
        response += f"🟢 {campaign.get('Company Name', 'N/A')}\n"
        response += f"👀 Views: {views:,}\n"
        response += f"💰 Cost: ₪{cost:,.2f}\n"
        response += f"📉 CPM: {(campaign.get('CPM', '0'))}\n"
        response += f"📅 {campaign.get('Date', 'N/A')}\n"

        campaign_url = campaign.get('Campaign URL', '#')
        response += f"🔗 [View campaign]({campaign_url})\n\n"

    avg_cpm = (total_cost / total_views * 1000 if total_views > 0 else 0)

    # summary at the bottom
    response += f"━━━━━━━━━━━━━━━\n"
    response += f"📈 Totals:\n"
    response += f"👀 Total Views: {total_views:,}\n"
    response += f"💰 Total Cost: ₪{total_cost:,.2f}\n"
    response += f"📉 Avg CPM: ₪{avg_cpm:.2f}\n\n"

    await message.answer(response, parse_mode="Markdown")
    logger.info(f"Stats sent to {username} for code {dash_code}")














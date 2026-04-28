import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# --- CẤU HÌNH WEB SERVER (ĐỂ TREO RENDER) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    # Render tự động cấp PORT qua biến môi trường
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# --- CẤU HÌNH BOT ---
# API Token mới bạn vừa cung cấp
TOKEN = '8762273971:AAHeaVFTiwGt_hVqRkQxQwH-WhasAU0UdWM'
LINK_VUOT = 'https://link4m.com/RJLsgj7'
ADMIN_VIP = '@bankaovippro' 

bot = telebot.TeleBot(TOKEN)

def get_main_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("✨ LẤY ACC FREE", callback_data='get_free')
    btn2 = types.InlineKeyboardButton("👑 MUA KEY VIP", callback_data='show_price')
    btn3 = types.InlineKeyboardButton("💬 HỖ TRỢ", url=f"https://t.me/bankaovippro")
    btn4 = types.InlineKeyboardButton("💎 ĐẶC QUYỀN", callback_data='perks')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

@bot.message_handler(commands=['start', 'menu'])
def main_menu(message):
    welcome_text = (
        "👑 <b>WELCOME TO PREMIUM SYSTEM</b> 👑\n"
        "<i>Hệ thống phân phối tài khoản - Admin Khôingu</i>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👤 <b>KHÁCH HÀNG:</b> <code>{name}</code>\n"
        "🆔 <b>MÃ ĐỊNH DANH:</b> <code>{user_id}</code>\n"
        "📊 <b>TRẠNG THÁI:</b> 🟢 <i>Normal Member</i>\n\n"
        "✨ <b>DỊCH VỤ MIỄN PHÍ:</b>\n"
        "👉 Vượt link để lấy trực tiếp Tài khoản & Mật khẩu.\n\n"
        "💎 <b>DỊCH VỤ PREMIUM:</b>\n"
        "👉 Nhận Acc ngay lập tức, không quảng cáo, không chờ đợi.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "💳 <b>Mua VIP liên hệ duy nhất tại:</b> {admin}\n"
        "👇 <b>BẤM CHỌN DỊCH VỤ DƯỚI ĐÂY:</b>"
    ).format(
        name=message.from_user.first_name,
        user_id=message.from_user.id, 
        admin=ADMIN_VIP
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='HTML', reply_markup=get_main_markup())

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "get_free":
        free_text = (
            "🚀 <b>CỔNG NHẬN ACC MIỄN PHÍ</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Hệ thống đang chuẩn bị tài khoản cho bạn...\n\n"
            "🔗 <b>Vui lòng vượt link để nhận dữ liệu:</b>\n"
            "👉 <pre>{link}</pre>\n\n"
            "⚠️ <i>Lưu ý: Sau khi hoàn thành các bước, tài khoản/mật khẩu sẽ hiện ra tại trang cuối web.</i>"
        ).format(link=LINK_VUOT)
        
        back_markup = types.InlineKeyboardMarkup()
        btn_link = types.InlineKeyboardButton("🔗 NHẤN ĐỂ VƯỢT LINK", url=LINK_VUOT)
        btn_back = types.InlineKeyboardButton("⬅️ QUAY LẠI MENU", callback_data='back_to_menu')
        back_markup.add(btn_link)
        back_markup.add(btn_back)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=free_text,
            parse_mode='HTML',
            reply_markup=back_markup,
            disable_web_page_preview=True
        )

    elif call.data == "show_price":
        price_text = (
            "👑 <b>BẢNG GIÁ ĐẶC QUYỀN VIP</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🗓 <b>1 NGÀY:</b>  <code>30.000 VNĐ</code>\n"
            "🗓 <b>7 NGÀY:</b>  <code>60.000 VNĐ</code>\n"
            "🗓 <b>30 NGÀY:</b> <code>150.000 VNĐ</code>\n"
            "♾ <b>VĨNH VIỄN:</b> <code>280.000 VNĐ</code>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🚀 <i>Đặc quyền: Không vượt link - Nhận acc VIP cực nhanh!</i>\n\n"
            f"📩 <b>Liên hệ ngay:</b> {ADMIN_VIP}"
        )
        
        premium_markup = types.InlineKeyboardMarkup()
        premium_markup.add(types.InlineKeyboardButton("👨‍💻 NHẮN TIN MUA VIP", url="https://t.me/bankaovippro"))
        premium_markup.add(types.InlineKeyboardButton("⬅️ QUAY LẠI", callback_data='back_to_menu'))

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=price_text,
            parse_mode='HTML',
            reply_markup=premium_markup
        )

    elif call.data == "perks":
        bot.answer_callback_query(call.id, "Đặc quyền VIP: Không link, Acc ngon, Hỗ trợ 24/7!", show_alert=True)

    elif call.data == "back_to_menu":
        welcome_text = (
            "👑 <b>PREMIUM SYSTEM - ADMIN HUÂN</b> 👑\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "👤 <b>KHÁCH HÀNG:</b> <code>{name}</code>\n"
            "📊 <b>TRẠNG THÁI:</b> 🟢 <i>Normal Member</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "👇 <b>VUI LÒNG CHỌN DỊCH VỤ:</b>"
        ).format(name=call.from_user.first_name)
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=welcome_text,
            parse_mode='HTML',
            reply_markup=get_main_markup()
        )

# Khởi chạy song song cả Web Server và Bot
if __name__ == "__main__":
    keep_alive() 
    print("--- BOT HUÂN ĐANG KHỞI CHẠY ---")
    bot.remove_webhook()
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

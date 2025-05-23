import streamlit as st
from datetime import datetime, timedelta
import random

class User:
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email
        self.balance = 500
        self.bots = []

class BotPlan:
    def __init__(self, name, duration_days, price):
        self.name = name
        self.duration = duration_days
        self.price = price

class TradingBot:
    def __init__(self, user_id, plan: BotPlan, trade_amount):
        self.user_id = user_id
        self.plan = plan
        self.trade_amount = trade_amount
        self.start_date = datetime.now()
        self.end_date = self.start_date + timedelta(days=plan.duration)
        self.total_profit = 0
        self.daily_profits = []
        self.active = True

    def calculate_daily_profit(self):
        if not self.active:
            return 0
        if datetime.now() > self.end_date:
            self.active = False
            return 0
        daily_rate = random.uniform(0.027, 0.032)
        daily_profit = self.trade_amount * daily_rate
        self.total_profit += daily_profit
        self.daily_profits.append(daily_profit)
        return daily_profit

plans = {
    'Bronze': BotPlan('Bronze', 7, 5),
    'Silver': BotPlan('Silver', 15, 10),
    'Gold': BotPlan('Gold', 30, 15)
}

st.title("منصة استثمار كريبتو روبوتية")
st.write("اختر خطة، حدّد مبلغ التداول، وانطلق!")

user = User(1, "user@example.com")

plan_name = st.selectbox("اختر الخطة", list(plans.keys()))
trade_amount = st.number_input("مبلغ التداول (USDT)", min_value=10, value=200)
selected_plan = plans[plan_name]

if st.button("شراء روبوت"):
    if user.balance >= selected_plan.price:
        user.balance -= selected_plan.price
        bot = TradingBot(user.user_id, selected_plan, trade_amount)
        user.bots.append(bot)
        st.success(f"تم شراء روبوت {plan_name}!")
    else:
        st.error("الرصيد غير كافٍ لشراء الروبوت.")

for i, bot in enumerate(user.bots):
    st.subheader(f"روبوت #{i+1} ({bot.plan.name})")
    if st.button(f"حساب ربح يومي لروبوت #{i+1}"):
        profit = bot.calculate_daily_profit()
        st.write(f"ربح اليوم: {profit:.2f} USDT")
        st.write(f"الربح الكلي: {bot.total_profit:.2f} USDT")
    st.write(f"نشط: {'نعم' if bot.active else 'لا'}")

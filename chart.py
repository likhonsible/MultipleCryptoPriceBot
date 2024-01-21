import requests
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import os
from PIL import Image
from pathlib import Path
from datetime import datetime, timedelta
bot = "jbdac"
types = "luldeep"


def save_chart(coin,days,currency):
    url = f'https://api.coingecko.com/api/v3/coins/{coin}/ohlc?vs_currency={currency}&days={days}'  # Fetch data for the past 7 days
    if coin == "binaryx-2":
        symbol = "BNX"
    elif coin == "cyberdragon-gold":
        symbol = "GOLD"
    

    data = requests.get(url).json()
    for da in data:
        dt_object = datetime.utcfromtimestamp(da[0] / 1000)
        da[0] = dt_object.strftime("%Y-%m-%d %H:%M:%S")

    df = pd.DataFrame(
        {
            'time': [i[0] for i in data],
            'open': [i[1] for i in data],
            'high': [i[2] for i in data],
            'low': [i[3] for i in data],
            'close': [i[4] for i in data],
        }
    )

    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    if not os.path.exists("img"):
        os.mkdir("img")

    with Image.open("img/background2.png") as bg_image:
        fig, ax = plt.subplots(figsize=(16, 9))  # Adjust the figure size for a wider time range
        
        mpf.plot(df, type='candle', ax=ax, style='yahoo', datetime_format='%m-%d\n%H:%M')

        ax.set_title(f'{symbol}/{currency} Price Chart (Past {days} Days)', color='#f3f5f4', fontsize=32)
        ax.set_xlabel('Time', color='#f3f5f4', fontsize=24)
        ax.set_ylabel(f'Price ({currency})', color='#f3f5f4', fontsize=24)
        
        ax.tick_params(axis='x', colors='#f3f5f4',labelsize=20)
        ax.tick_params(axis='y', colors='#f3f5f4',labelsize=20)
        ax.spines['left'].set_color('#727886')
        ax.spines['left'].set_linewidth(2)
        ax.spines['bottom'].set_color('#727886')
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['right'].set_color('#727886')
        ax.spines['right'].set_linewidth(2)
        ax.spines['top'].set_color('#727886')
        ax.spines['top'].set_linewidth(2)
        
        current_price = df['close'].iloc[-1]
        ax.axhline(y=current_price, color='red', linestyle='--', label='Current Price')
        # ax.set_yticks(ax.get_yticks().tolist() + [current_price])
        
        # ax.yaxis.set_major_locator(FixedLocator([current_price]))
        
        min_price = df['low'].min()
        max_price = df['high'].max()
        tick_step = (max_price - min_price) / 6  # Set the number of desired ticks (e.g., 5 here)
        y_ticks = [min_price + tick_step * i for i in range(7)]
        distances = [abs(y_tick - current_price) for y_tick in y_ticks]
        
        # Exclude the y-axis tick closest to the current price
        y_ticks = [y_tick for y_tick, distance in zip(y_ticks, distances) if distance != min(distances)]
        ax.set_yticks(y_ticks + [current_price])
        ax.set_facecolor('#181d33')
        tick_labels = ax.get_yticklabels()
        tick_labels[-1].set_color('red')
        ax.set_yticklabels(tick_labels)
        
        fig.patch.set_facecolor('#181d33')
        fig.figimage(bg_image, xo=0, yo=0, alpha=0.1)
        plt.legend()
        plt.tight_layout(pad=4.0)
        image_path = "img/chart.png"
        plt.savefig(image_path)
        
    return image_path


# def save_chart(coin,days,currency):
#     url = f'https://api.coingecko.com/api/v3/coins/{coin}/ohlc?vs_currency={currency}&days={days}'
#     if coin == "binaryx-2":
#         symbol = "BNX"
#     elif coin == "cyberdragon-gold":
#         symbol = "GOLD"
    
#     data = requests.get(url).json()
#     for da in data:
#         dt_object = datetime.utcfromtimestamp(da[0] / 1000)
#         da[0] = dt_object.strftime("%Y-%m-%d %H:%M:%S")

#     df = pd.DataFrame(
#         {
#             'time': [i[0] for i in data],
#             'open': [i[1] for i in data],
#             'high': [i[2] for i in data],
#             'low': [i[3] for i in data],
#             'close': [i[4] for i in data],
#         }
#     )

#     df['time'] = pd.to_datetime(df['time'])
#     df.set_index('time', inplace=True)

#     if not os.path.exists("img"):
#         os.mkdir("img")

#     with Image.open("chart_bg.png") as bg_image:
#         fig, ax = plt.subplots(figsize=(12, 7))
#         plt.subplots_adjust(right=0.9)
#         fpath = Path(mpl.get_data_path(), "/home/runner/binaryx/AbradeBold.ttf")

#         mpf.plot(df, type='candle', ax=ax, style='yahoo', datetime_format='%m-%d\n%H:%M')
        
#         ax.set_title(f'{symbol}/{currency} Price Chart (Past {days} Days)', color='#f3f5f4', font=fpath, fontsize=32)
#         ax.set_xlabel('Time', color='#f3f5f4', font=fpath, fontsize=24)
#         ax.set_ylabel('Price (USD)', color='#f3f5f4', font=fpath, fontsize=24)
        
#         ax.tick_params(axis='x', colors='#f3f5f4',labelsize=20)
#         ax.tick_params(axis='y', colors='#f3f5f4',labelsize=20)
#         ax.spines['left'].set_color('#727886')
#         ax.spines['left'].set_linewidth(2)
#         ax.spines['bottom'].set_color('#727886')
#         ax.spines['bottom'].set_linewidth(2)
#         ax.spines['right'].set_color('#727886')
#         ax.spines['right'].set_linewidth(2)
#         ax.spines['top'].set_color('#727886')
#         ax.spines['top'].set_linewidth(2)
        
#         current_price = df['close'].iloc[-1]
#         ax.axhline(y=current_price, color='red', linestyle='--', label='Current Price')
#         min_price = df['low'].min()
#         max_price = df['high'].max()
#         tick_step = (max_price - min_price) / 6  # Set the number of desired ticks (e.g., 5 here)
#         y_ticks = [min_price + tick_step * i for i in range(7)]
#         distances = [abs(y_tick - current_price) for y_tick in y_ticks]
        
#         # Exclude the y-axis tick closest to the current price
#         y_ticks = [y_tick for y_tick, distance in zip(y_ticks, distances) if distance != min(distances)]
#         ax.set_yticks(y_ticks + [current_price])
#         ax.set_facecolor('#181d33')
#         tick_labels = ax.get_yticklabels()
#         tick_labels[-1].set_color('red')
#         ax.set_yticklabels(tick_labels)
        
#         fig.patch.set_facecolor('#181d33')
#         fig.figimage(bg_image, xo=0, yo=0, alpha=0.1)
#         plt.legend()
#         plt.tight_layout(pad=4.0)
#         image_path = "img/chart.png"
#         plt.savefig(image_path)
        
#     return image_path

@bot.message_handler(['bnxhistory'])
def bnx_handler(message):
    try:
        bot.send_chat_action(message.chat.id,'upload_document')
        coin = "binaryx-2"
        args = message.text.split(" ")
        if len(args) == 1:
            image_path = save_chart(coin,1,"USD")
        elif len(args) == 2:
            txt = message.text.split(" ")[1]
            if txt == "7d":
                image_path = save_chart(coin,7,"USD")
            elif txt == "30d":
                image_path = save_chart(coin,30,"USD")
            else:
                txt = txt.upper()
                image_path = save_chart(coin,1,f"{txt}")
        elif len(args) == 3:
            txt = message.text.split(" ")[1]
            currency = message.text.split(" ")[2]
            if txt == "7d":
                image_path = save_chart(coin,7,{currency})
            elif txt == "30d":
                image_path = save_chart(coin,30,{currency})
            else:
                image_path = save_chart(coin,1,{currency})
        else:
            image_path = save_chart(coin,1,"USD")
        
        if image_path == None:
            bot.send_message(message.chat.id,f"{currency} not found")
            return
        crypto_symbol = 'BNX'
        coin_id = 23635
        url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id={coin_id}"
        headers = {'X-CMC_PRO_API_KEY': API_KEY}
        response = requests.get(url, headers=headers)
        data = response.json()
        short = data['data'][str(coin_id)]['quote']['USD']
        price = short['price']
        per24 = short['percent_change_24h']
        per1 = short['percent_change_1h']
        per7 = short['percent_change_7d']
        vol = short['volume_24h']
        marcap = short['market_cap']
        csupply = data['data'][str(coin_id)]['circulating_supply']
        tsupply = data['data'][str(coin_id)]['total_supply']

        caption = f"<b>📈 BinaryX (BNX) Chart 📉</b>\n\n"
        caption += f"💰 <b>Price</b>: ${price:.3f}\n"
        caption += f"⚡️ <b>1hr Change</b>:   {per1:.2f}%\n"
        caption += f"🌙 <b>24hr Change</b>: {per24:.2f}%\n"
        caption += f"📅 <b>7d Change</b>:    {per7:.2f}%\n"
        caption += f"💹 <b>Volume</b>: ${vol:.2f}\n"
        caption += f"🏦 <b>Market Cap</b>: ${marcap:.2f}\n"
        caption += f"💼 <b>Circulating Supply</b>: ${csupply:.2f}\n"
        caption += f"📊 <b>Total Supply</b>: ${tsupply:.2f}"

        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton('💠 Buy BNX 💠', url='https://pancakeswap.finance/swap?outputCurrency=0x5b1f874d0b0C5ee17a495CbB70AB8bf64107A3BD'))
        with open(image_path, 'rb') as chart_image:
            bot.send_photo(message.chat.id,chart_image ,caption=caption,parse_mode='HTML',reply_markup=markup)
    except Exception as e :
        bot.send_message(1443989714,f"Error in chart - \n\n\n\n{e}")
        bot.send_message(message.chat.id,"Error in geting chat data")

def save_chart(coin,days,currency):
    try:
        url = f'https://api.coingecko.com/api/v3/coins/{coin}/ohlc?vs_currency={currency}&days={days}'
        if coin == "binaryx-2":
            symbol = "BNX"
        elif coin == "cyberdragon-gold":
            symbol = "GOLD"
        
        data = requests.get(url).json()
        for da in data:
            dt_object = datetime.utcfromtimestamp(da[0] / 1000)
            da[0] = dt_object.strftime("%Y-%m-%d %H:%M:%S")

        df = pd.DataFrame(
            {
                'time': [i[0] for i in data],
                'open': [i[1] for i in data],
                'high': [i[2] for i in data],
                'low': [i[3] for i in data],
                'close': [i[4] for i in data],
            }
        )

        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)

        if not os.path.exists("img"):
            os.mkdir("img")

        with Image.open("background2.png") as bg_image:
            fig, ax = plt.subplots(figsize=(16, 9))
            fpath = Path(mpl.get_data_path(), "/home/runner/binaryx/AbradeBold.ttf")

            mpf.plot(df, type='candle', ax=ax, style='yahoo', datetime_format='%m-%d\n%H:%M')
            
            ax.set_title(f'{symbol}/{currency} Price Chart (Past {days} Days)', color='#f3f5f4', font=fpath, fontsize=24)
            ax.set_xlabel('Time', color='#f3f5f4', font=fpath, fontsize=24)
            ax.set_ylabel('Price (USD)', color='#f3f5f4', font=fpath, fontsize=24)
            
            ax.tick_params(axis='x', colors='#f3f5f4',labelsize=16)
            ax.tick_params(axis='y', colors='#f3f5f4',labelsize=16)
            ax.spines['left'].set_color('#727886')
            ax.spines['left'].set_linewidth(2)
            ax.spines['bottom'].set_color('#727886')
            ax.spines['bottom'].set_linewidth(2)
            ax.spines['right'].set_color('#727886')
            ax.spines['right'].set_linewidth(2)
            ax.spines['top'].set_color('#727886')
            ax.spines['top'].set_linewidth(2)
            
            current_price = df['close'].iloc[-1]
            ax.axhline(y=current_price, color='red', linestyle='--', label='Current Price')
            min_price = df['low'].min()
            max_price = df['high'].max()
            tick_step = (max_price - min_price) / 6  # Set the number of desired ticks (e.g., 5 here)
            y_ticks = [min_price + tick_step * i for i in range(7)]
            distances = [abs(y_tick - current_price) for y_tick in y_ticks]
            
            # Exclude the y-axis tick closest to the current price
            y_ticks = [y_tick for y_tick, distance in zip(y_ticks, distances) if distance != min(distances)]
            ax.set_yticks(y_ticks + [current_price])
            ax.set_facecolor('#181d33')
            tick_labels = ax.get_yticklabels()
            tick_labels[-1].set_color('red')
            ax.set_yticklabels(tick_labels)
            
            fig.patch.set_facecolor('#181d33')
            fig.figimage(bg_image, xo=0, yo=0, alpha=0.1)
            plt.legend()
            plt.tight_layout(pad=4.0)
            image_path = "img/chart.png"
            plt.savefig(image_path)
            
        return image_path
    except Exception:
        return None


save_chart("cyberdragon-gold",7,"USD")
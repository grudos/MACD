from csv import reader
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

n = 1000
closingPrice = []
MACD_values = []
SIGNAL_values = []
date = []
days = []

profit_1 = 0
units_1 = n
action_1 = ""

profit_2 = 0
units_2 = n
bought_units_2 = 0
action_2 = ""

def readFile(fileName):
    with open('data/'+fileName+'.csv', "r") as read_obj:
        csv_reader = reader(read_obj)
        numLine = 0
        for row in csv_reader:
            if numLine >= n:
                break
            closingPrice.append(float(row[4]))
            date.append(row[0])
            numLine += 1

def EMA(N, day, values):
    alpha = 2/(N+1)
    factor = 1.0 - alpha
    val = 0.0
    divider = 0.0
    for exponent in range(N+1):
        if day >= 0:
            val += (values[day]*pow(factor, exponent))
            divider += pow(factor, exponent)
            day -= 1
        else:
            break
    val /= divider
    return val

def MACD(day, closingPrice):
    EMA12 = EMA(12, day, closingPrice)
    EMA26 = EMA(26, day, closingPrice)
    MACD_value = EMA12 - EMA26
    return MACD_value

def SIGNAL(day, MACD_values):
    SIGNAL_value = EMA(9, day, MACD_values)
    return SIGNAL_value

def strategy_1(day, action):
    global profit_1
    global units_1
    if action == "buy":
        profit_1 -= (n * closingPrice[day])
        units_1 = 0
    elif action == "sell":
        profit_1 += (n * closingPrice[day])
    print("STARTEGY 1")
    print("Profit strategy_1 = " + str(profit_1))
    print("Units strategy_1 = "+str(units_1))
    print("Day strategy_1 = "+str(day))

def strategy_2(day, action):
    global profit_2
    global units_2
    global bought_units_2
    if action == "buy":
        profit_2 -= ((n/4) * closingPrice[day])
        bought_units_2 += (n/4)
        units_2 -= (n/4)
    elif action == "sell":
        profit_2 += (bought_units_2 * closingPrice[day])
        bought_units_2 = 0
    print("STARTEGY 2")
    print("Profit strategy_2 = "+str(profit_2))
    print("Units strategy_2 = "+str(units_2))
    print("Day strategy_2 = "+str(day))




fileName = "wig20"
readFile(fileName)

for day in range(n):
    days.append(day)
    MACD_values.append(MACD(day, closingPrice))
    SIGNAL_values.append(SIGNAL(day, MACD_values))
    # Signal to buy and sell in strategy 1
    if day >= 37 and action_1 != "end" and units_1 == n and MACD_values[day-2] < SIGNAL_values[day-2] and MACD_values[day-1] < SIGNAL_values[day-1] and SIGNAL_values[day-1] >= SIGNAL_values[day-2]:
        action_1 = "buy"
        strategy_1(day, action_1)
    elif day >= 37 and action_1 != "end" and units_1 == 0 and MACD_values[day-2] > SIGNAL_values[day-2] and MACD_values[day-1] > SIGNAL_values[day-1] and SIGNAL_values[day-1] <= SIGNAL_values[day-2]:
        action_1 = "sell"
        strategy_1(day, action_1)
        action_1 = "end"
    # Signal to buy and sell in strategy 2
    if day >= 37 and action_2 != "end" and units_2 > 0 and MACD_values[day-2] < SIGNAL_values[day-2] and MACD_values[day-1] < SIGNAL_values[day-1] and SIGNAL_values[day-1] >= SIGNAL_values[day-2]:
        action_2 = "buy"
        strategy_2(day, action_2)
    elif day >= 37 and action_2 != "end" and bought_units_2 > 0 and MACD_values[day-2] > SIGNAL_values[day-2] and MACD_values[day-1] > SIGNAL_values[day-1] and SIGNAL_values[day-1] <= SIGNAL_values[day-2]:
        action_2 = "sell"
        strategy_2(day, action_2)
        if units_2 == 0:
            action_2 = "end"

figure(num=None, figsize=(20, 9), dpi=60)
plt.plot(days, closingPrice, label="closing Price")
plt.legend(loc="lower left")
plt.title("Closing price")
plt.xlabel("Days")
plt.ylabel("Closing price")
plt.savefig('results/'+fileName+'_ClosingPrices.png')
plt.show()

figure(num=None, figsize=(20, 9), dpi=60)
plt.plot(days[35:], MACD_values[35:], label="MACD")
plt.plot(days[35:], SIGNAL_values[35:], label="SIGNAL")
plt.legend(loc="lower left")
plt.title("MACD")
plt.xlabel("Days")
plt.ylabel("Values")
plt.savefig('results/'+fileName+'_MACD.png')
plt.show()

figure(num=None, figsize=(20, 9), dpi=60)
plt.plot(days[35:], MACD_values[35:], label="MACD")
plt.plot(days[35:], SIGNAL_values[35:], label="SIGNAL")
plt.plot(days, closingPrice, label="closing Price")
plt.legend(loc="upper right")
plt.title("MACD and closing prices")
plt.xlabel("Days")
plt.ylabel("Values")
plt.savefig('results/'+fileName+'_connected.png')
plt.show()
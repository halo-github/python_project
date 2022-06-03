import pandas as pd
import matplotlib.pyplot as plt
import time

data_file = "D:\Program Files (x86)\Holdfast\platform 7.5.1\kuaijie\qh.xlsx"

dt = pd.read_excel(data_file)

if __name__ == "__main__":
    print(dt)
    dt = dt.loc[:,["date","quanyi"]]
    today = time.strftime("%m.%d",time.localtime())
    print(type(today))
    pt = input("今日权益：")
    print(len(dt.index))
    if int(pt) > 0:
        dt.loc[len(dt.index)] = [today,str(pt)]
        dt.to_excel(data_file)

    plt.title("收益")
    plt.xlabel("date")
    plt.ylabel("sum")
    x = [str(i) for i in dt["date"]]
    y = dt["quanyi"]
    plt.plot(x,y)
    plt.show()

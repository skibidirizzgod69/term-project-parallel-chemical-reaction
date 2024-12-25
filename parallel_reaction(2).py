import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np


# 清除當前介面
def clear_frame():
    global current_frame
    if current_frame is not None:
        current_frame.destroy()


# 步驟 1：輸入並聯反應數量
def step1():
    clear_frame()

    def confirm_reactions(): #檢測輸入是否為正整數並處存數據
        try: 
            num_reactions = int(entry.get())
            if num_reactions < 1: # 輸入的反應數量必須是正整數
                raise ValueError 
            reaction_data['num_reactions'] = num_reactions # 存儲數據 
            step2(num_reactions)
        except ValueError:
            error_label.config(text="請輸入有效的正整數！")

    global current_frame
    current_frame = tk.Frame(root)
    current_frame.pack() # 需要此行才能把frame所有內容放置在主視窗上

    tk.Label(current_frame, text="有幾個並聯反應？").pack()
    entry = tk.Entry(current_frame)
    entry.pack()
    error_label = tk.Label(current_frame, text="", fg="red")
    error_label.pack()
    tk.Button(current_frame, text="Confirm", command=confirm_reactions).pack()

# 步驟 2：輸入每個反應的反應物和產物數量
def step2(num_reactions):
    clear_frame()

    def confirm_reactants_products():
        try:
            reaction_counts = [] # 反應物和產物數量
            for i in range(num_reactions): # 逐一讀取每個反應的反應物和產物數量
                reactants = int(reactant_entries[i].get())  #get()返回的是字符串，所以要轉換成整數
                products = int(product_entries[i].get())
                if reactants < 1 or products < 1:
                    raise ValueError
                reaction_counts.append((reactants, products)) # 格式：[(reactants1, products1), (reactants2, products2), ...] (list)
            reaction_data['reaction_counts'] = reaction_counts # 存儲數據 
            step3(reaction_counts)
        except ValueError:
            error_label.config(text="請輸入有效的正整數！")

    global current_frame
    current_frame = tk.Frame(root)
    current_frame.pack()

    reactant_entries = [] # 建立空列表 (list)
    product_entries = []

    for i in range(num_reactions):
        tk.Label(current_frame, text=f"反應 {i + 1} 的反應物和產物數：").pack()
        tk.Label(current_frame, text="反應物：").pack()
        reactant_entry = tk.Entry(current_frame)
        reactant_entry.pack()
        reactant_entries.append(reactant_entry) # 格式：[reactant1, reactant2, ...] (tuple)
        tk.Label(current_frame, text="產物：").pack()
        product_entry = tk.Entry(current_frame)
        product_entry.pack()
        product_entries.append(product_entry)

    error_label = tk.Label(current_frame, text="", fg="red")
    error_label.pack()
    tk.Button(current_frame, text="Confirm", command=confirm_reactants_products).pack()

# 步驟 3：輸入反應物和產物名稱
def step3(reaction_counts):
    clear_frame()

    def confirm_names():
        try:
            reactions_name = [] # 反應物和產物名稱
            reactions_stiochiometry = [] # 反應物和產物的化學劑量數
            for i in range(len(reaction_counts)):
                reactants = [reactant_entries[i][j].get() for j in range(reaction_counts[i][0])] # 逐一讀取每個反應的反應物和產物名稱
                products = [product_entries[i][j].get() for j in range(reaction_counts[i][1])] 
                reactant_stiochiometries = [int(reactant_stiochiometry_entries[i][j].get()) for j in range(reaction_counts[i][0])] # 逐一讀取每個反應的反應物和產物的化學劑量數
                product_stiochiometries = [int(product_stiochiometry_entries[i][j].get()) for j in range(reaction_counts[i][1])]
                if any(not reactant for reactant in reactants) or any(not product for product in products): # 檢查反應物和產物名稱是否為空字串
                    raise ValueError("反應物和產物名稱不能為空！")
                if len(reactants) != len(set(reactants)): # 檢查反應物是否有重複
                    raise ValueError("反應物名稱不能重複！")
                if len(products) != len(set(products)): # 檢查產物是否有重複
                    raise ValueError("產物名稱不能重複！")
                if bool(set(reactants) & set(products)): # 檢查反應物和產物名稱是否重複
                    raise ValueError("反應物和產物名稱不能重複！")
                if any(stiochiometry <= 0 for stiochiometry in reactant_stiochiometries) or any(stiochiometry <= 0 for stiochiometry in product_stiochiometries): # 檢查化學劑量數是否為正數
                    raise ValueError("化學劑量數必須為正數！")
                reactions_name.append({'reactants': reactants, 'products': products}) # 格式：[{'reactants': [reactant1, reactant2, ...], 'products': [product1, product2, ...]}, ...] (list)
                reactions_stiochiometry.append({'reactants_stiochiometry': reactant_stiochiometries, 'products_stiochiometry': product_stiochiometries})
            reaction_data['reactions'] = reactions_name # 存儲數據
            reaction_data['reactions_stiochiometry'] = reactions_stiochiometry 
            step4()
        except ValueError as a:
            error_label.config(text=f"錯誤：{a}")

    global current_frame
    current_frame = tk.Frame(root)
    current_frame.pack()

    reactant_entries = [] #格式：[[reactant1, reactant2, ...], [reactant1, reactant2, ...], ...] (list of lists)
    reactant_stiochiometry_entries = []
    product_entries = []
    product_stiochiometry_entries = []

    for i, (num_reactants, num_products) in enumerate(reaction_counts): # 逐一讀取每個反應的反應物和產物名稱, i=0, 1, 2, ...表示第i個反應
        tk.Label(current_frame, text=f"反應 {i + 1} 的名稱：").pack()
        reactant_entry_row = []
        reactant_stiochiometry_entries_row = []
        for j in range(num_reactants):
            tk.Label(current_frame, text=f"反應物 {j + 1}的名稱：").pack()
            reactant_entry = tk.Entry(current_frame)
            reactant_entry.pack()
            reactant_entry_row.append(reactant_entry)
            tk.Label(current_frame, text=f"反應物 {j + 1}的化學劑量數：").pack()
            reactant_stiochiometry_entry = tk.Entry(current_frame)
            reactant_stiochiometry_entry.pack()
            reactant_stiochiometry_entries_row.append(reactant_stiochiometry_entry)
        reactant_entries.append(reactant_entry_row)
        reactant_stiochiometry_entries.append(reactant_stiochiometry_entries_row)
# 結果：reactant_entries = [[reactant1, reactant2, ...], [reactant1, reactant2, ...], ...] (list of lists)

        product_entry_row = []
        product_stiochiometry_entries_row = []
        for j in range(num_products):
            tk.Label(current_frame, text=f"產物 {j + 1}：").pack()
            product_entry = tk.Entry(current_frame)
            product_entry.pack()
            product_entry_row.append(product_entry)
            tk.Label(current_frame, text=f"產物 {j + 1}的化學劑量數：").pack()
            product_stiochiometry_entry = tk.Entry(current_frame)
            product_stiochiometry_entry.pack()
            product_stiochiometry_entries_row.append(product_stiochiometry_entry)
        product_entries.append(product_entry_row)
        product_stiochiometry_entries.append(product_stiochiometry_entries_row)
# 結果：product_entries = [[product1, product2, ...], [product1, product2, ...], ...] (list of lists)

    error_label = tk.Label(current_frame, text="", fg="red")
    error_label.pack()
    tk.Button(current_frame, text="Confirm", command=confirm_names).pack()

# 步驟 4：輸入反應參數
def step4():
    clear_frame()

    def confirm_parameters(): # 檢測輸入之反應參數是否為有效數字並儲存數據
        try:
            parameters = [] # 反應參數
            for i in range(reaction_data['num_reactions']): # 逐一讀取每個反應的參數
                ea = float(ea_entries[i].get()) # 活化能
                if ea <= 0:
                    raise ValueError
            
            for i in range(reaction_data['num_reactions']): # 逐一讀取每個反應的參數
                A = float(A_entries[i].get()) # 阿瑞尼斯常數A
                if A <= 0:
                    raise ValueError
                
                orders = [int(order.get()) for order in order_entries[i]] # 反應級數
                if any(order < 0 for order in orders):
                    raise ValueError
                
                reactant_partial_pressures = [float(partial_pressure.get()) for partial_pressure in reactant_partial_pressure_entries[i]] # 分壓
                if any(partial_pressure <= 0 for partial_pressure in reactant_partial_pressures):
                    raise ValueError
                
                temp = float(temp_entries[i].get()) # 溫度
                if temp <= 0:
                    raise ValueError
                parameters.append({'ea': ea,'A': A , 'orders': orders,'reactant_partial_pressures': reactant_partial_pressures, 'temperature': temp}) 
            time = float(initial_time.get())
            if time <= 0:
                raise ValueError
            reaction_data['time'] = time
            reaction_data['parameters'] = parameters # 存儲數據 格式：[{'ea': ea1, 'A': A1, 'orders': [order1, order2, ...], 'reactant_partial_pressures': [partial_pressure1, partial_pressure2, ...], 'temperature': temp1}, ...] (list)
            step5()
        except ValueError:
            error_label.config(text=f"錯誤!(反應級數為正整數，活化能、阿瑞尼斯常數、分壓、溫度、時間必須為正數)")

    global current_frame
    current_frame = tk.Frame(root)
    current_frame.pack()

    ea_entries = [] # 建立空列表 (list)
    A_entries = []
    order_entries = []
    reactant_partial_pressure_entries = []
    temp_entries = []

    for i, reaction in enumerate(reaction_data['reactions']): # reaction_data['reactions'] = [{'reactants': [reactant1, reactant2, ...], 'products': [product1, product2, ...]}, ...] (list)
        tk.Label(current_frame, text=f"反應 {i + 1} 的參數：").pack()
        tk.Label(current_frame, text="反應活化能 Ea：").pack()
        ea_entry = tk.Entry(current_frame)
        ea_entry.pack()
        ea_entries.append(ea_entry) # 格式：[ea1, ea2, ...] (list)

        tk.Label(current_frame, text="阿瑞尼斯常數 A：").pack()
        A_entry = tk.Entry(current_frame)
        A_entry.pack()
        A_entries.append(A_entry) # 格式：[A1, A2, ...] (list)

        order_row = []
        for reactant in reaction['reactants']:
            tk.Label(current_frame, text=f"反應物 {reactant} 的反應級數：").pack()
            order_entry = tk.Entry(current_frame)
            order_entry.pack()
            order_row.append(order_entry) # 格式：[order1, order2, ...] (list)
        order_entries.append(order_row) # 格式：[[order1, order2, ...], [order1, order2, ...], ...] (list of lists)

        reactant_partial_pressure_row=[]
        for reactant in reaction['reactants']:
            tk.Label(current_frame, text=f"反應物 {reactant} 的分壓：").pack()
            reactant_partial_pressure_entry = tk.Entry(current_frame)
            reactant_partial_pressure_entry.pack()
            reactant_partial_pressure_row.append(reactant_partial_pressure_entry) 
        reactant_partial_pressure_entries.append(reactant_partial_pressure_row) 

        tk.Label(current_frame, text="溫度：").pack()
        temp_entry = tk.Entry(current_frame)
        temp_entry.pack()
        temp_entries.append(temp_entry)
    tk.Label(current_frame, text="輸入反應時間:").pack()
    initial_time = tk.Entry(current_frame)
    initial_time.pack()
    error_label = tk.Label(current_frame, text="", fg="red")
    error_label.pack()
    tk.Button(current_frame, text="Confirm", command=confirm_parameters).pack()


# 步驟 5：繪製分壓對時間圖
def step5():
    clear_frame()

    def plot_pressure_vs_time():

        time = reaction_data['time']  # 總模擬時間
        dt = 0.1  # 時間步長
        time_points = np.arange(0, time + dt, dt)  # 包括結束時間點
        all_reactant_pressures = []  # 反應物分壓數據
        all_product_pressures = []   # 產物分壓數據

        for reaction, reaction_info,reaction_stiochiometry in zip(reaction_data['parameters'], reaction_data['reactions'], reaction_data['reactions_stiochiometry']): # 逐一讀取每個反應的參數
                # 初始化參數
                k = reaction['A'] * np.exp(-reaction['ea'] / (8.314 * reaction['temperature']))  # 速率常數
                orders = reaction['orders']  # 反應級數 格式：[order1, order2, ...] (list)
                reactant_partial_pressures = reaction['reactant_partial_pressures'] # 反應物分壓 格式：[partial_pressure1, partial_pressure2, ...] (list)
                products = reaction_info['products']  # 產物名稱列表
                num_products = len(products)
                product_partial_pressures = [0.0] * num_products  # 初始時產物分壓為 0

                reactant_pressures = []
                product_pressures = []

                for _ in time_points: # 逐一計算每個時間點的反應物和產物分壓
                    # 保存當前反應物與產物分壓
                    reactant_pressures.append(reactant_partial_pressures.copy())
                    product_pressures.append(product_partial_pressures.copy())

                        # 計算反應速率
                    rate = k * np.prod([P**order for P, order in zip(reactant_partial_pressures, orders)])

                        # 更新反應物分壓
                    reactant_partial_pressures = [max(P - stioch * rate * dt, 0) for P, stioch in zip(reactant_partial_pressures, reaction_stiochiometry['reactants_stiochiometry'])]

                        # 更新產物分壓
                    product_partial_pressures = [P + stioch * rate * dt for P, stioch in zip(product_partial_pressures, reaction_stiochiometry['products_stiochiometry'])]

                all_reactant_pressures.append(np.array(reactant_pressures)) # 轉換成 numpy array
                all_product_pressures.append(np.array(product_pressures))

                # 繪製圖表
        plt.figure(figsize=(12, 8))
        for i, (reactant_pressures, product_pressures) in enumerate(zip(all_reactant_pressures, all_product_pressures)):
                # 反應物曲線
            reactant_combined_pressures = {}
            for i, reactant_pressures in enumerate(all_reactant_pressures):
                for j, reactant in enumerate(reaction_data['reactions'][i]['reactants']):
                    if reactant not in reactant_combined_pressures:
                        reactant_combined_pressures[reactant] = np.zeros_like(time_points)
                    reactant_combined_pressures[reactant] += reactant_pressures[:, j]

            for reactant, pressures in reactant_combined_pressures.items():
                plt.plot(time_points, pressures, linestyle='--', label=f'{reactant}')

                # 產物曲線
            for j in range(product_pressures.shape[1]):
                plt.plot(time_points, product_pressures[:, j], linestyle='--', label=f'react {i+1} product {j+1}')

        plt.xlabel('time (s)')
        plt.ylabel('partial pressure (atm)')
        plt.title('Partial Pressure vs Time for Reactions')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    global current_frame
    current_frame = tk.Frame(root)
    current_frame.pack()

    tk.Label(current_frame, text="點擊下方按鈕繪製分壓對時間圖").pack()
    tk.Button(current_frame, text="繪製圖表", command=plot_pressure_vs_time).pack()





# 主窗口
root = tk.Tk()
root.title("化學反應模擬器")
root.geometry("400x1000")
s= tk.Scrollbar(root)

# 當前 Frame
current_frame = None

# 數據存儲
reaction_data = {}

# 啟動流程
step1()
root.mainloop()

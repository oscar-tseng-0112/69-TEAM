import pandas as pd

import uuid


# --- 1. 定義區域與票價規則 ---

# 根據您的需求：

# 藍區: 原價 $6000, 第一排 +80%, 之後每排 -5%

# 紅/紫區: 原價 $4000, 第一排 +65%, 之後每排 -5%

# 黃區: 原價 $2000, 第一排 +50%, 之後每排 -5%


venue_config = {

    "BLUE": {

        "name": "藍區",

        "keywords": ["藍", "藍區", "BLUE"],

        "base_price": 6000,

        "first_row_weight": 1.80, # 1 + 80%

        "decay": 0.05

    },

    "RED": {

        "name": "紅區",

        "keywords": ["紅", "紅區", "RED"],

        "base_price": 4000,

        "first_row_weight": 1.65, # 1 + 65%

        "decay": 0.05

    },

    "PURPLE": {

        "name": "紫區",

        "keywords": ["紫", "紫區", "PURPLE"],

        "base_price": 4000,

        "first_row_weight": 1.65, # 1 + 65%

        "decay": 0.05

    },

    "YELLOW": {

        "name": "黃區",

        "keywords": ["黃", "黃區", "YELLOW"],

        "base_price": 2000,

        "first_row_weight": 1.50, # 1 + 50%

        "decay": 0.05

    }

}


# --- 2. 資料生成函數 (建立資料庫) ---

def generate_price_table():

    data_list = []

   

    for code, config in venue_config.items():

        base_price = config["base_price"]

        start_weight = config["first_row_weight"]

        decay = config["decay"]

       

        # 假設每一區都有 10 排

        for row in range(1, 11):

            # 計算權重：第一排不扣，第二排扣 1個 decay，依此類推

            current_weight = start_weight - ((row - 1) * decay)

           

            # 計算價格：原價 * 權重 (取整數)

            final_price = int(base_price * current_weight)

           

            # 存入資料表

            data_list.append({

                "area_code": code,           # 代號 (用於程式邏輯)

                "area_name": config["name"], # 顯示名稱 (藍區)

                "row": row,                  # 排數

                "price": final_price         # 計算後的價格

            })

           

    return pd.DataFrame(data_list)


# --- 3. 搜尋功能 (Search Algorithm) ---

def search_ticket_price(df):

    print("\n" + "="*40)

    print("🎫 歡迎使用 69 Team 票價查詢系統")

    print("="*40)

   

    while True:

        user_input = input("\n請輸入您想查詢的區域 (輸入 q 離開)：").strip()

       

        if user_input.lower() == 'q':

            print("系統已關閉。")

            break

       

        # [搜尋演算法] 步驟 1: 模糊比對使用者輸入

        target_code = None

        for code, config in venue_config.items():

            # 檢查使用者輸入是否在我們定義的關鍵字清單中 (例如輸入 "藍" 或 "Blue")

            # 使用 upper() 讓英文不分大小寫

            if user_input.upper() in [k.upper() for k in config["keywords"]]:

                target_code = code

                break

       

        if not target_code:

            print("❌ 找不到該區域，請確認輸入 (例如：藍區、紅區)。")

            continue


        # [搜尋演算法] 步驟 2: 從資料庫中篩選 (Filter)

        result = df[df['area_code'] == target_code]

        area_name = venue_config[target_code]['name']

       

        # 顯示結果

        print(f"\n📊 【{area_name}】 票價表：")

        print("-" * 30)

        print(f"{'排數':<10} | {'價格':<10}")

        print("-" * 30)

       

        # 遍歷結果並印出

        for index, row in result.iterrows():

            print(f"第 {row['row']:<2} 排    | ${row['price']}")

        print("-" * 30)


# --- 4. 主程式執行 ---

if __name__ == "__main__":

    # 生成資料

    df_prices = generate_price_table()

   

    # 啟動搜尋介面

    search_ticket_price(df_prices)
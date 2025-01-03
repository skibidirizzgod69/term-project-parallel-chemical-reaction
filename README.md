# 平行化學反應模擬 (Parallel Chemical Reaction Simulation)
## (1) 程式的功能
此程式是一個基於 `Tkinter` 的化學反應模擬器，幫助使用者輸入多條並聯化學反應的數據，並根據輸入計算反應進行中的反應物和產物分壓隨時間的變化，最終繪製圖表。
考慮的反應為單向反應(不考慮逆反應)。
- **反應動力學模擬**: 模擬任意數量的平行反應，展示反應物與生成物的濃度變化。
- **互動式圖形介面**: 提供使用者輸入初始條件並視覺化結果。
- **參數自訂化**: 可調整反應參數，溫度初始壓力、阿瑞尼斯常數、活化能。
- **數據視覺化**: 繪製反應物與生成物濃度隨時間的變化圖。

## (2) 使用方式 
1. 環境設置：
   確保已安裝 Python3.8或更新版本
  需安裝必要套件
   ```
   pip install numpy matplotlib scipy
   ```
3. 執行模擬程式：
   ```bash
   python term_project.py
   ```
4. 在 GUI 中輸入以下參數：
   - step1: 有幾個平行反應
   - step2: 各反應反應物和產物數量
   - step3:反應物名稱和化學劑量數
   - step4: 產物 的初始分壓 (atm)、阿瑞尼斯常數、活化能、溫度(K)、反應時間
   - step5: 點擊 "繪製圖表" 按鈕查看結果
5. 產生分壓對時間圖

## (3) 程式的架構 
### `clear_frame`
- **功能**：清除當前介面（`current_frame`）。
### `step1`
- **功能**：輸入並聯反應的數量。
### `step2`
- **功能**：輸入每個反應的反應物和產物數量。
### `step3`
- **功能**：輸入反應物和產物的名稱和化學劑量數。
### `step4`
- **功能**：輸入反應的參數（如活化能、反應級數等）。
### `step5`
- **功能**：模擬反應並繪製分壓對時間的圖表。
## (4) 開發過程 
1.發想與修改:
   -從原本的固定反應在不同溫度下反應，改成設計任意數量平行反應的進行                  
2.初始功能開發:
   - 整合 Tkinter 建立互動界面
   - 讓使用者逐一輸入必要條件
   - 整合和儲存各項輸入參數
   - 針對不合理輸入內容提出錯誤信息
3. 運算功能和繪圖功能開發:
   -考慮阿瑞尼斯方程式對速率影響
   -使用 SciPy 的 `odeint` 函數解微分方程得知瞬時速度
   -把不同反應中同反應物合併(符合真實情形，反應物共用)
   -利用 Matplotlib 視覺化呈現反應過程
4. 測試與優化:
   - 測試不同溫度與初始壓力的模擬效果
   - 增強 GUI 錯誤處理

## (5) 參考資料來源 
1. **ChatGPT**: 提供初始程式架構，但內部程式碼有大量bug和錯誤，或是不合我需求，所以大部分內容都被我改掉了
   對話紀錄:
   - 初期構想 https://chatgpt.com/share/676b8848-0928-800f-bb61-752587a0ad2e
   - 問題解決 https://chatgpt.com/share/676b8b4a-fb7c-800f-9f03-a0895d5bbb29
3. **維基百科**: https://zh.wikipedia.org/zh-tw/%E9%98%BF%E4%BC%A6%E5%B0%BC%E4%B9%8C%E6%96%AF%E6%96%B9%E7%A8%8B
4. 使用github copilot 機器人輔助寫程式

## (6) 程式修改或增強的內容 
1. 添加任意數量反應模擬：chatgpt最初提供之版本只能運算給定特定兩反應。
2. 增強 GUI 功能：透過 Tkinter 實現互動式輸入與錯誤處理。
3. 合併同反應物: 把同反應物合併，使其最終在圖表上呈現唯一曲線，且變化量考量所有涉及反應。
4. 繪圖優化：把原本只能畫出反應物曲線，我加入產物曲線，且原本不能順利運行。
5. 把產物中相同名稱物合併成同一條曲線，使其符合真實情況
- **貢獻部分**:
  - 修改輸入內容，從原來只能輸入一產物，改成可輸入任意數量，並且加入考量化學劑量數、產物、阿瑞尼斯常數、活化能，並且可選取反應時間。
  - 原本產生的程式運行有許多錯誤，像是只顯示一個輸入框來輸入多個反應物，圖表無法正確生成等等，我透過大量修改函數內容才能運行。
  - 添加錯誤處理機制，提示使用者輸入錯誤參數時的警告。
  - 添加許多註解方便理解



# 日序 DAYFLOW

日序是個人行程與待辦管理 Web 原型，提供今日總覽、行程月曆和待辦任務清單。介面以繁體中文呈現，使用原生 HTML、CSS、JavaScript，並以 Firebase Authentication 和 Cloud Firestore 提供登入與雲端資料保存。

## 功能

- 使用 Google 帳戶登入與登出；每個帳戶的行程及任務分開保存。
- 在今日總覽查看當日行程、未完成待辦、數量摘要與提醒摘要。
- 以月曆日期格顯示行程標題並切換月份；選取日期後在月曆下方查看當日日程，待辦不顯示在行程月曆。
- 在待辦任務清單逐筆查看所有日期的任務，可選擇依日期或優先度排序；次排序使用另一項條件，並標示逾期狀態。
- 新增、編輯、刪除行程或任務，並直接勾選任務完成狀態。
- 行程支援日期、起訖時間、地點、備註與提醒；任務支援截止日期／時間、提醒、優先順序及完成狀態。
- 同一瀏覽器另保存每位使用者的本機資料副本；雲端寫入失敗時會顯示提示。
- 「日序小助手」使用 Firebase AI Logic 與 Gemini 3.8 Flash，根據所選日期行程和待辦提供繁體中文規劃建議，支援多輪追問。
- 支援桌面與行動版版面。

提醒目前只顯示在今日總覽，不會排程或送出瀏覽器／手機通知。

## 執行方式

這是無建置步驟的單頁應用。由於頁面使用 Firebase ES modules，請透過本機 HTTP 伺服器開啟，而非直接以 `file://` 開啟。例如：

```powershell
python -m http.server 8000
```

然後瀏覽 `http://localhost:8000/`。

## Firebase 設定

目前 `index.html` 內含 Firebase Web app 設定。若改用自己的 Firebase 專案，請在 Firebase Console：

1. 建立 Web app，啟用 Google provider 的 Firebase Authentication。
2. 建立 Cloud Firestore，並設定安全規則，限制使用者只能讀寫自己的 `users/{uid}/planner/main` 文件。
3. 將 Web app 的 `apiKey`、`authDomain`、`projectId` 和 `appId` 更新至 `index.html` 的 `firebaseConfig`。
4. 若部署到網頁，將部署網域加入 Firebase Authentication 的授權網域。
5. 在 Firebase 專案目錄執行 `npx -y firebase-tools@latest init ailogic`，啟用 Firebase AI Logic / Gemini Developer API。
6. 在 Firebase Console 的「App Check」為 Web app 註冊 reCAPTCHA Enterprise，將取得的 site key 填入 `index.html` 的 `appCheckSiteKey`。本機 `localhost` 會自動使用 App Check debug provider；第一次使用時，請將瀏覽器 console 印出的 debug token 加到 Firebase Console > App Check > Apps > Manage debug tokens。請勿公開 debug token，也不要在正式部署使用 debug provider。

登入成功後，應用程式先讀取 `users/{uid}/planner/main`；沒有有效雲端資料時會使用該帳戶的本機副本，若兩者皆無則以空白行程及任務開始。每次變更會先寫入本機，再排入 Firestore 寫入。Firestore 權限或連線錯誤不會提供即時雲端同步保證。

Gemini 對話只會附帶所選日期的行程、地點、備註及任務，不會傳送其他日期的資料。正式部署前需完成 reCAPTCHA Enterprise App Check 設定。網頁中的 site key 是公開識別值，不可把 Gemini API key 或 App Check debug token 放進前端。

## 資料格式

資料文件包含 `events` 與 `tasks` 陣列。行程欄位為 `id`、`title`、`date`、`start`、`end`、`place`、`note`、`reminder`；任務欄位為 `id`、`title`、`date`、`dueTime`、`priority`、`done`、`reminder`。日期格式為 `YYYY-MM-DD`，時間使用 24 小時制；提醒值以分鐘表示（0、5、15、30、60、1440）。

## 專案檔案

- `index.html`：完整前端介面、樣式及互動程式。
- `PRD.md`：依目前程式實作整理的產品需求文件。

本原型尚無伺服器端程式、離線同步佇列、推播通知、外部日曆整合或分析埋點。清除瀏覽器網站資料會刪除本機副本；資料仍以 Firebase Firestore 雲端文件為主。

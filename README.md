# 日序 DAYFLOW

日序是個人行程與待辦管理 Web 原型，提供今日總覽、行程月曆和任務時間線。介面以繁體中文呈現，使用原生 HTML、CSS、JavaScript，並以 Firebase Authentication 和 Cloud Firestore 提供登入與雲端資料保存。

## 功能

- 使用 Google 帳戶登入與登出；每個帳戶的行程及任務分開保存。
- 在今日總覽查看當日行程、未完成待辦、數量摘要與提醒摘要。
- 以月曆查看各日行程數及未完成任務數，並切換月份、選取日期。
- 在任務時間線查看所選日期 24 小時內的行程與未完成任務；任務依截止時間定位，並標示逾期狀態。
- 新增、編輯、刪除行程或任務，並直接勾選任務完成狀態。
- 行程支援日期、起訖時間、地點、備註與提醒；任務支援截止日期／時間、提醒、優先順序及完成狀態。
- 同一瀏覽器另保存每位使用者的本機資料副本；雲端寫入失敗時會顯示提示。
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

登入成功後，應用程式先讀取 `users/{uid}/planner/main`；沒有有效雲端資料時會使用該帳戶的本機副本，若兩者皆無則以空白行程及任務開始。每次變更會先寫入本機，再排入 Firestore 寫入。Firestore 權限或連線錯誤不會提供即時雲端同步保證。

## 資料格式

資料文件包含 `events` 與 `tasks` 陣列。行程欄位為 `id`、`title`、`date`、`start`、`end`、`place`、`note`、`reminder`；任務欄位為 `id`、`title`、`date`、`dueTime`、`priority`、`done`、`reminder`。日期格式為 `YYYY-MM-DD`，時間使用 24 小時制；提醒值以分鐘表示（0、5、15、30、60、1440）。

## 專案檔案

- `index.html`：完整前端介面、樣式及互動程式。
- `PRD.md`：依目前程式實作整理的產品需求文件。

本原型尚無伺服器端程式、離線同步佇列、推播通知、外部日曆整合或分析埋點。清除瀏覽器網站資料會刪除本機副本；資料仍以 Firebase Firestore 雲端文件為主。

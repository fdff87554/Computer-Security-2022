# 課堂 Example

* 首先觀看頁面可以看到有一個 `Source` 可以觀看，因此就先觀察一下 Source Code，可以看到 php 裡面有 `source`, `name`, `page` 三個變數，其中 `source` 是用來顯示 `.php` 的原始碼，而 `name` 則會把資料傳遞到 `hi.php` 去做資料顯示，而 `page` 則是會在 `say.php`。
* 因此我們知道我們總共有 `index.php`, `hi.php`, `say.php` 三個頁面，而在 `index.php` 中，我們可以操控的變數叫做 `page`。
* 再往下看，`hi.php` 的頁面會顯示一個 `Welcome,` + name 的頁面，而 `say.php` 則是一個接收 input `name` 然後傳遞給 `hi.php` 的頁面，因此我們這邊還有一個可以操作的變數叫做 `name`。
* 那題目的會用 page 來做 path traversal，因此一樣測試一下是否有辦法操作 LFI，起手式 `?page=../../../../../../../../../../../../etc/passwd`，可以看到成功讀取到 `/etc/passwd` 的內容，結合前面看到的 `name` 變數會被 `$_SESSION['name'] = $_GET['name']`，因此猜測這題可以達到 LFI to RCE。
* 準備好 php 一句話木馬 `<?php system($_GET['cmd']); ?>` 並且讓 `$_SESSION['name']` 去紀錄這個 php 木馬到 session 中，並且讓 LFI 依照我們這題取得的 `session_id=57de771577e80274bc65ae3775a5e5c0` 去 include `/tmp/sess_57de771577e80274bc65ae3775a5e5c0` 讓上面的 system 去執行。
* 確定 payload 被加入 session file 中之後，就可以利用 `?page=../../../../../../tmp/sess_57de771577e80274bc65ae3775a5e5c0&cmd=ls` 去看看我們有沒有拿到 shell，可以看到成功拿到 shell，接著就可以拿到 flag 了。
    > 會用 `&` 是因為 url 上面有兩個參數。

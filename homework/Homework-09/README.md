# 2022 Computer Security HW9 Writeup - Web

* [HW9 github (Writeup and Payload)](https://github.com/fdff87554/Computer-Security-2022/tree/main/homework/Homework-09)

## Hello from Windows 98 - Lab
* 首先先做頁面的觀察跟嘗試，因為題目有直接給 source code 可以做觀看，因此就觀察一下，可以看到全部共有三個頁面，初始頁面 `/index.php`、接收輸入並且建立 session 的 `say.php` 頁面，還有顯示輸入資料的 `hi.php` 頁面。
* 由於題目跳轉頁面的方式是利用 `page` 這個變數接收檔名去做顯示，因此我們這邊嘗試輸入 `?page=../../../../etc/passwd` 來看看環境是否有 LFI 的漏洞，結果發現可以成功讀取檔案，又因為會建立 session，因此我們可以嘗試利用 seesion file 的 LFI 來做 RCE 的攻擊。
* 首先目標是希望 session file 會記錄到我們希望建立的木馬，因此準備 php 一句話木馬 `<?php system($_GET['cmd']); ?>`，並且利用一開始由 server 給我們的 `Set-Cookie: PHPSESSID=dbf1212bbb92456e2882440743c5914d; path=/` 確定我們檔案的 session_id 是 `dbf1212bbb92456e2882440743c5914d`，準備好 php 木馬 跟有 session file 之後，就利用 `../../../../tmp/sess_dbf1212bbb92456e2882440743c5914d&cmd=ls` 作為我們的 LFI payload 看看能不能列出 files，並如下圖成功取得 shell。
    > 會用 `&` 是因為 url 上面有兩個參數。
    > ![web-lab01-php-oneline-shell](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/web-lab01-php-oneline-shell.png)
    > ![web-lab01-php-session-file-LFI](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/web-lab01-php-session-file-LFI.png)
    > ![web-lab01-php-session-file-LFI2RCE](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/web-lab01-php-session-file-LFI2RCE.png)
* 到這裡就可以直接印出我們的 flag.txt 取得 flag: `FLAG{LFI_t0_rC3_1s_e4Sy!}`
    > ![web-lab01-ans](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/web-lab01-ans.png)
`

<!-- https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/ -->
---
###### tags: `CyberSec` `Writeup` `2022`

<style>
.navbar-brand::after { content: " × Crazyfire Lee"; }
</style>
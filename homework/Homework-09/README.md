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


## Whois Tool - Lab
* 這題題目的 source code 非常簡單，就是會把我們的輸入 `host` 串接進 `echo 'whois "{$host}" 2>&1;';`，而且有個限制就是字串輸入不能超過 15 個字元，因此我們的目標就是要找出一個可以 bypass 這個限制的 payload。
* 概念很簡單，我們其實不在意 `whois` 的查找，而且我們希望確保我們的 payload 不會被視為 `whois` 的查找，因此我們建構了 payload `"; ls #` 來分別做到，截斷前面的 whois 查找，並且利用 `;` 做到前一個指令結束之後執行 `ls` 並且利用 `#` 註解掉剩下的部分，可以看到我們的 payload 成功執行了 `ls`，並且可以成功看到有 `flag.txt` 的檔案。
    > ![web-lab02-ls](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/web-lab02-ls.png)
* 基於上面的概念理論上我們可以直接建構 `"; cat flag.txt #` 這樣的 payload 去印出 flag.txt 來取得 flag，但題目設計的非常人性化，這邊個 payload 剛好卡在大於 15 個字元，為了減少字元的使用，這邊決定利用 `*` 萬用字元來避免長度限制，因為同目錄底下沒有其他 f 開頭的檔案了，因此可以直接利用 `"; cat f* #` 來印出 flag: `FLAG{c0mM4nd_1nj3cT10n_';whoami}`
    > ![web-lab02-ans](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/web-lab02-ans.png)
* 那因為我們還知道有其他指令串些的方式如 `&&` 用在前一個指令成功時接著執行的指令，還有 `||` 用在前一個指令失敗時的後一個指令執行的狀況，因此這邊延伸一個 payload 是 `"&& cat f* #`，會是 `&&` 而不是 `||` 的原因是因為 `"` 對 `whois` 指令的截斷，必沒有觸發 `whois` 指令的錯誤 (找不到東西不是一種錯誤，是一種結果)，因此對於我們來說要讓 `cat flag.txt` 被執行到就要利用 `&&` 來達成。
    > ![web-lab02-ans](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/web-lab02-ans-more.png)


## Normal Login Panel (Flag 1) - Lab

## Normal Login Panel (Flag 2) - Lab



---
###### tags: `CyberSec` `Writeup` `2022`

<style>
.navbar-brand::after { content: " × Crazyfire Lee"; }
</style>
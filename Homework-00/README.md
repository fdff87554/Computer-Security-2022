# 2022 Computer Security HW0 Writeup

* [HW0 github (Writeup and Payload)](https://github.com/fdff87554/Computer-Security-2022/tree/main/Homework-00)

## Nine - Reverse

* 這題其實設計的概念跟在更早之前另一個 AIS3 Junior Tonya 設計的 Reverse 題目有點概念類似，只是要用到一些 Reverse 的工具而 AIS3 Junior 有直接給 Source code
* 因此看到的第一時間決定先直接玩玩看，想說會不會有什麼好玩的 bug，結果發現直接發現石頭碰到牆壁會被吃掉，所以在真的去逆向檔案之前就拿到 Flag 了
    > `FLAG{You're_lucky_that_I_have_a_thing_for_pancakes}`
* 因為後續還有第二題 Nine-Revenge，因此還是有看一下檔案，這邊因為很久沒逆向，特別記錄一下整個逆向流程
* 首先一看到檔案想到的就是可以靜態分析看究竟 flag 是哪裡算出來的，或者也想過用動態分析去斷點跳位置
* 因為個人完全忘記動態分析怎麼分析比較好，因此打算先從靜態分析下手，這邊第一時間想到的就是 IDA or Ghidra，剛好朋友有推薦一個對於快速理解檔案資訊很棒的工具 [Detect It Easy](https://github.com/horsicq/Detect-It-Easy) 可以大幅加速對檔案的理解，因此這次用來看了一下檔案
* 從截圖中可以看到畫面正中間就說這個檔案的撰寫跟 .NET 有關係，那到這邊先暫停其他分析工具，因為提到 .NET 的分析工具就會想到 dnSpy 這個好用的工具，因此我們就快速轉戰 dnSpy
    > ![](https://i.imgur.com/bF9OLQd.png)
* 因為剛剛的分析工具也可以發現這個程式是 32-bit 的，所以直接選用 32-bit version 的 dnSpy 比較好做各種操作，打開之後直接往下看可以直接看到 `Stage` 裡面有一個 `Flag()` function，其實感覺非常有計算 flag 的 function 的感覺，但為了避免太快，還是先好好看一下整個 `Stage()`，可以發現幾個對目標比較重要的 function，分別是
    * 計算 flag 的 `Flag()`
    * 判斷是否有取得 flag 的 `StageKeyDown()`
    * 設定玩家初始狀況的 `StageLoad()`
    * 初始遊戲設定的 `initializeComponent()` 等等
* 這邊開始解過這個題目有幾個不同的想法，分別是
    * 因為看到 `Flag()` function 是怎麼算 flag 出來的，因此其實可以直接嘗試把 flag 算出來
    * 因為知道 `StageKeyDown()` function 判定玩家勝利跟初始設定玩家狀態的 `StageLoad()` function 可以調整玩家初始位置，其實也可以算是利用動態 debug 功能繞過石頭們
* 這邊先說利用 debug 的做法（這邊記錄一下這個作法是討論的時候確定的，這邊特別記錄一下以便之後回憶），因為知道目標是吃到"旗"這個位置，打開遊戲可以知道其座標在 `X=5, Y=1` 的位置，因此目標就是在 `playerPosition` 被設定的時候，改成目標座標的左右，這樣就可以，因此右鍵設定 breakpoints 在 stage 的 89 行，也就是 `this.playerPosition = new Point(2, 6)` 的下一行，因為這時候才會有 `this.playerPosition` 的狀態，然後依照截圖那樣把 playerPosition 改成 (4, 1) 就可以在只動一步的狀況下直接碰到 flag，這邊要注意的事情是，調整之後畫面上的"人"的位置並沒有變化，但實際上紀錄的位置已經在指定的座標了
    > ![](https://i.imgur.com/WBnTLnX.png)
* 接下來來說直接另外幹 flag 出來，這邊仔細看 `Flag()` function 可以看到 C# 做了一個 Base64 Convert 而且在這之前做了一個 `substring(1)` 的選擇，去查一下 C# 的 `substring()` funciton 可以知道如果只有一個 integer 則代表從 string 的定位置開始解析， convert 完之後他對整個 convert array 做 xor 135，然後再把整個 array 顯示成 UTF-8 string，也就是我們的 flag，看到這邊我馬上想到的就是用 python 寫一個 decode code 自己算一次出來，但其實有眾多做法，我們一個一個講
    * Python code 解法（我自己的解法），利用下方 Example code 把 flag 算出來，因為知道 substring(1) ，所以 key 直接跳過第一個字元
        ```python=
        import base64

        # key integer nine.exe: LwcvGwPze6PKg9eLY6/Lk7P7Y8+/m89jO2O/m8eLY5tjz7+7p4Njh6PXY9+bp5Obs4vT6
        key = "wcvGwPze6PKg9eLY6/Lk7P7Y8+/m89jO2O/m8eLY5tjz7+7p4Njh6PXY9+bp5Obs4vT6"
        key = base64.b64decode(key)
        tmp = [k^135 for k in key]
        print(tmp)
        for i in tmp:
            print(chr(i), end="")
        ```
    * 無腦直接重跑程式大法，因為其實這個 function 就是完整的 function，我們可以直接用 online C# compiler 跑一次拿答案，完全不用自己轉換
        ```csharp=
        using System;

        public class HelloWorld
        {
            public static void Main(string[] args)
            {
                byte[] array = Convert.FromBase64String("LwcvGwPze6PKg9eLY6/Lk7P7Y8+/m89jO2O/m8eLY5tjz7+7p4Njh6PXY9+bp5Obs4vT6".Substring(1));
                for (int i = 0; i < array.Length; i++)
                {
                    array[i] ^= 135;
                }
                Console.WriteLine (System.Text.Encoding.UTF8.GetString(array));
            }
        }
        ```
    * 無情 CyberChef 大法，完全不用自己那邊開心寫 python
        > ![](https://i.imgur.com/N5w6lHW.png)
* 以上就是關於這題的解題紀錄

## Nine - revenge - Reverse

* 這題一樣先隨手玩一下，但沒有奇怪的 bug 了，因此一樣依照上面的思路去看題目，這邊用改 playerPosition 的可以直接拿到 flag，如果用那如果看 code 分析會需要注意小改幾個地方
    > `FLAG{The_stone_is_not_fragile_anymore...}`
* `Flag()` function 多了什麼？多了一個 replace，去仔細看 C# 的說明可以知道如果是 string 的狀態會把整個 substring 替換掉，那我們不用為難自己，我們自己先 Replace 好然後一樣丟到剛剛的 Python code 就可以拿到答案了，因為其實就是刪除部分字串而已，或者一樣丟 CyberChef，然後如果一樣用 C# compiler 可以一樣無腦輸出答案。
* 因為流程基本近似，這邊 writeup 不重複紀錄上面第一題解法

## Welcome - Pwn

* 關於這個題目看到的第一刻下意識以為是要玩 buffer overflow，但玩了一下程式之後發現一個很好玩的狀況並且順便對照了一下程式碼，就是當我讀取檔案之後，我使用 write_function 會因為 buf 沒有被淨空而允許我往後面的檔案內容讀取，而且讀的是 chal 這個檔案的 hex，這時候突然想到，可能可以定位一下 flag 的所在位置，所以利用工具拆一下題目給的 chal 並且如下方截圖一樣看到 `flag{}` 的所在位置在於 hex 的 3010 這個地方，正準備開洗的時候看到程式有給一個直接跳到指定 offset 的精美小 function，利用 seek_function 可以直接接換 offset 位置，然後只要搭配 read / write function 應該就可以碰到 flag 的 offset 了，所以直接利用 `1` -> `/home/chal/chal` -> `5` -> `12304` -> `2` -> `3` 這個流程就可以拿到 `flag{CS2022Fall_is_good}`
    > ![](https://i.imgur.com/mGtMg5z.png)

## Let's meet at class - Crypto

* 首先看到整個 codes 第一個想法是應該要幹五個 key，也知道 key 的 range 會是 key_1 2~1000, key_2 1002~2000 以此類推，所以第一個想法是五個 for loop 下去爆炸吧～然後時間一定會炸掉所以沒救了。
* 仔細研究一下有什麼辦法可以解決問題，有聽同學說明可以利用空間換時間，因此開始思考怎麼換，由於公式是 `hint = keys[0] ^ keys[1] ^ keys[2] ^ keys[3] ^ keys[4]`，所以如果我列舉 `keys[4]` 然後看其他 xor 結果能有答案落點在 `keys[4]` 之中，就代表 `keys[4]` 的答案了，依照這個答案同理我們可以先把 `keys[3] ^ keys[4]` 的所有可能性列出來，這樣我們就可以利用三個 for loop 去找到是不是有答案落點在窮舉的 `keys[3] ^ keys[4]` 了。
* 有這樣的概念的那一刻看到出題者佛心的給了 `keys[4] = pow(4668, 65537, p)`，那這樣代表我們的問題只剩下慢慢撞推出 `keys[3] = {pow(i, 65537, p) ^ keys[4] ^ hint for i in range(3002, 4000)}` 這些可能性中，`keys[0][i] ^ keys[1][j] ^ keys[2][k]` 滿足的狀況，很順利的拿到了五把 keys 之後，我們來面對 `enc`
* enc 的計算公式可以知道 enc 其實就是 `flag x k1 x k2 x ... x k5 % p`，但因為有 `% p` 這件事情，我們要消去 k1, k2, k3 就會變得很麻煩，所以利用 `flag = enc * pow(key_0 * key_1 * key_2 * key_3 * key_4, -1, p) % p` 消去 k0, k1, k2, k3, k4，然後拿到 flag
* 最後就是 flag -> FLAG 了，也就是 `long_to_bytes(flag)` 就可以拿到我們的 flag `FLAG{enCrypTIon_wI7H_A_kEy_i5_N0t_secur3_7Hen_h0w_ab0u7_f1ve_Keys}`

## PyScript - Web

* 這題算是比 Crypto 早解的題目，但是因為剛好撞到一些問題題目被作廢了，所以沒有第一時間補 flag 上去平台了，這邊記錄一下看到題目時的想法跟解法。
* 從下方 source 截圖可以看到題目直接把 source code 給我們看了，其中
    * `$flag = file_get_contents('/flag');` 代表著把整個 `/flag` 文件當作字串讀入 `$flag` 這個變數
* 接下來幾個看不懂的東西分別是 
    * `@` 這個錯誤控制運算符會把所有 error message 都壓掉，所以不是什麼有意義的東西
    * `2>&1` 這個則是將轉到 STDERR 的輸出傳遞給與正常輸出相同的輸出
    * `$_FILES["file"]["tmp_name"]` 則是 file_upload 之後生成的 tmp_name 而已
* 看到這邊大致上知道目標是利用一支程式同時做到執行 node JS 的 file read 跟 python3 的 file read 來做到達成 if 條件讓 echo 輸出 flag，


---
###### tags: `CyberSec` `Writeup` `2022`

<style>
.navbar-brand::after { content: " × Crazyfire Lee"; }
</style>
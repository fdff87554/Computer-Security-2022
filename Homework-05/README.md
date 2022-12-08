# 2022 Computer Security HW5 Writeup - Reverse

* [HW5 github (Writeup and Payload)](https://github.com/fdff87554/Computer-Security-2022/tree/main/Homework-05)


## dropper

* 先用 Detect It Easy 看看檔案，可以知道其有被 UPX(3.96) 加殼過，因此需要拆殼
    > ![](https://i.imgur.com/0UZBWMa.png)
* 因為是利用 UPX 加殼，因此先試著用 UPX 來脫殼，如果無法脫殼再開始手動脫殼，好消息是 UPX 有脫殼成功
    > ![](https://i.imgur.com/xbbKvZK.png)
    > ![](https://i.imgur.com/aLKSf56.png)
    * 脫殼後可以看到 DIE 識別出 compiler 是 Microsoft Visual C++
* 之後觀看一下 x64dbg 的運作狀況，來確認是不是有什麼特徵可以操作，但可惜的是，在 system break point 之後，程式就停住了，並且沒有觀察出什麼明顯的特徵，因此換靜態分析。
    > ![](https://i.imgur.com/2ONV4kC.jpg)
* 開始靜態分析之後，可以發現在 main 中，在 105、119、141 快速呼叫了同一個 function 三次，之後又大量的被呼叫到，因此先檢查一下 `sub_140001030` 是在做什麼，而這邊決定回到 x64dbg 觀察一下，因為這樣可以加速知道 function 的實際參數操作狀況，因此在第一次 `call sub_140001030` 的 `200A` 這個位置在 x64dbg 設置 break point 來觀察究竟是執行了什麼操作。
    > ![](https://i.imgur.com/x7GH8aO.png)
* 從下面截圖可以發現 function `sub_140001030` 呼叫了 `Advapi32.dll`，因此可以猜測此 function 是類似 GetProcAddress 的 function。
    > ![](https://i.imgur.com/lT2faZG.png)
* 但是這邊會發現，在中間的部分，有一段區域長得比較不一樣，在 `sub_140001030` 之後多接了 `sub_1400036D0`，進去 function 觀察後會發現裡面有些 std allocate 的東西，因此猜測這邊是包裝字串。
    > ![](https://i.imgur.com/r8RjPyS.png)
* 因為現在 IDA 很多 function 都看不出來，我決定先把所有 `sub_140001030` 能拿回來的 string 都收集之後填到 IDA 最下面看起來就是在做一些判斷的位置，畢竟感覺中間除了正常的檔案名稱以外應該會有些目標的資訊。
    > ![](https://i.imgur.com/toJ2NSJ.png)
    > ![](https://i.imgur.com/Q1T0AFr.jpg)
    * 這邊使用工人智慧把資料全部取出來，可以看到所有的 string 如下圖
        > ![](https://i.imgur.com/edpZnog.png)
* 依據拿到的資料們慢慢填上 IDA 的 function，跟修正部分資料之後，可以看到大致變成如下圖的資料狀態
    > ![](https://i.imgur.com/Fo5FQ4t.png)
* 基本上一開始一堆 if 都是在做加密前的準備，最後將一堆 byte 加密，並寫入到 Windows 的登錄檔，例如 `CryptHashData` 得到猛個雜湊值後，用此雜湊值當作 `CryptDeriveKey` 的參數得到某一把 key。但在進入到處裡 flag 的部分之前，有個超級久的 sleep，因此把 sleep 的指令跳過去，就可以從登錄檔拿到 FLAG `FLAG{H3r3_U_G0_iT_Is_UR_flAg}` 了。
    > ![](https://i.imgur.com/YqHN6Di.png)
    > ![](https://i.imgur.com/zxga8IB.png)
    > ![](https://i.imgur.com/kxyqBI9.png)


---
###### tags: `CyberSec` `Writeup` `2022`

<style>
.navbar-brand::after { content: " × Crazyfire Lee"; }
</style>
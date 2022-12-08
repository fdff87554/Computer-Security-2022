# 2022 Computer Security HW4 Writeup - Reverse

* [HW4 github (Writeup and Payload)](https://github.com/fdff87554/Computer-Security-2022/tree/main/Homework-04)

## ooxx

* 這題一樣抱持著設計者絕對不壞，不會拆了我的電腦的心態直接打開檔案，可以看到是一個 ooxx 的遊戲，玩完之後可以看到會出現彈出視窗並且寫 o / x wins 這樣的字樣，回顧這次的課程可以知道這東西就是 `MessageBoxA` 在處理的，因此我第一個鎖定的部分就是 `user32.dll` 中的 `MessageBox` 相關部分。
* 先打開 x64dbg 來看一下發生了什麼事情，在符號裡面選 `user32.dll` 然後搜尋 `MessageBox` 把所有的 `MessageBox` 都選起來設定中斷點
    > ![](https://i.imgur.com/AwVnxcO.png)
* 設完中斷點之後執行並玩一次遊戲可以發現他確實在 `MessageBoxA` 的位置被中斷了，但是這邊有一個重點，就是這個中斷已經是準備整理 Windows 視窗的資訊了，也就是已經進入了 `MessageBoxA` (可以從旁邊的 FPU 視窗看到對應的東西都已經準備好了)，但我希望我留存的位置是在進來準備 `MessageBox` 之前，因此這個位置應該就不是我想要的，但重複玩了幾次都沒觀察到更好的資訊，因此決定開 IDA 來看一下。
    > ![](https://i.imgur.com/Dxbzzvf.jpg)
* 打開 IDA 一樣先看一下 string，因為我們有其實已經知道 `MessageBox` 會顯示例如 `x win` 這種字串，理論上這些字串的顯示區域就是我們的目標了，但事與願違，在 string 裡面除了 `Resul` 這個字串以外，沒有其他跟 Windows 視窗顯示有關係的字串，所以只能慢慢找資料從哪裡出現的了。
* 從 entrypoint 這邊的操作觀察發現，在看過第 17 行的 function 後，裡面感覺已經是程式在處理資料顯示的部分，從 16 行則感覺是處理資訊的部分，而在 `sub_140001C50` 這個 function 中又可以發現其 Return 的 function `sub_1400017F0` 裡面用到了 `MessageBoxA`，對應回去剛剛動態分析觀察到的狀況，資訊在計算完之後，會呼叫 `MessageBoxA` 對 Windows 畫面做準備，因此把目標放在這邊，猜測這邊就是把所有訊息準備出去的位置。
    > ![](https://i.imgur.com/KAMk0fd.png)
    > ![](https://i.imgur.com/Aq76SHx.png)
    > ![](https://i.imgur.com/WyY8W5M.png)
* 但到現在還沒找到究竟字串是在哪裡處理的，然後看到下面既然那麼多 if 而且還做 xor(在 function sub_140001480)，就猜想會不會是在這裡處理字串，拿到了 `X Win!`
    > ![](https://i.imgur.com/FyYnbJm.jpg)
* 到這裡我就猜測這個部分真的就是處理所有的輸出了，觀察了一下下面的 if else 應該分別處理了平手跟 o 勝利的字串，但 else if 裡面在 `MessageBoxA` 之後又額外做了一些事情，感覺就很像在準備我們的 flag Owo，因此直接把目標放在希望跳到這個位置執行，所以回到了 x64dbg 我直接 jump 到 `18CA` 並且把 EIP 指向這邊直接執行(其實是指向他的前面 `18C0` 因為這邊才會準備對應的資料)，先把斷點設定在整個 function 的起始位置 `17F0`，執行並卡在 `17F0` 後 EIP 跳到 `18C0` 並且再次執行就可以拿到 FLAG `FLAG{Y0u_Won_A_gaM3_yoU_cOuldn0T_pO5s16ly_w1n}` 了
    > ![](https://i.imgur.com/Zm1VRWb.jpg)
    > 
    > ![](https://i.imgur.com/wLmhbYB.jpg)
    > 
    > ![](https://i.imgur.com/0Oq7plp.png)
    > 
    > ![](https://i.imgur.com/8IbMfdH.png)

## trojan

* 這份作業裡面有包含了一個封包檔案，打開來之後先用 Follow 裡面的 TCP Stream 裡面看到從我方有送出一個 `cDqr0hUUz1` 的部分給惡意的 Server(這是唯一從本地網外送的東西)，因此這個 string 就算是我的 keyword 了。
* IDA 開檔案，一樣 string 查詢 `cDqr0hUUz1` 有發現這個 string 的存在，從 code 裡面挖到之後看到資料有做了一個 xor `0vCh8RrvqkrbxN9Q7Ydx`，那在觀察資料的過程中也有發現，他會回傳一個 png 檔案給我，並經過這個 xor 變成圖片儲存起來，因此我們就 dump 回傳的封包然後 xor 這個字串。
* 這邊有一個小小小小的問題，就是為什麼明明字串是 length 20 但是 mod 21 呢？因為其實字串最後有一個 `0x00` 做結尾(花了我半天)，所以要在字串結尾加入 `0x00`，自己寫了個 payload 拿到 flag
    > ![](https://i.imgur.com/2zYgPHq.png)
    ```python=
    tmp = "0vCh8RrvqkrbxN9Q7Ydx"
    keys = [ord(t) for t in tmp]
    keys.append(0x00)


    with open('tmp.txt', 'r',encoding="unicode_escape") as fp:
        inp = fp.read()
        # hex_list = ["{:02x}".format(ord(c)) for c in fp.read()]

    hex_list = bytes.fromhex(inp)

    answer = []
    for i in range(len(hex_list)):
        ans = hex(hex_list[i] ^ keys[i%21])[2:]
        if len(ans) == 1:
            ans = "0" + ans

        answer.append(ans)
    print("".join(answer))
    ```





---
###### tags: `CyberSec` `Writeup` `2022`

<style>
.navbar-brand::after { content: " × Crazyfire Lee"; }
</style>
# 2022 Computer Security HW3 Writeup - Reverse

* [HW3 github (Writeup and Payload)](https://github.com/fdff87554/Computer-Security-2022/tree/main/Homework-03)

## Sacred Arts

* 在 Reverse 這件事情的過程中，我的理解是就是逐步搜集資料並且藉由收集資料的過程慢慢發現蛛絲馬跡把資料挖出來，因為理解我拿到什麼這件事情很重要
* 這個題目給了我一個 `sacred_arts_1d2c7a15746e1a82` 的檔案，這時可以先用 `file` 這個指令對這個檔案有基礎的認識，可以拿到如下圖的資料並且知道
    * 這是一個 64 bits 的 ELF (Executable Linkable Format) 檔案
    * libc 函數的調用為 statically linked 代表是已經 linking 好的檔案，不會執行過程中才由 OS 做 linking
    * `stripped` 代表 debugging 相關的資料都被整理乾淨了
    > ![](https://i.imgur.com/ivPuknO.png)
* 那我們這邊用 IDA 打開程式之後，可以看到左邊空空沒有任何的 functions，所以我們也沒有所謂的 main function 可以特別看結構，用 f5 看 pseudocode 也發現沒辦法，那既然都沒有要乖乖看組語之前，我們可以先用 shift + f12 看所有的 strings，有發現有三個
    > ![](https://i.imgur.com/Yarjdh0.png)
* 對於我們來說，我們要盡量往可能找得到判斷式 or flag 的地方，那既然有一個 `/tmp/flag` 我們就先看一下，進去之後可以發現他們只是一個資料載入，並沒有特別的資料，因此我們慢慢往下看
    > ![](https://i.imgur.com/tjbzegm.png)
* 可以看到剛剛第二個 string `wrong` 就下在下面，因此可以發現應該會有判斷的過程了，因此決定先飛到 correct 的 `hello world` 字串
    > ![](https://i.imgur.com/ItUyZyq.png)
* 到這邊直接發現 `hello world` 這個字串上面有一個很神奇的 loop 還有 cmp，而且 cmp 如果比較出問題會跳到剛剛看到的 `wrong` string 的位置，因此仔細看的一下究竟這個位置做了什麼
    > ![](https://i.imgur.com/gFTRQvS.png)
* 可以看到 `mov rax, [rsp+rdx]` 去拿上面 offset 的資料，然後把資料塞到 `rax`，然後 `rax` 會先做一次 `neg`(2's negative)，然後再做 `al, ah` 的 exchange，然後去比較有沒有跟剛剛 load 進來的 `byte_40108B` 資料的 offset 值一樣，因此我們可以發現我們的目標就是他剛剛 load 用來檢查資料的那串好朋友
* 回到 `byte_40108B` 可以看到理論上預期他應該是一個 array，那這時候上課老師有講過可以利用快捷鍵 `D` 去調整 data size，把它調成 qward，而且我們也知道他應該是一個 array，直接右鍵選 `Array` 去調整 array_size = 7, ithems on a line = 1, Element print with = -1，就可以拿到一個乾淨的 array
    > ![](https://i.imgur.com/hzHbjqo.png)
    > ![](https://i.imgur.com/qGSjLw1.png)
* 那我們就直接把這串 array 也就是我們的目標返做一次操作拿 flag 試試看，payload 如下
    ```python=
    keys = [0x8D909984B8BEBAB3, 0x8D9A929E98D18B92, 0x0D0888BD19290D29C, 0x8C9DC08F978FBDD1, 0x0D9C7C7CCCDCB92C2, 0x0C8CFC7CEC2BE8D91, 0x0FFFFFFFFFFFFCF82]

    for i in range(len(keys)):
        tmp = hex(keys[i])[2:]
        tmp = tmp[:12] + tmp[14:] + tmp[12:14]
        keys[i] = int(f"0x{tmp}", base=16)

    for i in range(len(keys)):
        print( bytes.fromhex(hex(~keys[i] + 1 & 0xFFFFFFFFFFFFFFFF)[2:])[::-1].decode('utf-8'), end='' )
    ```
* 可以拿到 flag `FLAG{forum.gamer.com.tw/C.php?bsn=42388&snA=18071}`


## Why

* 一樣先用 `file` 取得程式的基本資訊，如下圖
    > ![](https://i.imgur.com/o30dTly.png)
* 那這題很棒棒的有 function，那這題直接看到 main function 裡面有一個 for 迴圈而且底下有一個 if 再做判斷，進去 enc_flag 可以看到一串好棒棒的資料，直接拿去做 + 10 推 buf 就可以拿到 flag 了，payload 如下
    ```python=
    key = [0x50, 0x56, 0x4B, 0x51, 0x85, 0x73, 0x78, 0x73, 0x7E, 0x69, 0x70, 0x73, 0x78, 0x73, 0x69, 0x77, 0x7A, 0x7C, 0x79, 0x7E, 0x6F, 0x6D, 0x7E, 0x2B, 0x87]
    for k in key:
        print(chr(k-10), end='')
    ```
* 可以拿到 flag `FLAG{init_fini_mprotect!}`
* 那這題其實希望告訴我們的部分是，程式在運行的過程前跟後其實有兩個區域，一個是 init 跟一個 fini，這兩個區域其實是可以放置資料的。

## Trace

* 這份 code 一打開再 main 那邊長得很可愛之外，可以點進去第一個 function 就看到他做了寫檔案的動作
    > ![](https://i.imgur.com/sqsXMq3.png)
* 直接找 `unk_4020` 可以看到 ELF，所以代表這個程式自己有他寫出去的程式的整個程式碼，因此我們直接先把他要寫出去的程式碼偷出來，利用 IDA 的 `idc.savefile(filename, 0, startAddress, size)` script 去把整個區段 dump 出來，dump 出來之後先去看一下這份檔案裡面藏了什麼，這們隱密
* 打開檔案就看到紅字，然後就看到一個註解 `; Trap to Debugger` 跟兩個 call 包著 int 3, endp 這樣的特徵，查了一下就是類似 debugger 被下斷點的作法，會把程式卡在這個 int 3 的特徵點，來做到 break point 的效果，那看到這邊在想著如果把這個部分著解掉是不是程式可以往下正常解析，因此就慢慢的把有這樣的部分都註解掉，而且中間利用 undefined 跟 code 去把 asm 慢慢還原往下推，這時候看到了一個 unk 在這邊做了 cmp，經過前面題目的訓練，有特殊的 xor 又有 cmp 就值得特別 decode 看看，因此就利用很簡單的 payload 解析了，結果就拿到 flag `FLAG{TrAc3_M3_1F_U_cAN}` 了
    > ![](https://i.imgur.com/ueaUZ8E.png)
    ```python=
    tmp = [0x37, 0x3D, 0x30, 0x36, 0x0A, 0x25, 0x3, 0x30, 0x12, 0x42, 0x2E, 0x3C, 0x42, 0x2E, 0x40, 0x37, 0x2E, 0x24, 0x2E, 0x12, 0x30, 0x3F, 0x0C, 0x0]

    for i in range(len(tmp)):
        tmp[i] = tmp[i] ^ 0x71

    print("".join([chr(i) for i in tmp]))

    ```


---
###### tags: `CyberSec` `Writeup` `2022`

<style>
.navbar-brand::after { content: " × Crazyfire Lee"; }
</style>
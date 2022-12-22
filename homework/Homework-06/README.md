# 2022 Computer Security HW6 Writeup - Pwn

[![hackmd-github-sync-badge](https://hackmd.io/95hGb9pqTd2YIGBXq37MBA/badge)](https://hackmd.io/95hGb9pqTd2YIGBXq37MBA)


* [HW6 github (Writeup and Payload)](https://github.com/fdff87554/Computer-Security-2022/tree/main/Homework-06)

## got2win - LAB
* 觀察一下程式碼，可以看到說只有一個 main function，
    * 會先於 `line: 13` 建立一個 file descriptor，並且以唯讀的方式開啟 `/home/chal/flag` 這個檔案。
    * 並於 `line: 14` 利用 read function 讀取 `/home/chal/flag` 的內容，並且將內容存入 `flag` 這個 buffer 中。
    * 而後會於 `line: 20` 接收我們的 input，並且會將我們的 input 存入 `addr` 這個 value 中。
    * 之後則會在 `line: 22` 利用 read function 在 addr 中 overwrite `0x8` 也就是 8 bytes 的內容。
    * 最後會在 `line: 25` 又操作了一次 read function 操作到 flag 這個內容。
* 可以注意到在 `line: 25` 中的 read function 中的 fd 是 1 (fd: 0 = stdin, fd: 1 = stdout, fd: 2 = stderr)，也就是說我們可以利用這個漏洞來 leak 出 flag 的內容。
* 先用 `checksec --file=chal` 檢查一下程式的保護機制，可以看到 `RELRO: Partial RELRO`, `Stack: Canary found`, `NX: NX enabled`, `PIE: No PIE (0x400000)`。
    * 因為沒有 PIE，所以我們可以直接用 `objdump -d -M intel chal | less` 來取得程式的 address。
    > ![pwn-got2win-checksec](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/pwn-got2win-checksec.png)
* 那我們的目標就是覆蓋掉 GOT 的 read 改成 write 讓他依照 stdout 的 fd 來輸出 flag 的內容。
* 打開 pwndbg 來找一下 GOT 的狀況，在 pwndbg 中直接輸入 `got` 就會取得 GOT 的狀況，位址會是 `0x404038`。
    > ![pwn-got2win-pwndbg-got](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/pwn-got2win-pwndbg-got.png)
* 用 `objdump -d -M intel chal | less` 來找一下 write@plt 的位址，可以發現 write@plt 的位址是 `0x4010c0`。
    > ![pwn-got2win-objdump-read](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/pwn-got2win-objdump-read.png)
* 那目標就是把 GOT 中的 read 改成 write@plt 的位址，因為這樣就等於實際執行了 write 而不是 read 了。會得到 flag: `FLAG{apple_1f3870be274f6c49b3e31a0c6728957f}`

## rop2win - LAB

* 起手式一樣先檢查 `checksec` 的狀況，如下圖有 Canary, NX, no-PIE (可以直接看 address), Partial RELRO。
    > ![pwn-rop2win-checksec](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/pwn-rop2win-checksec.png)
* 之後觀察一下 source，可以看到有加入 `seccomp` 這個 lib 來保護 syscall 的使用，可以看到只有 `open`, `read`, `write` 這幾個 syscall 可以做使用，其他的 syscall 都會被擋掉。
    > ![pwn-rop2win-source-syscall](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/pwn-rop2win-source-syscall.png)
* 首先先找到 `ROP_addr` 的位址，可以看到 `ROP_addr` 的位址是 `4e3360`，`fn_addr` 則是 `4e3340`。
    > ![pwn-rop2win-pwndbg-ROP_addr](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/pwn-rop2win-pwndbg-ROP_addr-fn_addr.png)
* 現在我們的目標很簡單，就是我們希望利用所有已知可用的操作來把 flag 給印出來，不是像其他題目一樣建立 `sh` 的原因是因為，這題的 `seccomp` 並沒有放行 `execve` 這個 syscall，所以我們只能用 `open`, `read`, `write` 這三個 syscall 來達成目的。
* 對應到這題的 c code，我們知道了有三次的輸入機會，分別是給 filename，拿到 ROP 跟 overflow，因此對於我們來說我們這題就是建構 ROP 去指定出我們需要的 syscall。
    * 操作 ROP 在沒有特殊的情況之下，我們會需要 control `rdi` (for param1), `rsi` (for param2), `rdx` (for param3) 跟 `rax` (for syscall number) 這四個 register，因此我們需要的 gadget 會是 `pop rdi; ret;`, `pop rsi; ret;`, `pop rdx; ret;` 跟 `pop rax; ret;` 這四個 gadget。
    * 而這題因為並沒有 `pop rdx ; ret`，因此我們用 `pop rdx ; pop rbx ; ret` 取代，並注意要特別多 parse 一個 `rbx` 的值。
* 看下面的 payload 可以看到我們主要的目標就是實作出 `open("/home/chal/flag", 0)`、`read(3, fn, 0x30)`、`write(1, fn, 0x30)` 這三個 syscall，其中 `read` 的 `fd` 會是 3 的原因是因為 read() 預設會開 0, 1, 2 三個 fd 也就是 stdin, stdout, stderr，因此我們猜測 fd: 3 會是我們的目標 fd。
    > ```python=
    > # open("/home/chal/flag", 0)
    > # read(3, fn, 0x30)
    > # write(1, fn, 0x30) - stdout
    > ROP = flat(
    >     # open(fd, 0)
    >     pop_rdi_ret, fn_addr,
    >     pop_rsi_ret, 0,
    >     pop_rax_ret, 2,
    >     syscall_ret,
    >     
    >     # read(fd, buf, 0x30)
    >     pop_rdi_ret, 3, # guessed opened file fd
    >     pop_rsi_ret, fn_addr,
    >     pop_rdx_ret, 0x30, 0,
    >     pop_rax_ret, 0,
    >     syscall_ret,
    >     
    >     # write(1, buf, 0x30) --> stdout
    >     pop_rdi_ret, 1, # stdout
    >     pop_rax_ret, 1,
    >     syscall_ret,
    > )
    > ```
* 剩下的操作就直接看 paylaod，就可以看到我們的 flag: `FLAG{banana_72b302bf297a228a75730123efef7c41}`

## rop++ - HW

* 這題是一題非常簡潔的 rop 題目，簡單來說就是要我們建構 rop，所以先用 `checksec` 檢查一下我們可以做哪些操作來取得我們要的資料，看到 Canary found / NX enabled / No PIE，所以可以直接查看 Code Address，直接先用 objdump 找 buf address 跟用 `ROPgadget` dump 出所有的 gadget，然後就可以開始建構 rop 了。
* 因為我們的目標還是建立一個空間來儲存我們輸入的 `/bin/sh` string 並且交由 `execve` 去執行，因此我們需要分兩部，也就是建立好正常的 read() rop 來讀取我們的 `/bin/sh` string，然後再建立一個 rop 來執行 `execve`。
* payload 如下，註解已經詳細說明行為了:
    > ```python=
    > ROP = flat(
    >     # read(0, buf, 0x200)
    >     pop_rdi_ret, 0,             # fd:0 - stdin
    >     pop_rsi_ret, writable_addr, # buf - "/bin/sh" string
    >     pop_rdx_ret, 0x7, 0,        # size
    >     pop_rax_ret, 0,             # syscall - read
    >     syscall_ret,
    >     
    >     # execve("/bin/sh", 0, 0)
    >     pop_rdi_ret, writable_addr, # "/bin/sh"
    >     pop_rsi_ret, 0,             # 0
    >     pop_rdx_ret, 0, 0,          # 0
    >     pop_rax_ret, 0x3b,          # syscall - execve
    >     syscall_ret,
    >)
    > ```
* 依照這樣的 Payload，我們只需要在輸入 `/bin/sh` 之後就可以 get shell 了，拿到 flag: `FLAG{chocolate_c378985d629e99a4e86213db0cd5e70d}`
    > ![rop++-demo-image](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/rop++-demo-image.png)


---
###### tags: `CyberSec` `Writeup` `2022`

<style>
.navbar-brand::after { content: " × Crazyfire Lee"; }
</style>
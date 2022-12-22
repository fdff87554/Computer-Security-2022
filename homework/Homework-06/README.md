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
* 首先先找到 `ROP_addr` 的位址，可以看到 `ROP_addr` 的位址是 ``。
    > ![pwn-rop2win-pwndbg-ROP_addr](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/pwn-rop2win-pwndbg-ROP_addr.png)

## how2know - HW

## rop++ - HW



---
###### tags: `CyberSec` `Writeup` `2022`

<style>
.navbar-brand::after { content: " × Crazyfire Lee"; }
</style>
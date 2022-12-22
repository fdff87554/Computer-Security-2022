# 2022 Computer Security - PWN

* 這個紀錄是關於 PWN 的課程 demo 還有知識點。

## Basic Information
* **E**xecutable and **L**inkable **F**ormat, ELF - Linux 中的執行檔
    * Segment & Section
        * Section - 告訴 Linker 動態連結時所需要的資料
            * 用來區分不同功能的資料，因為不同功能會需要不同的**權限**、**大小**
                * 程式碼屬於 .text section，會需要**執行權限**
                * 常數字串屬於 .rodata section，只需要**讀取權限** 
        * Segment - 告訴 OS 程式被載入時的資訊
    * Memory Layout
        * `.text` - 程式碼
        * `.rodata` - read-only data，如字串
        * `.data` - 初始化後的變數
        * `.bss` - 上未初始化的變數
        * `heap` - 動態分配的記憶體空間
        * `lib` - shared library
        * `tls` - thread local storage
        * `stack` - 用來儲存當前 function 的執行狀態的空間
        > ![Memory Layout](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/memory-layout.png)
    * Protection
        * **P**osition-**I**ndependent **E**xecutable, PIE - 程式碼會以相對位置的方式表示，而非絕對位置
        * **N**o-e**X**cute, NX - `.text` 之外的 section 不會有執行權限
        * stack protector, Canary - 在 stack 的結尾塞入一個**隨機數**，return 前透過檢查是否有被修改來判斷執行是否出現問題
        * **REL**ocation **R**ead-**O**nly, RELRO - 分成 Full / Partial / No 三種型態，分別代表在 runtime 解析外部 Function 時使用的不同機制
        * **Sec**cure **comp**uting mode, Seccomp - 制定規則來禁止 / 允許呼叫特定的 syscall
        * **A**ddress **S**pace **L**ayout **R**andomization, ASLR - 程式載入時，stack / heap 等記憶體區塊會使用隨機的位址作為 base address
            * 在一定範圍內隨機，且 **末 12 bits** 是固定的，每次載入不會更動
* **G**lobal **O**ffset **T**able - GOT
    * 當執行檔是**動態鏈結**時，會是用 GOT 這個 table 來存放外部 function 在執行期間所 bind 到的所有位址。
        * 其初始時會先存放**用來 resolve function 的程式碼**的位址
        * 當 resolve 完成後，會將這些位址替換成**真正的 function 位址**。
    * 而在呼叫這些外部 function 時，會執行 PLT (Procedure Linkage Table) 中的程式碼 (跳板程式)，這些程式碼會先去 GOT 取出對應 symbol entry 的值做執行。
    * 為了避免浪費在初始化時就一次載入大量的外部 function 而造成的效能問題，因此在執行期間才會去 resolve。
    * 這種動態載入位址的方式也被稱為 **lazy binding**。
    * Exploit:
        * **GOT hijacking** - 可以透過 **overwrite GOT entry** 來控制執行流程。
        * **Ret2plt** - 控制執行流程到 **function@plt**，也代表執行該 function (以 functionA 代稱)
        * **Leak libc** - functionA 在被解析後，GOT 會存放 functionA 的絕對位址，因此如果可以讀取 GOT，就能得到位於 libaray 當中的 address。
            * FunctionA 的絕對位置減去他在 Lib 當中的 offset，能得到 libaray **base address**，繞過 **ASLR**。
        * **Ret2libc** - 有了 library base address，也能加上其他 function 的 offset 來取得其他 function 在 library 中的位址 (以 functionB 代稱)
            * 藉由控制程式流程，讓程式跳到 functionB 上，意即執行此 functionB。


## BOF

* Mitigation - canary (stack guard)
    * 啟用 canary 後，OS 會在載入程式時，在 TLS 當中 offset `0x28` 的位置，放置 8 bytes 的隨機數，該值就稱作 canary。
    * 當程式執行到 `ret` 時，會先檢查 stack 上的 canary 是否被修改 (跟 TLS 記憶體的值是否相同)，如果被修改 (代表發生 stack overflow)，則會直接結束程式。
    * 但因為 canary 的第一個 byte 必定為 00，所以可以利用這個特性來 bypass canary。
    * fs register - 用來存放 TLS 的 base address，雖然存取 fs 取得 TLS address 是 OS 做的，本身 fs 的值是 0，因此 TLS 的位址並不是那麼好找，但因為 runtime 時 TLS 與 lib 在 **多數情況下** 有固定的 offset，因此可以透過 debugging 取得 offset，打 exploit 時就可以直接利用加減 offset 來取得 TLS address。
    * gdb debugging 時，取得 TLS address 的方法有:
        * `pwndbg> tls`
        * `pwndbg> search -8 <canary>`
        > canary 的值可以透過查看 function prologue 跟 epilogue 來找到，或是直接用 pwndbg 中下 canary 也可以。
    > ![using canary and without canary](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/canary-example.png)
* Mitigation - memory randomization
    * 過去的程式碼因為 address 都是固定的，因此只要能控制執行流程，就可以直接控制程式執行，因此會有 buffer overflow 的問題。
    * 因此提出了 memory randomization，讓程式碼的 address 都是隨機的，編譯時將程式內的資料以相對位置儲存。
    * **每次執行時會加上一個隨機的 base address，此時資料的絕對位置才會被確定**。
    * 雖然每次的 base address 不相同，但資料的 offset 都是固定的，因此可以透過這個特性來取得資料的絕對位置。
    * 分別在 **應用程式層** 跟 **作業系統層** 來實施:
        * PIE (Position-Independent Executable) - 隨機化執行黨載入時的 base address
        * ASLR (Address Space Layout Randomization) - 隨機化所有需要重新定位 (relocation) 的記憶體區塊如 stack、library、heap 等的 base address。
    * 只要沒有開啟 ASLR 的情況下，即使程式開啟 PIE，也會因為每次產生的 **base address 相同**，保護效果跟沒有開 PIE 一樣。
        > ```bash=
        > # disable aslr
        > echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
        > # enable aslr
        > echo 2 | sudo tee /proc/sys/kernel/randomize_va_space
        > ```
* Mitigation - GOT
    * **Lazy binding** 在保護機制 RELRO 為 **Partial RELRO** 的情況下才會執行。
    * **No RELRO** - 初始化時，GOT 當中直接儲存 function 的 address，並且 GOT 存在於**可讀可寫權限 (rw-) 的 segment**
    * **Full RELRO** - 初始化時，GOT 當中直接儲存 function 的 address，但 GOT 存在於**只有讀取權限 (r--) 的 segment**


## ROP
* ROP (**R**eturn **O**riented **P**rogramming) - 透過 return address 來控制程式執行流程，因此可以透過 return address 來執行任意的指令。
    * 因為我們無法執行控制的資料，因此直接使用存在於程式中的指令來執行完成目標行為，而格式為 `<operation>; ret` 的指令可以串起存在於不同位址的指令，在這個過程中使用到的程式碼就叫做 ROP gadget。
        * e.g., `pop rdi; ret, pop rsi; ret, pop rdx; ret` 這三個指令可以串起來執行 `syscall`，因此可以用來執行 `execve("/bin/sh", NULL, NULL)`。
    * 因為參數的傳遞是透過 Register，因此很容易能透過這些 gadget 來控制呼叫 function 前的參數。
* Exploit
    * Target - `sys_execve("/bin/sh", NULL, NULL)`
    * Overflow
    * Control rdi (param1)
    * Control rsi (param2)
    * Control rdx (param3)
    * Control rip (syscall number)
    * syscall

## Demo

### Demo 1 - Basic Stack Overflow `demo_BOF1`

> Env: `gcc -o demo_BOF1 -fno-stack-protector -fno-pie -no-pie demo_BOF1.c` 用來關閉 stack protector 與 PIE

* `demo_BOF1`: 目標碰到 `backdoor()` 這個 function，可以先用 `objdump -d -M intel ./demo_BOF1 | less` 來觀察找到 `backdoor` function 的所在位置，可以看到位置是在 `0011c9`，把 return address 控制成目標的 `401156` 就可以操作到 backdoor function 了，
    > ![Objdump Memory Address for demo_BOF1](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/objdump-memory-address-demo_BOF1.png)
* 利用 `b'a' * 0x10` 來覆蓋掉 `name[0x10]` 的 space，並且把 `return address` 覆蓋成 `backdoor` 的位址，就可以成功執行 `backdoor` 了
    > ![Python Script for demo_BOF1 01](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/python-script-demo_BOF1-01.png)
* 從 gdb 的操作中可以看到我們已經成功進入 `backdoor` function 並且 load 到 `system('/bin/sh')` 了，但這邊會發現指令並沒有被正常執行
    > ![GDB for demo_BOF1 point to backdoor start 01](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/gdb-demo_BOF1-point-to-backdoor-start-01.png)
    > ![GDB for demo_BOF1 point to backdoor start 02](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/gdb-demo_BOF1-point-to-backdoor-start-02.png)
* 原因是因為我們觸發了 glibc rsp 16 bytes 對其問題，在 64 bits 環境下，有些 glibc 版本會預設 stack 位址 要對齊 16 bytes，意即 rsp 的值要能被 16 整除 ，rsp 最後一碼必須為 0。針對這個問題其實目標就是去 +8 or -8 讓 stack 去對齊 0x10，而只要我們略過 `push rbp` 就可以達成這個目的，因為原本的 rbp 跟 rsp 是有對其的，我只要避免 `push rdp` 影響到了這個對其，其實就達到要求了。
    > ![Python Script for demo_BOF1 02](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/python-script-demo_BOF1-02.png)
    > ![GDB for demo_BOF1 point to backdoor start 03](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/gdb-demo_BOF1-point-to-backdoor-start-03.png)
    > ![GDB for demo_BOF1 point to backdoor start 04](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/gdb-demo_BOF1-point-to-backdoor-start-04.png)


### Demo 2 - Stack Overflow with Canary `demo_BOF2`

> Env: `gcc -o demo_BOF2 -fstack-protector -fno-pie -no-pie demo_BOF2.c` 用來開啟 stack protector 與關閉 PIE

### Demo 3 - ROP gadget `demo_ROP`

* 利用 `ROPgadget` 這個 tool 來取得所有的 ROP 狀況，command 如下
    > `ROPgadget --multibr --binary ./demo_ROP`
    * 但我這邊不確定是不是編譯的過程中有開到什麼 security feature，沒有拿到期望的 `pop rdi` 之類的 gadget

### Demo 4 - ROP with one gadget `demo_one_gadget_with_ROP`

* 可以利用 `ldd` 來檢查 process 所使用的 libc 版本，command: `ldd ./demo_one_gadget_with_ROP`，並找到對應的 one gadget `one_gadget /lib/x86_64-linux-gnu/libc.so.6`
    > ![ldd for demo_one_gadget_with_ROP](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/ldd-demo_one_gadget_with_ROP.png)
    > ![one_gadget for demo_one_gadget_with_ROP](https://github.com/fdff87554/Computer-Security-2022/blob/main/images/pwn/one_gadget-demo_one_gadget_with_ROP.png)



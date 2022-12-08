# 2022 Computer Security HW1 Writeup - Crypto

* [HW1 github (Writeup and Payload)](https://github.com/fdff87554/Computer-Security-2022/tree/main/Homework-01)

## COR - LFSR

* 這個題目主要是在講 Linear Feedback Shift Register (LFSR) 的 Correlation Attack (關聯攻擊)，先順便記錄一下 LFSR 的運作概念。
* LFSR 其實就是一個 Shift Register，但是這個 Shift Register push back 最前面的時候，會受到中間層的影響做 `XOR` 之後回補第一位，所以 Recursive Function 會長 $$S_{i+3} = S_{i+1} \oplus S_{i}$$ for 三層的 LFSR Example。那這邊有個重點就是 LFSR 會有循環的產生，舉例來說如果是三層的 LFSR 最多每七次會做一個循環，原因是因為每一個 FF 的可能性都是 0 or 1，因此三層的 LFSR 最多會有八種組合，但因為 `0, 0, 0` 這種組合在 LFSR 中不會有任何改變，也就是他屬於一種特例（怎麼跑都是 `0, 0, 0`），所以最大的循環週期會是 7 次。
* 因為要不要做 `XOR` 的行為是可控的並且是由我們選擇的，其實可以把整個 LFSR 寫成 Polynomial 的形式也就是 $$P(x) = x^{m} + p_{m-1}x^{m-1} + p_{m-2}x^{m-2} + ... + p_{1}x^{1} + p_{0}$$ 其中 $p_x$ 就是我們在控制要 `XOR` 的位置們
* 那我們來看一下題目之後來說明為什麼會造成 Correlation Attack，今天題目給了我們一段這樣的 code 
    ```python=
    class triLFSR:
        def __init__(self, lfsr1, lfsr2, lfsr3):
            self.lfsr1 = lfsr1
            self.lfsr2 = lfsr2
            self.lfsr3 = lfsr3

        def getbit(self):
            x1 = self.lfsr1.getbit()
            x2 = self.lfsr2.getbit()
            x3 = self.lfsr3.getbit()
            return x2 if x1 else x3
    ```
    可以看到輸出交給了三層的 LFSR 去做決定，分別是 x1 究竟是 0/1 決定了輸出 x2 or x3 的 LFSR，所以輸出的 0 / 1 可能是來自 x2 or x3。
* 整個概念看起來沒什麼漏洞，LFSR 的輸出本來就已經由一個 random 生成的長度決定了，然後又由三個 LFSR 決定了最終的輸出，但事實上這樣的輸出是會有問題的，讓我們來看看為什麼。
* 我們假設 Random 生成這件事情產生的 0 / 1 比例是趨近於一半一半的，也就是我們的輸出會有 50% 會是 0, 50% 會是 1，不管 LFSR 的操作狀況怎樣，這件 0 / 1 比例是不會變的，那今天又多了 x1 去選擇是 x2 or x3，代表還會有一半的機率會是 x2 or x3，因此最終的 output 跟 s2 or s3 的相似機率都有約 75% 的相似。
* 我們已經知道產生這樣的相似是有多麽的難，因此我們只要爆破 s2 跟 output 有 7 成左右的相似 and s3 跟 output 有 7 成左右的相似，我們就可以大膽推估其實這就是我們要的 s2 and s3，那既然我們已經有 s2 / s3 了，就可以回推 s1 了。
* 基於上述理由，我們可以先從找出 7 成相似於 output 的 s2 / s3 開始，為了速度問題我們需要準備 cpp 的版本做 LFSR 的運作計算，依照流程先分別先爆破 s2 / s3 拿到 `s2 = 3859549`, `s3 = 5056686` 之後爆破 s1 那到 `s1 = 29402511` 之後轉到 python 利用 s1, s2, s3 拿到當初 XOR 的秘文然後對 output XOR 拿到明文，這邊要注意，因為題目在最後面 200 bit 補了垃圾，因此我們只取前面的 232 bit 回送 bits_to_string 拿明文。
* 拿到 FLAG `FLAG{W0W_you_Kn0w_COR_477ACK}`，payload 請參考 `cor_sol.cpp` & `cor_sol.py`。

## POA - AES

* 這題講的是 AES 的 Padding Oracle Attack，照例我們先來記錄一下 AES 的一些運作。
* AES 是 Block Cipher（區塊加密），也就是會將明文切分成固定長度組配合金鑰去做加解密，而 AES 採用固定 128 bits（16 bytes）的明文配合 AES xxx（xxx 為金鑰長度，如 AES 128 使用 128 bits 金鑰）做區塊加密。
* 那這邊如過要加密任意長度明文，就會因為需準備建構 128 bits 的先決條件而準備一些加工，
    * 加工方式有分 ECB, CBC, CFB, OFB, CTR... mode 去做加工
    * 有 AEAD（Authenticated Encryption and Associated Data）的加工有 CCM, GCM, OCB...
        * AEAD 是
            * Authenticated Encryption（AE）
                * 會多計算一個 MAC（Message Authentication Code）
            * Associated Data（AD）
                * 可以連供一些沒加密的資料一起做 Authentication，Ex: Header Information
* 那接下來就會提到不同加工 Mode 會造成的一些攻擊，分別有 ECB Mode / Cut&Paste, ECB Mode / Prepend Oracle Attack, CBC Mode / Bit-Flipping Attack, CBC Mode / Padding Oracle Attack 等等，那這邊直接記錄一下 CBC Mode 跟 Padding Oracle Attack 還有這題的解題思路，其他筆記會記錄在非作業區。
* CBC Mode 的區塊加密相較 ECB Mode 會更加安全的最主要原因在於每一輪的加密金鑰都依賴於前面的所有明文，相同的區塊明文是有加密出不同的區塊密文的，且整個系統中會有一個 Initial Vector（初始向量）用在對資料做 XOR。
    > ![](https://i.imgur.com/NGrspCz.png)
    > ![](https://i.imgur.com/rnOnzHn.png)
* 這樣的加解密流程可以解讀成每一段明文 or 密文在被加解密的過程都會受到 `當前明/密文` / `前層明/密文` / `Key` 的影響去生成 or 解密接下來的明/密文。
* 那為什麼會有 Padding Oracle Attack 的產生？這個攻擊是在 AES 使用 **`CBC Mode`** 做加密並且搭配 **`PKCS#7 Padding Scheme`** 的時候會，而且伺服器會幫我們解密資料，並且在解密出來的訊息 Padding 錯誤時會噴錯。
* 先來說說 `PKCS#7` 這個 Padding 格式，這個 Padding 格式會依照總共要填補幾個 bytes 會順片填補相同的數字的 byte 幾個，Ex 要填充 5 bytes 的資料就填補 5 個 0x05。那檢查 Padding 錯誤的方式就是抓最後一個 bytes 就會知道共要填補幾個 & 都要填補跟最後一個 bytes 一樣的數字。
* 那為什麼這樣會造成危險呢？首先就是我們完全知道 server 會怎麼回傳 Yes/No 資料給我們，Server 檢查究竟有幾個 Padding 資料時完完全全依賴於最後一個 bytes，如果最後一個 bytes 是 `0x02`，就代表他有 2 個填補且兩個填補都需要是 `0x02`，也就是造成了**明文的期望**被控制了，感覺明文的期望被控制了也還好，AES 應該可以 handle 被爆破的問題...嗎？
* AES CBC Mode 的加解密流程如下圖，我們看解密的過程可以知道我們的未知（目標）明文是密文解密之後生成 Middle Value 並且跟前一段密文做 XOR 取得的。
    > ![](https://i.imgur.com/xZNLzqj.png)
* 剛剛提過 CBC Mode 其實一個區塊的加解密最主要影響操作的部分就是目標區塊 + 目標區塊的前一個區塊兩個區塊互相影響，這也意味著其實我們，如果能操控區塊密文，其實就能操作產生的區塊明文。
* 這會造成什麼大問題，最大的問題在於我們有機會回推剛剛圖片中的 Middle Value，而只要擁有 Middle Value 跟我們必定有的密文，我們就一定能回推正確的明文了，這就是 Padding Oracle Attack 的核心。
    > ![](https://i.imgur.com/QGyFLUx.png)
    > ![](https://i.imgur.com/YApUEYG.png)
* 基於上述原因，又因為我們知道 padding 的格式，我們等於可以依序暴力嘗試出最後一個 padding 的 bytes 並且利用建構自己期望的 bytes 來符合期望的 padding 格式，且利用這樣的特性來直接取得真實明文，而且這件事情最可怕的是我只需要目標區段 + 前一個區段，就可以做了，不需要管其他部分，對於攻擊者來說等於就是一直控制 IV 來影響解析明文成目標型態來取得結果。
* 說完 POA 就可以來看看題目，這次的題目就是一個 POA 只是更簡單直觀的，題目模仿了 POA 的模式，告訴我們只要是 `0x00` 就會往下檢查直到找到設定好的 Padding `0x80`，也就是說我們的建構目標變成了固定的 `0x80`，而當我們要往下找其他 byte 之前，只需要構建成 `0x00` 就會跳過檢查了。
    ```python=
    def pad(data, block_size):
        data += bytes([0x80] + [0x00] * (15 - len(data) % block_size))
        return data
    
    def unpad(data, block_size):
        if len(data) % block_size:
            raise ValueError

        padding_len = 0
        # 重點在這個 for loop，可以看到預期 padding 只會看到 0x00 來做填補跳過 and 0x80 為第一個填補
        # 剩下的 ValueError 跟不是 ValueError 就是 POA 的 Server 的重點，伺服器的回傳狀況
        for i in range(1, len(data) + 1):
            if data[-i] == 0x80:
                padding_len = i
                break
            elif data[-i] != 0x00:
                raise ValueError
        else:
            raise ValueError

        return data[:-padding_len]
    ```
* 針對題目設計跟上面提到的 POA 重點，我們還要稍微注意一件事情就是資料本身產生 `0x00` 造成資料解析跳躍的問題，因此我們把尚未要解析的密文區段的 IV 都用 `0x00` 填補打亂明文解密，就可以確保所有東西都在可以控制的範圍內了，因此從下面的 Payload 可以看到這邊利用這樣的方式來建構 IV Loop 來暴力找尋目標 PT 也就是 `0x80`
    ```python=
    for k in range(1, 256):
        # Create target IV to loop out right PT byte for padding
        if j == 1:
            tmp_iv = b'\x00' * (len(iv) - j) + bytes([k])
        else:
            tmp_iv = b'\x00' * (len(iv) - j) + bytes([k]) + iv[-(j-1):]
        tmp = tmp_iv + ct
    ```
    這邊會直接拿 `iv[-(j-1):]` 來作為 `0x00` 的原因是因為後面是直接把解析出來的答案給替換掉 IV 了，如下
    ```python=
    if b')' in output:
        print(chr(tmp_iv[-j] ^ 0x80 ^ iv[-j]))
        ans.append(chr(tmp_iv[-j] ^ 0x80 ^ iv[-j]))
        if j == 1:
            iv = iv[:-j] + bytes([0x80 ^ k])
        else:
            iv = iv[:-j] + bytes([0x80 ^ k]) + iv[-(j-1):]
    ```
* 拿到 FLAG `FLAG{ip4d_pr0_iS_r3ally_pr0_4Nd_f1aT!!!!}`，payload 請參考 `poa_sol.py`。

## LSB - RSA

* LSB Oracle 是 PSA Attack 的一種特例，這種特例允許我們選擇密文且會洩漏最低位回來給我們。
* 在一次的 RSA 加密中，明文為 m，模數為 n，加密指數為 e，密文為 c。
* 我們可以構造出 $c' = ((2^e) \times c) \% n= ((2^e) \times (m^e)) \% n = ((2 \times m)^e) \% n$，因爲 m 的兩倍可能大於 n，所以經過解密得到的明文是 $m'= (2 \times m) \% n$。
* 我們還能夠知道 $m'$ 的最低位 lsb 是 1 還是 0。因爲 n是奇數，而 $2 * m$ 是偶數，所以如果 lsb 是 0，說明$(2 * m) \% n$ 是偶數，沒有超過 n，即 $m < \frac{n}{2.0}$，反之則 $m > \frac{n}{2.0}$。
* 因此構造密文 $c'' = ((4 ^ e) \times c) \% n$ 可以使其解密後成為 $m'' = (4 \times m) \% n$，判斷 $m"$ 的奇偶性可以知道 m 和 n/4 的大小關係。所以我們就有了一個二分算法，可以在對數時間內將m的範圍逼近到一個足夠狹窄的空間。
* 在 mod 3 的世界其實也是一樣的，只是今天狀況變成解 1/3，所以依照 PPT 的寫法我們可以把 payload 寫完
* 拿到 FLAG `FLAG{lE4ST_519Nific4N7_Bu7_m0S7_1MporT4Nt}`，payload 請參考 lsb_sol.py。

## XOR-revenge

* 這題在觀察之後可以看到 `getbit()` 的部分時做了 Galosi LFSR 並依次吐出當次 Output bit，且總共 output 了 `len(flag) + 70` 次，之後再將前 `len(flag)` 次的 output 跟 flag 做 xor。
* 觀察到 `polynomial: 0x1da785fc480000001` 是 primitive polynomials，也就是會有 Maxium period ，窮舉 state 狀態顯然不行
* 再觀察到沒有受 flag 污染的 output 是最後、共 70 個 bit，若有辦法用上課教的 companion matrix，就有辦法用連續 n 個 output 推出 state。
* 但這樣會有兩個大問題，分別就是
    * Next state 不是單純的 `<< 1`，而是非線性的操作 XOR Poly
    * 只有 "每次 37 次" 的 output，並不是連續的輸出
* 那這邊有幾個東西要注意的就是我們利用 confution matrix 解出來的 flag 其實是被污染過後的 flag，我們要再乘上 `x^{-37 \times flaglen}` 才可以回推 initial state 拿到 flag。
* 拿到 FLAG `FLAG{Y0u_c4N_nO7_Bru73_f0RCe_tH15_TiM3!!!}`，payload 請參考 xor_sol.py。



## dlog - Discrete Logarithm

* dlog 這題主要是在說 Discrete Logarithm（離散對數問題）中一個很特殊的案例，也就是 Pohlig-Hellman 的爆破，這個特殊案例會在當 $\alpha ^x = \beta \ (\mod p)$ 中的 $p - 1$ 是一個極度破碎的 prime 的時候，我們能夠在 $O(\sum i(logn + \sqrt p_i))$ 的時間複雜度之下爆破出我們的目標 x
* 回來看看題目，題目允許我們給自己的 p 跟 b，並且會回傳 `pow(b, flag, p)` 給我們，所以我們拿到的回傳值會是基於我們給的 b, p 生成的 discrete logarithm
* 基於上面說過的，只要我們給的 prime p 能在 p - 1 時越破碎越好，就代表著我們能用合理的時間解出答案，又因為我們能自己給 p，因此對我們來說最重要的事情就是建構 p 這件事情了
* 這邊直接上 code 和對應註解
    ```python=
    # 因為目標是要找到一個非常破碎的 p-1，才能有機會利用 Pohlig-Hellman 去爆破
    # 所以先嘗試生成一個很破碎的 prime p-1 且這個 p-1 長度逼近 1024
    p = 0
    while True:
        p_find = False
        # 利用 getPrime(32) 隨機產生一個 32-bit 的 prime，因為目標長度逼近 1024，所以要產生 32 個
        p_1 = 2
        for _ in range(32):
            p_1 *= getPrime(32)
        
        # 這邊嘗試 10000 次去看這邊不合適的原因是不是因為用來補長度的 prime 不合適
        # 如果 10000 次都沒拿到答案則從生成 p-1 開始重來
        for _ in range(10000):
            # 由於 getPrime(32) 並不一定會產生出 32-bit 的 prime，所以要利用補另一個 prime 來補足 1024-bits
            p = p_1 * getPrime(1024 - p_1.bit_length()) + 1
            if p.bit_length() == 1024 and isPrime(p):
                p_find = True
                break
        if p_find:
            break
    print(p)
    ```
* 拿到我們建構的 p 跟任意給一個 b 之後，我們可以拿到 server 回傳的 secret，利用 SageMathCell 我們可以完成下列運算拿到 flag
    ```python=
    p = 111299370064906882197696170883187094864431275880225875107737139146305348587887490923063190779100557914408358898671290623524747281333040982349308354343361847094273643636773104474808861737708391454754116417210576588277182522232336976155604379929949140890264921765884674267255629260614725786856099732616052578427
    b = 2
    secret = 99197481246450929628826249466735868954977694915133311778124497443552359558534747415764014641196098881178869431890803192727048412186116587641905347571746369053299777903830434887561630215725305663204831001330517261494250884316698767105915874515326362633686333161100750242079291896387266394700304776498306107895

    b = Mod(b, p)
    secret = Mod(secret, p)
    flag = secret.log(b)
    ```
* 最後做一個 `long_to_byts(flag)`
* FLAG `FLAG{D0_No7_SLiP!!!1t'5_SM0o7h_OwO}`，payload 請參考 `dlog_sol.py`。

## DH - Diffie-Hellman Key Exchange

* Diffie-Hellman Key Exchange 的概念在於利用 $A = \alpha ^ a(\mod p)$ 跟 $B = \alpha ^ b(\mod p)$ 來交換密鑰 `a, b`，原因在於利用所有東西都在 $(\mod p)$ 底下運行，所以只要有 `A, B` 就能計算共同的 Secret $K = B^a = (a^b)^a (\mod p) = a^{b \times a} (\mod p)$、$K = A^b = (a^a)^b (\mod p) = a^{a \times b} (\mod p)$
* 基於純粹的 DH 來說，理論上應該是沒有什麼漏洞的題目，但我們先來看看題目的 code，從下面的 code 可以看到一開始會先 random 一個 1024 bits 的 p 然後讓我們給一個 g 作為上面對應的 $\alpha$ 底，今天題目有特別檢查 `g == 1` 跟 `g == p-1` 的特例，原因是因為如果今天 `g == 1 or g == p-1`，因為在環底下會造成 `g = 1` 的特例，並且造成後續我們的 A 都會是 1 or -1 的特例產生，連帶造成 B 也會是這樣，因此 flag 會直接印出來，所以可以看到題目有針對 g, A 做檢查來避免這樣的特例產生。
    ```python=
    g = int(input().strip())
    g %= p
    if g == 1 or g == p - 1:
        print("Bad :(")
        exit(0)

    a = random.randint(2, p - 2)
    A = pow(g, a, p)
    if A == 1 or A == p - 1:
        print("Bad :(")
        exit(0)
    ```
* 所以對我們來說直接建構 `g = 1 or g = p-1` 這條對我們來說是捷徑的到路沒了，因為第一個檢查就不會過，那嘗試建構 `A = 1 or A = p-1` 也被完美封鎖了，看起來這個題目應該沒有漏洞了才對，其實就是在這裡。我們唯一在這個題目架構下拿到 flag 的方式就是讓最後的 `pow(A, b, p)` 這邊變成 1 我們才有機會直接拿到 flag，意味著我們需要建構我們的 `B` 符合我們的期望，而題目並沒有檢查 `B == 1 or B == p-1`，所以目標會是 `g != 1 or g != p-1` 且 `A != 1 or A != p-1` 的狀況下 `B == 1 or B == p-1`，那究竟可以怎麼做到這件事情呢？我們可以玩一個對賭遊戲來試試看。
* 我們今天的能操控的是一個 random 產生的 p 跟一個我們可以輸入的 g，我們今天先讓 `g = pow(x, (p - 1) // 3, p), x is any number` 這樣可以有什麼效果就是我一定能繞過 `g == 1 or g == p-1` 的檢查，且有機會繞過 `A == 1, A == p-1` 的檢查並且在 `B` 有 2/27 的機率堵到 `B == 1`
* FLAG `FLAG{M4yBe_i_N33d_70_checK_7he_0rDEr_OF_G}`，payload 請參考 `dh_sol.py`。


## node - Elliptic Curve Discrete Logarithm Problem

* node 這題橢圓曲線的離散對數問題(Discrete Logarithm Problem with Elliptic Curves, ECDLP)，先基本說明一些先備知識
* 橢圓曲線（Elliptic Curve）
    * 橢圓曲線的定義其實有分成**實數域**和**循環群**上的橢圓曲線，
        * 實數域上的橢圓曲線：給定兩實數 $a, b$，我們定義**實數域**上的橢圓曲線是**平面上**滿足 $y^2 = x^3 + ax + b$ 的實數點集合。
        * 循環群上的橢圓曲線：給定一個質數 $p$ 以及兩整數 $a, b \in \mathbb{Z}_p$，我們定義**循環群**上的橢圓曲線是**平面上**滿足 $y^2 = x^3 + ax + b (\mod p)$ 的整數點 $(x, y)$ 以及一個無窮遠點所形成的集合。
* 橢圓曲線的離散對數問題(Discrete Logarithm Problem with Elliptic Curves, ECDLP)
    * 在給定一個橢圓曲線 E 以及一個循環群 $(G, )$ 並以 P 代表其中一個可以透過運算元生成整個群的元素;以 T 代表群的任意一個元素。橢圓曲線的離散對數問題是指：
        * 給定 P 和 T，求最小的 d 使得 P 加了 d 次之後等於 T。
    * 在加密系統中，T 就是公鑰，而 d 就是私鑰。
* 那從 code 可以看到題目開頭就有給我們
    * $a, b$: 橢圓曲線的係數
    * $p$: prime
    * $x, y$: 橢圓曲線原點, P
    * $F_x, F_y$: 橢圓曲線原點斜率交點 dP, Q
* 那由於我們知道 ECDLP 在 $4a^4 + 27b^2 = 0$ 時，此橢圓曲線會變成 Singular 且 ECDLP 的難度會快速下降，因此我們先來檢查一下 `a, b` 有沒有符合，可以發現有，因此這題 EC 是 Singular 的
* 那 Singular point 又會有兩種 Type，
    * Node: $y^2 = (x - \alpha)^2(x - \beta)$
    * Cusp: $y^2 = x^3$
    
    為了檢查是哪種 Type，很簡單的用 `print(x ** 3 == y ** 2)` 就可以直接檢查是不是 Cusp Type 了，這邊很開心的是 `False`，也就是跟題目一樣，他是 node type
* 那我們知道 node type 可以把原本的橢圓曲線公式 $y^2 = x^3 + ax + b$ 轉換成 $y^2 = (x - \alpha)^2(x - \beta)$，那我們稍微快樂的計算一下可以得到 $\alpha = 1, \beta = -2$，那 node type 在取得 $\alpha, \beta$
* 我們知道 node type 新定義了函式 $\phi(P(x, y)) = \frac{y + \sqrt{\alpha - \beta} (x - \alpha)}{y - \sqrt{\alpha - \beta} (x - \alpha)}$，且又知道如果我們有 homomorphism 性質 $\phi(P + Q) = \phi(P) \times \phi(Q)$ 就代表 $\phi(dP) = \phi(P)^d$
* 那當我們成功可以把問題簡化成 $\phi(P)^d$ 之後，就有辦法利用 Pohlig-Hellman 去解這題題目了，所以依照定理我們把 code 寫出來並給 sage 幫我們解 `.log`
```python=
def phi(x, y):
	a = Mod(1, p)
	b = Mod(-2, p)
	
	val = sqrt(a-b) * (x-a)
	cal = (y + val) / (y - val)

	return cal

p = 143934749405770267808039109533241671783161568136679499142376907171125336784176335731782823029409453622696871327278373730914810500964540833790836471525295291332255885782612535793955727295077649715977839675098393245636668277194569964284391085500147264756136769461365057766454689540925417898489465044267493955801
x, y = 101806057140780850544714530443644783825785167075147195900696966628348944447492085252540090679241301721340985975519224144331425477628386574016040358648752353263802400527250163297781189749285392087154377684890287451078937692380556192126971669069015673662635561425735593795743852141232711066181542250670387203333, 21070877061047140448223994337863615306499412743288524847405886929295212764999318872250771845966630538832460153205159221566590942573559588219757767072634072564645999959084653451405037079311490089767010764955418929624276491280034578150363584012913337588035080509421139229710578342261017441353044437092977119013
x, y = Mod(x, p), Mod(y, p)
F_x = 98015495932907076864096258407988962007376328849899810250322002325625359735922937686533359455570369291999900476297694445557845368802830788062976760815467239661283157094425185337540578842851843497177780602415322706226426265515846633379203744588829488176045794602858847864402137150751961826536524265308139934971
F_y = 87166136054299272658534592982430361675520319206099499992529237663935246617561944716447831162561604277568397630920048376392806047558420891922813475124718967889074322061747341780368922425396061468851460185861964432392408561769588468524187868171386564578362923777824279396698093857550091931091983893092436864205
F_x, F_y = Mod(F_x, p), Mod(F_y, p)
flag = phi(F_x, F_y).log(phi(x, y))

print(flag)
```
* FLAG `FLAG{I_h3arD_th47_ECDlp_1s_h4rDEr_THaN_dlp}`，payload 請參考 `node_sol.py`。

---
###### tags: `CyberSec` `Writeup` `2022`

<style>
.navbar-brand::after { content: " × Crazyfire Lee"; }
</style>
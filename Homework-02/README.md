# 2022 Computer Security HW2 Writeup - Crypto

* [HW2 github (Writeup and Payload)](https://github.com/fdff87554/Computer-Security-2022/tree/main/Homework-02)

## AES - Side Channel Attack

* 這次的題目是關於 Side Channel Attack 的題目，關於這題題目主要是利用側錄硬體實際計算 AES 加密的過程中因為加密執行差異造成的能耗等不同，來推算 AES 加密過程中的金鑰來取得敏感資料，那對於旁通道攻擊其實是這類型攻擊的通稱，不僅限於 AES 加密，只是這次的題目剛好是 AES-128 的攻擊。
* 那這次的題目是利用 DPA (Differential Power Analysis) 的概念去做操作，主要攻擊點有兩個，分別是首輪加密前（搭配 pt）跟最後加密後（搭配密文），可以是手上有的資料去做攻擊點的選擇
* 那 DPA 的整個操作流程可以分成五個部分，首先是
    * 選擇分析的中間值
    * 量測功耗狀況
    * 計算假設的中間值
    * 把假設的中間值映射到假設功耗
    * 把假設功耗跟真實功耗做比較
* 我選擇分析開始，也就是 pt 搭配 pm 做分析，因此我麼中間值的選擇位置會是 pt 做完 subbytes 之後，做 ShiftRows 之前的位置，而我們也取得了功耗量測得數據，也就是 50 比數據，且有 1806 個特徵點
* 那因為我們要做 subbytes 的操作，因此要先準備 sbox 的替換矩陣 `payload line: 5~20`
* 針對 16-bytes 的 key 來說，逐個 bytes 會對照每個 plaintext 的 i-th bytes 做相同的步驟的解析，那我們搭配 payload 的操作說明
    * 第一步取得 i-th byte 的明文並且取得 hypothetical intermediate values, `payload line: 101, 104`
    * 利用 Hamming Weight 作為 Power Analysis Model 計算 hypothetical intermediate values 的 Power Model `payload line: 107`
    * 利用計算出來的 Power Model 跟實際的功耗計算出假設功耗 `payload line: 110`
    * 找到功耗最大值所在的 key 位置即是我們希望的 key `payload line: 113`
* 這樣就可以取得我們要的 FLAG `FLAG{18MbH9oEnbXHyHTR}`
* 這題其實就是造著 PPT 中的操作邏輯逐步撰寫就可以取得 FLAG 了

---
###### tags: `CyberSec` `Writeup` `2022`

<style>
.navbar-brand::after { content: " × Crazyfire Lee"; }
</style>
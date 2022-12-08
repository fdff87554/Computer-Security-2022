#include "<bits/stdc++.h>"

using namespace std;

// class of LFSR, this version not need the int2bit convert to save time
class LFSR {
private:
    int seed;
    vector<int> taps;
    int length;
public:
    LFSR(int seed, vector<int> taps, int length) {
        this->seed = seed;
        this->taps = taps;
        this->length = length;
    }

    int getbit() {
        int new_bit = 0;
        int ret = state & 1;

        for (auto i: taps) {
            new_bit ^= !!(state & (1 << i));
        }
        state = (state >> 1) | (new_bit << (length-1));

        return ret;
    }
};



int main() {
    // output array from the question
    int output[] = {1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1};

    // LFSR taps from question
    vector<int> t_1 = {0, 13, 16, 26};
    vector<int> t_2 = {0, 5, 7, 22};
    vector<int> t_3 = {0, 17, 19, 24};

    // // s2: 3859549
    // for (int i = 0; i < (1<<23)-1; i++) {
    //     int cnt = 0;
    //     LFSR lfsr(i, t_2, 23);
    //     for (int i = 0; i < 232; i++) {
    //         lfsr.getbit();
    //     }
    //     for (int i = 0; i < 200; i++) {
    //         if (lfsr.getbit() == array[i + 232]) {
    //             cnt += 1;
    //         }
    //     }
    //     if (i % 100000 == 0) {
    //         cout << i << endl;
    //     }
    //     if (cnt >= 200 * 0.7) {
    //         cout << "finish: " << i << endl;
    //         break;
    //     }
    // }

    vector<int> s2;
    LFSR lfsr_2(3859549, t_2, 23);
    for (int i = 0; i < 432; i++) {
        s2.push_back(lfsr_2.getbit());
    }

    // // s3: 5056686
    // for (int i = 0; i < (1<<25)-1; i++) {
    //     int cnt = 0;
    //     LFSR lfsr(i, t_3, 25);
    //     for (int i = 0; i < 232; i++) {
    //         lfsr.getbit();
    //     }
    //     for (int i = 0; i < 200; i++) {
    //         if (lfsr.getbit() == array[i + 232]) {
    //             cnt += 1;
    //         }
    //     }
    //     if (i % 100000 == 0) {
    //         cout << i << endl;
    //     }
    //     if (cnt >= 200 * 0.7) {
    //         cout << "finish: " << i << endl;
    //         break;
    //     }
    // }

    vector<int> s3;
    LFSR lfsr_3(5056686, t_3, 25);
    for (int i = 0; i < 432; i++) {
        s3.push_back(lfsr_3.getbit());
    }

    // s1: 29402511
    for (int i = 0; i < (1<<27)-1; i++) {
        bool flag = true;
        int cnt = 0;
        LFSR lfsr(i, t_1, 27);
        
        for (int i = 0; i < 232; i++) {
            lfsr.getbit();
        }
        for (int i = 232; i < 432; i++) {
            if ((lfsr.getbit() ? s2[i] : s3[i]) != array[i]) {
                flag = false;
                break;
            }
        }
        if (i % 100000 == 0) {
            cout << i << endl;
        }
        
        if (flag) {
            cout << "finish: " << i << endl;
            break;
        }
    }

    return 0;
}

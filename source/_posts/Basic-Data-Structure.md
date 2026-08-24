---
title: "Ch.02 Basic Data Structures"
date: 2026-02-18 17:16:33
tags:
  - "ALGO"
---
# Ch02: 动手写数据结构（基础篇）

## 写在前面

> 1.  本篇博客已完成，内容涵盖多种基本数据结构，包括单链表、双链表、栈、队列、单调栈、单调队列、字典树、并查集、堆和哈希表.
> 2.  ALGO系列附带算法可视化项目工具，github链接如下：[Algorithm-Visualizer](https://github.com/williamllk-ai/Algorithm-Visualizer)，目前支持部分排序算法、数据结构和图上树上问题的可视化.
> 3.  考虑到二叉树涉及内容较多，会单开一个基础数据结构番外篇来讲解.

## 单链表

### 结构简介

> 通过指针（可用数组实现）关联线性表后一节点.

### 基本操作（数组模拟）

1.  **初始化**: `int head, e[N], ne[N], idx;`

    ```cpp
    void init(){
        head = -1;
        idx = 0;
    }
    ```

2.  **加入节点**：`e[idx] = x, ne[idx] = ne[k], ne[k] = idx ++`

3.  **删除节点**：`ne[k] = ne[ne[k]];`

### 模板例题

> 题干：[洛谷 B3631 单向链表](https://www.luogu.com.cn/problem/B3631)

```cpp
//AC代码
//本题无需e数组和idx，值可直接作为下标，只需ne数组即可

#include <iostream>

using namespace std;

const int N = 1000010;
int n, ne[N];

int main(){
    scanf("%d", &n);
    ne[1] = 0;
    while (n --){
        int op, a, b;
        scanf("%d", &op);
        if (op == 1){
            scanf("%d%d", &a, &b);
            ne[b] = ne[a];
            ne[a] = b;
        }else if (op == 2){
            scanf("%d", &a);
            printf("%d\n", ne[a]);
        } else{
            scanf("%d", &a);
            ne[a] = ne[ne[a]];
        }
    }
    return 0;
}
```

## 双链表

### 结构简介

> 一个指针关联后一节点，另一个指针关联前一节点.

### 基础操作

1.  **初始化**：
    1.  `int e[N], l[N], r[N], idx;` r数组模拟右指针，l数组模拟左指针
    2.  `r[0] = 1; l[1] = 0; idx = 2;` 其中0,1作为头尾标记，可根据实际情况改变
2.  **插入右侧**：`e[idx] = x; l[idx] = k; r[idx] = r[k]; l[r[k]] = idx; r[k] = idx ++;`
3.  **插入左侧**:`add_to_right(l[k], x);`
4.  **删除节点**：`l[r[k]] = l[k]; r[l[k]] = r[k];`

### 模板例题

> 题干：[洛谷 B4324 【模板】双向链表](https://www.luogu.com.cn/problem/B4324)

> 题目简析：
>
> 1.  本题节点数值给定是1-N，不存在冲突，无需e数组存储数字，用实际值代表idx即可.
> 2.  本题插入节点方式较为特殊，由题意知需先删除被插入节点，实现过程中只需完成remove和add_to_left函数的实现，其余操作调用这两个函数即可.

```cpp
//AC代码
#include <iostream>

using namespace std;

const int N = 1000010;
const int R = 500005;
int n, m;
int l[N], r[N];

//初始化
void init(int n){
    r[0] = 1;
    for (int i = 1; i <= n; i ++){
        l[i] = i - 1;
        r[i] = i + 1; 
    }
    r[n] = R;
    l[R] = n;
}

//核心函数-remove
void remove(int x){
    r[l[x]] = r[x];
    l[r[x]] = l[x];
}

//核心函数add_to_left
void add_to_left(int x, int y){
    remove(x);
    l[x] = l[y];
    r[l[y]] = x;
    r[x] = y;
    l[y] = x;
}

void add_to_right(int x, int y){
    remove(x);
    add_to_left(x, r[y]);
}

int main(){
    scanf("%d%d", &n, &m);
    init(n);     
    while (m --){
        int op, x, y;
        scanf("%d", &op);
        if (op == 1){
            scanf("%d%d", &x, &y);
            add_to_left(x, y);
        } else if (op == 2){
            scanf("%d%d", &x, &y);
            add_to_right(x, y);
        } else{
            scanf("%d", &x);
            remove(x);
        }
    }
    if (r[0] == R) puts("Empty!");
    else{
        for (int i = r[0]; i != R; i = r[i]){
            printf("%d ", i);
        }
    }
    return 0;
}
```

## 栈

### 结构简介

> 先进后出（FILO）.

### 基本操作

1.  初始化：`int stk[N], tt;` 下标从1开始
2.  push（入栈）：`stk[++ tt] = x;`
3.  pop（出栈）：`tt --;`
4.  query（查询栈顶）：`printf("%d\n", stk[tt]);`
5.  empty（是否非空）：`if (tt > 0) `

### 模板例题

> 题干：[洛谷 B3614 【模板】栈](https://www.luogu.com.cn/problem/B3614)

```cpp
//AC代码

#include <iostream>
#include <cstdio>
#include <cstring>

using namespace std;

const int N = 1000010;

unsigned long long q[N];
int tt, n;

int main(){
    scanf("%d", &n);
    while (n --){
        int t;
        scanf("%d", &t);
        tt = 0;
        while (t --){
            char op[10];
            scanf("%s", op);
            if (!strcmp(op, "push")){               //入栈
                unsigned long long x;
                scanf("%llu", &x);
                q[++ tt] = x;                       
            } else if (!strcmp(op, "pop")){         //出栈
                if (tt) tt --;                      
                else puts("Empty");
            } 
            else if (!strcmp(op, "query")){         //查询栈顶
                if (tt) printf("%llu\n", q[tt]);    
                else puts("Anguei!");
            } 
            else printf("%d\n", tt);                //查询大小
        }
    }
    return 0;
}
```

## 队列

### 结构简介

> 先进先出（FIFO）.

### 基本操作

1.  **初始化**：`int q[N], hh, tt = -1;` 下标从0开始，与栈不同
2.  **push从队尾入队**：`q[++ tt] = x;`
3.  **pop从队头出队**：`q[++ tt] = x;`
4.  **query查询队头元素**：`printf("%d\n", q[hh]);`
5.  **队列大小**：`size = tt - hh + 1;`
6.  **empty检验是否为空**：`if (tt >= hh) printf("NO\n"); else printf("YES\n");`
7.  \***用数组模拟时也可以查询队尾元素**：`printf("%d\n", q[tt]);`

### 模板例题

> 题干：[洛谷 B3616 【模板】队列](https://www.luogu.com.cn/problem/B3616)

```cpp
//AC代码
#include <iostream>

using namespace std;

const int N = 10010;
int n, q[N], hh, tt;

void init(){
    hh = 0, tt = -1;
}

int main(){
    scanf("%d", &n);
    init();
    while (n --){
        int op, x;
        scanf("%d", &op);
        if (op == 1){
            scanf("%d", &x);
            q[++ tt] = x;
        } else if (op == 2)
            if (tt >= hh) hh ++;
            else puts("ERR_CANNOT_POP");
        else if (op == 3)
            if (tt >= hh) printf("%d\n", q[hh]);
            else puts("ERR_CANNOT_QUERY");
        else printf("%d\n", tt - hh + 1);
    }
    return 0;
}
```

## 单调栈

### 结构简介

> 维护一定单调性的栈，从而只保留有意义数据，用于解决特定问题.

### 基础操作

**构建单调栈**：

```cpp
for (int i = 1; i <= n; i ++){
    while (tt && check(stk[tt], i)) tt --; //将不可能称为答案的值出栈
    stk[++ tt] = i;    //将当前值入栈
}
```

### 模板例题

> 题干：[洛谷 P5788 【模板】单调栈](https://www.luogu.com.cn/problem/P5788)

> 题目简析：
>
> 1.  本题查询的是右侧第一个大于a\[i\]的数，可以反向遍历构建单调栈，或者用延迟结算的方式正向便利.下方代码采用反向遍历方式，与基础操作部分思路一致.
> 2.  本题一个需要注意的点在于单调栈里存储的是下标i，调用时注意要使用a\[stk\[i\]\].

```cpp
//AC代码
#include <iostream>
#include <cstdio>

using namespace std;

const int N = 3000010;
int n, tt;
int a[N], stk[N], ans[N];

int main(){
    scanf("%d", &n);
    for (int i = 1; i <= n; i ++) scanf("%d", &a[i]);
    for (int i = n; i >= 1; i --){
        while (tt && a[i] >= a[stk[tt]]) tt --;
        if (tt) ans[i] = stk[tt];
        else ans[i] = 0;
        stk[++ tt] = i;
    }
    for (int i = 1; i <= n; i ++) printf("%d ", ans[i]);
    return 0;
}
```

## 单调队列

### 结构简介

> 类似单调栈，维护一定单调性的队列，从而只保留有意义数据，用于解决特定问题，支持操作与单调栈类似，但多一个维度.

### 模板例题

> 题干：[洛谷 P1886 【模板】单调队列 / 滑动窗口](https://www.luogu.com.cn/problem/P1886)

> 题目简析：
>
> - 分两轮维护两次单调队列.
> - 以求最小值为例，维护严格增的单调队列。若存在 $i < j$ 而 $a\lbrack i\rbrack \geq a\lbrack j\rbrack$ ，则从 $a\lbrack j\rbrack$ 进入滑动窗口起， $a\lbrack i\rbrack$ 不可能成为之后任意一个窗口最小值的答案，因此单调队列内保留的是严格增的备选答案（包括当前与后续窗口）.同时，根据严格增性质可知，队头对应的值 $a\lbrack q\lbrack hh\rbrack\rbrack$ 即为当前滑动窗口的最小值.

```cpp
//AC代码

#include <iostream>
#include <cstdio>

using namespace std;

const int N = 1000010;
int n, k;
int a[N], q[N], tt, hh;

int main(){
    scanf("%d%d", &n, &k);
    for (int i = 0; i < n; i ++) scanf("%d", &a[i]);

    //第一轮 维护严格增的单调队列，队头对应的元素即为最小值
    hh = 0, tt = -1;    
    for (int i = 0; i < n; i ++){
        if (tt >= hh && q[hh] < i - k + 1) hh ++;   //查验滑动窗口大小
        while (tt >= hh && a[q[tt]] >= a[i]) tt --; //查验单调性
        q[++ tt] = i;                               //入队
        if (i >= k - 1) printf("%d ", a[q[hh]]);    //输出结果
    }
    
    puts("");
    
    //第二轮 维护严格减的单调队列，队头对应的元素即为最大值
    hh = 0, tt = -1;    //一定要再次初始化！
    for (int i = 0; i < n; i ++){
        if (tt >= hh && q[hh] < i - k + 1) hh ++;
        while (tt >= hh && a[q[tt]] <= a[i]) tt --;
        q[++ tt] = i;
        if (i >= k - 1) printf("%d ", a[q[hh]]);
    }
    return 0;
}
```

## 字典树（Trie）

### 结构简介

> 用树的形式存储字符串（也可以是二进制串等），便于插入和查找.

### 核心操作

1.  初始化：`const int N = 100010; int son[N][26], cnt[N], idx;`

2.  insert操作；插入一个新字符串

    ```cpp
    void insert(char str[]){
        int p = 0;
        for (int i = 0; str[i]; i ++){
            int u = str[i] - 'a';
            if (!son[p][u]) son[p][u] = ++idx;
            p = son[p][u];
        }
        cnt[p] ++;
    }
    ```

3.  query操作：查询字符串出现次数

    ```cpp
    int query(char str[]){
        int p = 0;
        for (int i = 0; str[i]; i ++){
            int u = str[i] - 'a';
            if (!son[p][u]) return 0;
            p = son[p][u];
        }
        return cnt[p];
    }
    ```

### 模板例题

> 题干：[洛谷 P8306 【模板】字典树](https://www.luogu.com.cn/problem/P8306)

> 题目简析：
>
> 1.  本题实现难度不高，但需注意时间/空间复杂度（详见题干）.
> 2.  cnt数组在本题中记录信息与上述模板不同，详见下方代码（如果用原本的cnt数组，则在计算作为前缀的字符串总数时需要遍历大量节点会超时）.
> 3.  注意初始化、ASCII码等细节，避免RE或TLE.

```cpp
//AC代码

#include <iostream>
#include <cstdio>
#include <algorithm>

using namespace std;

const int N = 3000010;      //注意大小
int son[N][70], cnt[N], idx;    //cnt记录以此节点为前缀最后一个字符，子孙中字符串的个数！
int t;
char str[N];

void init(){
    //一定要先用idx来初始化，如果用memset会超时！
    for (int i = 0;  i <= idx; i ++){
        cnt[i] = 0;
        for (int j = 0; j < 62; j ++)
            son[i][j] = 0;
    }
    idx = 0;
}

int get_number(char ch){
    //注意输入的可以有大小写或数字
    if (ch >= '0' && ch <= '9') return ch - '0';
    if (ch >= 'A' && ch <= 'Z') return ch - 'A' + 10;
    return ch - 'a' + 36;
}

void insert(char str[]){
    //常规insert
    int p = 0;
    for (int i = 0; str[i]; i ++){
        int u = get_number(str[i]);
        if (!son[p][u]) son[p][u] = ++ idx;
        p = son[p][u];
        cnt[p] ++;
    }
}

int query(char str[]){
    //query修改不多
    int p = 0;
    for (int i = 0; str[i]; i ++){
        int u = get_number(str[i]);
        if (!son[p][u]) return 0;
        p = son[p][u];
    }
    return cnt[p];
}

int main(){
    scanf("%d", &t);
    while (t --){
        int n, q;
        scanf("%d%d", &n, &q);
        init();
        while (n --){
            scanf("%s", str);
            insert(str);
        }
        while (q --){
            scanf("%s", str);
            printf("%d\n", query(str));
        }
    }
    return 0;
}
```

## 并查集

### 结构简介

> 用森林的形式存储元素集合从属关系，一棵树便是一个集合.

### 基本操作

1.  初始化：`p[i] = i;`
2.  find函数求根节点：`if (p[x] != x) p[x] = find(p[x]); return p[x];`
3.  并查集可维护一些核外信息，如每棵树（集合）的大小等.

### 模板例题

> 题干：[洛谷 P3367 【模板】并查集](https://www.luogu.com.cn/problem/P3367)

```cpp
//AC代码
#include <iostream>

using namespace std;

const int N = 1000010;

int n, m;
int p[N];

int find(int x){    //并查集核心操作，递归求根，O(n)
    if (p[x] != x) p[x] = find(p[x]);
    return p[x];
}

int main(){
    scanf("%d%d", &n, &m);
    for (int i = 1; i <= n; i ++) p[i] = i;
    while (m --){
        int op, a, b;
        scanf("%d%d%d", &op, &a, &b);
        if (op == 1) p[find(a)] = find(b);  //合并操作
        else
            if (find(a) == find(b)) puts("Y");
            else puts("N");
    }
    return 0;
}
```

## 堆

### 结构简介

>        堆的本质是一棵**存在大小关系的完全二叉树**。以**小根堆**为例，其特征便是**每个节点的值都小于其两个子节点**（左右子节点间大小关系不做要求），同理可知大根堆特点。堆结构是C++ STL里**priority queue**的背后实现原理。以下代码用数组模拟树结构，即节点 $i$ 的左子节点为 $2i$ ，右子节点为 $2i + 1$ .

### 基础操作

1.  建堆

    1.  逐个插入，时间复杂度为 $O(N\log N)$
    2.  自底部向上，对非叶子节点进行down操作，时间复杂度可缩减到 $O(N)$ :  
        `for (int i = n / 2; i; i --) down(i);` （下标从1开始）

2.  down操作（根据大小关系交换节点，将上层节点向下交换）

    ```cpp
    void down(int u){
        int t = u;
        if (u * 2 <= s && h[u * 2] < h[t]) t = u * 2;
        if (u * 2 + 1 <= s && h[u * 2 + 1] < h[t]) t = u * 2 + 1;
        if (u != t){
            heap_swap(u, t); //需要记录其他信息时额外定义函数，无需记录时swap即可
            down(t);
        }
    }
    ```

3.  up操作（根据大小关系交换节点，将下层节点向上交换）

    ```cpp
    void up(int u){
        while (u / 2 && h[u] < h[u / 2]){
            heap_swap(u, u / 2);
            u >>= 1;
        }
    }
    ```

### 支持操作（以小根堆为例）

1.  插入一个数：`heap[++ size] = x; up(size);`
2.  求集合当中最小值：`heap[1]`
3.  删除最小值：`heap[1] = heap[size --]; down(1)`
4.  删除任意一个元素：`heap[k] = heap[size --]; down(k); up(k)`
5.  修改任意一个元素：`heap[k] = x; down(k); up(k);`

### 模板例题

> 题干：[洛谷 P3378 【模板】堆](https://www.luogu.com.cn/problem/P3378)

```cpp
//AC代码
//标准模板题
#include <iostream>

using namespace std;

const int N = 1000010;
int n, idx; //idx同时也是Heap的大小
int h[N];

void down(int u){
    int t = u;
    if (2 * u <= idx && h[2 * u] < h[t]) t = 2 * u;
    if (2 * u + 1 <= idx && h[2 * u + 1] < h[t]) t = 2 * u + 1;
    if (u != t){
        swap(h[u], h[t]);
        down(t);
    }
}

void up(int u){
    while (u / 2 && h[u / 2] > h[u]) {
        swap(h[u], h[u >> 1]);
        u >>= 1;
    }
}

int main(){
    scanf("%d", &n);

    while (n --){
        int op, x;
        scanf("%d", &op);
        if (op == 1){
            scanf("%d", &x);
            h[++ idx] = x;
            up(idx);
        }else if (op == 2) printf("%d\n", h[1]);
        else{
            h[1] = h[idx --];
            down(1);
        }
    }

    return 0;
}
```

## 哈希表

### 结构简介

> 通过映射关系，实现O(1)复杂度的插入与查询

### 一般哈希

1.  拉链法

> 哈希数组 $h$ 上每个位置作为一个单链表的head，记录映射到 $h\lbrack i\rbrack$ 上的数的集合.

```cpp
//核心模块代码示例
const int N = 100003;
int n, h[N], e[N], ne[N], idx;

void insert(int x){
    int k = (x % N + N) % N;    //+N是为了解决C++中负数取模还是负数的问题
    e[idx] = x, ne[idx] = h[k], h[k] = idx ++;  //查到单链表头部
}

void find(int x){
    int k = (x % N + N) % N;
    for (int i = h[k]; i != -1; i = ne[i]){ //主函数将h的值初始化为1
        if (e[i] == x){
            puts("Yes");
            return;
        }
    }
    puts("No");
}
```

2.  开放寻址法

> 开两到三倍大小的哈希数组 $h$ ，顺移寻找每个数对应的哈希数组的位置.

```cpp
//核心模块代码示例
const int N = 200003, null = 0x3f3f3f3f;    //初始化h
int n, h[N];

int find(int x){
    int k = ((x % N) + N) % N;
    while (h[k] != null && h[k] != x){
        k ++;
        if (k == N) k = 0;
    }
    return k;
}
```

### 字符串哈希

> 用 $p$ 进制（ $p$ 取131或13331）存储前缀字符串，模 $N$ 获取哈希值（ $N$ 取 $2^{64}$ ，cpp中可以直接用`unsigned long long`处理，溢出即模运算），进而通过类似前缀和的方式得到字符串片段的哈希值进行匹配比较.

实现不难，下直接呈现模板例题及AC代码供参考.

> 模板例题：[P3370 【模板】字符串哈希](https://www.luogu.com.cn/problem/P3370)

```cpp
//AC代码

#include <iostream>
#include <cstdio>
#include <algorithm>

using namespace std;

typedef unsigned long long ULL;

const int N = 10010, M = 1510, P = 131;

ULL h, a[N];
char str[M];
int n;

//核心用P进制获取字符串哈希
ULL get_hash(char str[]){
    ULL h = 0;
    for (int i = 0; str[i]; i ++){
        h = h * P + str[i];
    }
    return h;
}

int main(){
    scanf("%d", &n);
    for (int i = 0; i < n; i ++){
        scanf("%s", str);
        h = get_hash(str);
        a[i] = h;
    }
    sort(a, a + n);

    int res = 0;
    for (int i = 0; i < n; i ++){
        if (!i || a[i] != a[i - 1]) res ++;
    }
    printf("%d", res);
    return 0;
}
```

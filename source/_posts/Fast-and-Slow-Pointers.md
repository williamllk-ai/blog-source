---
title: 【算法小节】 - 快慢指针
date: 2026-08-08 20:28:27
tags: ALGO
---
# 【算法小节】 - 快慢指针

## 双指针

**双指**针是一种在数组处理中常见的基础算法，通过存储**两个指针**（通常是下标）的**位置**和**变化**来完成一些**线性时间**的基础算法问题，常见的双指针算法有：
- 首尾双指针
- 快慢指针
- ...

其中**首尾双指针**最为常见，多用于反转数组或字符串的处理，或许在见到**双指针**这个名词前就已有潜移默化的思想，以下是一个反转字符串的基础示例：

```cpp
string reversed(string s){
    int i = 0, j = s.size() - 1;
    while (i < j) swap(s[i ++], s[j --]);
    return s;
}
```

略微复杂一点的首尾双指针会在**快速排序**中见到，但也比较易于理解，也容易想到，此处不加赘述，主要讲讲同样功能强大但没那么常见的**快慢指针**。

## 快慢指针

**快慢指针**顾名思义由一个快指针和一个慢指针构成，常见用法主要有：
- 取中间点
- 原地更新（O(1) 空间复杂度）
- ...

### 取中间点

这是一个快慢指针的常见基础用法，核心思路就是**每回合慢指针走一个，快指针走两个**，从而当快指针走到终点或者超出终点的时候，慢指针恰好落在需要的中点位置，以下是一个 leetcode 例题的解析与代码。

题目链接：[2095. Delete the Middle Node of a Linked List](https://leetcode.cn/problems/delete-the-middle-node-of-a-linked-list/)

题目简述：要求很简单，就是删除一个链表中的中间节点，其中此题对于中间节点的明确定义是第  $\left\lceil \frac{n}{2} \right\rceil$ 个节点，其中 $n$ 是链表的长度。

思路分析：
1. 设置快慢指针，慢指针每次走一格，快指针每次走两个，通过条件判断让慢指针停在要删除的节点前一个，然后使用 `slow = slow -> next` 的节点删除操作，完成题目要求
2. 需要注意的是，如果以 `head` 作为 `slow` 的起始节点，存在的问题就是 `head` 不会被删除，而当 `n = 1` 的时候，返回的应该是 `nullptr`，因此需要对 `n == 1` 进行特判。
3. 除了特判，一个更加连贯的处理逻辑是**在 `head` 之前增加一个哑节点 `dummy`**，让 `slow` 和 `fast` 都从 `dummy` 开始，如此一来删除逻辑可以得到统一。这种思路需要注意的是 `while` 语句中的判断条件需要重新修订，确保逻辑正确。

AC代码：
```cpp
class Solution {
public:
    ListNode* deleteMiddle(ListNode* head) {
        ListNode dummy(0, head);
        ListNode *slow = &dummy, *fast = dummy.next;
        while (fast != nullptr &&fast->next != nullptr){
            slow = slow -> next;
            fast = fast -> next -> next;
        }
        slow->next = slow->next->next;
        return dummy.next;
    }
};
```

### 原地更新

取中间点的问题是我第一次接触快慢指针，而下面这种**原地更新** 的使用方式更是有趣，用来解决 **$O(1)$ 空间复杂度**的问题尤为合适，下面用一个功能实现和一个例题来详细解释。

<br>

首先，第一个要实现的功能非常常见，就是 **移除多余空格**，这一问题有许多种写法，也有很多库函数可以直接使用来完成这个任务。至于如何手写这个功能，我认为快慢指针是其中一种简介美观的写法。

具体思路就是，快指针从前往后遍历，当遇到非空字符时，开始将单词复制到慢指针对应的位置，两个指针同步向后，直到遍历完这个单词或者整个字符串，最后对字符串进行一个 `resize` 即可得到原地更新的字符串。具体代码实现如下：

```cpp
// 这个函数实现的功能有两个
// 1. 删除句子前后多余空格
// 2. 删除单词与单词之间多余的空格，仅保留一个空格
string RemoveExtraSpace(string s){
    int slow = 0;
    for (int i = 0; i < s.size(); i ++){
        if (s[i] != ' '){
            if (slow) s[slow ++] = ' ';
            while (i < s.size() && s[i] != ' ')
                s[slow ++] = s[i ++];
        }
    }
    s.resize(slow);
    return s;
}
```

<br>

第二个例子也是一道 leetcode 题目，[443. String Compression](https://leetcode.cn/problems/string-compression/)，这个题目题面里就要求了对字符串进行原地修正，实现 **$O(1)$ 空间复杂度** 。

简要叙述题干意思就是将 `aabbbccccd` 这样一个字符串根据字符重复数量压缩成 `a2b3c4d`，其中只出现一次的字符就直接照搬，不用增加一个 1 。

由此，我们很容易注意到，压缩后的字符串一定比原始字符串更短，因为对于同一个字符段，出现 1 次或者重复 2 次时与压缩后的长度一样，而大于 2 次时，压缩后的长度就会变短，因此可以想到使用快慢指针，将快指针遍历到的字符串直接复制到慢指针即可，操作核心逻辑和上一个 `RemoveExtraSpace` 类似，实现略有不同，以下是 AC 代码：

```cpp
class Solution {
public:
    int compress(vector<char>& chars) {
        int fast = 0, slow = 0, count = 1;
        while (fast < chars.size()){
            chars[slow ++] = chars[fast ++];
            while (fast < chars.size() && chars[fast] == chars[fast - 1]){
                count ++;
                fast ++;
            }
            if (count > 1){
                string cnt = to_string(count);
                for (int i = 0; i < cnt.size(); i ++)
                    chars[slow ++] = cnt[i];
                count = 1;
            }
        }
        return slow;
    }
};
```

---
title: MIT 18.065 Lecture 1 & 2 
date: 2026-02-05 22:54:47
author: williamllk
tags: LA
---

# MIT 18.065 — Lecture 1 & 2

## Lecture 1 — Introduction to Linear Algebra

### 1. What does a matrix do?

- **Matrix = linear transformation**: It transforms vectors into new vectors via a linear combination of its columns.
  
- Matrix \(A\) acting on vector \(x\):
  $$ A x = x_1 a_1 + x_2 a_2 + \dots + x_n a_n $$

- **Key takeaway**: A matrix is a machine for combining vectors in a particular way.

---

### 2. Column Space (Range of the Matrix)

- The **column space** of a matrix \(A\) is the set of all vectors that can be formed by linear combinations of its columns:
  $$ \text{Col}(A) = \{ A x : x \in \mathbb{R}^n \} $$

- The **dimension of the column space** is the **rank** of the matrix.
  
---

### 3. Rank

- **Rank** of a matrix is the number of linearly independent columns.
- **Rank of \(A\)** determines the dimension of the column space:
  $$ \text{rank}(A) \leq \min(m, n) $$

- If rank is full, the matrix maps all input vectors to a full-dimensional output space.

---

### 4. Null Space

- The **null space** of a matrix \(A\) is the set of vectors \(x\) for which \(A x = 0\).
  $$ N(A) = \{ x : A x = 0 \} $$

- The null space describes the **dependencies** among columns.

---

### 5. Rank–Nullity Theorem

- The sum of the rank and the nullity of a matrix is equal to the number of columns:
  $$ \text{rank}(A) + \dim N(A) = n $$

---

### 6. CR Factorization

- **CR decomposition** of a matrix \($A$\):
  $$ A = C R $$

- \(C\) contains the **linearly independent columns**, and \(R\) contains the coefficients for the linear combinations.
- $R$ is the row-reducd echelon form of matrix $A$.

---

## Lecture 2 — Rank-One Matrices and Outer Products

### 1. Outer Product

- **Outer product** of vectors \(a \in \mathbb{R}^m\) and \(b \in \mathbb{R}^p\):
  $$ a b^T \in \mathbb{R}^{m \times p} $$

- The entry at position \((i,j)\) of the matrix is:
  $$ (a b^T)_{ij} = a_i b_j $$

- Outer products generate **rank-1 matrices**.

---

### 2. Rank-One Matrices

- **Rank-One Matrix**: If \(a \neq 0\) and \(b \neq 0\), then the rank of \(a b^T\) is 1.
  
- This is because every column of \(a b^T\) is a multiple of the vector \(a\).

---

### 3. Matrix Multiplication as Sum of Rank-One Matrices

- A matrix multiplication can be viewed as a sum of outer products:
  $$ A B = a_1 b_1^T + a_2 b_2^T + \dots + a_n b_n^T $$

- This is the basic idea of matrix multiplication: **breaking down matrices into rank-1 pieces**.

---


### Key Takeaways:

- **Matrices = Linear combinations** of columns.
- **Rank** describes the dimension of the space a matrix can map to.
- **Null space** shows the dependencies among columns.
- **Outer products** are the building blocks of matrices.
- **Matrix multiplication** = sum of rank-1 outer products.

---


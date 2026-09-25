# 🧩 Sudoku CSP Game

> **A Sudoku game where every move is a constraint.**

Welcome to **Sudoku CSP Game** — a Python-powered Sudoku experience built around the idea of a **Constraint Satisfaction Problem (CSP)**.

This project turns a classic logic puzzle into an interactive computer science project. Behind every empty cell, every number, and every decision is a set of constraints that must be respected.

The goal is simple:

**Solve the puzzle while satisfying every rule.**

---

## 🌟 Why This Project?

Sudoku looks simple.

Nine rows.  
Nine columns.  
Nine 3×3 boxes.  
Numbers from 1 to 9.

But underneath that simplicity is a beautiful computational problem.

Each empty Sudoku cell can be treated as a **variable**. Its possible values form a **domain**, and the Sudoku rules become **constraints**.

That makes Sudoku a natural and intuitive example of a **Constraint Satisfaction Problem**.

This project brings that concept into an interactive Streamlit application so that CSP is not just something you read about in a textbook —

**you can actually play with it.**

---

## 🎯 Project Objective

The main objective of this project is to design and implement an interactive Sudoku game using Python while demonstrating the fundamental concepts of a **Constraint Satisfaction Problem**.

The player must fill the empty cells while satisfying:

- No repeated number in a row
- No repeated number in a column
- No repeated number inside a 3×3 box
- Every empty cell must contain a valid value from **1 to 9**

---

## 🧠 Sudoku as a Constraint Satisfaction Problem

A CSP can be described through three main components:

### 1. Variables

Every empty Sudoku cell is a variable.

Each variable represents one unknown Sudoku cell.

### 2. Domains

Each empty cell can take a value from:

```text
{1, 2, 3, 4, 5, 6, 7, 8, 9}

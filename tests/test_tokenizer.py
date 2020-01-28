#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2018-2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import string

from latex2mathml.tokenizer import tokenize


def test_leteral_expression():
    latex_expression = 'ax+bx = (a+b)x'
    assert ['a', 'x', '+', 'b', 'x', '=', 
            '(', 'a', '+', 'b', ')', 'x'] == list(tokenize(latex_expression))


def test_single_backslash1():
    assert ['\\'] == list(tokenize('\\'))

def test_double_backslash1():
    assert [r'\\'] == list(tokenize(r'\\'))

def test_single_backslash():
    assert ['\\'] == list(tokenize('\\'))

def test_spaces():
    spaces =r'a\, b\; c\quad d \qquad e'
    assert ['a', r'\,', 'b', r'\;', 'c', 
            r'\quad', 'd', r'\qquad', 'e'] == list(tokenize(spaces))


def test_alphabets():
    alphabets = string.ascii_letters
    assert list(alphabets) == list(tokenize(alphabets))


def test_numbers():
    numbers = '1234567890'
    assert [numbers] == list(tokenize(numbers))


def test_backslash_after_number():
    assert ['123', '\\'] == list(tokenize('123\\'))


def test_double_backslash_after_number():
    assert ['123', r'\\'] == list(tokenize(r'123\\'))


def test_numbers_with_decimals():
    decimal = '12.56'
    assert [decimal] == list(tokenize(decimal))


def test_numbers_with_comma():
    decimal = '12,56'
    assert ['12', ',', '56'] == list(tokenize(decimal))


def test_incomplete_decimal():
    decimal = r'12.\\'
    assert ['12', '.', r'\\'] == list(tokenize(decimal))


def test_numbers_and_alphabets():
    s = '5x'
    assert list(s) == list(tokenize(s))


def test_decimals_and_alphabets():
    s = '5.8x'
    assert ['5.8', 'x'] == list(tokenize(s))


def test_string_with_spaces():
    s = '3 x'
    assert ['3', 'x'] == list(tokenize(s))


def test_operators():
    s = '+-*/=()[]_^{}'
    assert list(s) == list(tokenize(s))


def test_numbers_alphabets_and_operators():
    s = '3 + 5x - 5y = 7'
    assert ['3', '+', '5', 'x', '-', '5', 'y', '=', '7'] == list(tokenize(s))


def test_symbols():
    s = r'\alpha\beta'
    assert [r'\alpha', r'\beta'] == list(tokenize(s))


def test_symbols_appended_number():
    s = r'\frac2x'
    assert [r'\frac', '2', 'x'] == list(tokenize(s))


def test_matrix():
    assert [r'\begin{matrix}', 'a', '&', 'b', r'\\', 'c', '&', 'd', r'\end{matrix}'] == \
           list(tokenize(r'\begin{matrix}a & b \\ c & d \end{matrix}'))


def test_matrix_with_alignment():
    assert [r'\begin{matrix*}', '[', 'r', ']', 'a', '&', 'b', r'\\', 'c', '&', 'd', r'\end{matrix*}'] == \
           list(tokenize(r'\begin{matrix*}[r]a & b \\ c & d \end{matrix*}'))


def test_matrix_with_negative_sign():
    assert [r'\begin{matrix}', '-', 'a', '&', 'b', r'\\', 'c', '&', 'd', r'\end{matrix}'] == \
           list(tokenize(r'\begin{matrix}-a & b \\ c & d \end{matrix}'))


def test_simple_array():
    assert [r'\begin{array}', '{', 'c', 'c', '}', '15', '&', '2', r'\\', '3', '&', '4', r'\end{array}'] == \
           list(tokenize(r'\begin{array}{cc} 15 & 2 \\ 3 & 4 \end{array}'''))


def test_subscript():
    assert ['a', '_', '{', '2', ',', 'n', '}'] == list(tokenize('a_{2,n}'))


def test_superscript_with_curly_braces():
    assert ['a', '^', '{', 'i', '+', '1', '}', '_', '3'] == list(tokenize('a^{i+1}_3'))


def test_issue_33():
    latex = r'''\begin{bmatrix}
     a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
     a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
     \vdots  & \vdots  & \ddots & \vdots  \\
     a_{m,1} & a_{m,2} & \cdots & a_{m,n}
    \end{bmatrix}'''
    expected = [r'\begin{bmatrix}', 'a', '_', '{', '1', ',', '1', '}', '&', 'a', '_', '{', '1', ',', '2', '}', '&',
                r'\cdots', '&', 'a', '_', '{', '1', ',', 'n', '}', r'\\', 'a', '_', '{', '2', ',', '1', '}', '&', 'a',
                '_', '{', '2', ',', '2', '}', '&', r'\cdots', '&', 'a', '_', '{', '2', ',', 'n', '}', r'\\', r'\vdots',
                '&', r'\vdots', '&', r'\ddots', '&', r'\vdots', r'\\', 'a', '_', '{', 'm', ',', '1', '}', '&', 'a',
                '_', '{', 'm', ',', '2', '}', '&', r'\cdots', '&', 'a', '_', '{', 'm', ',', 'n', '}', r'\end{bmatrix}']
    assert expected == list(tokenize(latex))


def test_issue_51():
    assert [r'\mathbb{R}'] == list(tokenize(r'\mathbb{R}'))


def test_issue_55():
    latex = r'\begin{array}{rcl}ABC&=&a\\A&=&abc\end{array}'
    expected = [r'\begin{array}', '{', 'r', 'c', 'l', '}', 'A', 'B', 'C', '&', '=', '&', 'a', r'\\', 'A', '&', '=', '&',
                'a', 'b', 'c', r'\end{array}']
    assert expected == list(tokenize(latex))

def test_text():
    latex = r'\text{if} a=b \text{then} b = a'
    expected = [r'\text', 'if', 'a', '=', 'b',
                r'\text', 'then', 'b', '=', 'a']
    assert expected == list(tokenize(latex))
    
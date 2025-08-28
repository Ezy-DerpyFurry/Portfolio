from functools import reduce

日本語がすき＿ = ""
日本語がす＿き二＿ = ""

try:
    日本語がすき＿ = eval("".join(map(chr, [105, 110, 116])))(input("Num: "))
except Exception as ま:
    (lambda a:
        print(f"Not a valid number.") if not 日本語がすき＿ else 
        (lambda z:
            (1, z+2, z*3)
        )(5)
    )(日本語がすき＿)
try:
    日本語がす＿き二＿ = eval("".join(map(chr, [105, 110, 116])))(input("Num2: "))
except Exception as ま:
    (lambda a:
        print(f"Not a valid number.") if not 日本語がす＿き二＿ else 
        (lambda z:
            (1, z+2, z*3)
        )(5)
    )(日本語がす＿き二＿)

for i in range(日本語がすき＿ or 1):
    r24L = reduce(lambda _ ,x: int(x), [(i + 1)])

for a in range(日本語がす＿き二＿ or 1):
    lOa本_ = reduce(lambda _ ,z: int(z), [(a + 1)])

r24水L = r24L
lOa水本_ = lOa本_

(lambda x, y: 
    print(f"Num1: {x}") if x > y else 
    (lambda z:
        print((f"Num1: {y}"))
    )(f" {y}")
)(r24水L, lOa水本_)


import re

from sympy import Symbol, simplify

from constants import VALUE_ERROR, TYPE_ERROR, ERROR_MESSAGE_EDUATION


def str_exp(line, x):
    line = line.replace(x, 'x')
    line = line.replace('^', '**')
    line = re.sub(r'(\d+)([a-z]|[а-я])', r'\1*\2', line)
    line = re.sub(r'(\))(\()', r'\1*\2', line)
    line = re.sub(r'(\d+)(\()', r'\1*\2', line)
    line = re.sub(r'([a-z]|[а-я])(\()', r'\1*\2', line)

    return line


def exp_str(expression, x):
    line = str(expression)

    line = line.replace('x', x)
    line = line.replace('**', '^')
    line = line.replace(' ', '')
    line = re.sub(r'(\d+)\*([a-z]|[а-я])', r'\1\2', line)
    line = re.sub(r'(\))\*(\()', r'\1\2', line)
    line = re.sub(r'(\d+)\*(\()', r'\1\2', line)
    line = re.sub(r'([a-z]|[а-я])\*(\()', r'\1\2', line)

    return line


def value(line):
    variables = set(re.findall(r'[a-z]|[а-я]', line))
    if len(variables) != 1:
        raise ValueError(TYPE_ERROR)

    return variables.pop()


def differentiation(line):
    x = Symbol('x')
    exp = eval(str_exp(line, value(line)))
    simpl_exp = simplify(exp.diff('x'))

    return exp_str(simpl_exp, value(line))


def delitel(line):
    koef = {'a': 0, 'b': 0, 'c': 0}
    line_do, line_posle = re.split('=', line)
    split_do = re.split(r'(\+|-)', line_do)
    split_posle = re.split(r'(\+|-)', line_posle)
    koefs = set()

    def current_koef(koefs):
        cur_koef = set()
        for koef in koefs:
            if '^2' in koef:
                cur_koef.add(koef[:-2])
            else:
                cur_koef.add(koef)
        if len(cur_koef) != 1:
            raise TypeError('Разные переменные')

    def cont(arr, reverse=1):
        sign = 1
        for el in arr:
            if re.search(r'([a-z]|[а-я])\^2', el):
                kof = re.search(r'([a-z]|[а-я])\^2', el).group()
                koefs.add(kof)
                kof = 'a'
                el = re.sub(r'([a-z]|[а-я])\^2', '', el)
                if not el:
                    el = 1
            elif re.search(r'[a-z]|[а-я]+', el):
                kof = re.search(r'[a-z]|[а-я]+', el).group()
                koefs.add(kof)
                kof = 'b'
                el = re.sub(r'([a-z]|[а-я]+)', '', el)

                if not el:
                    el = 1
            elif el == '+':
                sign = 1
                continue
            elif el == '-':
                sign = -1
                continue
            else:
                kof = 'c'

            koef[kof] += int(el) * sign * reverse

    try:
        cont(split_do)
        cont(split_posle, -1)
        current_koef(koefs)
    except ValueError:
        raise ValueError(VALUE_ERROR)
    except TypeError:
        raise TypeError(TYPE_ERROR)
    except Exception:
        raise ValueError(ERROR_MESSAGE_EDUATION)

    return koef


def discriminant(a, b, c):
    return b**2-4*a*c


def converter(x):
    if x.is_integer():
        return int(x)

    return round(x, 2)


def roots(d, a, b):
    if d < 0:
        return None

    x1 = (-b + d**0.5)/2*a
    x2 = (-b - d**0.5)/2*a

    x1 = converter(x1)
    x2 = converter(x2)

    if x1 == x2:
        return x1,

    return x1, x2


def quadratic_equation(line):
    koef = delitel(line)
    a, b, c = koef['a'], koef['b'], koef['c']
    d = discriminant(a, b, c)
    x = roots(d, a, b)

    return x


def eduation(line):
    koef = delitel(line)

    if koef['a'] == 0:
        return converter(-koef['c'] / koef['b'])
    else:
        return quadratic_equation(line)


def test():
    assert differentiation('(x+2)^2-3x^3') == '-9x^2+2x+4'
    assert differentiation('(5+x)/(x-3)') == '-8/(x-3)^2'
    assert differentiation('(x^2-3x)/(x^2+1)') == '(3x^2+2x-3)/(x^4+2x^2+1)'
    assert differentiation('((2-x)/(x+3))**2') == '10(x-2)/(x+3)^3'
    assert differentiation('y^2+6y') == '2y+6'

    assert delitel('2x^2+3x^2-3x-3=5+x-x^2') == {'a': 6, 'b': -4, 'c': -8}
    assert delitel('x^2-6x+9=0') == {'a': 1, 'b': -6, 'c': 9}
    assert delitel('x=2') == {'a': 0, 'b': 1, 'c': -2}
    assert delitel('я^2-6я+9=0') == {'a': 1, 'b': -6, 'c': 9}


if __name__ == '__main__':
    test()

import re
from typing import Dict
from sympy import symbols, solve, diff, integrate, simplify, factor, expand, N
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations,
    implicit_multiplication_application, convert_xor
)

# ===== SYMBOLS & PARSING =====
x, y, z = symbols('x y z')
_ALLOWED_LOCALS = {'x': x, 'y': y, 'z': z}
_TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application, convert_xor)

# ===== UNIT CONVERSIONS =====
def handle_conversion(query: str) -> Dict:
    q_lower = query.lower()
    try:
        # Celsius to Fahrenheit
        match = re.search(r'([0-9.]+)\s*°?\s*c\s*(to|in)\s*f', q_lower)
        if match:
            c = float(match.group(1))
            f = c * 9/5 + 32
            return {"handled": True, "reply": f"{c}°C = {f}°F"}

        # Fahrenheit to Celsius
        match = re.search(r'([0-9.]+)\s*°?\s*f\s*(to|in)\s*c', q_lower)
        if match:
            f = float(match.group(1))
            c = (f - 32) * 5/9
            return {"handled": True, "reply": f"{f}°F = {c}°C"}

        # km to m
        match = re.search(r'([0-9.]+)\s*km\s*(to|in)\s*m', q_lower)
        if match:
            km = float(match.group(1))
            m = km * 1000
            return {"handled": True, "reply": f"{km} km = {m} m"}

        # m to km
        match = re.search(r'([0-9.]+)\s*m\s*(to|in)\s*km', q_lower)
        if match:
            m = float(match.group(1))
            km = m / 1000
            return {"handled": True, "reply": f"{m} m = {km} km"}

    except Exception as e:
        return {"handled": True, "reply": f"Error in conversion: {e}"}

    return {"handled": False, "reply": None}

# ===== MATH QUERY DETECTION =====
def is_math_query(query: str) -> bool:
    math_keywords = ["solve", "equation", "derivative", "differentiate",
                     "integral", "integrate", "simplify", "factor", "expand", "root"]
    q_lower = query.lower()
    if any(k in q_lower for k in math_keywords):
        return True
    if re.search(r"[0-9xXyYz\+\-\*\/\^=]", query):
        return True
    return False

# ===== SYMPY SAFE PARSE =====
def safe_parse(expr_str: str):
    s = expr_str.replace('^', '**').replace(',', '')
    return parse_expr(s, local_dict=_ALLOWED_LOCALS, transformations=_TRANSFORMATIONS, evaluate=True)

def _extract_math_piece(query: str) -> str:
    candidates = re.findall(r'[0-9a-zA-Z\+\-\*\/\^\(\)\.\s,]+', query)
    if not candidates: return query
    filtered = [c.strip() for c in candidates if re.search(r'[0-9\+\-\*\/\^=x-yX-Z]', c)]
    return max(filtered, key=len) if filtered else query

# ===== SOLVE MATH =====
def solve_math(query: str) -> str:
    # Check for unit conversion first
    conv_result = handle_conversion(query)
    if conv_result["handled"]:
        return conv_result["reply"]

    math_piece = _extract_math_piece(query)

    try:
        q_lower = query.lower()
        # CALCULUS
        if re.search(r'\b(derivative|differentiate|d/dx)\b', q_lower):
            expr_text = re.sub(r'\b(derivative|differentiate|d/dx|derivative of)\b', '', q_lower, flags=re.IGNORECASE).strip() or math_piece
            expr = safe_parse(expr_text)
            deriv = diff(expr, x)
            return f"Derivative (d/dx): {simplify(deriv)}"

        if re.search(r'\b(integral|integrate|antiderivative)\b', q_lower):
            expr_text = re.sub(r'\b(integral of|integrate|antiderivative of)\b', '', q_lower, flags=re.IGNORECASE).strip() or math_piece
            expr = safe_parse(expr_text)
            integ = integrate(expr, x)
            return f"Indefinite integral: {simplify(integ)} + C"

        # ALGEBRA
        if re.search(r'\b(simplify|simplification)\b', q_lower):
            expr_text = re.sub(r'\b(simplify|simplification of)\b', '', q_lower, flags=re.IGNORECASE).strip() or math_piece
            expr = safe_parse(expr_text)
            return f"Simplified: {simplify(expr)}"

        if re.search(r'\b(factor|factorize)\b', q_lower):
            expr_text = re.sub(r'\b(factor|factorize)\b', '', q_lower, flags=re.IGNORECASE).strip() or math_piece
            expr = safe_parse(expr_text)
            return f"Factored: {factor(expr)}"

        if re.search(r'\b(expand)\b', q_lower):
            expr_text = re.sub(r'\b(expand)\b', '', q_lower, flags=re.IGNORECASE).strip() or math_piece
            expr = safe_parse(expr_text)
            return f"Expanded: {expand(expr)}"

        # EQUATION SOLVE OR EVALUATE
        if '=' in math_piece:
            left, right = math_piece.split('=', 1)
            eq = safe_parse(left) - safe_parse(right)
            symbols_in_eq = list(eq.free_symbols)
            sols = solve(eq, symbols_in_eq) if symbols_in_eq else solve(eq)
            return f"Solved: {sols}"

        expr = safe_parse(math_piece)
        try:
            numeric = N(expr)
            return f"Result: {numeric}"
        except Exception:
            return f"Result: {simplify(expr)}"

    except Exception as e:
        return f"Error parsing math expression: {e}"

# ===== MAIN HANDLER =====
def handle_math_query(user_message: str) -> Dict:
    if not user_message.strip():
        return {"handled": True, "reply": "Please enter a math question."}

    # Conversion check first
    conv_result = handle_conversion(user_message)
    if conv_result["handled"]:
        return conv_result

    if is_math_query(user_message):
        return {"handled": True, "reply": solve_math(user_message)}

    return {"handled": False, "reply": "I cannot solve this math problem."}

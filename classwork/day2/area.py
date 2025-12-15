import math

def area_circle(radius: float) -> float:
    return math.pi * radius ** 2

def area_rectangle(width: float, height: float) -> float:
    return width * height

def area_triangle(base: float, height: float) -> float:
    return 0.5 * base * height
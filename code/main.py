import math
import matplotlib.pyplot as plt

"Elliptische Kurve: y^2 = x^3 + ax + b (mod p)"
"Punkte sind in der Formq=(x_1,y_1)"

def is_on_curve(P,a,b,p):
    if P is None:
        return True
    x,y = P
    return (y**2 - x**3+a*x+b) % p == 0


def double_point(P,a,p):
    x1, y1 = P
    if  y1 % p == 0: #Vertikale Tangente: Punkt ist Unendlich
        return None
    m = ((3*x1**2+a) * pow(2 * y1, -1, p)) % p
    x3 = (m**2-2*x1) % p
    y3 = (m*(x1-x3)-y1) % p
    return x3,y3

def add_points(P,Q,a,p):
    # Points at infinity
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P + (-P) = infinity
    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P == Q:
        return double_point(P, a, p)

   # P != Q
    m = ((y2-y1) * pow(x2 - x1, -1, p)) % p
    x3 = (m**2-x1-x2) % p
    y3 = (m*(x1-x3)-y1) % p
    return x3, y3

def calculate_curve_points(a, b, p):
    points = []
    for x in range(p):
        for y in range(p):
            if (y**2-x**3-a*x-b)%p == 0:
                points.append((x,y))
    return points

def point_order(P,a,p,group_order):
    R = None

    for n in range(1,group_order+1):
        R = add_points(P,R,a,p)
        if R is None:
            return n

def find_generator(a,b,p):
    points = calculate_curve_points(a,b,p)
    group_order = len(points)+1

    for P in points:
        order = point_order(P,a,p,group_order)

        if order == group_order:
            return P, order
    return None,None

def calculate_multiples(P,a,p,order):
    multiples = []
    R = None

    for n in range(1,order):
        R = add_points(R,P,a,p)
        multiples.append(R)

    return multiples

def plot_curve_points(P , a, b, p):
    curve_points = calculate_curve_points(a,b,p)
    group_order = len(curve_points) + 1
    multiples = calculate_multiples(P,a,p,group_order)

    xs = [point[0] for point in curve_points]
    ys = [point[1] for point in curve_points]

    plt.figure(figsize=(8, 8))
    plt.scatter(xs, ys, s=80, color="green")
    plt.scatter(P[0], P[1], color="red", s=120, edgecolors="black",
        zorder=3,
        label=f"P = {P}") #Generator hervorheben
    for n,point in enumerate(multiples, start=1):
        if point is not None:
            plt.annotate(
                f"{n}P",
                point,
                xytext=(6, 4),
                textcoords="offset points"
            )

    plt.xticks(range(p))
    plt.yticks(range(p))
    plt.xlim(-0.5, p - 0.5)
    plt.ylim(-0.5, p - 0.5)
    plt.grid(True, alpha=0.4)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title( rf"$E: y^2 \equiv x^3 + {a}x + {b}"
    rf"\;(\mathrm{{mod}}\; {p})$")
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        "ell_curve_finite_field.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()
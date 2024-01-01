import sympy


# Thanks again to hyper-neutrino for introducing me to numpy
# As a mathematician, I can see me using this way more in the future (https://github.com/hyper-neutrino)

def part_1(filename: str, lhs: int = 7, rhs: int = 27) -> int:
    # get trajectories
    lines = open(filename).read().splitlines()
    trajectories = [tuple(map(int, line.replace(' @', ',').split(', '))) for line in lines]
    # running result
    res = 0
    # now loop over each pair of trajectories
    for i, t1 in enumerate(trajectories):
        for t2 in trajectories[:i]:
            # unwrap the trajectories
            x1, y1, _, vx1, vy1, _ = t1
            x2, y2, _, vx2, vy2, _ = t2
            # create 2 numpy symbols for the intersection point if it exists
            px, py = sympy.symbols("px py")
            # the math is as follows
            # for each trajectory we know it is a line of form ax+by=c and for each t the points (x+t*vx,y+t*vy) is
            # on this line, so solving this gives us that for each point p=(px,py) (at some t) it holds that
            # vy*(px-sx)=vx*(py-sy) with a given point s=(sx,sy) on the line
            # if we give these equations to sympy it will solve for p if we use the same symbols in both equations,
            # eliminating the need for us to solve the system manually each time
            intersections = sympy.solve([
                vy * (px - sx) - vx * (py - sy) for sx, sy, _, vx, vy, _ in [t1, t2]
            ])
            # if the set of intersections is empty, the lines are parallel
            # also check if it is in the desired region
            if (
                    len(intersections) > 0 and lhs <= intersections[px] <= rhs and lhs <= intersections[py] <= rhs
            ):
                # now check that the moment of intersecting is not in the past, i.e. if the stone has moved in the same
                # direction as the velocity vector
                # we do this by sign checking for the difference in coordinates, multiplied by the velocity, these
                # should have the same sign
                if all(0 <= (intersections[px] - sx) * vx and 0 <= (intersections[py] - sy) * vy for
                       sx, sy, _, vx, vy, _ in [t1, t2]):
                    # if so, these could intersect in the region, so add one to the counter
                    res += 1
    return res


def part_2(filename: str) -> int:
    # get trajectories
    lines = open(filename).read().splitlines()
    trajectories = [tuple(map(int, line.replace(' @', ',').split(', '))) for line in lines]
    # now for each hailstone we know that at some time it will intersect with our stone
    # assume our stone has (v_xs, v_ys, v_zs) as velocity vector and starts at (xs, ys, zs)
    # assume the hailstone has (v_xh, v_yh, v_zh) as velocity vector and starts at (xh, yh, zh)
    # then we know that at some moment in time the following equations should hold
    # (xs-xh)/(v_xh-v_xs)=(ys-yh)/(v_yh-v_ys)=(zs-zh)/(v_zh-v_zs)
    # so we will construct these equations with the parameters of our stone as sympy variables for solving
    xs, ys, zs, v_xs, v_ys, v_zs = sympy.symbols("xs ys zs v_xs v_ys v_zs")
    eqs = []
    answers = []
    # now assume there is only one integer solution, hard assumption, but the problem seems to be written s.t. this is
    # the case
    # so while we don't have exactly one answer that has all values as integers, find more solutions and overlap the
    # with more equations
    while len(answers) != 1:
        for xh, yh, zh, v_xh, v_yh, v_zh in trajectories[:3]:
            eqs.append((xs - xh) * (v_yh - v_ys) - (ys - yh) * (v_xh - v_xs))
            eqs.append((ys - yh) * (v_zh - v_zs) - (zs - zh) * (v_yh - v_ys))
            answer = sympy.solve(eqs)
            answers = [a for a in answer if all(t % 1 == 0 for t in a.values())]
    # return sum of coordinates and done
    return answers[0][xs] + answers[0][ys] + answers[0][zs]

import time, random

##### Input generation: n random (x, y) points #####
def make_points(n):
    points = []
    for i in range(n):
        x = random.randint(0, n * 10)  # Make the range larger as n increases
        y = random.randint(0, n * 10)
        points.append((x, y))
    return points

##### Scan from right to left on a sorted array #####
def pareto_scan(sorted_array):
    result = []
    max_y = 0

    i = len(sorted_array) - 1

    # If the current y is greater than or equal to the maximum so far, add it to the result
    while i >= 0:
        x = sorted_array[i][0]
        y = sorted_array[i][1]

        if y >= max_y:
            result.append((x, y))
            max_y = y

        i -= 1

    result.reverse()  # reverse the list to make x in ascending order
    return result


##### Divide & Conquer : STEP1(Sort) #####
def pareto_d_and_c(points):
    if not points:
        return []
    pts = sorted(points)  # Sort the points in ascending order of x
    return sub_pareto(pts)

##### Divide & Conquer SETP2(Divide), SETP3(Conquer), SETP4(Merge)#####
def sub_pareto(pts): 
    n = len(pts)

    if n <= 20:
        return pareto_scan(pts)

    mid = n // 2
    left = pts[:mid]  ### STEP2(Divide): Split the set into two halves
    right = pts[mid:]

    L = sub_pareto(left)  ### STEP3(Conquer): Recursive calls
    R = sub_pareto(right)

    ### STEP4(Merge):
    if len(R) == 0:
        return L

    max_y_R = 0
    for point in R:   # find a maximum Y in R
        y = point[1]
        if y > max_y_R:
            max_y_R = y

    # In the left subset L, remove points whose y is smaller than the maximum y of the right subset
    L2 = []
    for point in L:
        y = point[1]
        if y >= max_y_R:
            L2.append(point)

    return L2 + R


def get_time(n, reps=99):   # Run the function 100 times and return the median value
    pts = make_points(n)    
    times = []
    for _ in range(reps):   
        t1 = time.perf_counter_ns()
        pareto_d_and_c(pts) 
        t2 = time.perf_counter_ns()
        times.append(t2 - t1)
    times.sort()
    return times[len(times)//2]  # return median 


if __name__ == "__main__":
    data_list = [10, 100, 1000, 10000, 100000]
    for n in data_list:
        print(f"{n},{get_time(n)}")
    
    # Print the result
    # print("\nExample result for n = 100:")
    # pts = make_points(100)
    # result = pareto_d_and_c(pts)
    # print(result)

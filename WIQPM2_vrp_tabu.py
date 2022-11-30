import random


def distance(p1, p2):
    return (abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))


def vrp_initialize(loc, veh):
    i = 0
    vrp_init = [0] * (loc - 1)
    while i < loc- 1:
        vrp_init[i] = (i+1, i%veh)
        i += 1
    return vrp_init


def dist_initialize(loc):
    vrp = [0] * loc
    for i in range(loc):
        x_rand = random.randint(0, 1000)
        y_rand = random.randint(0, 1000)
        vrp[i] = (x_rand, y_rand)
    return vrp


def transform_vrp(vrp):
    vrp_dict = {}
    for i in range(len(vrp)):
        for j in range(len(vrp)):
            vrp_dict[(i, j)] = distance(vrp[i], vrp[j])
    return vrp_dict


def dstnc(dict, v, veh):
    dist = [0] * veh
    prev = [0] * veh
    for i in range(len(v)):
        dist[v[i][1]] += dict[prev[v[i][1]], v[i][0]]
        prev[v[i][1]] = v[i][0]
    for i in range(veh):
        dist[i] += dict[prev[i], 0]
    return dist


def traveled(dist):
    d = 0
    for i in dist:
        d += i
    return d

def neighbor_search(v, object_f, veh, iterations, neighbor):
    tabu_size = round(len(v) * veh / 4)
    v_best = list(v)
    f_best = object_f(v)
    v_base = list(v_best)
    f_base = f_best
    tabu_list = list()
    swap_a = 0
    swap_b = 0
    i = 0
    while i < iterations:
        f_veh_route_best = f_base
        v_neighbor_best = v_base
        veh_route_best = [0] * len(v)
        index_in_curr = [0] * len(v)
        veh_rand = random.randint(0, veh-1)
        r_ind = 0
        for j in range(len(v)):
            if v_base[j][1] == veh_rand:
                veh_route_best[r_ind] = v_base[j][0]
                index_in_curr[r_ind] = j
                r_ind += 1
        if r_ind > 1:
            for k in range(neighbor):
                v_current = list(v_base)
                a = random.randint(0, r_ind-1)
                b = random.randint(0, r_ind-1)
                while a == b:
                    b = random.randint(0, r_ind-1)
                temp_a = (veh_route_best[a], veh_rand)
                temp_b = (veh_route_best[b], veh_rand)
                v_current[index_in_curr[a]] = temp_b
                v_current[index_in_curr[b]] = temp_a
                f_current = object_f(v_current)
                if f_current < f_veh_route_best:
                    f_veh_route_best = f_current
                    v_neighbor_best = v_current
                    swap_a = temp_a
                    swap_b = temp_b
            if (swap_a and swap_b) not in tabu_list:
                v_base = v_neighbor_best
                f_base = f_veh_route_best
                tabu_list.append(swap_a)
                tabu_list.append(swap_b)
                if len(tabu_list) >= (tabu_size - 2):
                    tabu_list.pop(0)
                    tabu_list.pop(0)
                if f_base < f_best:
                    v_best = v_base
                    f_best = f_base
        f_veh_route_best = f_base
        v_neighbor_best = v_base
        swap_a = 0
        swap_b = 0
        if veh > 1:
            for k in range(neighbor):
                v_current = list(v_base)
                a = random.randint(0, len(v)-1)
                b = random.randint(0, len(v)-1)
                while a == b:
                    b = random.randint(0, len(v)-1)
                temp_a = (v_current[a][0], v_current[b][1])
                temp_b = (v_current[b][0], v_current[a][1])
                v_current[a] = temp_b
                v_current[b] = temp_a
                f_current = object_f(v_current)
                if f_current < f_veh_route_best:
                    f_veh_route_best = f_current
                    v_neighbor_best = v_current
                    swap_a = temp_a
                    swap_b = temp_b
            if (swap_a and swap_b) not in tabu_list:
                v_base = v_neighbor_best
                f_base = f_veh_route_best
                tabu_list.append(swap_a)
                tabu_list.append(swap_b)
                if len(tabu_list) >= (tabu_size - 2):
                    tabu_list.pop(0)
                    tabu_list.pop(0)
                if f_base < f_best:
                    v_best = v_base
                    f_best = f_base
        i += 1
    return v_best


def print_solution(v, veh, dist):
    for i in range(veh):
        print("Route for vehicle", i+1)
        print(0, "-> ", end = "")
        for j in range(len(v)):
            if v[j][1] == i:
                print(v[j][0], "-> ", end = "")
        print(0)
        print("Distance of route: ", dist[i], "m\n")
    print("\nTotal distance: ",traveled(dist), "m")


def print_file(loc, veh, vrp, v_best, dist):
    f = open("vrp_solution.txt", "w")
    f.write("Locations: ")
    f.write(str(loc))
    f.write(" Vehicle: ")
    f.write(str(veh))
    f.write("\n")
    f.write(str(vrp))
    f.write("\n")
    f.write("\n")
    for i in range(veh):
        f.write("Route for vehicle ")
        f.write(str(i+1))
        f.write(": ")
        f.write(" 0")
        f.write(" -> ")
        for j in range(len(v_best)):
            if v_best[j][1] == i:
                f.write(str(v_best[j][0]))
                f.write(" -> ")
        f.write("0")
        f.write("\nDistance of route: ")
        f.write(str(dist[i]))
        f.write("m\n")
    d = 0
    for i in dist:
        d += i
    f.write("\nTotal distance: ")
    f.write(str(d))
    f.write("m\n")
    


def main():
    locations = [10, 20, 50, 100, 200, 500]
    vehicle = [1, 2, 4, 5, 10, 20]
    l_ind = random.randint(0, len(locations)-1)
    if l_ind >= 2:
        v_ind = random.randint(0, len(vehicle)-1)
    else:
        v_ind = random.randint(0, len(vehicle)-3)
    loc = locations[l_ind]
    veh = vehicle[v_ind]


    vrp = dist_initialize(loc)
    print(vrp)
    vrp_dict = transform_vrp(vrp)
    vrp_init = vrp_initialize(loc, veh)
    print(vrp_init)
    
    object_f = lambda sched: traveled(dstnc(vrp_dict, sched, veh))
    v_improved = neighbor_search(vrp_init, object_f, veh, 200, 100)
    print_solution(v_improved, veh, dstnc(vrp_dict, v_improved, veh))
    print_file(loc, veh, vrp, v_improved, dstnc(vrp_dict, v_improved, veh))

main()
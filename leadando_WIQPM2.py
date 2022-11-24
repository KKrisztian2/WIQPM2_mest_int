import random


def distance(l1, l2):
    return (abs(l1[0] - l2[0]) + abs(l1[1] - l2[1]))


def vrp_initialize(loc, veh):
    i = 0
    vrp_init = [0] * (loc - 1)
    while i < loc- 1:
        v_rand = random.randint(0, veh-1)
        vrp_init[i] = (i+1, v_rand)
        i += 1
    return vrp_init


def dist_initialize(loc):
    vrp = [0] * loc
    for i in range(loc):
        x_rand = random.randint(0, 1000)
        y_rand = random.randint(0, 1000)
        vrp[i] = (x_rand, y_rand)
    return vrp


def transform_vrp(tsp):
    tsp_dict = {}
    for i in range(len(tsp)):
        for j in range(len(tsp)):
            tsp_dict[(i, j)] = distance(tsp[i], tsp[j])
    return tsp_dict


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

def local_search(v, object_f, veh, iterations):
    tabu_size = round(len(v) * veh / 2)
    tabu_size = 4
    v_best = list(v)
    f_best = object_f(v)
    tabu_list = list()
    i = 0
    while i < iterations:
        v_current = list(v_best)
        veh_route = [0] * len(v)
        index_in_curr = [0] * len(v)
        veh_rand = random.randint(0, veh-1)
        r_ind = 0
        for j in range(len(v)):
            if v_current[j][1] == veh_rand:
                veh_route[r_ind] = v_current[j][0]
                index_in_curr[r_ind] = j
                r_ind += 1
        if r_ind > 1:
            a = random.randint(0, r_ind-1)
            b = random.randint(0, r_ind-1)
            while a == b:
                b = random.randint(0, r_ind-1)
            temp_a = (veh_route[a], veh_rand)
            temp_b = (veh_route[b], veh_rand)
            if(temp_a and temp_b) not in tabu_list:
                v_current[index_in_curr[a]] = temp_b
                v_current[index_in_curr[b]] = temp_a
                i += 1
                tabu_list.append(temp_a)
                tabu_list.append(temp_b)
                f_current = object_f(v_current)
                if f_current < f_best:
                    f_best = f_current
                    v_best = v_current
                if len(tabu_list) == (tabu_size - 1):
                    tabu_list.pop(0)
                if len(tabu_list) == (tabu_size):
                    tabu_list.pop(0)
                    tabu_list.pop(1)
        a = random.randint(0, len(v)-1)
        b = random.randint(0, len(v)-1)
        if veh > 1:
            temp_a = (v_current[a][0], random.randint(0, veh-1))
            temp_b = (v_current[b][0], random.randint(0, veh-1))
            if(temp_a and temp_b) not in tabu_list:
                v_current[a] = temp_b
                v_current[b] = temp_a
                i += 1
                tabu_list.append(temp_a)
                tabu_list.append(temp_b)
                f_current = object_f(v_current)
                if f_current < f_best:
                    f_best = f_current
                    v_best = v_current
                if len(tabu_list) == (tabu_size - 1):
                    tabu_list.pop(0)
                if len(tabu_list) == (tabu_size):
                    tabu_list.pop(0)
                    tabu_list.pop(1)
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
    v_improved = local_search(vrp_init, object_f, veh, 100000)
    print_solution(v_improved, veh, dstnc(vrp_dict, v_improved, veh))
    print_file(loc, veh, vrp, v_improved, dstnc(vrp_dict, v_improved, veh))

main()
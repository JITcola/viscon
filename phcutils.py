from phcpy.solutions import make_solution
from phcpy.curves import set_homotopy_continuation_gamma
from phcpy.curves import set_homotopy_continuation_parameter
from phcpy.solver import number_of_symbols
from phcpy.solutions import strsol2dict
from phcpy.solutions import variables
from phcpy.curves import standard_set_homotopy
from phcpy.curves import standard_set_solution
from phcpy.curves import standard_predict_correct
from phcpy.curves import standard_get_solution
from phcpy.curves import standard_t_value
from phcpy.curves import standard_step_size
from phcpy.curves import standard_pole_radius
from phcpy.curves import standard_closest_pole
from phcpy.curves import standard_series_coefficients
from phcpy.curves import standard_pade_vector
from phcpy.curves import standard_poles


def wiz_sols_to_phc_sols(sols):
    result = []
    poly_vars = sols[0][0]
    for sol in sols:
        sol_coords = [complex(coord) for coord in sol[1]]
        result.append(make_solution(poly_vars, sol_coords))
    return result


def run_tracker(start, sols, target, sol_num, gamma, min_step, max_step,
                num_steps):
    set_homotopy_continuation_gamma(gamma.real, gamma.imag)
    set_homotopy_continuation_parameter(5, min_step)
    set_homotopy_continuation_parameter(4, max_step)
    set_homotopy_continuation_parameter(12, num_steps)
    dim = number_of_symbols(start)
    result = [[], [], [], [], [], [], []]
    for i in range(dim):
        result[2].append([])
    standard_set_homotopy(target, start, False)
    idx = 0
    choice_sol = sol_num
    solution = sols[choice_sol-1]
    idx = idx + 1
    standard_set_solution(dim, solution, False)
    solution = standard_get_solution(False)
    solution_dict = strsol2dict(solution)
    var_names = variables(solution_dict)
    var_names.sort()
    result[0].append(standard_t_value())
    result[1].append(standard_step_size())
    for i in range(len(var_names)):
        result[2][i].append(solution_dict[var_names[i]])
    result[3].append(standard_closest_pole())
    result[4].append(standard_pole_radius())
    result[5].append(standard_series_coefficients(dim))
    result[6].append(standard_pade_vector(dim))
    for i in range(num_steps):
        standard_predict_correct(False)
        solution = standard_get_solution(False)
        solution_dict = strsol2dict(solution)
        result[0].append(standard_t_value())
        result[1].append(standard_step_size())
        for j in range(len(var_names)):
            result[2][j].append(solution_dict[var_names[j]])
        result[3].append(standard_closest_pole())
        result[4].append(standard_pole_radius())
        result[5].append(standard_series_coefficients(dim))
        result[6].append(standard_pade_vector(dim))
    for i in range(len(result[2])):
        for j in range(len(result[2][i])):
            result[2][i][j] = (result[2][i][j].real, result[2][i][j].imag)
    return result

# Ask the user to input two space separated even numbers less than 100 until requirements fulfilled
while True:
    nm = input("Please, enter two space separated integers for the dimensions of the area:\n").split()
    # Check if input is exactly 2 entries
    if len(nm) != 2:
        continue
    # Check if input entries are integers
    try:
        N, M = int(nm[0]), int(nm[1])
    except ValueError:
        continue
    # Check if in input entries a even numbers less than 100
    if (N < 1 or N > 100) or (M < 1 or M > 100) or N % 2 != 0 or M % 2 != 0:
        print("N and M should be positive even numbers less than 100!")
    else:
        break

# Create a list of strings for the output with a leading asterisk for every line
result = ["*" for i in range(N * 2)]


# Use a dictionary to check the number of occurrence of each brick id
def check_bricks(dic):
    for val in dic.values():
        if val != 2:
            print("Bricks should span exactly two squares!")
            return False
    return True


# Ask the user to input the positions of the bricks in the first layer
while True:
    layer1 = []  # Instantiate an empty array for the positions of bricks in layer 1
    bricks = {}  # Instantiate an empty dictionary used to check the number of occurrence of each brick id
    print("Please, enter bricks description row by row:")
    for _ in range(N):
        row = list(map(int, input().rstrip().split()))
        # Check if the required number of brick ids are provided
        if len(row) != M:
            print("Please, enter a valid number of bricks:")
            continue
        # Populate the dictionary with brick ids as keys and number of occurrence as values
        for number in row:
            bricks[number] = 1 if number not in bricks.keys() else bricks[number] + 1
        layer1.append(row)  # Add the row of brick ids to variable layer1

    if check_bricks(bricks):
        break

# Create another array with dimensions MxN for holding brick ids for the second layer and populate it with 0s
layer2 = [[0 for i in range(M)] for j in range(N)]


# A function rotating bricks 90 degrees to the right for a 2x2 slice of the layer
def shift_clockwise(layer, k, l):
    layer2[k][l] = layer[1][0]
    layer2[k][l + 1] = layer[0][0]
    layer2[k + 1][l + 1] = layer[0][1]
    layer2[k + 1][l] = layer[1][1]


""" A function used for filling in the lines for the result variable in case the bricks are vertically rotated.
    the function is performed on a 2x2 slice of the layer """


def fill_result_shifted(k, l):
    brick_id = layer2[k][l]
    result[k * 2] += str(brick_id).rjust(2) + "*"
    result[k * 2 + 1] += "  *"
    result[k * 2 + 2] += str(brick_id).rjust(2) + "*"
    result[k * 2 + 3] += 3 * "*"
    brick_id = layer2[k][l + 1]
    result[k * 2] += str(brick_id).rjust(2) + "*"
    result[k * 2 + 1] += "  *"
    result[k * 2 + 2] += str(brick_id).rjust(2) + "*"
    result[k * 2 + 3] += 3 * "*"


""" A function used for filling in the lines for the result variable in case the bricks are horizontally positioned.
    The function is performed on a 2x2 slice of the layer """


def fill_result(k, l):
    brick_id = layer2[k][l]
    result[k * 2] += str(brick_id).rjust(2) + " " + str(brick_id).rjust(2) + "*"
    result[k * 2 + 1] += 6 * "*"
    brick_id = layer2[k + 1][l]
    result[(k + 1) * 2] += str(brick_id).rjust(2) + " " + str(brick_id).rjust(2) + "*"
    result[(k + 1) * 2 + 1] += 6 * "*"


# A function used to populate a 2x2 slice of the resulting layer with the next consecutive values as brick ids
def fill_slice(m, n, k, l, brick_id):
    val = brick_id
    for row in range(k, n):
        for col in range(l, m, 2):
            layer2[row][col] = val
            layer2[row][col + 1] = val
            val += 1


# A function used to check if the bricks in a 2x2 slice of layer2 coincide with the same bricks in layer1
def check_slice(k, l):
    brick_id = layer1[k][l]
    if (layer2[k][l] == brick_id and layer2[k][l + 1] == brick_id and layer1[k][l + 1] == brick_id) \
            or (layer2[k][l] == brick_id and layer2[k + 1][l] == brick_id and layer1[k + 1][l] == brick_id):
        return False
    brick_id = layer1[k + 1][l]
    if layer2[k + 1][l] == brick_id and layer2[k + 1][l + 1] == brick_id and layer1[k + 1][l + 1] == brick_id:
        return False

    return True


""" Traverse the grid by 2x2 slices populating layer2 with consecutive numbers and checking for coincidence
between the bricks in both layers. If such is found rotate the bricks in layer2. 
Update the lines in the result variable"""
i = 0
value = 1  # Used for populating layer2 starting at 1 and incrementing on the fly
while i < N:
    j = 0
    while j < M:
        fill_slice(j + 2, i + 2, i, j, value)  # Populate a 2x2 slice in layer2 with value
        # Create a copy of the slice if rotation is necessary
        temp = [layer2[row][j:j + 2] for row in range(i, i + 2)]
        # Check for coincidence between bricks in both layers, rotate if necessary and update the result
        if check_slice(i, j):
            fill_result(i, j)
        else:
            shift_clockwise(temp, i, j)
            fill_result_shifted(i, j)
        value += 2
        j += 2
    i += 2

print((M * 3 + 1) * "*")  # Print the top edge of layer2
# Print the resulting layer
for line in result:
    print(line)

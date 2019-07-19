import createTrainingData

def get_data():
    x = []
    y = [] #Position, Rotation, Velocity, Angular_Velocity, jump, pitch, yaw, roll
    for i in range(1,28):
        gameData = createTrainingData.loadSavedTrainingData("data/replay"+str(i)+".pbz2")
        jumped_1 = False
        jumped_2 = False
        jump_time_1 = 1000
        jump_time_2 = 1000
        for j in range(len(gameData)):
            player1_x, player1_y = get_player_data(gameData, j, 0)
            player2_x, player2_y = get_player_data(gameData, j, 1)
            ball = get_ball_data(gameData, j)
            time = gameData[i]["GameState"]["time"]
            #if they jump get data until they a) jump again or b) can't jump again
            if time - jump_time_1 > 1.5 and jumped_1:
                jumped_1 = False
            elif player1_x[0] == 1 and jumped_1:
                x.append(player1_x + player2_x + ball)
                y.append(player1_y)
                jumped_1 == False
            elif player1_y[0] == 1 and not jumped_1:
                x.append(player1_x + player2_x + ball)
                y.append(player1_y)
                jumped_1 == True
                jump_time_1 = time
            elif player1_x[0] == 0 and jumped_1:
                x.append(player1_x + player2_x + ball)
                y.append(player1_y)


            if time - jump_time_2 > 1.5 and jumped_2:
                jumped_2 = False
            elif player2_x[0] == 1 and jumped_2:
                x.append(player2_x + player1_x + ball)
                y.append(player2_y)
                jumped_2 == False
            elif player2_y[0] == 1 and not jumped_2:
                x.append(player2_x + player1_x + ball)
                y.append(player2_y)
                jumped_2 == True
                jump_time_2 = time
            elif player2_x[0] == 0 and jumped_2:
                x.append(player2_x + player1_x + ball)
                y.append(player2_y)
    return x, y

def get_player_data(gameData, frame, index):
    position = gameData[frame]["PlayerData"][index]["position"]
    position = [position[0]/4096, position[1]/5120, position[2]/2044]
    rotation = gameData[frame]["PlayerData"][index]["rotation"]
    velocity = gameData[frame]["PlayerData"][index]["velocity"]
    velocity = [velocity[0]/23000, velocity[1]/23000, velocity[2]/23000]
    angular_velocity = gameData[frame]["PlayerData"][index]["angular_velocity"]
    angular_velocity = [angular_velocity[0]/5500, angular_velocity[1]/5500, angular_velocity[2]/5500]
    jump = gameData[frame]["PlayerData"][index]["jump"]
    pitch = gameData[frame]["PlayerData"][index]["pitch"]
    yaw = gameData[frame]["PlayerData"][index]["yaw"]
    roll = gameData[frame]["PlayerData"][index]["roll"]
    x = position + rotation + velocity + angular_velocity
    y = [1 if jump else 0, pitch, yaw, roll]
    return x, y

def get_ball_data(gameData, frame):
    location = gameData[frame]["GameState"]["ball"]["position"]
    location = [location[0]/4096, location[1]/5120, location[2]/2044]
    velocity = gameData[frame]["GameState"]["ball"]["velocity"]
    velocity = [velocity[0]/23000, velocity[1]/23000, velocity[2]/23000]
    return location + velocity

import random
from time import time
from generation.GenRandom import GenRandom

class GenRandomCorridors(GenRandom):

    def __init__(self, maze):
        super().__init__(maze)

    def get_random_lenght_corridor(self) -> int:
        return random.randint(2, random.randint(2, (self.get_width()-2)//3))

    def generate_corridors(self, debug=False):

        
        # Initialize the maze generation
        self.set_origin(self.get_cell_current().x, self.get_cell_current().y)
        self.set_finish(self.get_width()-2, self.get_height()-2)
        print("[DEBUG] Origin set at:", self.get_origin().x, self.get_origin().y)
        print("[DEBUG] Finish set at:", self.get_finish().x, self.get_finish().y)
        print("[DEBUG] Current cell at:", self.get_cell_current().x, self.get_cell_current().y," Direction:", self.maze.get_direction())
        


#-------------------------------------Generation Loop-------------------------------------#
        finished=False

        while not finished:

            i=self.get_random_lenght_corridor()

    #-------------------------------------Corridor Loop-------------------------------------#

            for iter in range(2, i): 

        #-------------------------------------Cell Loop-------------------------------------#   
                end_corridor = False
                if iter==i-1: 
                    end_corridor = True 
        
        #-------------------------------------1.1 Verification-------------------------------------#
                # TODO - Add the corners to avoid shadow looping
                current_cell = self.get_cell_current()
                print(f'Current Cell: {repr(current_cell)}')
                current_direction = self.get_direction()
                cells = {
                    "front": {
                        "cell": self.get_cell_front(current_cell),
                        "neighboor": self.get_cell_front(current_cell,howfar=2),
                        # "state_cell": None,  # good_path, not_path, loop_path
                        # "state_neighboor": None,
                        # "state_path": None,
                        "relative_direction": 0
                    },
                    "right": {
                        "cell": self.get_cell_right(current_cell),
                        "neighboor": self.get_cell_right(current_cell,howfar=2),
                        # "state_cell": None,
                        # "state_neighboor": None,
                        # "state_path": None,
                        "relative_direction": 1
                    },
                    "left": {
                        "cell": self.get_cell_left(current_cell),
                        "neighboor": self.get_cell_left(current_cell,howfar=2),
                        # "state_cell": None,
                        # "state_neighboor": None
                        # "state_path": None,
                        "relative_direction": 3
                    },
                    "back": {
                        "cell": self.get_cell_back(current_cell),
                        "neighboor": self.get_cell_back(current_cell,howfar=2),
                        # "state_cell": None,
                        # "state_neighboor": None
                        # "state_path": None,
                        "relative_direction": 2
                    },
                    "free_neightboor": 0
                }
                
                for key, value in cells.items():
                    if not isinstance(value, dict):
                        continue  # ignore les ints
                    value["state_cell"]=self.state_to_str(value["cell"])
                    value["state_neighboor"]=self.state_to_str(value["neighboor"])
                    if value["state_cell"] == "wall" or value["state_cell"] == "visited":
                        value["state_path"]="unvalid"
                    elif value["state_cell"] == "free" and (value["state_neighboor"] == "free" or value["state_neighboor"] == "wall"):
                        value["state_path"]="valid"
                        cells["free_neightboor"]+=1
                    elif value["state_cell"] == "free" and value["state_neighboor"] == "visited":
                        value["state_path"]="looping"
                    else:
                        raise ValueError("The state of a path cannot be undefined")

        #-------------------------------------1.2 Print Verification-------------------------------------#
                
                for key, value in cells.items():
                    if not isinstance(value, dict):
                        continue  # ignore les ints
                    print(key)
                    for cle,truc in value.items():
                        print(f'{cle}: {repr(truc)}')
                    print(f'Free neighboors: {cells["free_neightboor"]}')

                        
                
        #-------------------------------------2.1 Blocking the loops-------------------------------------#
                
                for key, direction in cells.items():
                    if not isinstance(direction, dict):
                        continue  # ignore free neightboor
                    if direction["state_path"]=="looping":
                        print(f'Cell (to the {key} of current) will create a loop: {direction["cell"]}')
                        match key:
                            case "front":
                                self.put_wall_infront()
                            case "right":
                                self.put_wall_right()
                            case "left":
                                self.put_wall_left()
                            case "back":
                                self.put_wall_back()


                action=""
                yield action  # --- C'est ici que ton step est renvoyé à pygame ---

                    

        #-------------------------------------2.2 Deciding next move-------------------------------------#
                
                next_move = {
                    # "turn":0,
                    # "forward":False
                }
                back_next_split=False

                if not end_corridor and cells["front"]["state_path"]=="valid": 
                    if cells["free_neightboor"] == 0:
                        # If deadend, to delete from split list
                        self.del_split_node(current_cell)
                        back_next_split=True                  
                    #forward without turning
                    print("valid")
                    next_move["turn"]=0
                    next_move["forward"]=True 
                elif end_corridor or cells["front"]["state_path"]=="unvalid" or cells["front"]["state_path"]=="looping":
                    end_corridor=True
                    if cells["free_neightboor"] == 0:
                        # If deadend, to delete from split list
                        self.del_split_node(current_cell)
                        back_next_split=True
                    else:
                        next_move["turn"] = self.choose_random_direction()
                        next_move["forward"]=True 
                    if cells["free_neightboor"] == 2:
                        # Check if avaiable for split
                        self.add_split_node(current_cell)

            
        #-------------------------------------3.1 Update position-------------------------------------#
                
                if not end_corridor and cells["front"]["state_path"]=="valid":
                    self.put_wall_onsides(current_cell)
                if back_next_split:
                    next_cell=self.get_last_split_node()
                    self.set_current(next_cell.x,next_cell.y)
                    end_corridor=True
                else:
                    match next_move["turn"]:
                        case 0:
                            pass
                        case 1:
                            self.turn_right()
                        case 2:
                            self.turn_back()
                        case 3:
                            self.turn_left()
                    if next_move["forward"]:
                        self.forward()


                if end_corridor:
                    break

                
                        
                    
                    




                

                # elif not end_corridor and cells["front"]["state_path"]=="looping":
                #     print("looping")
                #     if cells["free_neightboor"]==0:
                #         pass
                #         # TODO - go back next split

                #     elif cells["free_neightboor"]==1:
                #         for key, direction in cells.items():
                #             if direction["state_path"]=="valid":
                #                 match key:
                #                     case "right":
                #                         next_move["turn"] = 1
                #                     case "left":
                #                         next_move["turn"] = 3
                #                     case "back":
                #                         next_move["turn"] = 2
                #                 next_move["forward"]=True 
                                
                #     elif cells["free_neightboor"]==2:
                #         # Check if avaiable for split
                #         split_list.append(current_cell)
                #         token=False
                #         for key, direction in cells.items():
                #             if direction["state_path"]=="valid":
                #                 if random.choice([True, False]) or token:
                #                     match key:
                #                         case "right":
                #                             next_move["turn"] = 1
                #                         case "left":
                #                             next_move["turn"] = 3
                #                         case "back":
                #                             next_move["turn"] = 2
                #                     next_move["forward"]=True 
                #                     break
                #                 else:
                #                     token=True

                    #verif if has a valid path
                        #not -> go back next split
                        #yes -> take random direction
            
                
                







#                     action = self.forward_not_to_loop()
#                     # Last cell of the corridor
#                 if not self.is_infront_valid(self.get_cell_current()):
#                     # End the corridor
#                     if self.is_deadend(self.get_cell_current()):
#                         print("[DEBUG] Deadend reached at:", x_loop, y_loop)
#                         if len(self.split_nodes)==0:
#                             print("[DEBUG] No more split nodes available, finishing generation.")
#                             finished = True
#                         elif len(self.split_nodes)>0:
#                             self.set_current(self.get_last_split_node().x, self.get_last_split_node().y)
#                             try:
#                                 self.del_split_node(x_loop, y_loop)
#                             except ValueError:
#                                 pass
#                             action = self.forward_not_to_loop()
#                             action = "Take a random direction from last split node and move forward"
                            
#                         # Go back to last split node
#                         # No need to put walls around
#                         action = "Go back to last available split node"
#                     elif self.is_cornered(self.get_cell_current()):
#                         print("[DEBUG] Cornered reached at:", x_loop, y_loop)
#                         # Change direction facing the good side
#                         self.forward_not_to_loop()
#                         action = "Change direction facing the good side and move forward"
#                     else:
#                         print("[DEBUG] Wall reached at:", x_loop, y_loop)
#                         # Create a split node
#                         self.add_split_node(self.get_cell(x_loop, y_loop))
#                         print("[DEBUG] Split node added at:", x_loop, y_loop)
#                         print("[DEBUG] Show split node list:", [(node.x, node.y) for node in self.split_nodes])
#                         # Turn to a random side 
#                         self.forward_not_to_loop()
#                         action = "Create split node and random turn and move forward"
#                     # If wall if front, we end the corridor to start a new one
#                     loop_break = True
#                 else:
#                     print("[DEBUG] Moving forward at:", x_loop, y_loop)
#                     # Puting walls on the sides of the corridor
#                     self.put_wall_onsides(self.get_cell_current())
#                     # Dont change direction, go forward
#                     self.forward_not_to_loop()
#                     action = "move forward"
                
#                 if finished:
#                     break

                

#                 if loop_break:
#                     break

#             # adding current cell as a new split node at the end of the corridor if possible
#             # x_loop, y_loop = self.get_current_cell().x, self.get_current_cell().y

#                 # if corridor_ended:
#                 #     # Check if deadend or cornered to handle split nodes
#                 #     if self.is_deadend(self.get_current_cell()):
#                 #         try:
#                 #             self.del_split_node(x_loop, y_loop)
#                 #         except ValueError:
#                 #             pass
#                 #         # Switch to the last split node
#                 #         self.maze.set_current(self.get_last_split_node().x, self.get_last_split_node().y)
#                 #     elif self.is_cornered(self.get_current_cell()):
#                 #         try:
#                 #             self.del_split_node(x_loop, y_loop)
#                 #         except ValueError:
#                 #             pass
#                 #         # Turn to the good side
#                 #         if self.is_rightside_valid(self.get_current_cell()):
#                 #             # Change direction to left
#                 #             self.turn_left()
#                 #         elif self.is_leftside_valid(self.get_current_cell()):
#                 #             # Change direction to right
#                 #             self.turn_right()
                        
#                     # Check if wall in front to create a split node

#                     # Break the for loop to start a new corridor

                    

#                 # Update the current cell 



                
#                 # #For the last cell of the corridor (checking corners and deadends))
#                 # self.get_current_cell().set_visited()
#                 # print("[DEBUG] Current cell visited at:", x_loop, y_loop)
#                 # if self.is_deadend(self.get_current_cell()):
#                 #     self.del_split_node(x_loop, y_loop)
#                 #     #Switch to the last split node
#                 # elif self.is_cornered(self.get_current_cell()):
#                 #     self.del_split_node(x_loop, y_loop)
#                 #     #Turn to the good side
#                 # elif self.is_infront_valid(self.get_current_cell()):
#                 #     self.add_split_node(x_loop, y_loop)
#                 #     #Turn to a random side (left or right)
#                 # else: #No wall in front
#                 #     #Continue forward



# #             if self.is_fully_generated():
# #                 finished = True
# #             self.turn_right()
# # Il faut que je flag les cases sur lequel on est déja passé pour pas les transfromer en murs et fasse la fonctionalité de split               


import json
import logging
from pathlib import Path

class Param:
    def __init__(self):
        self.content= {}

    def updateparamfromfile(self):
        p=Path(__file__).parents[2] / "data/interface/param.json"
        try:
            with p.open("r", encoding="utf-8") as f:
                self.content = json.load(f)
                logging.info(f"UI parameters loaded successfully: {self.content}")
        except FileNotFoundError:
            logging.warning("UI param file not found")
        except Exception as e:
            logging.error(f"Error reading UI param file: {e}")

    def get_width(self):
        return self.content["WIDTH"]
    
    def get_height(self):
        return self.content["HEIGHT"]
    
    def get_nav_height(self):
        return self.content["NAV_H"]
    
    def get_control_width(self):
        return self.content["CONTROL_W"]
    
    def get_maze_width(self):
        return self.get_width() - self.get_control_width()
    
    def get_width_debug(self):
        return self.content["WIDTH_DEBUG"]

    def get_height_debug(self):
        return self.content["HEIGHT_DEBUG"]
    
    def __str__(self):
        return f"{self.content}"

    def __repr__(self):
        return f"Param({self.content})"
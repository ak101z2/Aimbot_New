import matplotlib.pyplot as plt
import numpy as np
import math
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

class Trajectory:
    def __init__(self, coordinates=[], tolerance=0):
        self.slope = math.nan
        self.intercept = math.nan
        self.coordinates = coordinates
        self.line_segments = []
        self.tolerance = tolerance
    
    def update(self, coordinate):
        if (self.is_consistent(coordinate)):
            self.coordinates.append(coordinate)
            self.perform_regression()
            self.calculate_line_segments
        else:
            self.coordinates.append(coordinate)
            self.slope = self.intercept = math.nan
            self.coordinates.clear()
            self.line_segments.clear()
    
    def is_consistent(self, coordinate):
        if self.slope == self.intercept == math.nan:
            return True
        x, y = coordinate
        predicted_y = self.slope*x + self.intercept
        if abs(predicted_y - y) <= self.tolerance:
            return True
        else:
            return False

    def perform_regression(self):
        x = [coord[0] for coord in self.coordinates]
        y = [coord[1] for coord in self.coordinates]
        x = np.array(x).reshape(-1, 1)
        model = LinearRegression()
        model.fit(x, y)
        self.slope = model.coef_[0]
        self.intercept = model.intercept_

    def calculate_line_segments():
        pass

    def __str__(self):
        return "Slope: " + self.slope + " , Intercept: " + self.intercept + " , Coordinates: " + self.coordinates




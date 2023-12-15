from shapely.geometry import Point, Polygon, LineString
import matplotlib.pyplot as plt
import random
import polygenerator as pg



def distance(p1, p2):
    # Calculate the distance between two points
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) ** 0.5

def find_middle_point(p1, p2):
    # Calculate the middle point on the line connecting p1 and p2
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

#complexity O(logn)

def find_cutting_point(first_point, middle_point1,middle_point2, polygon):
    total_area = polygon_area(polygon)
    precision = 0.0001  # Adjust as needed

    left = middle_point1
    right = middle_point2

    while abs(left[0] - right[0]) > precision or abs(left[1] - right[1]) > precision:
        # Calculate the midpoint
        mid = find_middle_point(left, right)


        # Calculate the area of the triangle formed by the cutting point, first point, and middle point
        triangle_area1 = polygon_area([first_point, mid, middle_point1])
        
        triangle_area2 = polygon_area([first_point, mid, middle_point2])

        

        if triangle_area1 > triangle_area2 :
            right = mid
        else:
            left = mid

    # The cutting point is found
    print(triangle_area1,triangle_area2)
   

    return mid


#complexity O(logn)
def find_cutting_vertex(polygon):
    # Calculate total area of the polygon
    total_area = polygon_area(polygon)
    
    # Define precision for binary search
    precision = 0.0001  # Adjust as needed
    
    left = 0
    right = len(polygon) - 1
    
    while left <= right:
        # Update the 'middle' index based on updated boundaries
        middle = (left + right) // 2
        
        # Calculate areas for left and right sides of the current 'middle' vertex
        area_left = polygon_area(polygon[:middle+1])  # Include the middle vertex in the calculation
        area_right = total_area - area_left
        
        if abs(area_left - area_right) < precision:
            return polygon[middle]  # Return the found vertex
        
        if area_left > area_right:
            right = middle - 1
        else:
            left = middle + 1
    
    return right,left # Return None if no such vertex is found


#complexity O(n)
def polygon_area(vertices):
    n = len(vertices)
    area = 0.0

    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]

    area = abs(area) / 2.0
    return area


#complexity O(n)
def point_position(xp, yp, polygon):
    test_point = Point(xp, yp)
    ray = LineString([(xp, yp), (xp + 1e6, yp)])  # Create a horizontal ray

    intersections = ray.intersection(polygon)
    unique_intersections = list(set(intersections.coords))  # Remove duplicate intersection points
    
    if len(unique_intersections)-1== 0 or len(unique_intersections)-1 % 2 == 1:
        return "Inside"
    else:
        return "Outside"




num_vertices = random.randint(4, 8)
polygon_vertices =pg.random_convex_polygon(num_vertices)
#polygon_vertices = [(1, 1), (4, 5), (7, 3), (5, 1)]
polygon = Polygon(polygon_vertices)

# Test point
test_point_x, test_point_y = 0, 1

position = point_position(test_point_x, test_point_y, polygon)
print(f"The point ({test_point_x}, {test_point_y}) is {position} the polygon.")
print(f"The area of the polygon is {polygon_area(polygon_vertices)}.")





    # Plotting the line passing through the centroid
v,v1= find_cutting_vertex(polygon_vertices)
cutting_point = find_cutting_point(polygon_vertices[0], polygon_vertices[v],polygon_vertices[v1], polygon_vertices)

# Plot the polygon
x, y = zip(*polygon.exterior.coords)
plt.plot(x, y, 'r-')

# Plot the test point
plt.plot(test_point_x, test_point_y, 'bo')

plt.plot(cutting_point[0], cutting_point[1], 'bo')

plt.text(test_point_x, test_point_y, f'({test_point_x}, {test_point_y})', verticalalignment='bottom')
plt.plot([cutting_point[0], polygon_vertices[0][0]], [cutting_point[1], polygon_vertices[0][1]], linestyle='--', color='red')


plt.plot([test_point_x, test_point_x + 10], [test_point_y, test_point_y], 'g--')


plt.title('Polygon with Test Point')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid()
plt.show()
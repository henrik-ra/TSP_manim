from manim import *
from manim_svg_animations import *

import os
import random
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
from manim_voiceover.services.gtts import GTTSService
import itertools
from itertools import permutations

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService
from scipy.spatial import KDTree
from basics import CustomGraph

# voices: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts

DARK_BLUE_COLOR = "#00008b"

class IntroNew(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-GuyNeural ",
                style="newscast-casual",
            )
        ) 

        svg_object = SVGMobject("world.svg").scale(3).set_color(WHITE)
        self.add(svg_object)
        self.wait(1)
 

        # with self.voiceover(text="Imagine you're a traveling salesperson - tasked with selling your products in various cities. Your goal?") as tracker:
        with self.voiceover(text="Welcome back, folks! Today, we're diving into the Traveling Salesperson Problem.") as tracker:
            None
        with self.voiceover(text="Imagine we have a traveling salesperson - tasked with selling your products in various cities.") as tracker:
            # remove map
            self.remove(svg_object)

            # Salesperson
            image = ImageMobject("Salesman.png").scale(0.3)
            start_pos = image.get_center()

            self.add(image)

        with self.voiceover(text="This guy is Alex, a salesperson with a big challenge.") as tracker:
            alex_label = Text("Alex", font_size=48).next_to(image, UP*2, buff=0.1)

            # Add the label to the scene
            self.play(Write(alex_label))

        # with self.voiceover(text="To visit each city exactly once and return to your starting point afterwards, all while traveling the shortest possible route.") as tracker:
        with self.voiceover(text="Alex has to sell products in various cities and wants to take the shortest route to save time. But how does Alex figure out the best route? Let's dive in and help Alex solve this puzzle.") as tracker:

            # to bring to front
            self.remove(image)
            # add map and remove name
            self.remove(alex_label)
            self.add(svg_object)

            # to bring to front
            self.add(image)

            move_up_right = start_pos + 0.5*DOWN + 2.6*RIGHT
            move_down_left = start_pos + 1.5*DOWN + 2*LEFT
            move_up_left = start_pos + 1.5*UP + 2.5*LEFT


            # Move image up and to the right, then back
            self.play(image.animate.move_to(move_up_right).scale(0.25))
            self.play(image.animate.move_to(start_pos).scale(4))
            # Move image down and to the left, then back
            self.play(image.animate.move_to(move_down_left).scale(0.25))
            self.play(image.animate.move_to(start_pos).scale(4))

            self.play(image.animate.move_to(move_up_left).scale(0.25))
            self.play(image.animate.move_to(start_pos).scale(4))

            self.wait(4)

            self.remove(image) 


        with self.voiceover(text="Let's say he needs to visit 4 cities.") as tracker:
            
            pin_svg_path = "map-pin.svg"
            # Definieren Sie die Punkte (Städte)

            points0 = [
                SVGMobject(pin_svg_path).scale(0.25).move_to(np.array([0, 0.5, 0])), # DE
                SVGMobject(pin_svg_path).scale(0.25).move_to(np.array([3, -1.75, 0])), # Australia
                SVGMobject(pin_svg_path).scale(0.25).move_to(np.array([0.5, -1.75, 0])), # Afrika
                SVGMobject(pin_svg_path).scale(0.25).move_to(np.array([-3.35, 0, 0])), # USA
            ]

           # points0 = [
            #     Dot(np.array([0, 0.22, 0]), color=DARK_GREY), # DE
            #     Dot(np.array([3, -2, 0]), color=DARK_GREY), # Australia
            #     Dot(np.array([0.5, -2, 0]), color=DARK_GREY), # Afrika
            #     Dot(np.array([-3.35, 0, 0]), color=DARK_GREY), # USA
            # ]

            # Stellen Sie die Punkte auf der Szene dar
            for point in points0:
                self.add(point)

        with self.voiceover(text="Sounds straightforward, right? What do you think happens if we add one more city to Alex's route?") as tracker:

            connections = [
            (0, 1),  # Verbindung von DE zu Afrika
            (1, 2),  # Verbindung von Afrika zu Australia
            (2, 3),  # Verbindung von Australia zu USA
            (3, 0)
            # Fügen Sie hier weitere Verbindungen hinzu
            ]

            # Load the plane image
            plane_image = ImageMobject("plane.png").scale(0.12)

            lines = []
            for start_index, end_index in connections:
                # Create a line between points
                line = Line(points0[start_index].get_center(), points0[end_index].get_center(), color=BLUE)
                lines.append(line)

                # Calculate the angle of the line
                # angle = line.get_angle()

                # Create a temporary copy of the plane for this line
                temp_plane = image.copy()
                # temp_plane = plane_image.copy()

                temp_plane.move_to(points0[start_index].get_center())

                # Rotate the plane to match the line's angle
                # temp_plane.rotate(angle)

                # Animate the line creation and the plane moving along it
                self.play(Create(line), MoveAlongPath(temp_plane, line), run_time=1.5)

                # Optionally fade out the plane at the end of its path
                self.play(FadeOut(temp_plane))

            self.wait(2)

            # Entfernen der Linien und Punkte von der Szene
            for line in lines:
                self.remove(line)
            for point in points0:
                self.remove(point)

        with self.voiceover(text="Of course, if we add more cities it get's more complex. So how do you determine the shortest possible route that connects all these cities?") as tracker:
            # Definieren Sie die Punkte (Städte)
            points = [
                Dot(np.array([0, 0.22, 0]), color=DARK_GREY), # DE
                Dot(np.array([-0.28, -0.16, 0]), color=DARK_GREY), # Spain

                Dot(np.array([2.5, -0.5, 0]), color=DARK_GREY), # Asia
                Dot(np.array([2.5, 0.3, 0]), color=DARK_GREY), # Asia

                Dot(np.array([0.5, -2, 0]), color=DARK_GREY), # Afrika
                # Dot(np.array([0.5, -1, 0]), color=DARK_GREY), # Afrika

                Dot(np.array([3, -2, 0]), color=DARK_GREY), # Australia

                Dot(np.array([-1.5, -1.6, 0]), color=DARK_GREY), # Südamerika

                Dot(np.array([-3.35, 0, 0]), color=DARK_GREY), # USA
                # Dot(np.array([-3.2, -0.2, 0]), color=DARK_GREY), # USA
                Dot(np.array([-3, 0.5, 0]), color=DARK_GREY), # Canada
            ]

            for point in points:
                self.add(point)
            
            # Label points for clarity
            # labels = ["Germany", "Spain", "Asia", "Asia", "Africa", "Australia", "South America", "USA", "Canada"]
            # label_objects = []
            # for i, point in enumerate(points):
            #     label = Text(labels[i], font_size=24, color=PURPLE).next_to(point, DOWN)
            #     label_objects.append(label)
            #     self.add(label)

        with self.voiceover(text="One approach is to try out every possible route. But here lies the problem: Complexity! So, with every new city Alex adds to the trip, the challenge of finding the shortest route grows significantly.") as tracker:
            
            # Generate all permutations of points
            point_indices = range(len(points))  
            all_routes = list(permutations(point_indices))

            # Animate each route
            for route in all_routes[:100]:
                # Create a path for the current route
                path = VMobject(color=BLUE)
                path.set_points_as_corners([points[i].get_center() for i in route] + [points[route[0]].get_center()])
                self.play(Create(path), run_time=0.1)
                self.wait(0.05)
                # Remove the path before drawing the next one
                self.remove(path)



        for point in points:
            self.remove(point)
        # for point, label in zip(points, label_objects):
        #     self.remove(point, label)
        
        self.play(FadeOut(svg_object))

        with self.voiceover(text="The Problem to find the shortest way between multiple points is called the Traveling Salesperson Problem (TSP)") as tracker:
            intro_text = Text("Traveling Salesman Problem (TSP)").to_edge(UP)
            self.play(Write(intro_text))


class Assumptions(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-GuyNeural ",
                style="newscast-casual",
            )
        )
        
        with self.voiceover(text="To solve it, we'll think of each city as a point, or 'node', on a graph. The edges symbolize possible paths Alex can take. "):
        # Define vertices and edges
                    # Define vertices and edges
            vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            # edges = [(1, 2), (2, 3), (3, 4), (2, 4), (2, 5), (6, 5),
            #         (1, 7), (5, 7), (2, 8), (1, 9)]
            edges = [(i, j) for i in vertices for j in vertices if i < j]


            # Create the custom graph
            graph = CustomGraph(vertices, edges)

            # Create labels using the add_labels method
            labels = graph.add_labels()

            # Animate the nodes
            for vertex in graph.vertices.values():
                self.play(GrowFromCenter(vertex), run_time=0.2)
            
            # Add and animate the labels
            self.add(labels)
            self.play(FadeIn(labels), run_time=0.5)
            self.wait(1)

            # Group the graph and labels together
            graph_with_labels = VGroup(graph, labels) # because lables didnt belong to graph so far, thus dont move

            # Apply transformations to the group
            self.play(graph_with_labels.animate.shift(LEFT*3).scale(0.8), run_time=1)
        
        with self.voiceover(text="It's complete, this means there's a direct path from every city to every other city."):
            # Add edges to make the graph complete
                        # Animate the edges
                        # Create and animate the text
            point1 = Text("1. Complete graph", font_size=36)
            point1.next_to(graph_with_labels, RIGHT, buff=1).shift(UP)   # Position the text to the right of the graph

            self.play(Write(point1))
            
            for edge in graph.get_edges_with_initial_opacity_zero():
                self.play(edge.animate.set_opacity(1), run_time=0.1)
            self.wait(1)

        # with self.voiceover(text="Our TSP is symmetric. It means the distance from city A to B is identical to the distance from B to A."):
        #     # Highlight symmetric edges
        #     edge_ab = graph.get_edge(0, 1)
        #     edge_ba = graph.get_edge(1, 0)
        #     self.play(edge_ab.animate.set_color(BLUE), edge_ba.animate.set_color(GREEN))
        #     self.wait(1)


        with self.voiceover(text="Our TSP is symmetric. It means the distance from city A to B is identical to the distance from B to A."):

                point_2 = Text("2. symmetric", font_size=36)
                point_2.next_to(point1, DOWN, aligned_edge=LEFT)
                self.play(Write(point_2))


                # Animation für das Hervorheben von bestimmten Kanten
                self.play(graph.edges[(2,7)].animate.set_color(RED), run_time=0.5)
                self.wait(2)

                # Erstellen eines Punktes als bewegliches Objekt
                moving_dot = Dot(color=RED, radius=0.1)

                # Erstellen eines Glüh-Effekts um den Punkt
                glow_effect = Circle(radius=0.15, color=RED, fill_opacity=0.5)
                glow_effect.add_updater(lambda m: m.move_to(moving_dot.get_center()))

                # Abrufen der Start- und Endpositionen der Kante (2,7)
                start_pos = graph.vertices[2].get_center()
                end_pos = graph.vertices[7].get_center()

                # Erstellen eines Pfades für die Kante
                edge_path = Line(start_pos, end_pos)

                # Hinzufügen des Punktes und des Glüh-Effekts zur Szene
                self.add(moving_dot, glow_effect)

                # Animieren des Punktes entlang des Pfades
                self.play(MoveAlongPath(moving_dot, edge_path), run_time=1.5)
                self.wait(1)
                # Animieren des Punktes zurück entlang desselben Pfades
                self.play(MoveAlongPath(moving_dot, edge_path.reverse_direction()), run_time=1.5)

                # Entfernen des Glüh-Effekts Updater
                glow_effect.clear_updaters()


        with self.voiceover(text="Also, in our model, the direct path between any two cities is always the shortest. This means for two cities A and B there is no path with an added point that is shorter than the direct connection.  adhering to the triangle inequality principle."):
                
                # Ausblenden des Punktes und des Glüh-Effekts
                self.play(FadeOut(moving_dot), FadeOut(glow_effect), run_time=0.5)

                # Zurücksetzen der Kantenfarbe auf die ursprüngliche Farbe
                self.play(graph.edges[(2,7)].animate.set_color(GREY), run_time=0.5) 
                
                point_3 = Text("3. triangle inequality", font_size=36)
                point_3.next_to(point_2, DOWN, aligned_edge=LEFT)
                self.play(Write(point_3))

                # Definieren der Knoten und Kanten
                vertices = [1, 2, 3]
                edges = [(1, 2), (2, 3)]

                # Erstellen eines benutzerdefinierten Layouts
                layout = {
                    1: LEFT,
                    2: ORIGIN,
                    3: RIGHT
                }

                # Erstellen des CustomGraph mit den definierten Knoten, Kanten und dem Layout
                graph2 = CustomGraph(vertices, edges, layout=layout)

                
                
                # Erstellen der Beschriftungen
                label_a = Text("A", font_size=24).next_to(graph2.vertices[1], UP, buff=0.1)
                label_n = Text("n", font_size=24).next_to(graph2.vertices[2], UP, buff=0.1)
                label_b = Text("B", font_size=24).next_to(graph2.vertices[3], UP, buff=0.1)

                # Gruppieren des Graphen und der Beschriftungen
                graph_with_labels = VGroup(graph2, label_a, label_n, label_b)

                # Verschieben der gesamten Gruppe nach rechts und unten
                graph_with_labels.shift(RIGHT*2.5 + DOWN*2)

                # Hinzufügen des Graphen und der Beschriftungen zur Szene
                self.play(Create(graph_with_labels))

                # Erstellen und Speichern der Pfeile in einer Liste
                arrows = []
                for edge in edges:
                    start_pos = graph2.vertices[edge[0]].get_center()
                    end_pos = graph2.vertices[edge[1]].get_center()
                    arrow = Arrow(start_pos, end_pos, buff=0.3, tip_length=0.2, stroke_width=3, stroke_color=GREY)
                    self.add(arrow)
                    arrows.append(arrow)

                # Halten der Szene
                self.wait(2)

                # Ausblenden der Pfeile
                for arrow in arrows:
                    self.play(FadeOut(arrow), run_time=0.5)

        #     # Illustrate triangle inequality
        #     direct_edge = graph.get_edge(0, 2)
        #     detour_edges = VGroup(graph.get_edge(0, 1), graph.get_edge(1, 2))
        #     self.play(direct_edge.animate.set_color(RED), detour_edges.animate.set_color(YELLOW))
        #     self.wait(1)


                # Entfernen des Mittleren Knotens "n" und der angrenzenden Kanten
                self.play(
                    FadeOut(graph2.vertices[2]),  # Entfernen des Knotens "n"
                    FadeOut(graph2.edges[(1, 2)]),  # Entfernen der Kante zwischen A und n
                    FadeOut(graph2.edges[(2, 3)]),  # Entfernen der Kante zwischen n und B
                    FadeOut(label_n),  # Entfernen der Beschriftung "n"
                    run_time=1
                )

                # Hinzufügen einer neuen Kante zwischen A und B
                new_edge = Line(graph2.vertices[1].get_center(), graph2.vertices[3].get_center(), buff=0.3)
                new_edge.set_z_index(-1)  # Setzt die Z-Ebene der Kante hinter die Knoten
                self.play(Create(new_edge), run_time=1)

                # Halten der Szene
                self.wait(2)

                # delete
                self.remove(new_edge)
                self.play(FadeOut(graph_with_labels))

        with self.voiceover(text="With these rules in mind, let's explore how Alex can find the shortest route.") as tracker:
            # Transition text
            self.wait(2)
          
        self.wait(1)



class BruteForce(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-GuyNeural ",
                style="newscast-casual",
            )
        )
        # the graph class expects a list of vertices and edges
        vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        edges = [(1, 2), (2, 3), (3, 4), (2, 4), (2, 5), (6, 5),
                 (1, 7), (5, 7), (2, 8), (1, 9)]

        h = CustomGraph(vertices, edges).shift(RIGHT * 0)

        # Verschieben des gesamten Graphen
        self.play(Create(h))

        self.wait(4)
        h.scale(0.5)

        # Animation für das Hervorheben von bestimmten Kanten
        for edge in h.edges:
            self.play(h.edges[edge].animate.set_color(RED), run_time=0.5)
            self.wait(0.1)
            self.play(h.edges[edge].animate.set_color(GREEN), run_time=0.5)

        self.wait(1)



class PointskNN(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-GuyNeural ",
                style="newscast-casual",
            )
        )

        # Erstelle 50 zufällige Punkte
        np_random = np.random.RandomState(42)
        points = [Dot(np.array([np_random.uniform(-4, 4), np_random.uniform(-3, 3), 0])) for _ in range(50)]
        self.add(*points)

        # Wähle einen Startpunkt
        current_point = random.choice(points)
        start_point = current_point  # Speichere den Startpunkt für später
        visited = {current_point}

        # Funktion, um die Distanz zwischen zwei Punkten zu berechnen
        def distance(p1, p2):
            return np.linalg.norm(p1.get_center() - p2.get_center())

        # Suche den nächsten unbesuchten Punkt
        for _ in range(len(points) - 1):
            next_point = min(
                (p for p in points if p not in visited),
                key=lambda p: distance(current_point, p)
            )
            visited.add(next_point)

            # Zeichne eine Linie zum nächsten Punkt
            line = Line(current_point.get_center(), next_point.get_center(), color=BLUE)
            self.play(Create(line), run_time=0.1)

            # Aktualisiere den aktuellen Punkt
            current_point = next_point

        # Zeichne eine Linie zurück zum Startpunkt
        line_to_start = Line(current_point.get_center(), start_point.get_center(), color=BLUE)
        self.play(Create(line_to_start), run_time=0.1)

        self.wait(2)

        
class GraphkNN(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-GuyNeural ",
                style="newscast-casual",
            )
        )
        # the graph class expects a list of vertices and edges
        vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        edges = [(1, 2), (2, 3), (3, 4), (2, 4), (2, 5), (6, 5),
                 (1, 7), (5, 7), (2, 8), (1, 9)]

        h = CustomGraph(vertices, edges).shift(RIGHT * 0)

        # Verschieben des gesamten Graphen
        self.play(Create(h))

        self.wait(4)
        h.scale(0.5)

        # Animation für das Hervorheben von bestimmten Kanten
        for edge in h.edges:
            self.play(h.edges[edge].animate.set_color(RED), run_time=0.5)
            self.wait(0.1)
            self.play(h.edges[edge].animate.set_color(GREEN), run_time=0.5)

        self.wait(1)


# class Intro(VoiceoverScene):
#     def construct(self):
#         self.set_speech_service(
#             AzureService(
#                 voice="en-US-GuyNeural ",
#                 style="newscast-casual",
#             )
#         ) 
#         # self.camera.background_color = BLACK

#         with self.voiceover(text="The Traveling Salesman Problem (TSP) is a classic problem in computer science and operations research.") as tracker:
#             # Introduction Text
#             intro_text = Text("Traveling Salesman Problem").to_edge(UP)
#             explanation1 = Text("The challenge: Find the shortest path visiting all cities.", font_size=24).next_to(intro_text, DOWN)
#             self.play(Write(intro_text), FadeIn(explanation1))
#             self.wait(2)
#             self.play(FadeOut(explanation1))

#         with self.voiceover(text="Let's assume we are an international salesman and need to visit clients all over the world. Our time is very expensive so we need to find the most feasible and shortest way.") as tracker:
            
#             # Load the image
#             image = ImageMobject("Salesman_stolen.png")
#             image.scale(0.3)  # Skalieren Sie das Bild nach Bedarf

#             # Start position
#             start_pos = image.get_center()

#             # Move up and to the right
#             move_up_right = start_pos + 1.5*UP + 3*RIGHT
#             # Move down and to the left
#             move_down_left = start_pos + 3*DOWN + 3*LEFT

#             # Add image to the scene
#             self.add(image)
#             self.wait(3)

#             # Move image up and to the right, then back
#             self.play(image.animate.move_to(move_up_right))
#             self.play(image.animate.move_to(start_pos))

#             # Move image down and to the left, then back
#             self.play(image.animate.move_to(move_down_left))
#             self.play(image.animate.move_to(start_pos))

#             self.wait(4)
#             self.remove(image)

#             # fade out header
#             self.play(FadeOut(intro_text))


#         with self.voiceover(text="There are several ways to calculate or find the shortest way between different point, cities in this case. This visualization is based on the k nearest neighbors method. This algorithm  involves the salesman starting at a city and, for each step, visiting the nearest unvisited city until all cities are visited. Essentially, the salesman looks at the 'k' closest cities and selects the nearest one as the next stop. While this is simple and intuitive, this heuristic does not guarantee the shortest overall route, especially as 'k' is typically set to 1 for TSP, hence it's often used for initial approximations.") as tracker:

#             # World Map
#             svg_object = SVGMobject("world.svg").scale(3).set_color(WHITE)
#             self.play(FadeIn(svg_object))
#             self.wait(5)
            
#             # Definieren Sie die Punkte (Städte)
#             points = [
#                 Dot(np.array([0, 0.22, 0]), color=DARK_GREY), # DE
#                 Dot(np.array([-0.28, -0.16, 0]), color=DARK_GREY), # Spain

#                 Dot(np.array([2.5, -0.5, 0]), color=DARK_GREY), # Asia
#                 Dot(np.array([2.5, 0.3, 0]), color=DARK_GREY), # Asia

#                 Dot(np.array([0.5, -2, 0]), color=DARK_GREY), # Afrika
#                 Dot(np.array([0.5, -1, 0]), color=DARK_GREY), # Afrika

#                 Dot(np.array([3, -2, 0]), color=DARK_GREY), # Australia

#                 # Dot(np.array([-1.7, -2, 0]), color=DARK_GREY), # Südamerika
#                 Dot(np.array([-1.5, -1.6, 0]), color=DARK_GREY), # Südamerika

#                 Dot(np.array([-3.35, 0, 0]), color=DARK_GREY), # USA
#                 Dot(np.array([-3.2, -0.2, 0]), color=DARK_GREY), # USA
#                 Dot(np.array([-3, 0.5, 0]), color=DARK_GREY), # Canada
#                 # Fügen Sie hier mehr Punkte hinzu
#             ]

#             # Stellen Sie die Punkte auf der Szene dar
#             for point in points:
#                 self.add(point)

#             # TSP Algorithmus: Nearest-Neighbor
#             route = self.nearest_neighbor(points, 0)

#             # Zeichnen Sie die Linien zwischen den Punkten basierend auf der Route
#             # for i in range(len(route) - 1):
#             #     start_point = points[route[i]].get_center()
#             #     end_point = points[route[i + 1]].get_center()
#             #     line = Line(start_point, end_point, color=DARK_BLUE, stroke_width=2)
#             #     self.play(Create(line), run_time=0.5)


#             self.wait(14)

#             # Delete World Map
#             self.play(FadeOut(svg_object))

#     def nearest_neighbor(self, points, start_index):
#         num_points = len(points)
#         visited = [False] * num_points
#         visited[start_index] = True
#         route = [start_index]

#         current_index = start_index
#         while len(route) < num_points:
#             nearest_index = None
#             nearest_distance = float('inf')

#             # Zeichnen und Löschen der Pfeile zu allen unbesuchten Punkten
#             temp_arrows = []
#             for i in range(num_points):
#                 if not visited[i]:
#                     arrow = Arrow(points[current_index].get_center(), points[i].get_center(), buff=0, color=DARK_BLUE)
#                     temp_arrows.append(arrow)
#                     self.play(Create(arrow), run_time=0.1)

#             # Finden der kürzesten Verbindung
#             for i in range(num_points):
#                 if not visited[i]:
#                     distance = np.linalg.norm(points[current_index].get_center() - points[i].get_center())
#                     if distance < nearest_distance:
#                         nearest_distance = distance
#                         nearest_index = i

#             # Löschen Sie alle Pfeile außer dem zur kürzesten Verbindung
#             for arrow in temp_arrows:
#                 if np.all(arrow.get_end() == points[nearest_index].get_center()):
#                     self.play(Transform(arrow, Line(arrow.get_start(), arrow.get_end(), color=ORANGE)))
#                 else:
#                     self.play(FadeOut(arrow), run_time=0.1)

#             visited[nearest_index] = True
#             route.append(nearest_index)
#             current_index = nearest_index

#         # Zeichnen der letzten Linie zurück zum Startpunkt
#         last_line = Line(points[current_index].get_center(), points[start_index].get_center(), color=ORANGE)
#         self.add(last_line)

#         route.append(start_index)  # Rückkehr zum Startpunkt


# USE TRACKER_DURATION
class AzureExample(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-GuyNeural ",
                style="newscast-casual",
            )
        )

        circle = Circle()
        square = Square().shift(2 * RIGHT)

        with self.voiceover(text="This circle is drawn as I speak.") as tracker:
            self.play(Create(circle), run_time=tracker.duration)

        with self.voiceover(text="Let's shift it to the left 2 units.") as tracker:
            self.play(circle.animate.shift(2 * LEFT), run_time=tracker.duration)

        with self.voiceover(text="Now, let's transform it into a square.") as tracker:
            self.play(Transform(circle, square), run_time=tracker.duration)

        with self.voiceover(
            text="You can also change the pitch of my voice like this.",
            prosody={"pitch": "+40Hz"},
        ) as tracker:
            pass

        with self.voiceover(text="Thank you for watching."):
            self.play(Uncreate(circle))

        self.wait(5)


if __name__ == "__main__":
    os.system(f"manim -pqh --disable_caching {__file__} IntroNew")

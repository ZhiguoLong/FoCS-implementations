from typing_extensions import runtime
from manim import BLACK, MathTex, Scene,Circle,Line,Text,Write,VGroup,Create,config,Graph
from manim import ReplacementTransform,Transform,FadeOut,Indicate
from manim import PINK,WHITE,BLUE,RED,BLACK,GREEN
from manim import LEFT,RIGHT,UP,DOWN,YELLOW,PURPLE,ORANGE

config.background_color = WHITE 

class AugmentingPath(Scene):
    def __init__(self):
        super().__init__()
        # toy example
        # self.X = ['1','2','3']
        # self.Y = ['u','v','x']
        # self.edges = [('1','u'),('1','x'),('2','v'),('2','x'),('3','u'),('3','v')]
        
        # lecture notes example
        self.X = ['x_1','x_2','x_3','x_4','x_5','x_6']
        self.Y = ['y_1','y_2','y_3','y_4','y_5']
        self.edges = [('x_1','y_1'),('x_1','y_2'),('x_2','y_3'),('x_3','y_1'),('x_3','y_3'),('x_3','y_5'),
            ('x_4','y_1'),('x_4','y_3'),('x_4','y_5'),('x_5','y_2'),('x_5','y_4'),('x_6','y_3'),('x_6','y_5')]
        self.M = {}

        # # lecture notes full example
        # self.X = ['x_1','x_2','x_3','x_4','x_5','x_6','x_7']
        # self.Y = ['y_1','y_2','y_3','y_4','y_5']
        # self.edges = [('x_1','y_1'),('x_1','y_2'),('x_1','y_4'),('x_2','y_3'),('x_2','y_5'),('x_3','y_4'),('x_3','y_5'),
        #     ('x_4','y_1'),('x_4','y_2'),('x_5','y_3'),('x_6','y_1'),('x_6','y_3'),('x_7','y_2'),('x_7','y_4'),('x_7','y_5')]
        # self.M = {}

        # # Slides example
        # self.X = ['x_1','x_2','x_3','x_4','x_5','x_6','x_7']
        # self.Y = ['y_1','y_2','y_3','y_4','y_5']
        # self.edges = [('x_1','y_1'),('x_1','y_2'),('x_1','y_4'),('x_2','y_3'),('x_2','y_5'),('x_3','y_4'),('x_3','y_5'),
        #     ('x_4','y_1'),('x_4','y_2'),('x_5','y_3'),('x_6','y_1'),('x_6','y_3'),('x_7','y_2'),('x_7','y_4'),('x_7','y_5')]
        # self.M = {}

        # # Slides example with given M
        # self.X = ['x_1','x_2','x_3','x_4','x_5','x_6','x_7']
        # self.Y = ['y_1','y_2','y_3','y_4','y_5']
        # self.edges = [('x_1','y_1'),('x_1','y_2'),('x_1','y_4'),('x_2','y_3'),('x_2','y_5'),('x_3','y_4'),('x_3','y_5'),
        #     ('x_4','y_1'),('x_4','y_2'),('x_5','y_3'),('x_6','y_1'),('x_6','y_3'),('x_7','y_2'),('x_7','y_4'),('x_7','y_5')]
        # self.M = {'x_1':'y_1','y_1':'x_1','x_2':'y_3','y_3':'x_2','x_7':'y_2','y_2':'x_7'}
        
        config.frame_width = len(self.X)+2

        self.edges_dict = {}
        for e in self.edges:
            if e[0] not in self.edges_dict:
                self.edges_dict[e[0]] = {e[1]}
            else:
                self.edges_dict[e[0]].add(e[1])
            if e[1] not in self.edges_dict:
                self.edges_dict[e[1]] = {e[0]}
            else:
                self.edges_dict[e[1]].add(e[0])
        
        self.B = [self.X,self.Y,self.edges,self.edges_dict]
    
    def breadth_first_search_scratch(self,B,M,top_nodes_dict,bottom_nodes_dict):
        visited = set()
        Ux = set()
        pred = dict()
        Y = B[1]
        X = B[0]
        edges = B[3]
        
        # M_tuple = [(x,M[x]) for x in X if x in M]
        # print("X:",X)
        # print("Y:",Y)
        for x in X:
            if x not in M:
                Ux.add(x)
        # print("Ux:",Ux)
        L = sorted(list(Ux))
        # print("L:",L)
        for l in L:
            visited.add(l)
            if l in top_nodes_dict:
                self.play(top_nodes_dict[l].animate.set_fill(color=GREEN))
            else:
                self.play(bottom_nodes_dict[l].animate.set_fill(color=GREEN))
        # print("visited:",visited)
        frame_height = config.frame_height
        L_tex = MathTex(r"\text{Starts with L}: ["+",".join(L)+"]", color=RED).move_to(UP*(frame_height/2-0.5))
        self.play(Write(L_tex))
        while len(L) > 0:
            a = L.pop(0)
            print("a:",a)
            # print("L:",L)
            if a in top_nodes_dict:
                self.play(top_nodes_dict[a].animate.set_fill(color=YELLOW))
                self.play(Indicate(top_nodes_dict[a]))
            else:
                self.play(bottom_nodes_dict[a].animate.set_fill(color=YELLOW))
                self.play(Indicate(bottom_nodes_dict[a]))
            L_tex_new = (MathTex("L: ["+",".join(L)+"]", color=BLACK)).move_to(UP*(frame_height/2-0.5))
            self.play(ReplacementTransform(L_tex, L_tex_new))
            if a in X:
                nbrs = sorted(edges[a])
                for b in nbrs:
                    print("b:",b)
                    self.play(Indicate(self.edge_lines[(a,b)]))
                    if b not in visited and (a not in M or b != M[a]):
                        visited.add(b)
                        self.play(Indicate(top_nodes_dict[b]))
                        self.play(top_nodes_dict[b].animate.set_fill(color=GREEN),run_time=1)
                        # draw_matching_graph(B,M_tuple,visited,a)
                        pred[b] = a
                        if b in M:
                            L.append(b)
                            L_tex_new_new = (MathTex("L: ["+",".join(L)+"]", color=BLACK)).move_to(UP*(frame_height/2-0.5))
                            self.play(ReplacementTransform(L_tex_new, L_tex_new_new))
                            L_tex_new = L_tex_new_new
                        else:
                            
                            print("M: ",M)
                            P = [b]
                            c = b
                            while c not in Ux:
                                d = pred[c]
                                c = d
                                P.append(c)
                            P.reverse()
                            if a in top_nodes_dict:
                                self.play(top_nodes_dict[a].animate.set_fill(color=GREEN))
                            else:
                                self.play(bottom_nodes_dict[a].animate.set_fill(color=GREEN))
                            self.play(FadeOut(L_tex_new))
                            self.wait(0.5)
                            P_text = (MathTex(r"\text{Found augmenting path}: ["+",".join(P)+"]", color=BLUE)).move_to(UP*(frame_height/2-0.5))
                            self.play(Write(P_text))
                            self.wait(0.5)
                            self.play(FadeOut(P_text))
                            self.wait(0.5)
                            return P
            else:
                b = M[a]
                print("b:",b)
                self.play(Indicate(self.edge_lines[(b,a)]))
                visited.add(b)
                # draw_matching_graph(B,M_tuple,visited,a)
                self.play(Indicate(bottom_nodes_dict[b]))
                self.play(bottom_nodes_dict[b].animate.set_fill(color=GREEN))
                pred[b] = a
                L.append(b)
                L_tex_new_new = (MathTex("L: ["+",".join(L)+"]", color=BLACK)).move_to(UP*(frame_height/2-0.5))
                self.play(ReplacementTransform(L_tex_new, L_tex_new_new))
                L_tex_new = L_tex_new_new
            # print(L)
            L_tex = (MathTex(f"L: ["+",".join(L)+"]", color=BLUE)).move_to(UP*(frame_height/2-0.5))
            self.play(ReplacementTransform(L_tex_new, L_tex))
            if a in top_nodes_dict:
                self.play(top_nodes_dict[a].animate.set_fill(color=GREEN))
            else:
                self.play(bottom_nodes_dict[a].animate.set_fill(color=GREEN))
        self.wait(0.5)
        self.play(FadeOut(L_tex))
        self.wait(0.5)
        end_Text = (Text(f"No augmenting paths found.", color=BLUE)).move_to(UP*(frame_height/2-0.5))
        self.play(Write(end_Text))
        self.wait(0.5)
        self.play(FadeOut(end_Text))
        self.wait(0.5)
    
    def maximum_matching(self,B,top_nodes_dict,bottom_nodes_dict,edge_lines):
        # M = {}
        # M = self.M
        P = self.breadth_first_search_scratch(B,self.M,top_nodes_dict,bottom_nodes_dict)

        node_group = VGroup(*[*top_nodes_dict.values(),*bottom_nodes_dict.values()])
        node_group.set_fill(color=BLACK)

        while P is not None:
            to_adjust_edges_matched = []
            to_adjust_edges_unmatched = []
            # adjust M
            m = len(P)
            for i in range(m-1):
                if i % 2==0:
                    x = P[i]
                    y = P[i+1]
                    self.M[x] = y
                    self.M[y] = x
                    print("add match:",x,y)
                    to_adjust_edges_matched.append(edge_lines[(x,y)])
                    # self.play(edge_lines[(x,y)].animate.set_color(RED).set_stroke_width(4),run_time=1)
                else:
                    x = P[i]
                    y = P[i+1]
                    # self.M.pop(x) # shouldn't pop x, because x has been matched to a new node
                    # self.M.pop(y) # shouldn't pop y, because y will be matched to a new node
                    print("remove match:",y,x)
                    to_adjust_edges_unmatched.append(edge_lines[(y,x)])
                    # self.play(edge_lines[(y,x)].animate.set_color(BLACK).set_stroke_width(2),run_time=1)
            print("M:",self.M)
            to_adjust_edges_group = VGroup(*[*to_adjust_edges_matched,*to_adjust_edges_unmatched])
            self.play(Indicate(to_adjust_edges_group),run_time=1.5)

            to_adjust_edges_matched_group = VGroup(*[*to_adjust_edges_matched])
            self.play(to_adjust_edges_matched_group.animate.set_color(RED).set_stroke(width=4),run_time=1)

            to_adjust_edges_unmatched_group = VGroup(*[*to_adjust_edges_unmatched])
            self.play(to_adjust_edges_unmatched_group.animate.set_color(BLACK).set_stroke(width=2),run_time=1)
            P = self.breadth_first_search_scratch(B,self.M,top_nodes_dict,bottom_nodes_dict)
            node_group.set_fill(color=BLACK)
            self.wait(0.5)
        return self.M

    def construct(self):
        # Define graph vertices - two partitions
        top_nodes = [Circle(radius=0.2, color=BLACK,fill_opacity=1) for _ in self.Y]
        top_nodes_dict = {self.Y[i]:top_nodes[i] for i in range(len(self.Y))}
        bottom_nodes = [Circle(radius=0.2, color=BLACK,fill_opacity=1) for _ in self.X]
        bottom_nodes_dict = {self.X[i]:bottom_nodes[i] for i in range(len(self.X))}
        
        # Position top nodes horizontally at the top
        for i, node in enumerate(top_nodes):
            node.move_to(UP * 2 + LEFT*1.5 * (2- i))
            self.add(node)
            self.add(MathTex(f"{self.Y[i]}",color=BLACK).next_to(node, UP))
        
        # Position bottom nodes horizontally at the bottom
        for i, node in enumerate(bottom_nodes):
            node.move_to(DOWN * 2 + LEFT*1.5 * (2.5- i))
            self.add(node)
            self.add(MathTex(f"{self.X[i]}",color=BLACK).next_to(node, DOWN))
        
        # # Add edges
        # edges = [
        #     (0, 0), (0, 1),  # L0 to R0, R1
        #     (1, 1), (1, 2),  # L1 to R1, R2
        #     (2, 2), (2, 3)   # L2 to R2, R3
        # ]
        
        self.edge_lines = {}
        for b,t in self.edges:
            start = top_nodes_dict[t].get_bottom()
            end = bottom_nodes_dict[b].get_top()
            if t in self.M and self.M[t] == b:
                line = Line(start, end, color=RED, stroke_width=4)
            else:
                line = Line(start, end, color=BLACK, stroke_width=2)
            self.edge_lines[(b,t)]=line
            self.play(Create(line), run_time=0.5)

        # top_group = VGroup(*[*top_nodes,*bottom_nodes,*edge_lines.values()])
        # top_group.scale_to_fit_width(config.frame_width * 0.9)

        self.M = self.maximum_matching(self.B,top_nodes_dict,bottom_nodes_dict,self.edge_lines)
        
        # # Add title
        # title = Text("Bipartite Graph", font_size=24).to_edge(UP)
        # self.play(Write(title))
        
        # # Highlight bipartition
        
        # bottom_group = VGroup(*bottom_nodes)
        # self.play(
        #     top_group.animate.set_color(BLUE),
        #     bottom_group.animate.set_color(RED),
        #     run_time=2
        # )
        
        self.wait(1)

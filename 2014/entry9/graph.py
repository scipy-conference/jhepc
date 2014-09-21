import argparse
import pickle
import sys
from graph_tool.all import *

parser = argparse.ArgumentParser(description='graph.')
parser.add_argument('--pdf', action='store_true', default=False, help='output to PDF')
parser.add_argument('--save', type=str, help='save graph state to filename')
parser.add_argument('--load', type=str, help='load graph state from filename')
parser.add_argument('--ignoreleafs', action='store_true', default=True, help='ignore leaf nodes (that are not incumbents)')
parser.add_argument('--iterations', type=int, nargs='+', help='render graph at given iteration(s)')
parser.add_argument('--dotfile', type=str, help='dot filename')

args = parser.parse_args()

# default format is PNG
if args.pdf == True:
    format = ".pdf"
else:
    format = ".png"

# optionally load graph and layout from pickle file; otherwise we require a DOT file to compute the layout
if args.load != None:
    input = open(args.load, 'rb')
    g = pickle.load(input)
    pos = g.vertex_properties['pos']
    input.close()
elif args.dotfile != None:
    g = load_graph(args.dotfile)
    pos = sfdp_layout(g, epsilon=0.001, max_level=50, verbose=True)

    # save layout as an internal property of the graph so it can be saved
    g.vertex_properties['pos'] = pos
else:
    print 'either a graph state must be loaded or a dot file must be specified'
    sys.exit(1)

# optionally save graph and layout to pickle file
if args.save != None:
    output = open(args.save, 'wb')
    pickle.dump(g, output, -1)
    output.close()

iteration = g.vertex_properties["iteration"]
iteration = iteration.copy(value_type="int")  # converts to int

iterationIncumbent = g.vertex_properties["iterationIncumbent"]
iterationIncumbent = iterationIncumbent.copy(value_type="long")  # converts to long

iterationAddedChildren = g.vertex_properties["iterationAddedChildren"]
iterationAddedChildren = iterationAddedChildren.copy(value_type="long")  # converts to long

# draw full graph
# default vertex size = 5
graph_draw(g, pos=pos, output="graph-full" + format, output_size=(8192,8192), vertex_fill_color=iteration)

# draw graph for given iterations
if args.iterations != None:
    included = g.new_vertex_property("bool")
    included.a = False

    vertexShape = g.new_vertex_property("int")

    vertexHalo = g.new_vertex_property("bool")
    vertexHalo.a = False

    vertexHaloColor = g.new_vertex_property("vector<float>")

    vertexHaloSize = g.new_vertex_property("float")

    for i in args.iterations:
        print i

        g.set_vertex_filter(None)

        for v in g.vertices():
            if args.ignoreleafs == True:
                if iteration[v] <= i and (iterationIncumbent[v] <= i or iterationAddedChildren[v] <= i):
                    included[v] = True
            else:
                if iteration[v] <= i:
                    included[v] = True

            if iterationIncumbent[v] == i:
                vertexShape[v] = 7 # double circle
                vertexHalo[v] = True
                vertexHaloColor[v] = [0.5, 0.5, 0.5, 0.5]
                vertexHaloSize[v] = 20.0
            else:
                vertexShape[v] = 0 # circle
                vertexHalo[v] = False

        g.set_vertex_filter(included)

        iterationFilename = "graph-iteration-" +  "{0:06d}".format(i) + format
        graph_draw(g, pos=pos, output=iterationFilename, output_size=(4096,4096), vertex_fill_color=iteration, vertex_shape=vertexShape, vertex_halo=vertexHalo, vertex_halo_color=vertexHaloColor, vertex_halo_size=vertexHaloSize)

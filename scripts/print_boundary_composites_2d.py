from plots.utils import get_template_root
import xml.etree.ElementTree as ET
import os.path

def print_composite(edge_indices,lbl):
    print(f"{lbl}:")
    print("E["+",".join(edge_indices)+"]")

def print_boundary_composites(session_fpath,xleft,xright,ytop,ybtm):
    # Read vertices from session
    tree = ET.parse(session_fpath)
    root = tree.getroot()
    geom = root.find('GEOMETRY')
    vert_coords = [(float(t[0]),float(t[1])) for t in [ v.text.split() for v in geom.find('VERTEX')]]

    # Loop over session edges, compiling a list of indices for each boundary
    left  = []
    right = []
    top   = []
    btm   = []
    for ii,edge in enumerate(geom.find('EDGE')):
        v0,v1 = (int(s) for s in edge.text.split())
        if vert_coords[v0][0]==xleft and vert_coords[v1][0]==xleft:
            left.append(str(ii))
        if vert_coords[v0][0]==xright and vert_coords[v1][0]==xright:
            right.append(str(ii))
        if vert_coords[v0][1]==ytop and vert_coords[v1][1]==ytop:
            top.append(str(ii))
        if vert_coords[v0][1]==ybtm and vert_coords[v1][1]==ybtm:
            btm.append(str(ii))

    print_composite(left,'left')
    print_composite(right,'right')
    print_composite(top,'top')
    print_composite(btm,'bottom')

if __name__=='__main__':
    template = '2d-diff'
    session_fpath = os.path.join(get_template_root(template),'session.xml')
    print_boundary_composites(session_fpath,xleft=0,xright=2,ytop=5,ybtm=0)
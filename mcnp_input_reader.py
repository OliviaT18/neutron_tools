# -*- coding: utf-8 -*-
"""
MCNP input file reader
S Lilley
March 2019
"""
import sys
import argparse
import neut_utilities as ut

class mcnp_cell():
    """ """
    def __init__(self):
        self.number = ""
        self.mat = ""
        self.density = 0.0
        self.imp_p = 1.0
        self.imp_n = 1.0
        self.geom = ""
        self.surfaces = []


def read_mode_card(lines):
    """ """
    mode = None
    for l in lines:
        if l[0:4].lower() == "mode":
           l = ut.string_cleaner(l)
           mode = l.split(" ")[1:]
    return mode
    
    
def check_mode_valid(mode):
    """ """
    particle_list = ["n", "p", "h", "e"]
    for particle in mode:
        if particle.lower() not in particle_list:
            return False
    return True
  
  
def get_full_line_comments(lines):
    """ """
    comments = []
    for l in lines:
        if len(l) > 1 and l[0].lower() == "c" and l[1] == " ":
            comments.append(l)
    return comments
    
    
def get_material_numbers(lines):
    """ """
    mat_nums = []
    for l in lines:
        if len(l) > 1 and l[0].lower() == "m" and l[1].isdigit():
             l = ut.string_cleaner(l)
             l = l.split(" ")[0]
             mnum = l[1:] 
             mat_nums.append(int(mnum))
    return mat_nums
   
   
def get_tally_numbers(lines):
    """ """
    tal_nums = []
    for l in lines:
        if len(l) > 1 and l[0].lower() == "f" and l[1].isdigit():
             l = ut.string_cleaner(l)
             l = l.split(" ")[0]
             l = l.split(":")[0]
             tnum = l[1:] 
             tal_nums.append(int(tnum))
    return tal_nums
    
    
def check_surface_type_validity(surface):
    """ check surface is a valid mcnp type"""
    return True


def check_plane(surface):
    """ check entries on plane surface are valid """
    return True


def check_sphere(surface):
    """ check entries on sphere surface are valid"""
    return True


def check_cylinder(surface):
    """ check entries on cylinder surface are valid"""
    return True


def check_cone(surface):
    """ check entries on conical surface are valid """
    return True


def check_GQ(surface):
    """ check entries on GQ surface are valid """
    return True
    

def find_blank_lines(lines):
    """ find the location and count of balnk lines in the file """
    count = 0
    blank_dict = {}
    
    for i, l in enumerate(lines):
        if l == "":
            count = count + 1
            blank_dict[count] = i
            
    return count, blank_dict
    
    
def split_blocs(lines):
    """ split into the cell, surf and data blocks """
    
    blank_count, blank_loc = find_blank_lines(lines)
    cell_bloc = lines[:blank_loc[1]]
    surf_bloc = lines[blank_loc[1]:blank_loc[2]]
    data_bloc = lines[blank_loc[2]:]
    
    return cell_bloc, surf_bloc, data_bloc

    
def process_imp(part, cell):
    """ """
    imp_val = part.split("=")[-1]
    imp_particle = part.split(":")[1][0]
    if imp_particle.lower() == "p":
        cell.imp_p = imp_val
    elif imp_particle.lower() == "n":
        cell.imp_n = imp_val
    
    return cell

    
def process_geom(geom, cell):
    """ """
    surfaces = []
    for part in geom:
        if "imp" in part:
            cell = process_imp(part, cell)
            
    cell.geom = " ".join(geom)
    return cell

    
def process_cell_block(bloc):
    """ """
    cell_list = []
    cell = None
    for line in bloc:
        if line[0].isdigit():
            if cell is not None:
                cell = process_geom(geom, cell)
                cell_list.append(cell)
                
            cell = mcnp_cell()
            line = ut.string_cleaner(line)
            line = line.split(" ")
            cell.number = line[0]
            cell.mat = line[1]
            geo_start_pos = 2
            if cell.mat is not "0":
                cell.density = line[2]
                geo_start_pos = 3
            geom = line[geo_start_pos:]
        elif line[0:4] == "     ":
            geom = cell.geom.append(line)
        
        
    return cell_list
    
    
def get_cell(cell_num, cell_list):
    """ get cell from cell list """
    for cell in cell_list:
        if cell_num == cell.number:
            return cell
    
    return None 

        
def cells_with_mat(mat_num, cell_list):
    """ get all cells with mat """
    cells = []
    for cell in cell_list:
        if mat_num == cell.mat:
            cells.append(cell)
    return cells
    
    
def print_cell(cell):
    """ pretty printing of cell object """
    print("Cell number: ", cell.number)
    print("Cell material: ", cell.mat)
    print("Cell density: ", cell.density)
    print("Cell geom: ", cell.geom)
    print("Cell surfaces: ", cell.surfaces)
    print("Cell imp p:", cell.imp_p)
     
    
def read_mcnp_input(fpath):
    """ """

    ifile = ut.get_lines(fpath)
    cell_bloc, surf_bloc, data_bloc = split_blocs(ifile)
    cell_list = process_cell_block(cell_bloc)
    print_cell(cell_list[0])

    comments = get_full_line_comments(ifile) 
    
    mat_nums = get_material_numbers(data_bloc)
    
    return ifile

     
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="reads MCNP input file")
    parser.add_argument("input", help="path to the mcnp input file")
    args = parser.parse_args()

    read_mcnp_input(args.input)
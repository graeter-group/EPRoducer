"""
Molecular structure utilities for EPR g-value calculations: connectivity
analysis, radical site location, and structure extraction from npz
datasets.
"""

from ase.io import read, write
from ase.geometry.analysis import Analysis
from ase import Atoms
import numpy as np
import networkx as nx


def HFC_relevantA(atoms, radicals, depth=2):
    """
    Extract the H, O and N atoms in the neighborhood of the radicals up to
    certain depth (neighbors of neighbors, moving only through heavy atoms).
    It also includes the H atoms bonded to those O and N atoms.

    Parameters
    ==========
    atoms: ase.Atoms
        Atoms object containing the molecule.
    radicals: list
        posible positions of the radicals, implying that that neighborhood is
        important for the HFC. Indexes starting from 1.
    depth: int. Default=2
        number of times that it searches the neighbors of the neighbors.

    Return
    ======
    (dict) {element: list of indexes} with the indexes of the H, O and N
    atoms grouped by element, e.g. {'H': [3, 4], 'O': [7]}. The indices start
    with 1.
    """
    centers = np.array(radicals) - 1
    elements = np.array(atoms.get_chemical_symbols())
    ana = Analysis(atoms)
    relevant = []

    for _ in range(depth):
        new_neighbors = []
        for i in centers:
            neighbors = np.array(ana.all_bonds[0][i])
            e_neighbors = elements[neighbors]
            hydrogens = e_neighbors == 'H'
            oxygens = e_neighbors == 'O'
            nitrogens = e_neighbors == 'N'
            condition = np.logical_or(np.logical_or(hydrogens,
                                                    oxygens),
                                                    nitrogens)
            relevant.append(neighbors[condition])
            new_neighbors.append(neighbors[e_neighbors != 'H'])
        centers = [index for sublist in new_neighbors for index in sublist]

    # Add last hydrogens
    centers = np.array([index for sublist in relevant for index in sublist])
    for i in centers:
        neighbors = np.array(ana.all_bonds[0][i])
        e_neighbors = elements[neighbors]
        hydrogens = e_neighbors == 'H'
        relevant.append(neighbors[hydrogens])

    relevant = np.array([index for sublist in relevant for index in sublist])
    relevant = np.unique(relevant)
    separated_relevant = {}
    for i, element  in enumerate(elements[relevant]):
        if element not in list(separated_relevant.keys()):
            separated_relevant[str(element)] = []
        separated_relevant[element].append(int(relevant[i] + 1))

    return separated_relevant


# add2executable
def iHFC_fromxyz(file, radicals, depth):
    """
    Extract the H, O and N atoms in the neighborhood of the radicals up to
    certain depth (see HFC_relevantA). Those atoms are the relevant ones for
    HyperFine Calculations (HFC). This function receives strings as inputs.

    Parameters
    ==========
    file: str
        path to the molecule that you want to analyse. ASE must be able to read
        this file.
    radicals: str
        index of the atoms of posible location of the radicals, implying that
        that neighborhoods of this atoms are important for the HFC. 1-based
        indexes. It should be a list of integers in string format, e.g.:
        "[1, 5, 7]".
    depth: str
        number of times that it searches the neighbors of the neighbors.

    Return
    ======
    (dict) {element: list of indexes} with the indexes of the H, O and N
    atoms grouped by element. The indices start from 1.
    """
    atoms = read(file)
    radicals = eval(radicals)
    depth = int(depth)

    return HFC_relevantA(atoms, radicals, depth)


def get_connectivity(atoms, engine):
    """
    Computes the connectivity of a molecule.

    Parameters
    ==========
    atoms: ase.Atoms
        molecule to be analyzed.
    engine: str
        'vmd' to use the bonds detected by VMD (VMD must be in the PATH) or
        'ase' to use the natural cutoffs of ase.neighborlist.

    Return
    ======
    (list) [n_atoms] list where the element i contains the indices of the
    atoms bonded to the atom i. Indices start from 0.
    """
    if engine == 'vmd':
        from ase.io import write
        from eprtools.ase_utils.molecules import vmd_connectivity
        import os

        id = int(np.random.random() * 1000000)
        write(f'tmp_Mview_{id}.xyz', atoms)
        connectivity = vmd_connectivity(f'tmp_Mview_{id}.xyz')
        os.remove(f'tmp_Mview_{id}.xyz')

    elif engine == 'ase':
        from ase.neighborlist import natural_cutoffs, NeighborList

        cutoffs = natural_cutoffs(atoms)
        nl = NeighborList(cutoffs, self_interaction=False, bothways=True)
        nl.update(atoms)
        connectivity = [nl.get_neighbors(i)[0] for i in range(len(atoms))]

    return connectivity


def ase_to_nx_graph(atoms, engine='vmd'):
    """
    Converts a molecule into a networkx graph whose nodes are the atoms, with
    their atomic number in the attribute 'atomic_number', and whose edges are
    the bonds.

    Parameters
    ==========
    atoms: ase.Atoms
        molecule to be converted.
    engine: str. Default='vmd'
        engine used to get the connectivity, 'vmd' or 'ase'. See
        get_connectivity.

    Return
    ======
    (networkx.Graph) graph of the molecule.
    """
    connectivity  = get_connectivity(atoms, engine)

    G = nx.Graph()
    for i, atom in enumerate(atoms):
        G.add_node(i, atomic_number=atom.number)

    for i in range(len(atoms)):
        indices = connectivity[i]
        for j in indices:
            if not G.has_edge(i, j):
                G.add_edge(i, j)

    return G

def get_isomorphic_permutation(nx_graph1, nx_graph2):
    """
    Returns a permutation list to reorder the atoms of `nx_graph2` to match
    `nx_graph1` based on their isomorphic structure (nodes are matched by
    their 'atomic_number'), such that e.g.:

    permutation = get_isomorphic_permutation(g1, g2)
    numbers2[permutation] == numbers1

    Parameters
    ==========
    nx_graph1: networkx.Graph
        first molecular graph (see ase_to_nx_graph).
    nx_graph2: networkx.Graph
        second molecular graph (see ase_to_nx_graph).

    Return
    ======
    (list) permutation such that the node i of nx_graph1 corresponds to the
    node permutation[i] of nx_graph2. Raises ValueError if the graphs are not
    isomorphic.
    """

    def node_match(n1, n2):
        """
        True if both nodes have the same atomic number.
        """
        return n1['atomic_number'] == n2['atomic_number']

    gm = nx.isomorphism.GraphMatcher(nx_graph1, nx_graph2, node_match=node_match)

    if gm.is_isomorphic():
        mapping = gm.mapping
        permutation = [mapping[i] for i in range(len(nx_graph1))]
        return permutation
    else:
        raise ValueError("Graphs are not isomorphic")

def get_permutation_of_heavy_atoms(heavy_ref_mol, heavy_mch_mol, engine='vmd'):
    """
    Finds the permutation that maps the heavy atoms of the reference molecule
    onto the heavy atoms of the molecule to match, using the isomorphism of
    their molecular graphs.

    Parameters
    ==========
    heavy_ref_mol: ase.Atoms
        reference molecule (only heavy atoms).
    heavy_mch_mol: ase.Atoms
        molecule to match (only heavy atoms).
    engine: str. Default='vmd'
        engine used to get the connectivity, 'vmd' or 'ase'. See
        get_connectivity.

    Return
    ======
    (list) permutation such that the atom i of heavy_ref_mol corresponds to
    the atom permutation[i] of heavy_mch_mol. Raises ValueError if the
    molecular graphs are not isomorphic.
    """
    graph_ref = ase_to_nx_graph(heavy_ref_mol, engine=engine)
    graph_2ma = ase_to_nx_graph(heavy_mch_mol, engine=engine)
    perm = get_isomorphic_permutation(graph_ref, graph_2ma)

    return perm

# add2executable
def rad_loc(ref_mol_xyz: str, rad_mol_xyz: str, engine='vmd') -> int:
    """
    Find the index of the atom where a hydrogen atom was attached. The heavy
    atoms of both molecules are matched by graph isomorphism and the first
    heavy atom with a different number of bonds is returned.

    Parameters
    ==========
    ref_mol_xyz: str
        path to the file describing the molecule with the hydrogen included.
    rad_mol_xyz: str
        path to the file describing the molecule without the hydrogen.
    engine: str. Default='vmd'
        engine to use to get the connectivity. It can be 'vmd' or 'ase'.

    Return
    ======
    (int) index, in rad_mol_xyz, of the atom where the hydrogen was attached.
    Index counting starting from 1. None if no atom lost a bond.
    """

    ref_mol = read(ref_mol_xyz)
    con_ref = get_connectivity(ref_mol, engine)
    elements = np.array(ref_mol.get_chemical_symbols()).copy()
    non_H_ref = np.where(elements != 'H')[0]
    heavy_ref_mol = ref_mol[elements != 'H']

    mch_mol = read(rad_mol_xyz)
    con_mch = get_connectivity(mch_mol, engine)
    elements = np.array(mch_mol.get_chemical_symbols()).copy()
    non_H_mch = np.where(elements != 'H')[0]
    heavy_mch_mol = mch_mol[elements != 'H']

    perm = get_permutation_of_heavy_atoms(heavy_ref_mol,
                                          heavy_mch_mol,
                                          engine=engine)

    for i, j in zip(non_H_ref, non_H_mch[perm]):
        if len(con_ref[i]) != len(con_mch[j]):
            return j + 1


# add2executable
def heavya_idx_from_ref(ref_mol_xyz: str, rad_mol_xyz: str,
                        index: int, engine: str='vmd') -> np.ndarray:
    """
    Find the index, in the radical, of the heavy atom that corresponds to a
    given heavy atom of the reference molecule. The heavy atoms of both
    molecules are matched by graph isomorphism.

    Parameters
    ==========
    ref_mol_xyz: str
        path to the file describing the molecule with the hydrogen included.
    rad_mol_xyz: str
        path to the file describing the molecule without the hydrogen.
    index: int
        index of the heavy atom in the reference molecule to match in the new
        molecule. Starting from 1.
    engine: str. Default='vmd'
        engine to use to get the connectivity. It can be 'vmd' or 'ase'.

    Return
    ======
    (int) index of the corresponding heavy atom in rad_mol_xyz. Index
    counting starting from 1.
    """

    ref_mol = read(ref_mol_xyz)
    elements = np.array(ref_mol.get_chemical_symbols()).copy()
    non_H_ref = np.where(elements != 'H')[0]
    heavy_ref_mol = ref_mol[elements != 'H']

    mch_mol = read(rad_mol_xyz)
    elements = np.array(mch_mol.get_chemical_symbols()).copy()
    non_H_mch = np.where(elements != 'H')[0]
    heavy_mch_mol = mch_mol[elements != 'H']

    perm = get_permutation_of_heavy_atoms(heavy_ref_mol, heavy_mch_mol,
                                          engine=engine)

    idx_in_reduced_ref = np.where(non_H_ref == int(index) - 1)[0]
    if len(idx_in_reduced_ref) != 1:
        raise ValueError(f"{index} seems not to be a heavy atom or it is not" +
                         " part of the molecule to match.")

    return non_H_mch[perm][idx_in_reduced_ref][0] + 1


def rad_loc_deprecated(ref_mol: str, radical: str) -> np.ndarray:
    """
    Find the index of the atom where a hydrogen atom was attached.

    Parametes
    =========
    ref_mol: str
        path to the file describing the molecule with the hydrogen included.
    radical: str
        path to the file describing the molecule without the hydrogen.

    Return
    ======
    (int) index of the atom where the hydrogen was attached. Index counting
    starting from 1.
    """
    withrad = read(radical)
    ana_rad = Analysis(withrad)
    cone_rad = ana_rad.all_bonds
    reference = read(ref_mol)
    Hs = np.where(np.array(reference.get_chemical_symbols()) == 'H')[0]

    for h in Hs:
        reference = read(ref_mol)
        del reference[h]

        ana = Analysis(reference)
        cone = ana.all_bonds

        if cone == cone_rad:
            reference = read(ref_mol)
            ana = Analysis(reference)
            cone = ana.all_bonds
            return cone[0][h][0] + 1


# add2executable
def ext_xyz_from_npz(npz_file, selection=None, create_xyz_files=True):
    """
    Extracts structures in xyz files from a given npz file.

    Parameters
    ==========
    npz_file: str
        file containing the structures.
    selection: list. Default=None
        list of indexes of the structures to extract. If None, all structures
        are extracted.
    create_xyz_files: bool. Default=True
        whether to create xyz files for the extracted structures or not.

    Return
    ======
    (list) list of ASE Atoms objects corresponding to the extracted structures.
    """
    data = np.load(npz_file)

    if selection is None:
        selection = np.arange(len(data['xyz']))

    a2ret = []
    for i in selection:
        atoms = Atoms(numbers=data['atomic_numbers'][i],
                      positions=data['xyz'][i])
        name = npz_file[:-4] + f'_{i:03}' + '.xyz'

        comment = f'total_charge: {data["total_charge"]}; ' + \
                   f'multiplicity: 2; ' + \
                   f'heavy_atom_missing_idxs: ' + \
                   f'{data["heavy_atom_missing_idxs"][i]}'
        if 'atom_chargerelevant_idx' in data and len(data["atom_chargerelevant_idx"][i]) != 0:
            charged = ', '.join([str(j) for j in
                                 data["atom_chargerelevant_idx"][i]])
            comment += '; atom_chargerelevant_idx: ' + \
                       f'{charged}'
        if 'source_names' in data:
            comment += f'; source_name: {data["source_names"][i]}'
        if create_xyz_files:
            write(name, atoms, comment=comment)
        a2ret.append(atoms)

    data.close()
    return a2ret


# add2executable
def nrand_rad(npz_file, n=None, Nmin=None, entry='energy_MACE',
              exclude=None):
    """
    Extracts a random subset of radical structures from a given npz file. It
    takes the Nmin structures with the lowest values of entry and randomly
    selects n of them.

    Parameters
    ==========
    npz_file: str
        file containing the radicals.
    n: int. Default=None
        number if radical structures to extract from the subset. If None, all
        the structures in the subset are selected.
    Nmin: int. Default=None
        number of structures in the subset that minimizes the entry parameter.
        If None, all the structures are included in the subset.
    entry: str. Default='energy_MACE'
        entry of the npz file from where the Nmin are selected.
    exclude: list. Default=None
        indexes of the structures that cannot be selected, e.g. because they
        were already computed.

    Return
    ======
    (list) indexes of the selected entries in the npz file.
    """
    confs_info = np.load(npz_file)
    if Nmin is None or Nmin > len(confs_info['xyz']):
        Nmin = len(confs_info['xyz'])

    if exclude is None:
        exclude = []
    entry_values = np.delete(confs_info[entry], exclude, axis=0)

    sorted_entries = np.unique(entry_values)[:Nmin]
    if n is None:
        n = len(sorted_entries)

    if len(entry_values) < n:
        raise ValueError("n is too large. There are only" +
                         f" {len(entry_values)} entries available after" +
                         " excluding the specified indices.")

    selected_entries = np.random.choice(sorted_entries, size=n, replace=False)
    selected_idx = []
    for value in selected_entries:
        indexes = np.where(confs_info[entry] == value)[0]
        result = indexes[~np.isin(indexes, exclude)]
        assert len(result) > 0, "No available entries to select from after excluding specified indices."
        index = np.random.choice(result)
        selected_idx.append(int(index))

    return selected_idx

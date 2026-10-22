#!/bin/bash
# Prints the bonds of a molecule detected by VMD: one line per atom with the
# indices (starting from 0) of the atoms bonded to it. VMD must be installed.
# Usage: eproducer extract_bonds_vmd <molecule.pdb or molecule.xyz>

if [ $# -ne 1 ]; then
    echo "Usage: $0 molecule.pdb"
    exit 1
fi

PDB=$1
TMPFILE=$(mktemp)

cat > $TMPFILE << EOF
mol new $PDB

set sel [atomselect top "all"]
foreach {i} [\$sel getbonds] {
    puts  "\$i"
}

quit
EOF

vmd -dispdev text -e $TMPFILE
rm $TMPFILE
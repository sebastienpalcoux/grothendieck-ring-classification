"""Read-only R928 semion, joint-spectrum, and integer-count research replay."""
import verify
import pair_rotation
import joint_spectrum
import integer_counts
import integer_support_lattice
if __name__=='__main__':
    verify.run(False)
    pair_rotation.run(False)
    joint_spectrum.run(False)
    integer_counts.run(False)
    integer_support_lattice.run(False)
    print('PASS complete R928 semion research campaigns; six integer-feasibility branches remain unresolved')

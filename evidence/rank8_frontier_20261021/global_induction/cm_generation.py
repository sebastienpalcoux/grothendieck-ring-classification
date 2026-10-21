"""Isolated full complex S and CM-real STS cone registration and replay."""
import sys
import column_generation as cg

VARIANT='cm_real_sts'

def install():
    if VARIANT in cg.VARIANTS:return
    cg.VARIANTS=(*cg.VARIANTS,VARIANT);original=cg.cone
    def cone(R,height,variant='streaming'):
        if variant!=VARIANT:return original(R,height,variant)
        key=(cg.st.digest(R),height,variant)
        if key not in cg._cones:
            sys.path.insert(0,str(cg.st.HERE.parent/'quadratic'))
            from atomic_cm_real_sts import AtomicCMRealSTS
            cg._cones[key]=AtomicCMRealSTS(R,height)
        return cg._cones[key]
    cg.cone=cone

install()

if __name__=='__main__':
    if '--ring' in sys.argv and '--variant' not in sys.argv:
        sys.argv.extend(['--variant',VARIANT])
    from complete_phase_one import main
    main()

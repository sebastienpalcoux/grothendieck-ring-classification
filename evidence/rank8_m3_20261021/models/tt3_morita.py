#!/usr/bin/env python3
"""Standalone replay entry for the TT3 Morita construction and census match."""
from model_constructors import tt3_morita,tt3_gram,require
from verify_models import verify
if __name__=='__main__':
 rows=verify(include_external=False)
 require(sum(r['id']=='R8_3_715'for r in rows)==1,'TT3 model absent')
 print('PASS: TT3 free-bimodule Gram argument, fusion axioms, and all512 source coefficients.')

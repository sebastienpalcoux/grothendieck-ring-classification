# Titsworth–Hagge package crosswalk

The authors' package contains 34 fusion-ring datasets. Exactly one has rank eleven: `fourStatePotts`, with eight category records sharing the same fusion rules. Its positive integral dimension character is (1,1,1,1,2,2,2,2,2,2,2), of global dimension 32. The tensor is commutative.

Reading all 1,331 literal coefficients as data, without executing the downloaded Mathematica code, gives the exact identification **R11_1_30**. The package-to-census basis map, in zero-based labels, is

`[0, 1, 2, 7, 9, 8, 4, 3, 10, 5, 6]`.

Every coefficient and every fusion-ring axiom was checked. The rank-eleven data do not match R11_1_104 or R11_1_153 and add no previously unmodeled ring. The existing independent SO(8)_2 construction already realizes R11_1_30. This audit does not reverify the third-party F-symbol pentagons or infer eight distinct equivalence classes merely from the eight record names.

The authors' public page is https://mktitsworth.com/fusion-categories/ . Its package link `https://bit.ly/fusionCategories` resolves to `https://www.dropbox.com/s/gjvj5id2tmyo2ey/FusionCategories.tar.gz?dl=0`. The page identifies Matthew Titsworth and Tobias Hagge as the authors and states copyright 2015 and CC BY-NC-SA 3.0 IGO: https://creativecommons.org/licenses/by-nc-sa/3.0/igo/ .

The archive and extracted third-party files remain local research inputs, outside the release dependency manifest. `titsworth_hagge_source.json` records their origin and archive hash; `titsworth_hagge_crosswalk.json` records the complete ring inventory and identification. The independent parser is `crosswalk_titsworth_hagge.py`, and its replay passed under optimized Python. The archive SHA-256 is `1e604a1d52d88ed850a3515232287f3f0d952b1189cbe9a23ae948a41e4be846`.

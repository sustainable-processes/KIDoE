stephen_reaction_templates = {
    ('N-alkylation', ): {
        'Aliphatic Amines and Anilines': {
            'Reagent': [
                '[N;+0;H1,H2;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O)]',
                '[CX4;!$(C([#6])([#6])[#6])]-[Cl,Br,I,$(O-S(=O)(=O)[#6])]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[N;H2;+0;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]>>[N;H1;-1:1]',
                        '[N;H1;+0;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]>>[N;H0;-1:1]',
                    ],
                    'Description':
                    'Deprotonation of the amine nitrogen',
                },
                1: {
                    'Templates': [
                        '[N;-1:1].[CX4;!$(C([#6])([#6])[#6]):2]-[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]>>[N;+0:1]-[C:2].[*-:3]',
                    ],
                    'Description':
                    'SN2 attack of the amide anion on the alkyl carbon, displacing the halide/sulfonate leaving group',
                },
            },
        },
        'Aromatic N-H Heterocycles': {
            'Reagent': [
                '[nH;+0]',
                '[CX4;!$(C([#6])([#6])[#6])]-[Cl,Br,I,$(O-S(=O)(=O)[#6])]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[nH;+0:1]>>[nH0;-1:1]',
                    ],
                    'Description': 'Deprotonation of heteroaromatic N-H nitrogen',
                },
                1: {
                    'Templates': [
                        '[nH0;-1:1].[CX4;!$(C([#6])([#6])[#6]):2]-[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]>>[n;H0;+0:1]-[C:2].[*-:3]',
                    ],
                    'Description':
                    'SN2 attack of the heteroaromatic amide anion on the alkyl carbon, displacing the halide/sulfonate leaving group',
                },
            },
        },
    },
    ('O-alkylation', ): {
        'Aliphatic Alcohols and Phenols': {
            'Reagent': [
                '[OX2H1;$(O-[#6]);!$(O-[C,S]=O)]',
                '[CX4;!$(C([#6])([#6])[#6])]-[Cl,Br,I,$(O-S(=O)(=O)[#6])]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[OX2H1;$(O-[#6]);!$(O-[C,S]=O):1]>>[O;H0;-1:1]',
                    ],
                    'Description': 'Deprotonation of the alcohol/phenol oxygen',
                },
                1: {
                    'Templates': [
                        '[O;-1:1].[CX4;!$(C([#6])([#6])[#6]):2]-[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]>>[O;+0:1]-[C:2].[*-:3]',
                    ],
                    'Description':
                    'SN2 attack of the alkoxide/phenolate on the alkyl carbon, displacing the halide/sulfonate leaving group',
                },
            },
        },
        'Phenol Difluoromethylation with Imine': {
            'Reagent': ['[c]O', '[*]=[N][*]', 'P(=O)C(F)(F)Br'],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        'P(=O)([*:1])([*:2])[C:3](F)(F)Br.[*:4]=[N][*:5]>>P(=O)([*:1])([*:2])([N+](=[*:4])[*:5]).[C;-1:3](F)(F)Br',
                    ],
                    'pKa': [None],
                    'Description':
                    'Phosphonate activation',
                },
                1: {
                    'Templates': [
                        '[C;-1:1](F)(F)[Br:2]>>[C;v2;+0;H0:1](F)(F).[Br-:2]',
                    ],
                    'pKa': [None],
                    'Description': 'Difluorocarbene formation',
                },
                2: {
                    'Templates': [
                        '[c:1][O;+0;H1].[*:2]=[N;+0;H0][*:3]>>[c:1][O;-1;H0].[*:2]=[N;+1;H1][*:3]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Phenol deprotonation',
                },
                3: {
                    'Templates': [
                        '[c:1][O;-1:2].[C;v2;+0;H0:3](F)(F)>>[c:1][O;+0:2][C;-1:3](F)F',
                    ],
                    'pKa': [None],
                    'Description':
                    'Carbene capture',
                },
                4: {
                    'Templates': [
                        '[c:1]O[C;-1](F)F.[*:2]=[N;+1;H1][*:3]>>[c:1]OC(F)F.[*:2]=[N;+0;H0][*:3]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Protonation',
                },
            },
        },
    },
    ('S-alkylation', ): {
        'Thiols and Thiophenols': {
            'Reagent': [
                '[SX2H1;$(S-[#6]);!$(S-[C,S]=O)]',
                '[CX4;!$(C([#6])([#6])[#6])]-[Cl,Br,I,$(O-S(=O)(=O)[#6])]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[SX2H1;$(S-[#6]);!$(S-[C,S]=O):1]>>[S;H0;-1:1]',
                    ],
                    'Description': 'Deprotonation of the thiol/thiophenol sulfur',
                },
                1: {
                    'Templates': [
                        '[S;-1:1].[CX4;!$(C([#6])([#6])[#6]):2]-[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]>>[S;+0:1]-[C:2].[*-:3]',
                    ],
                    'Description':
                    'SN2 attack of the thiolate/thiophenolate on the alkyl carbon, displacing the halide/sulfonate leaving group',
                },
            },
        }
    },
    ('Reductive Amination', ): {
        'Reaction': {
            'Reagent': [
                '[N;+0;H1,H2,H3;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O);!$(N-[O,N])]',
                '[CX3;$([CH1]=O),$([CH0]([#6])([#6])=O);!$(C-[O,N,S,F,Cl,Br,I])]=[OX1]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[N;+0;H1,H2,H3;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O);!$(N-[O,N]):1].[CX3;$([CH1]=O),$([CH0]([#6])([#6])=O);!$(C-[O,N,S,F,Cl,Br,I]):2]=[OX1:3]>>[N+:1]-[C:2]-[O-:3]',
                    ],
                    'Description':
                    'Nucleophilic addition of the amine to the carbonyl carbon, forming a zwitterionic tetrahedral ammonium alkoxide intermediate',
                },
                1: {
                    'Templates': [
                        '[N+:1](-[H:5])-[C:2]-[O-:3]>>[N+0:1]-[C:2]-[O+0:3]-[H:5]',
                    ],
                    'Description':
                    'Proton transfer from the ammonium nitrogen to the alkoxide oxygen, giving the neutral hemiaminal (carbinolamine)',
                },
                2: {
                    'Templates': [
                        '[N;+0:1]-[C:2]-[OX2H1]>>[N+:1]=[C:2]',
                    ],
                    'Description':
                    'Loss of hydroxide from the hemiaminal, forming the iminium cation',
                },
                3: {
                    'Templates': [
                        '[N+:1]=[C:2]>>[N+0:1]-[C:2]',
                    ],
                    'Description':
                    'Reduction of the iminium cation (hydride addition) to give the final amine',
                },
            },
        },
    },
    ('N-arylation', ): {
        'Aliphatic Amines and Anilines': {
            'Reagent': [
                '[N;+0;H1,H2;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O)]',
                '[c]-[Cl,Br,I,$(O-S(=O)(=O)[#6])]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[N;H2;+0;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]>>[N;H1;-1:1]',
                        '[N;H1;+0;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]>>[N;H0;-1:1]',
                    ],
                    'Description':
                    'Deprotonation of the amine nitrogen',
                },
                1: {
                    'Templates': [
                        '[N;-1:1].[c:2]-[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]>>[N;+0:1]-[c:2].[*-:3]',
                    ],
                    'Description':
                    'SNAr attack of the amide anion on the aromatic carbon, displacing the halide/sulfonate leaving group',
                },
            },
        },
        'Aromatic N-H Heterocycles': {
            'Reagent': [
                '[nH;+0]',
                '[c]-[Cl,Br,I,$(O-S(=O)(=O)[#6])]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[nH;+0:1]>>[nH0;-1:1]',
                    ],
                    'Description': 'Deprotonation of heteroaromatic N-H nitrogen',
                },
                1: {
                    'Templates': [
                        '[nH0;-1:1].[c:2]-[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]>>[n;H0;+0:1]-[c:2].[*-:3]',
                    ],
                    'Description':
                    'SNAr attack of the heteroaromatic amide anion on the aromatic carbon, displacing the halide/sulfonate leaving group',
                },
            },
        },
    },
    ('O-arylation'): {
        'Aliphatic Alcohols': {
            'Reagent': [
                '[OX2H1;+0;!$(O-a);!$(O-C=[O,S,N])]',
                '[c]-[Cl,Br,I,$(O-S(=O)(=O)[#6])]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[OX2H1;+0;!$(O-a);!$(O-C=[O,S,N]):1]>>[O;H0;-1:1]',
                    ],
                    'Description': 'Deprotonation of the aliphatic alcohol oxygen',
                },
                1: {
                    'Templates': [
                        '[O;-1:1].[c:2]-[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]>>[O;+0:1]-[c:2].[*-:3]',
                    ],
                    'Description':
                    'SNAr attack of the alkoxide on the aromatic carbon, displacing the halide/sulfonate leaving group',
                },
            },
        }
    },
    ('S-arylation'): {
        'Aliphatic Sulfides': {
            'Reagent': [
                '[SX2H1;+0;!$(S-a);!$(S-C=[O,S,N])]',
                '[c]-[Cl,Br,I,$(O-S(=O)(=O)[#6])]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[SX2H1;+0;!$(S-a);!$(S-C=[O,S,N]):1]>>[S;H0;-1:1]',
                    ],
                    'Description': 'Deprotonation of the aliphatic sulfide sulfur',
                },
                1: {
                    'Templates': [
                        '[S;-1:1].[c:2]-[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]>>[S;+0:1]-[c:2].[*-:3]',
                    ],
                    'Description':
                    'SNAr attack of the thiolate on the aromatic carbon, displacing the halide/sulfonate leaving group',
                },
            },
        }
    },
    ('N-acylation', ): {
        'Aliphatic Amines and Anilines': {
            'Reagent': [
                '[N;+0;H1,H2,H3;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O)]',
                '[CX3](=[OX1])[Cl]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[N;+0;H3;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]>>[N;H2;-1:1]',
                        '[N;+0;H2;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]>>[N;H1;-1:1]',
                        '[N;+0;H1;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]>>[N;H0;-1:1]',
                    ],
                    'Description':
                    'Deprotonation of the amine nitrogen, giving the nucleophilic amide anion',
                },
                1: {
                    'Templates': [
                        '[N;-1:1].[CX3:2](=[OX1:3])[Cl;H0;+0:4]>>[N;+0:1]-[C;H0;+0:2](-[O;H0;-1:3])[Cl;H0;+0:4]',
                    ],
                    'Description':
                    'Nucleophilic addition of the amide anion to the acyl chloride carbonyl carbon, forming a tetrahedral intermediate',
                },
                2: {
                    'Templates': [
                        '[N;+0:1]-[C;H0;+0:2](-[O;H0;-1:3])[Cl;H0;+0:4]>>[N;+0:1]-[C;H0;+0:2](=[O;H0;+0:3]).[Cl;H0;-1:4]',
                    ],
                    'Description':
                    'Collapse of the tetrahedral intermediate, expelling chloride and reforming the carbonyl to give the neutral amide',
                },
            },
        },
        'Aromatic N-H Heterocycles': {
            'Reagent': [
                '[nH;+0]',
                '[CX3](=[OX1])[Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[nH;+0:1]>>[n;H0;-1:1]',
                    ],
                    'Description':
                    'Deprotonation of the heteroaromatic N-H nitrogen, giving the nucleophilic amide anion',
                },
                1: {
                    'Templates': [
                        '[n;-1:1].[CX3:2](=[OX1:3])[Cl;H0;+0:4]>>[n;+0:1]-[C;H0;+0:2](-[O;H0;-1:3])[Cl;H0;+0:4]',
                    ],
                    'Description':
                    'Nucleophilic addition of the heteroaromatic amide anion to the acyl chloride carbonyl carbon, forming a tetrahedral intermediate',
                },
                2: {
                    'Templates': [
                        '[n;+0:1]-[C;H0;+0:2](-[O;H0;-1:3])[Cl;H0;+0:4]>>[n;+0:1]-[C;H0;+0:2](=[O;H0;+0:3]).[Cl;H0;-1:4]',
                    ],
                    'Description':
                    'Collapse of the tetrahedral intermediate, expelling chloride and reforming the carbonyl to give the neutral N-acyl heterocycle',
                },
            },
        },
    },
    ('O-acylation', ): {
        'Alcohols and Phenols to Ester': {
            'Reagent': [
                '[OX2H1;$(O-[#6]);!$(O-[C,S]=O)]',
                '[CX3](=[OX1])[Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[OX2H1;$(O-[#6]);!$(O-[C,S]=O):1]>>[O;H0;-1:1]',
                    ],
                    'Description':
                    'Deprotonation of the alcohol/phenol oxygen, giving the nucleophilic alkoxide/phenolate',
                },
                1: {
                    'Templates': [
                        '[O;-1:1].[CX3:2](=[OX1:3])[Cl;H0;+0:4]>>[O;+0:1]-[C;H0;+0:2](-[O;H0;-1:3])[Cl;H0;+0:4]',
                    ],
                    'Description':
                    'Nucleophilic addition of the alkoxide/phenolate to the acyl chloride carbonyl carbon, forming a tetrahedral intermediate',
                },
                2: {
                    'Templates': [
                        '[O;+0:1]-[C;H0;+0:2](-[O;H0;-1:3])[Cl;H0;+0:4]>>[O;+0:1]-[C;H0;+0:2](=[O;H0;+0:3]).[Cl;H0;-1:4]',
                    ],
                    'Description':
                    'Collapse of the tetrahedral intermediate, expelling chloride and reforming the carbonyl to give the neutral ester',
                },
            },
        },
    },
    ('Amidination', ): {
        'Aliphatic Amines and Anilines': {
            'Reagent': [
                '[N;+0;H1,H2,H3;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O)]',
                '[CX3](=[N])[Cl]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[N;+0;H3;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]>>[N;H2;-1:1]',
                        '[N;+0;H2;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]>>[N;H1;-1:1]',
                        '[N;+0;H1;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]>>[N;H0;-1:1]',
                    ],
                    'Description':
                    'Deprotonation of the amine nitrogen, giving the nucleophilic amide anion',
                },
                1: {
                    'Templates': [
                        '[N;-1:1].[CX3:2](=[N:3])[Cl;H0;+0:4]>>[N;+0:1]-[C;H0;+0:2]([N;-1:3])[Cl;H0;+0:4]',
                    ],
                    'Description':
                    'Nucleophilic addition of the amide anion to the imidoyl chloride carbon, forming a tetrahedral intermediate',
                },
                2: {
                    'Templates': [
                        '[N;+0:1]-[C;H0;+0:2]([N;-1:3])[Cl;H0;+0:4]>>[N;+0:1]-[C;H0;+0:2](=[N;+0:3]).[Cl;H0;-1:4]',
                    ],
                    'Description':
                    'Collapse of the tetrahedral intermediate, expelling chloride and reforming the C=N double bond to give the neutral amidine',
                },
            },
        },
        'Aromatic N-H Heterocycles': {
            'Reagent': [
                '[nH;+0]',
                '[CX3](=[N])[Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[nH;+0:1]>>[n;H0;-1:1]',
                    ],
                    'Description':
                    'Deprotonation of the heteroaromatic N-H nitrogen, giving the nucleophilic amide anion',
                },
                1: {
                    'Templates': [
                        '[n;-1:1].[CX3:2](=[N:3])[Cl;H0;+0:4]>>[n;+0:1]-[C;H0;+0:2]([N;-1:3])[Cl;H0;+0:4]',
                    ],
                    'Description':
                    'Nucleophilic addition of the heteroaromatic amide anion to the imidoyl chloride carbon, forming a tetrahedral intermediate',
                },
                2: {
                    'Templates': [
                        '[n;+0:1]-[C;H0;+0:2]([N;-1:3])[Cl;H0;+0:4]>>[n;+0:1]-[C;H0;+0:2](=[N;+0:3]).[Cl;H0;-1:4]',
                    ],
                    'Description':
                    'Collapse of the tetrahedral intermediate, expelling chloride and reforming the C=N double bond to give the neutral N-heteroaryl amidine',
                },
            },
        },
    },
    ('N-sulfonylation', ): {
        'Aliphatic Amines and Anilines': {
            'Reagent': [
                '[N;+0;H1,H2,H3;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O)]',
                '[S;+0](=[O])(=[O])[Cl]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[N;+0;H3;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]>>[N;H2;-1:1]',
                        '[N;+0;H2;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]>>[N;H1;-1:1]',
                        '[N;+0;H1;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]>>[N;H0;-1:1]',
                    ],
                    'Description':
                    'Deprotonation of the amine nitrogen, giving the nucleophilic amide anion',
                },
                1: {
                    'Templates': [
                        '[N;-1:1].[S;+0:2](=[O:3])(=[O:4])[Cl;H0;+0:5]>>[N;+0:1]-[S;+0:2](=[O:3])(=[O:4]).[Cl;H0;-1:5]',
                    ],
                    'Description':
                    'SN2 attack of the amide anion on the sulfonyl sulfur, displacing the chloride leaving group',
                },
            },
        },
        'Aromatic N-H Heterocycles': {
            'Reagent': [
                '[nH;+0]',
                '[S;+0](=[O])(=[O])[Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[nH;+0:1]>>[n;H0;-1:1]',
                    ],
                    'Description':
                    'Deprotonation of the heteroaromatic N-H nitrogen, giving the nucleophilic amide anion',
                },
                1: {
                    'Templates': [
                        '[n;-1:1].[S;+0:2](=[O:3])(=[O:4])[Cl;H0;+0:5]>>[n;+0:1]-[S;+0:2](=[O:3])(=[O:4]).[Cl;H0;-1:5]',
                    ],
                    'Description':
                    'SN2 attack of the heteroaromatic amide anion on the sulfonyl sulfur, displacing the chloride leaving group',
                },
            },
        },
    },
    ('Suzuki coupling', ): {
        'Reaction': {
            'Reagent':
            ['[B]-[c,C;+0]', '[Cl,Br,I,O$([O]-S)]-[c,C;+0]', '[Pd;D0;+0]', '[OH1;-1]'],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[Cl,Br,I,O$([O]-S):7]-[c,C;+0:5].[Pd;D0;+0:6]>>[Cl,Br,I,O$([O]-S):7]-[Pd:6]-[c,C;+0:5]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Oxidative addition',
                },
                1: {
                    'Templates': [
                        '[OH1;-1:8].[Cl,Br,I,O$([O]-S):7]-[Pd:6]-[c,C;+0:5]>>[Cl,Br,I,O$([O]-S);-1:7].[OH1;+0:8]-[Pd:6]-[c,C;+0:5]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Halide leaving',
                },
                2: {
                    'Templates': [
                        '[B:2]-[c,C;+0:4].[OH1;-1:1]>>[c,C;+0:4]-[B;-1:2]-[OH1;+0:1]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Borate formation',
                },
                3: {
                    'Templates': [
                        '[B;-1:2]-[c,C;+0:4].[OH1;+0:8]-[Pd:6]-[c,C;+0:5]>>[c,C;+0:4]-[Pd:6]-[c,C;+0:5].[B;+0:2].[OH1;-1:8]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Transmetalation, releasing neutral boric acid and hydroxide',
                },
                4: {
                    'Templates': [
                        '[c,C;+0:4]-[Pd:6]-[c,C;+0:5]>>[c,C;+0:4]-[c,C;+0:5].[Pd:6]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Reductive elimination',
                },
            },
        },
    },
    ('Buchwald-Hartwig amination', ): {
        'Reaction': {
            'Reagent': [
                '[Cl,Br,I,$(O-S(=O)(=O)[#6])]-[c,C;+0]',
                '[N;+0;H1,H2;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O)]',
                '[Pd;D0;+0]',
                '[OH1;-1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]-[c,C;+0:5].[Pd;D0;+0:6]>>[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]-[Pd:6]-[c,C;+0:5]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Oxidative addition of the aryl/vinyl halide (or pseudohalide) to Pd(0), forming an aryl/vinyl-Pd(II)-halide complex',
                },
                1: {
                    'Templates': [
                        '[OH1;-1:8].[N;+0;H1;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]([H:7])>>[O;+0:8]([H:7]).[N;H0;-1:1]',
                        '[OH1;-1:8].[N;+0;H2;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]([H:7])>>[O;+0:8]([H:7]).[N;-1:1]',
                    ],
                    'pKa': [None, None],
                    'Description':
                    'Deprotonation of the amine by base, giving the nucleophilic amide anion',
                },
                2: {
                    'Templates': [
                        '[N;-1:1].[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]-[Pd:6]-[c,C;+0:5]>>[N;+0:1]-[Pd:6]-[c,C;+0:5].[Cl,Br,I,$(O-S(=O)(=O)[#6]);-1:3]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Ligand exchange: the amide anion displaces the halide on the aryl/vinyl-Pd(II) complex, giving an amido-Pd(II) intermediate',
                },
                3: {
                    'Templates': [
                        '[N;+0:1]-[Pd:6]-[c,C;+0:5]>>[N:1]-[c,C;+0:5].[Pd;D0;+0:6]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Reductive elimination, forming the new aryl/vinyl-amine C-N bond (the Buchwald-Hartwig coupling product) and regenerating Pd(0)',
                },
            },
        },
    },
    ('Heck reaction', ): {
        'Reaction': {
            'Reagent': [
                '[Cl,Br,I,$(O-S(=O)(=O)[#6])]-[c,C;+0]',
                '[CX3;H1,H2]=[CX3]',
                '[Pd;D0;+0]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]-[c,C;+0:5].[Pd;D0;+0:6]>>[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]-[Pd:6]-[c,C;+0:5]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Oxidative addition of the aryl/vinyl halide (or pseudohalide) to Pd(0), forming an aryl/vinyl-Pd(II)-halide complex',
                },
                1: {
                    'Templates': [
                        '[c,C;+0:5]-[Pd:6]-[Cl,Br,I,$(O-S(=O)(=O)[#6]):3].[CX3;H1,H2:1]=[CX3;H0,H1,H2:2]>>[c,C;+0:5]-[C:1]-[C:2]-[Pd:6]-[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Coordination of the alkene to Pd(II) followed by syn-carbopalladation (migratory insertion) across the double bond, placing the aryl/vinyl group on one alkene carbon and Pd on the adjacent carbon',
                },
                2: {
                    'Templates': [
                        '[C;H1,H2:1]([H:7])-[C:2]-[Pd:6]-[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]>>[C:1]=[C:2].[Pd;D0;+0:6].[H:7][Cl,Br,I,$(O-S(=O)(=O)[#6]):3]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Syn β-hydride elimination from the carbon adjacent to Pd, followed by reductive elimination of the hydrogen halide, forming the new C=C double bond (the Heck product) and regenerating Pd(0)',
                },
            },
        },
    },
    ('Sonogashira reaction', ): {
        'Reaction': {
            'Reagent': [
                '[Cl,Br,I,$(O-S(=O)(=O)[#6])]-[c,C;+0]',
                '[CX2;H1]#[CX2]',
                '[Pd;D0;+0]',
                '[Cu;+1;D0]',
                '[OH1;-1]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]-[c,C;+0:5].[Pd;D0;+0:6]>>[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]-[Pd:6]-[c,C;+0:5]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Oxidative addition of the aryl/vinyl halide (or pseudohalide) to Pd(0), forming an aryl/vinyl-Pd(II)-halide complex',
                },
                1: {
                    'Templates': [
                        '[OH1;-1:8].[CX2;H1:1]([H:7])#[CX2:2]>>[O;+0:8]([H:7]).[C;H0;-1:1]#[CX2:2]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Deprotonation of the terminal alkyne by base, giving the acetylide anion',
                },
                2: {
                    'Templates': [
                        '[Cu;+1;D0:9].[C;H0;-1:1]#[CX2:2]>>[Cu;+0:9]-[C;+0:1]#[CX2:2]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Transmetalation of the acetylide onto Cu(I), forming the copper acetylide',
                },
                3: {
                    'Templates': [
                        '[c,C;+0:5]-[Pd:6]-[Cl,Br,I,$(O-S(=O)(=O)[#6]):3].[Cu;+0:9]-[C;+0:1]#[CX2:2]>>[c,C;+0:5]-[Pd:6]-[C;+0:1]#[CX2:2].[Cu;+0:9]-[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Transmetalation: the copper acetylide transfers its alkynyl group to the aryl/vinyl-Pd(II) complex, displacing the halide onto copper',
                },
                4: {
                    'Templates': [
                        '[c,C;+0:5]-[Pd:6]-[C;+0:1]#[CX2:2]>>[c,C;+0:5]-[C:1]#[CX2:2].[Pd;D0;+0:6]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Reductive elimination, forming the new aryl/vinyl-alkynyl C-C bond (the Sonogashira coupling product) and regenerating Pd(0)',
                },
            },
        },
    },
    ('Claisen condensation', ): {
        'Reaction': {
            'Reagent': [
                '[CX4;H1,H2,H3]-[CX3](=[OX1])[OX2][#6]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CX4;H3;+0:1]-[CX3:2](=[OX1:3])[OX2:4][#6:5]>>[C;H2;-1:1]-[CX3:2](=[OX1:3])[OX2:4][#6:5]',
                        '[CX4;H2;+0:1]-[CX3:2](=[OX1:3])[OX2:4][#6:5]>>[C;H1;-1:1]-[CX3:2](=[OX1:3])[OX2:4][#6:5]',
                        '[CX4;H1;+0:1]-[CX3:2](=[OX1:3])[OX2:4][#6:5]>>[C;H0;-1:1]-[CX3:2](=[OX1:3])[OX2:4][#6:5]',
                    ],
                    'Description':
                    'Deprotonation of the alpha-carbon by base, giving the resonance-stabilized ester enolate (carbanion)',
                },
                1: {
                    'Templates': [
                        '[CX3;-1;$([CX3]-[CX3]=[OX1]):1].[CX3:6](=[OX1:7])[OX2:8][#6:9]>>[C;+0:1]-[C;H0;+0:6](-[O;-1:7])[OX2:8][#6:9]',
                    ],
                    'Description':
                    'Nucleophilic addition of the ester enolate to the carbonyl carbon of a second ester molecule, forming a tetrahedral alkoxide intermediate',
                },
                2: {
                    'Templates': [
                        '[C;+0:1]-[C;H0;+0:6](-[O;-1:7])[OX2:8][#6:9]>>[C;+0:1]-[C;H0;+0:6](=[O;+0:7]).[O;-1:8][#6:9]',
                    ],
                    'Description':
                    'Collapse of the tetrahedral intermediate, expelling the alkoxide leaving group and reforming the carbonyl to give the neutral beta-ketoester',
                },
            },
        },
    },
    ('Grignard addition', ): {
        'Aldehydes and Ketones': {
            'Reagent': [
                '[#6]-[Mg]-[Cl,Br,I]',
                '[CX3;H0,H1;!$([CX3](=[OX1])[OX2,NX3,NX2,SX2,F,Cl,Br,I])](=[OX1])[#6]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[#6:1]-[Mg:2]-[Cl,Br,I:3].[CX3;H0,H1;!$([CX3](=[OX1])[OX2,NX3,NX2,SX2,F,Cl,Br,I]):4](=[OX1:5])[#6:6]>>[#6:1]-[C;+0:4](-[O;+0:5]-[Mg:2]-[Cl,Br,I:3])[#6:6]',
                    ],
                    'Description':
                    'Nucleophilic addition of the Grignard carbanion to the aldehyde/ketone carbonyl carbon, forming a magnesium alkoxide intermediate',
                },
                1: {
                    'Templates': [
                        '[C:4]-[O;+0:5]-[Mg:2]-[Cl,Br,I:3].[OX2;H2:10]([H:11])>>[C:4]-[O;+0:5][H:11].[Mg:2](-[Cl,Br,I:3])-[O;+0:10]',
                    ],
                    'Description':
                    'Aqueous workup: water protonates the magnesium alkoxide, giving the neutral alcohol and a magnesium hydroxo-halide byproduct',
                },
            },
        },
        'Esters': {
            'Reagent': [
                '[#6]-[Mg]-[Cl,Br,I]',
                '[CX3](=[OX1])[OX2][#6]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[#6:1]-[Mg:2]-[Cl,Br,I:3].[CX3:4](=[OX1:5])[OX2:6][#6:7]>>[#6:1]-[C;+0:4](-[O;+0:5]-[Mg:2]-[Cl,Br,I:3])[OX2:6][#6:7]',
                    ],
                    'Description':
                    'First nucleophilic addition of the Grignard carbanion to the ester carbonyl carbon, forming a tetrahedral magnesium alkoxide intermediate',
                },
                1: {
                    'Templates': [
                        '[#6:1]-[C;+0:4](-[O;+0:5]-[Mg:2]-[Cl,Br,I:3])[OX2:6][#6:7]>>[#6:1]-[C;+0:4](=[O;+0:5]).[Mg:2](-[Cl,Br,I:3])-[O;+0:6][#6:7]',
                    ],
                    'Description':
                    'Collapse of the tetrahedral intermediate, expelling the alkoxy leaving group and reforming the carbonyl to give a ketone in situ',
                },
                2: {
                    'Templates': [
                        '[#6:11]-[Mg:12]-[Cl,Br,I:13].[CX3;H0;!$([CX3](=[OX1])[OX2,NX3,NX2,SX2,F,Cl,Br,I]):4](=[OX1:5])[#6:1]>>[#6:11]-[C;+0:4](-[O;+0:5]-[Mg:12]-[Cl,Br,I:13])[#6:1]',
                    ],
                    'Description':
                    'Second nucleophilic addition of the Grignard carbanion to the in-situ ketone, forming a second magnesium alkoxide intermediate',
                },
                3: {
                    'Templates': [
                        '[C;H0;!$([#6]-[OX2;!$([OX2][Mg])]):4]-[O;+0:5]-[Mg:12]-[Cl,Br,I:13].[OX2;H2:10]([H:14])>>[C:4]-[O;+0:5][H:14].[Mg:12](-[Cl,Br,I:13])-[O;+0:10]',
                    ],
                    'Description':
                    'Aqueous workup: water protonates the magnesium alkoxide, giving the neutral tertiary alcohol and a magnesium hydroxo-halide byproduct',
                },
            },
        },
        'Weinreb Amides': {
            'Reagent': [
                '[#6]-[Mg]-[Cl,Br,I]',
                '[CX3](=[OX1])[NX3;$(N-[OX2])]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[#6:1]-[Mg:2]-[Cl,Br,I:3].[CX3:4](=[OX1:5])[NX3;$(N-[OX2]):6]>>[#6:1]-[C;+0:4](-[O;+0:5]-[Mg:2]-[Cl,Br,I:3])[NX3:6]',
                    ],
                    'Description':
                    'Nucleophilic addition of the Grignard carbanion to the Weinreb amide carbonyl carbon, forming a chelated magnesium alkoxide-aminal intermediate that resists further collapse at low temperature',
                },
                1: {
                    'Templates': [
                        '[#6:1]-[C;+0:4](-[O;+0:5]-[Mg:2]-[Cl,Br,I:3])[NX3:6].[OX2;H2:10]([H:11])>>[#6:1]-[C;+0:4](=[O;+0:5]).[Mg:2](-[Cl,Br,I:3])-[O;+0:10].[N:6][H:11]',
                    ],
                    'Description':
                    'Aqueous workup: water collapses the chelated intermediate, expelling the N-methoxy-N-methylamine leaving group and giving the neutral ketone',
                },
            },
        },
        'Nitriles': {
            'Reagent': [
                '[#6]-[Mg]-[Cl,Br,I]',
                '[CX2]#[NX1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[#6:1]-[Mg:2]-[Cl,Br,I:3].[#6:6]-[CX2:4]#[NX1:5]>>[#6:1]-[C;+0:4](=[N;+0:5]-[Mg:2]-[Cl,Br,I:3])[#6:6]',
                    ],
                    'Description':
                    'Nucleophilic addition of the Grignard carbanion to the nitrile carbon, forming a metalated ketimine (magnesium aza-enolate) intermediate',
                },
                1: {
                    'Templates': [
                        '[#6:1]-[C;+0:4](=[N:5]-[Mg:2]-[Cl,Br,I:3])[#6:6].[OX2;H2:10]>>[#6:1]-[C;+0:4](=[O;+0:10])[#6:6].[Mg:2](-[Cl,Br,I:3])-[N;H2;+0:5]',
                    ],
                    'Description':
                    'Aqueous hydrolysis of the metalated ketimine, giving the neutral ketone and releasing the nitrogen as a magnesium amido-halide byproduct',
                },
            },
        },
        'Epoxides': {
            'Reagent': [
                '[#6]-[Mg]-[Cl,Br,I]',
                '[CX4]1[OX2][CX4]1',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[#6:1]-[Mg:2]-[Cl,Br,I:3].[CX4:4]1[OX2:5][CX4:6]1>>[#6:1]-[C:4]-[C:6]-[O;+0:5]-[Mg:2]-[Cl,Br,I:3]',
                    ],
                    'Description':
                    'SN2-like nucleophilic attack of the Grignard carbanion on an epoxide carbon, opening the three-membered ring and forming a magnesium alkoxide intermediate',
                },
                1: {
                    'Templates': [
                        '[C:4]-[O;+0:5]-[Mg:2]-[Cl,Br,I:3].[OX2;H2:10]([H:11])>>[C:4]-[O;+0:5][H:11].[Mg:2](-[Cl,Br,I:3])-[O;+0:10]',
                    ],
                    'Description':
                    'Aqueous workup: water protonates the magnesium alkoxide, giving the neutral ring-opened alcohol and a magnesium hydroxo-halide byproduct',
                },
            },
        },
    },
    ('Organolithium addition', ): {
        'Aldehydes and Ketones': {
            'Reagent': [
                '[#6]-[Li]',
                '[CX3;H0,H1;!$([CX3](=[OX1])[OX2,NX3,NX2,SX2,F,Cl,Br,I])](=[OX1])[#6]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[#6:1]-[Li:2].[CX3;H0,H1;!$([CX3](=[OX1])[OX2,NX3,NX2,SX2,F,Cl,Br,I]):4](=[OX1:5])[#6:6]>>[#6:1]-[C;+0:4](-[O;+0:5]-[Li:2])[#6:6]',
                    ],
                    'Description':
                    'Nucleophilic addition of the organolithium carbanion to the aldehyde/ketone carbonyl carbon, forming a lithium alkoxide intermediate',
                },
                1: {
                    'Templates': [
                        '[C:4]-[O;+0:5]-[Li:2].[OX2;H2:10]([H:11])>>[C:4]-[O;+0:5][H:11].[Li:2]-[O;+0:10]',
                    ],
                    'Description':
                    'Aqueous workup: water protonates the lithium alkoxide, giving the neutral alcohol and lithium hydroxide',
                },
            },
        },
        'Esters': {
            'Reagent': [
                '[#6]-[Li]',
                '[CX3](=[OX1])[OX2][#6]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[#6:1]-[Li:2].[CX3:4](=[OX1:5])[OX2:6][#6:7]>>[#6:1]-[C;+0:4](-[O;+0:5]-[Li:2])[OX2:6][#6:7]',
                    ],
                    'Description':
                    'First nucleophilic addition of the organolithium carbanion to the ester carbonyl carbon, forming a tetrahedral lithium alkoxide intermediate',
                },
                1: {
                    'Templates': [
                        '[#6:1]-[C;+0:4](-[O;+0:5]-[Li:2])[OX2:6][#6:7]>>[#6:1]-[C;+0:4](=[O;+0:5]).[Li:2]-[O;+0:6][#6:7]',
                    ],
                    'Description':
                    'Collapse of the tetrahedral intermediate, expelling the alkoxy leaving group and reforming the carbonyl to give a ketone in situ',
                },
                2: {
                    'Templates': [
                        '[#6:11]-[Li:12].[CX3;H0;!$([CX3](=[OX1])[OX2,NX3,NX2,SX2,F,Cl,Br,I]):4](=[OX1:5])[#6:1]>>[#6:11]-[C;+0:4](-[O;+0:5]-[Li:12])[#6:1]',
                    ],
                    'Description':
                    'Second nucleophilic addition of the organolithium carbanion to the in-situ ketone, forming a second lithium alkoxide intermediate',
                },
                3: {
                    'Templates': [
                        '[C;H0;!$([#6]-[OX2;!$([OX2][Li])]):4]-[O;+0:5]-[Li:12].[OX2;H2:10]([H:14])>>[C:4]-[O;+0:5][H:14].[Li:12]-[O;+0:10]',
                    ],
                    'Description':
                    'Aqueous workup: water protonates the lithium alkoxide, giving the neutral tertiary alcohol and lithium hydroxide',
                },
            },
        },
        'Weinreb Amides': {
            'Reagent': [
                '[#6]-[Li]',
                '[CX3](=[OX1])[NX3;$(N-[OX2])]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[#6:1]-[Li:2].[CX3:4](=[OX1:5])[NX3;$(N-[OX2]):6]>>[#6:1]-[C;+0:4](-[O;+0:5]-[Li:2])[NX3:6]',
                    ],
                    'Description':
                    'Nucleophilic addition of the organolithium carbanion to the Weinreb amide carbonyl carbon, forming a chelated lithium alkoxide-aminal intermediate that resists further collapse at low temperature',
                },
                1: {
                    'Templates': [
                        '[#6:1]-[C;+0:4](-[O;+0:5]-[Li:2])[NX3:6].[OX2;H2:10]([H:11])>>[#6:1]-[C;+0:4](=[O;+0:5]).[Li:2]-[O;+0:10].[N:6][H:11]',
                    ],
                    'Description':
                    'Aqueous workup: water collapses the chelated intermediate, expelling the N-methoxy-N-methylamine leaving group and giving the neutral ketone',
                },
            },
        },
        'Nitriles': {
            'Reagent': [
                '[#6]-[Li]',
                '[CX2]#[NX1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[#6:1]-[Li:2].[#6:6]-[CX2:4]#[NX1:5]>>[#6:1]-[C;+0:4](=[N;+0:5]-[Li:2])[#6:6]',
                    ],
                    'Description':
                    'Nucleophilic addition of the organolithium carbanion to the nitrile carbon, forming a metalated ketimine (lithium aza-enolate) intermediate',
                },
                1: {
                    'Templates': [
                        '[#6:1]-[C;+0:4](=[N:5]-[Li:2])[#6:6].[OX2;H2:10]>>[#6:1]-[C;+0:4](=[O;+0:10])[#6:6].[Li:2]-[N;H2;+0:5]',
                    ],
                    'Description':
                    'Aqueous hydrolysis of the metalated ketimine, giving the neutral ketone and releasing the nitrogen as lithium amide',
                },
            },
        },
        'Epoxides': {
            'Reagent': [
                '[#6]-[Li]',
                '[CX4]1[OX2][CX4]1',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[#6:1]-[Li:2].[CX4:4]1[OX2:5][CX4:6]1>>[#6:1]-[C:4]-[C:6]-[O;+0:5]-[Li:2]',
                    ],
                    'Description':
                    'SN2-like nucleophilic attack of the organolithium carbanion on an epoxide carbon, opening the three-membered ring and forming a lithium alkoxide intermediate',
                },
                1: {
                    'Templates': [
                        '[C:4]-[O;+0:5]-[Li:2].[OX2;H2:10]([H:11])>>[C:4]-[O;+0:5][H:11].[Li:2]-[O;+0:10]',
                    ],
                    'Description':
                    'Aqueous workup: water protonates the lithium alkoxide, giving the neutral ring-opened alcohol and lithium hydroxide',
                },
            },
        },
    },
    ('Halogen-metal exchange', ): {
        'Reaction': {
            'Reagent': [
                '[#6]-[Li]',
                '[Cl,Br,I]-[$([c;+0]),$([C;+0]=[CX3])]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[#6:1]-[Li:2].[Cl,Br,I:3]-[$([c;+0]),$([C;+0]=[CX3]):4]>>[#6:1]-[Cl,Br,I:3].[$([c;+0]),$([C;+0]=[CX3]):4]-[Li:2]',
                    ],
                    'Description':
                    'Halogen-metal exchange: the organolithium carbanion and the aryl/vinyl halide swap lithium and halide, driven by the greater stability of the aryl/vinyl carbanion, giving a new organolithium and a new alkyl halide',
                },
            },
        },
    },
    ('Friedel-Crafts acylation', ): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c][c][c]1',
                '[CX3](=[OX1])[Cl]',
                '[Al;D3;+0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CX3:1](=[OX1:2])[Cl;H0;+0:3].[Al;D3;+0:4]>>[C;+1:1]=[O;+0:2].[Al;-1:4]-[Cl;+0:3]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Lewis acid activation: AlCl3 abstracts the chloride from the acyl chloride, forming the electrophilic acylium cation and tetrachloroaluminate',
                },
                1: {
                    'Templates': [
                        '[C;+1:1]=[O;+0:2].[c;H1:9]2[c:10][c:11][c:12][c:13][c:14]2>>[C;+0:1](=[O;+0:2])[C;H1:9]2[CH1:10]=[CH1:11][CH1:12]=[CH1:13][CH1;+1:14]2',
                    ],
                    'pKa': [None],
                    'Description':
                    'Electrophilic addition of the acylium cation to the ring, forming a Wheland intermediate',
                },
                2: {
                    'Templates': [
                        '[C;+0:1](=[O;+0:2])[CH1:9]2[CH1:10]=[CH1:11][CH1:12]=[CH1:13][CH1;+1:14]2.[Al;-1:4]-[Cl;+0:3]>>[C:1](=[O:2])[c;H0;+0:9]2[c:10][c:11][c:12][c:13][c;H1;+0:14]2.[Al;D3;+0:4].[Cl;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Loss of the ring proton to tetrachloroaluminate, rearomatizing the ring and regenerating AlCl3 and HCl',
                },
            },
        },
    },
    ('Paal-Knorr Synthesis', ): {
        'Pyrrole Synthesis': {
            'Reagent': [
                '[N;+0;H2,H3;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O)]',
                '[CX3;$([#6](=[OX1])[#6])](=[OX1])[CH2][CH2][CX3;$([#6](=[OX1])[#6])](=[OX1])',
                '[OX2H1;$([OX2H1][CX3]=[OX1]),$([OX2H1][SX4](=[OX1])=[OX1])]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[N;+0;H2,H3;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1].[CX3;$([#6](=[OX1])[#6]):2](=[OX1:3])[CH2:4][CH2:5][CX3;$([#6](=[OX1])[#6]):6](=[OX1:7])>>[N+:1]-[C:2](-[O-:3])[CH2:4][CH2:5][CX3:6](=[OX1:7])',
                    ],
                    'Description':
                    'Nucleophilic addition of the amine to one carbonyl carbon of the 1,4-diketone, forming a zwitterionic tetrahedral ammonium alkoxide intermediate',
                },
                1: {
                    'Templates': [
                        '[N+:1](-[H:9])-[C:2](-[O-:3])[C:4][C:5][CX3:6]=[OX1:7]>>[N+0:1]-[C:2](-[O+0:3]-[H:9])[C:4][C:5][CX3:6]=[OX1:7]',
                    ],
                    'Description':
                    'Proton transfer from the ammonium nitrogen to the alkoxide oxygen, giving the neutral hemiaminal',
                },
                2: {
                    'Templates': [
                        '[N;+0:1]-[C:2](-[OX2H1])[CH2:4][CH2:5][CX3:6]=[OX1:7]>>[N+:1]=[C:2][CH2:4][CH2:5][CX3:6]=[OX1:7]',
                    ],
                    'Description':
                    'Loss of water from the hemiaminal, forming the iminium cation',
                },
                3: {
                    'Templates': [
                        '[N+:1]=[C:2][CH2;H2:4][CH2:5][CX3:6]=[OX1:7]>>[N;+0:1]-[C:2]=[CH1:4][CH2:5][CX3:6]=[OX1:7]',
                    ],
                    'Description':
                    'Tautomerization of the iminium to the enamine, giving back a neutral nucleophilic nitrogen',
                },
                4: {
                    'Templates': [
                        '[N;+0:1]-[C:2]=[CH1:4][CH2:5][CX3:6]=[OX1:7]>>[N+:1]1[C:2]=[CH1:4][CH2:5][C:6]1(-[O-:7])',
                    ],
                    'Description':
                    'Intramolecular nucleophilic addition of the enamine nitrogen to the distal carbonyl carbon, closing the five-membered ring and forming a second zwitterionic ammonium alkoxide',
                },
                5: {
                    'Templates': [
                        '[N+:1](-[H:10])1[C:2]=[C:4][C:5][C:6]1(-[O-:7])>>[N;+0:1]1[C:2]=[C:4][C:5][C:6]1(-[O;+0:7]-[H:10])',
                    ],
                    'Description':
                    'Proton transfer from the ring ammonium nitrogen to the alkoxide oxygen, giving the neutral cyclic hemiaminal',
                },
                6: {
                    'Templates': [
                        '[N;H1;+0:1]1[C;H0:2]=[CH1:4][CH2;H2:5][C;H0:6]1(-[OX2H1])>>[n;H1;+0:1]1[c;H0:2][c;H1:4][c;H1:5][c;H0:6]1',
                    ],
                    'Description':
                    'Loss of the second water (from the carbon bearing the hydroxyl and the adjacent ring carbon), aromatizing the ring to give the neutral pyrrole',
                },
            },
        },
        'Furan Synthesis': {
            'Reagent': [
                '[CX3;$([#6](=[OX1])[#6])](=[OX1])[CH2][CH2][CX3;$([#6](=[OX1])[#6])](=[OX1])',
                '[OX2H1;$([OX2H1][CX3]=[OX1]),$([OX2H1][SX4](=[OX1])=[OX1])]',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CX3;$([#6](=[OX1])[#6]):2](=[OX1:3])[CH2:4][CH2;H2:5][CX3;$([#6](=[OX1])[#6]):6](=[OX1:7])>>[CX3:2](=[OX1:3])[CH2:4][CH1:5]=[C:6]-[OX2;H1:7]',
                    ],
                    'Description':
                    'Acid-catalyzed keto-enol tautomerization of one carbonyl, giving a nucleophilic enol oxygen',
                },
                1: {
                    'Templates': [
                        '[CX3:2](=[OX1:3])[CH2:4][CH1:5]=[C:6]-[OX2;H1:7]>>[C:2]1(-[O-:3])[CH2:4][CH1:5]=[C:6]-[O;H1;+1:7]1',
                    ],
                    'Description':
                    'Intramolecular nucleophilic addition of the enol oxygen to the distal carbonyl carbon, closing the five-membered ring and forming a zwitterionic oxonium alkoxide',
                },
                2: {
                    'Templates': [
                        '[O;+1:7](-[H:9])1[C:6]=[C:5][C:4][C:2]1(-[O-:3])>>[O;+0:7]1[C:6]=[C:5][C:4][C:2]1(-[O;+0:3]-[H:9])',
                    ],
                    'Description':
                    'Proton transfer from the ring oxonium oxygen to the alkoxide oxygen, giving the neutral cyclic hemiketal',
                },
                3: {
                    'Templates': [
                        '[O;H0;+0:7]1[C;H0:6]=[CH1:5][CH2;H2:4][C;H0:2]1(-[OX2H1:3])>>[o;+0:7]1[c;H0:6][c;H1:5][c;H1:4][c;H0:2]1',
                    ],
                    'Description':
                    'Loss of the second water (from the carbon bearing the hydroxyl and the adjacent ring carbon), aromatizing the ring to give the neutral furan',
                },
            },
        },
        'Thiophene Synthesis': {
            'Reagent': [
                '[SH2]',
                '[CX3;$([#6](=[OX1])[#6])](=[OX1])[CH2][CH2][CX3;$([#6](=[OX1])[#6])](=[OX1])',
            ],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[SH2:10].[CX3;$([#6](=[OX1])[#6]):2](=[OX1])[CH2:4][CH2:5][CX3;$([#6](=[OX1])[#6]):6](=[OX1:7])>>[C:2](=[S;H0:10])[CH2:4][CH2:5][CX3:6](=[OX1:7])',
                    ],
                    'Description':
                    'Thionation of one carbonyl by hydrogen sulfide, giving a thioketone (water loss implicit)',
                },
                1: {
                    'Templates': [
                        '[C:2](=[SH0:10])[CH2;H2:4][CH2:5][CX3:6]=[OX1:7]>>[C:2](-[S;H1:10])=[CH1:4][CH2:5][CX3:6]=[OX1:7]',
                    ],
                    'Description':
                    'Tautomerization of the thioketone to the thioenol, giving a nucleophilic thiol sulfur',
                },
                2: {
                    'Templates': [
                        '[C:2](-[SX2;H1:10])=[CH1:4][CH2:5][CX3:6]=[OX1:7]>>[S;H1;+1:10]1[C:2]=[CH1:4][CH2:5][C:6]1(-[O-:7])',
                    ],
                    'Description':
                    'Intramolecular nucleophilic addition of the thioenol sulfur to the distal carbonyl carbon, closing the five-membered ring and forming a zwitterionic sulfonium alkoxide',
                },
                3: {
                    'Templates': [
                        '[S;+1:10](-[H:11])1[C:2]=[C:4][C:5][C:6]1(-[O-:7])>>[S;+0:10]1[C:2]=[C:4][C:5][C:6]1(-[O;+0:7]-[H:11])',
                    ],
                    'Description':
                    'Proton transfer from the ring sulfonium sulfur to the alkoxide oxygen, giving the neutral cyclic hemithioketal',
                },
                4: {
                    'Templates': [
                        '[S;H0;+0:10]1[C;H0:2]=[CH1:4][CH2;H2:5][C;H0:6]1(-[OX2H1:7])>>[s;+0:10]1[c;H0:2][c;H1:4][c;H1:5][c;H0:6]1',
                    ],
                    'Description':
                    'Loss of water (from the carbon bearing the hydroxyl and the adjacent ring carbon), aromatizing the ring to give the neutral thiophene',
                },
            },
        },
    },
    ('Knorr Synthesis', ): {
        'Pyrrole Synthesis': {
            'Reagent': [
                '[CX3](=[OX1])[CH1,CH2][N;+0;H2]',
                '[CX3;$([#6](=[OX1])[#6])](=[OX1])[CH2][CX3;$([#6](=[OX1])[#6])](=[OX1])',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CX3:1](=[OX1:2])[CH1,CH2:3][N;+0;H2:4].[CX3;$([#6](=[OX1])[#6]):6](=[OX1:7])[CH2:8][CX3;$([#6](=[OX1])[#6]):9](=[OX1:10])>>[CX3:1](=[OX1:2])[C:3][N+;H2:4]-[C:6](-[O-:7])[CH2:8][CX3:9](=[OX1:10])',
                    ],
                    'Description':
                    'Nucleophilic addition of the alpha-aminoketone amine to one carbonyl of the 1,3-dicarbonyl component, forming a zwitterionic tetrahedral ammonium alkoxide intermediate',
                },
                1: {
                    'Templates': [
                        '[CX3:1](=[OX1:2])[C:3][N+:4](-[H:12])-[C:6](-[O-:7])[C:8][CX3:9]=[OX1:10]>>[CX3:1](=[OX1:2])[C:3][N+0:4]-[C:6](-[O+0:7]-[H:12])[C:8][CX3:9]=[OX1:10]',
                    ],
                    'Description':
                    'Proton transfer from the ammonium nitrogen to the alkoxide oxygen, giving the neutral hemiaminal',
                },
                2: {
                    'Templates': [
                        '[CX3:1](=[OX1:2])[C:3][N;+0:4]-[C:6](-[OX2H1])[CH2:8][CX3:9]=[OX1:10]>>[CX3:1](=[OX1:2])[C:3][N+:4]=[C:6][CH2:8][CX3:9]=[OX1:10]',
                    ],
                    'Description':
                    'Loss of water from the hemiaminal, forming the iminium cation',
                },
                3: {
                    'Templates': [
                        '[CX3:1](=[OX1:2])[C:3][N+:4]=[C:6][CH2;H2:8][CX3:9]=[OX1:10]>>[CX3:1](=[OX1:2])[C:3][N;+0:4]-[C:6]=[CH1:8][CX3:9]=[OX1:10]',
                    ],
                    'Description':
                    'Tautomerization of the iminium to the enamine via the active methylene of the 1,3-dicarbonyl component, giving back a neutral nucleophilic enamine carbon',
                },
                4: {
                    'Templates': [
                        '[CX3:1](=[OX1:2])[C:3][N;+0:4]-[C:6]=[CH1:8][CX3:9]=[OX1:10]>>[C:1]1(-[O-:2])[C:3][N+:4]=[C:6]-[C:8]1[CX3:9]=[OX1:10]',
                    ],
                    'Description':
                    'Intramolecular aldol-type addition of the enamine carbon to the aminoketone carbonyl, closing the five-membered ring and forming a zwitterionic iminium alkoxide',
                },
                5: {
                    'Templates': [
                        '[C:1]1(-[O-:2])[CH2;H2:3][N+;H1:4]=[C:6][CH1;H1:8]1[CX3:9]=[OX1:10]>>[c;H0:1]1[c;H1:3][n;H1;+0:4][c;H0:6][c;H0:8]1[CX3:9]=[OX1:10]',
                        '[C:1]1(-[O-:2])[CH1;H1:3][N+;H1:4]=[C:6][CH1;H1:8]1[CX3:9]=[OX1:10]>>[c;H0:1]1[c;H0:3][n;H1;+0:4][c;H0:6][c;H0:8]1[CX3:9]=[OX1:10]',
                    ],
                    'Description':
                    'Loss of water (from the carbon bearing the alkoxide and the adjacent ring carbon), aromatizing the ring to give the neutral pyrrole',
                },
            },
        },
    },
    ('Catalytic Hydrogenation (H2, Pd-C)', ): {
        'Nitro to Amine': {
            'Reagent': [
                '[c][N+](=[O])[O-]',
                '[H][H]',
                '[Pd;D0;+0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:1][N+:2](=[O:3])[O-:4].[H][H]>>[c:1][N;+0:2]=[O:3]',
                    ],
                    'Description':
                    'Reduction of the nitro group to the nitroso intermediate (loses one oxygen as water)',
                },
                1: {
                    'Templates': [
                        '[c:1][N;+0:2]=[O:3].[H][H]>>[c:1][N;H1;+0:2]-[O;H1;+0:3]',
                    ],
                    'Description':
                    'Reduction of the nitroso group across the N=O bond, giving the N-arylhydroxylamine',
                },
                2: {
                    'Templates': [
                        '[c:1][N;H1;+0:2]-[O;H1:3].[H][H]>>[c:1][N;H2;+0:2]',
                    ],
                    'Description':
                    'Reduction of the hydroxylamine, losing the oxygen as water and giving the neutral primary aniline',
                },
            },
        },
        'Imine to Amine': {
            'Reagent': [
                '[CX3]=[NX2]',
                '[H][H]',
                '[Pd;D0;+0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CX3;H0,H1:1]=[NX2;H0,H1:2].[H][H]>>[C:1][N:2]',
                    ],
                    'Description':
                    'Reduction across the C=N double bond, giving the neutral secondary (or primary) amine',
                },
            },
        },
        'Nitrile to Amine': {
            'Reagent': [
                '[CX2]#[NX1]',
                '[H][H]',
                '[Pd;D0;+0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CX2:1]#[NX1:2].[H][H]>>[CX3:1]=[NX2;H1:2]',
                    ],
                    'Description':
                    'First reduction of the nitrile to the imine intermediate',
                },
                1: {
                    'Templates': [
                        '[CX3;H0,H1:1]=[NX2;H0,H1:2].[H][H]>>[C:1][N:2]',
                    ],
                    'Description':
                    'Second reduction across the resulting C=N bond, giving the neutral primary amine',
                },
            },
        },
        'Alkene to Alkane': {
            'Reagent': [
                '[CX3;H1,H2]=[CX3;H0,H1,H2]',
                '[H][H]',
                '[Pd;D0;+0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CX3;H1,H2:1]=[CX3;H0,H1,H2:2].[H][H]>>[C:1][C:2]',
                    ],
                    'Description':
                    'Alkene is hydrogenated to the alkane',
                },
            },
        },
        'Alkyne to Alkane': {
            'Reagent': [
                '[CX2]#[CX2]',
                '[H][H]',
                '[Pd;D0;+0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CX2:1]#[CX2:2].[H][H].[H][H]>>[C:1][C:2]',
                    ],
                    'Description':
                    'Alkyne is hydrogenated to the alkane',
                },
            },
        },
        'Aryl/Vinyl Halide Hydrogenolysis': {
            'Reagent': [
                '[c,C;+0]-[Cl,Br,I]',
                '[H][H]',
                '[Pd;D0;+0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c,C;+0:1]-[Cl,Br,I:2].[H][H]>>[c,C;+0:1].[Cl,Br,I;H1;+0:2]',
                    ],
                    'Description':
                    'The halide is replaced with hydrogen and the hydrogen halide is released as a byproduct',
                },
            },
        },
        'Benzylic Ether Hydrogenolysis': {
            'Reagent': [
                '[c][CH2][OX2][#6]',
                '[H][H]',
                '[Pd;D0;+0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:1][CH2;H2:2]-[OX2:3][#6:4].[H][H]>>[c:1][CH3:2].[OX2;H1:3][#6:4]',
                    ],
                    'Description':
                    'Benzylic ethers are cleaved, a classic way benzyl (Bn) protecting groups are unintentionally removed under the same conditions used for nitro reduction',
                },
            },
        },
        'Amide to Amine': {
            'Reagent': [
                '[CX3](=[OX1])[NX3]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[N;+0:3]-[CX3:1]=[OX1:2].[H][H]>>[N+:3]=[CX3;+0:1]',
                    ],
                    'Description':
                    'Hydride delivery from borane to the amide carbonyl carbon, losing the oxygen (as a borate equivalent) and forming the iminium cation',
                },
                1: {
                    'Templates': [
                        '[N+:3]=[CX3:1].[H][H]>>[N;+0:3]-[C:1]',
                    ],
                    'Description':
                    'A second hydride delivery reduces the iminium cation, giving the neutral amine',
                },
            },
        },
        'Carboxylic Acid to Alcohol': {
            'Reagent': [
                '[CX3](=[OX1])[OX2;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CX3:1](=[OX1:2])[OX2;H1:3].[H][H]>>[CH2:1][OX2;H1:3]',
                    ],
                    'Description':
                    'Borane reduces a free carboxylic acid to the primary alcohol even faster than it reduces an amide, so if both are present the acid goes first',
                },
            },
        },
    },
    ('Amide Reduction (BH3)', ): {
        'Amide to Amine': {
            'Reagent': [
                '[CX3](=[OX1])[NX3]',
                '[BH3]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CX3:1](=[OX1:2])[N;+0:3].[BH3:5]>>[C;H1:1](-[O:2][B;H2:5])[N;+0:3]',
                    ],
                    'Description':
                    'Hydride delivery from borane to the amide carbonyl carbon, forming a tetrahedral intermediate with the oxygen coordinated to the resulting BH2 fragment',
                },
                1: {
                    'Templates': [
                        '[C;H1:1](-[O:2][B;H2:5])[N;+0:3]>>[C;+0:1]=[N+:3].[O;-1:2][B;H2:5]',
                    ],
                    'Description':
                    'Collapse of the tetrahedral intermediate, expelling the oxygen as a borinate anion and forming the iminium cation',
                },
                2: {
                    'Templates': [
                        '[C;+0:1]=[N+:3].[O;-1:2][B;H2:5]>>[C;H2:1][N;+0:3].[O;-1:2][B;H1;+1:5]',
                    ],
                    'Description':
                    'The borinate byproduct delivers its second hydride to the iminium cation, giving the neutral amine',
                },
            },
        },
        'Carboxylic Acid to Alcohol': {
            'Reagent': [
                '[CX3](=[OX1])[OX2;H1]',
                '[BH3]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CX3:1](=[OX1:2])[OX2;H1:3]>>[CH2:1][OX2;H1:3]',
                    ],
                    'Description':
                    'Borane reduces a free carboxylic acid to the primary alcohol even faster than it reduces an amide, so if both are present the acid goes first',
                },
            },
        },
        'Alkene to Alkane': {
            'Reagent': [
                '[CX3;H1,H2]=[CX3;H0,H1,H2]',
                '[BH3]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CX3;H1,H2:1]=[CX3;H0,H1,H2:2]>>[C:1][C:2]',
                    ],
                    'Description':
                    'Borane hydroborates any alkene present, and simple aqueous/acidic workup delivers the net anti-Markovnikov reduction to the alkane',
                },
            },
        },
        'Alkyne to Alkane': {
            'Reagent': [
                '[CX2]#[CX2]',
                '[BH3]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CX2:1]#[CX2:2]>>[C:1][C:2]',
                    ],
                    'Description':
                    'Borane also hydroborates alkynes present in the substrate, giving the alkane after protonolytic workup',
                },
            },
        },
    },
    ('Ketone/Aldehyde Reduction (NaBH4)', ): {
        'Carbonyl to Alcohol': {
            'Reagent': [
                '[CX3;H0,H1;!$([CX3](=[OX1])[OX2,NX3,NX2,SX2,F,Cl,Br,I])](=[OX1])',
                '[BH4-]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CX3;H0,H1;!$([CX3](=[OX1])[OX2,NX3,NX2,SX2,F,Cl,Br,I]):1](=[OX1:2]).[BH4-:5]>>[C:1][O:2][B;H3;-1:5]',
                    ],
                    'Description':
                    'Hydride delivery from borohydride to the aldehyde/ketone carbonyl carbon, forming an alkoxide-borane adduct',
                },
                1: {
                    'Templates': [
                        '[C:1][O;+0:2][B;-1:5].[OX2;H2:10]([H:11])>>[C:1][O;+0:2][H:11].[B;-1:5][O;+0:10]',
                    ],
                    'Description':
                    'Aqueous workup: water protonates the alkoxide, giving the neutral alcohol and a hydroxyborate byproduct',
                },
            },
        },
    },
    ('Ester Reduction (LiAlH4)', ): {
        'Ester to Alcohol': {
            'Reagent': [
                '[CX3](=[OX1])[OX2][#6]',
                '[AlH4-]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CX3:1](=[OX1:2])[OX2:3][#6:4].[AlH4-:5]>>[C;H1:1](-[O:2][Al;H3;-1:5])[OX2:3][#6:4]',
                    ],
                    'Description':
                    'First hydride delivery from aluminum hydride to the ester carbonyl carbon, forming a tetrahedral intermediate with the oxygen coordinated to the resulting AlH3 fragment',
                },
                1: {
                    'Templates': [
                        '[C;H1:1](-[O:2][Al;H3;-1:5])[OX2:3][#6:4]>>[C:1]=[O;+0:2].[Al;H3;+0:5].[O;-1:3][#6:4]',
                    ],
                    'Description':
                    'Collapse of the tetrahedral intermediate, expelling the alkoxy leaving group and releasing neutral alane, reforming the carbonyl to give an aldehyde in situ',
                },
                2: {
                    'Templates': [
                        '[CX3;H0,H1;!$([CX3](=[OX1])[OX2,NX3,NX2,SX2,F,Cl,Br,I]):1](=[OX1:2]).[AlH4-:11]>>[C:1][O:2][Al;H3;-1:11]',
                    ],
                    'Description':
                    'Second hydride delivery from a fresh equivalent of aluminum hydride reduces the in-situ aldehyde, forming a second alkoxide-alanate adduct',
                },
                3: {
                    'Templates': [
                        '[C;!$([#6]-[OX2;!$([OX2][Al])]):1][O;+0:2][Al;-1:11].[OX2;H2:12]([H:13])>>[C:1][O;+0:2][H:13].[Al;-1:11][O;+0:12]',
                    ],
                    'Description':
                    'Aqueous workup: water protonates the alkoxide, giving the neutral primary alcohol and a hydroxyalanate byproduct',
                },
            },
        },
    },
    ('Alcohol Oxidation (Dess-Martin Periodinane)', ): {
        'Primary Alcohol to Aldehyde': {
            'Reagent': [
                '[CH2][OX2;H1]',
                'CC(=O)OI1(c2ccccc2C(=O)O1)(OC(=O)C)OC(=O)C',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CH2;H2:1][OX2;H1:2]([H:10]).[I;D5:5][OX2:6][CX3:7](=[OX1:8])[C:9]>>[C:1][O:2][I:5].[O:6]([H:10])[CX3:7](=[OX1:8])[C:9]',
                    ],
                    'Description':
                    'Ligand exchange: the alcohol oxygen displaces one acetoxy ligand on the hypervalent iodine(V) center, releasing one equivalent of acetic acid and forming an alkoxy-iodinane intermediate',
                },
                1: {
                    'Templates': [
                        '[CH2;H2:1]([H:11])[O:2][I;D5:5]([OX2:22][CX3:23](=[OX1:24])[C:25])>>[C:1]=[O:2].[I;D3:5].[O;-1:22][CX3:23](=[OX1:24])[C:25].[H+:11]',
                    ],
                    'Description':
                    'Intramolecular elimination: loss of the alpha C-H and the alkoxy-iodine bond, giving the aldehyde and reducing iodine(V) to the neutral iodine(III) byproduct, with the remaining acetoxy ligand released as acetate',
                },
            },
        },
    },
    ('Alcohol Oxidation (Jones Reagent, CrO3/H2SO4)', ): {
        'Primary Alcohol to Carboxylic Acid': {
            'Reagent': [
                '[CH2][OX2;H1]',
                '[Cr](=O)(=O)=O',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[CH2;H2:1][OX2;H1:2]>>[CH1:1]=[O:2]',
                    ],
                    'Description':
                    'Oxidation of the primary alcohol to the aldehyde, hydrated in situ by the aqueous acidic medium',
                },
                1: {
                    'Templates': [
                        '[CX3;H1:1](=[OX1:2])>>[CX3:1](=[OX1:2])[OH]',
                    ],
                    'Description':
                    'Further oxidation of the hydrated aldehyde (gem-diol), removing two hydrogens to give the carboxylic acid; unlike DMP, Jones reagent does not stop cleanly at the aldehyde',
                },
            },
        },
    },
    # side reaction of suzuki coupling
    ('Suzuki Protodeboronation', ): {
        'Reaction': {
            'Reagent':
            ['[B]-[c,C;+0]', '[OH1;-1]'],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[B:2]-[c,C;+0:4].[OH1;-1:1]>>[c,C;+0:4]-[B;-1:2]-[OH1;+0:1]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Borate formation: hydroxide adds to the boron, forming the nucleophilic tetrahedral boronate (same activation step as regular transmetalation)',
                },
                1: {
                    'Templates': [
                        '[c,C;+0:4]-[B;-1:2].[OX2;H2:10]([H:11])>>[c,C;+0:4][H:11].[B;+0:2].[O;-1:10]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Side reaction: instead of transmetalating onto Pd, the boronate undergoes protonolysis by water, replacing the boron coupling partner with hydrogen and releasing boric acid; this competing pathway is especially fast for electron-poor or heteroaryl boronic acids, destroying the coupling partner before it can reach Pd',
                },
            },
        },
    },
    # side reaction of suzuki coupling
    ('Suzuki Boron Coupling Partner Homocoupling', ): {
        'Reaction': {
            'Reagent':
            ['[B]-[c,C;+0]', '[Pd;D0;+0]', '[O]=[O]'],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[Pd;D0;+0:6].[O:7]=[O:8]>>[Pd:6]1[O:7][O:8]1',
                    ],
                    'pKa': [None],
                    'Description':
                    'Side reaction: trace oxygen oxidizes Pd(0), giving a Pd(II) eta2-peroxo complex (the O=O bond is retained, not cleaved)',
                },
                1: {
                    'Templates': [
                        '[Pd:6]1[O:7][O:8]1.[c,C;+0:20][B;+0:21]([O:22])[O:23]>>[Pd;+1:6][O:7][O:8][B;-1:21]([c,C;+0:20])([O:22])[O:23]',
                    ],
                    'pKa': [None],
                    'Description':
                    'The boron coupling partner inserts into the Pd-bound peroxide: boron attacks the distal peroxide oxygen, opening the Pd-O-O ring into a Pd-O-O-B(Ar)(OH)2 chain with the aryl/vinyl group still on boron',
                },
                2: {
                    'Templates': [
                        '[Pd;+1:6][O:7][O:8][B;-1:21]([c,C;+0:20])([O:22])[O:23]>>[Pd;+0:6]([c,C;+0:20])[O:7][O:8][B;+0:21]([O:22])[O:23]',
                    ],
                    'pKa': [None],
                    'Description':
                    '1,2-Migration of the aryl/vinyl group from boron to palladium, giving an aryl/vinyl-Pd(II) complex still bearing the peroxyborate chain as a ligand',
                },
                3: {
                    'Templates': [
                        '[Pd:6]([c,C;+0:20])[O:7][O:8][B:21]([O:22])[O:23].[OX2;H2:30]>>[Pd:6]([c,C;+0:20])[OH1:30].[OH1:7][O:8][B:21]([O:22])[O:23]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Water displaces the peroxyborate chain from Pd, giving an aryl/vinyl-Pd(II)-hydroxide complex and releasing free peroxyboric acid, (HO)2B-OO-H, as a byproduct',
                },
                4: {
                    'Templates': [
                        '[OH1:7][O:8][B:21]([O:22])[O:23].[c,C;+0:40][B;+0:41]([O:42])[O:43]>>[c,C;+0:40][OH1:7].[B:21]([O:22])([O:23])[O:8][B;+0:41]([O:42])[O:43]',
                    ],
                    'pKa': [None],
                    'Description':
                    'The released peroxyborate oxidizes a third equivalent of the boron coupling partner: the terminal peroxide oxygen is transferred to the aryl/vinyl group, giving the phenol/enol and a B-O-B boric anhydride, so overall one O2 consumes three equivalents of the boron coupling partner',
                },
                5: {
                    'Templates': [
                        '[B:21]([O:22])([O:23])[O;H0:8][B;+0:41]([O:42])[O:43].[OX2;H2:30]>>[B:21]([O:22])([O:23])[OH1:8].[B;+0:41]([O:42])([O:43])[OH1:30]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Hydrolysis of the B-O-B boric anhydride by water, giving two B-OH species',
                },
                6: {
                    'Templates': [
                        '[Pd:6]([c,C;+0:20])[OH1:30].[c,C;+0:40][B;+0:41]([O:42])[O:43]>>[Pd:6]([c,C;+0:20])[c,C;+0:40].[B;+0:41]([OH1:30])([O:42])[O:43]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Another equivalent of the boron coupling partner transmetalates directly onto the aryl/vinyl-Pd(II)-hydroxide complex, giving the bis(aryl/vinyl)-Pd(II) complex and boric acid',
                },
                7: {
                    'Templates': [
                        '[c,C;+0:20]-[Pd:6]-[c,C;+0:40]>>[c,C;+0:20]-[c,C;+0:40].[Pd;D0;+0:6]',
                    ],
                    'pKa': [None],
                    'Description':
                    'Reductive elimination, giving the symmetric homocoupled biaryl (the boron coupling partner coupled with itself, not with the halide partner) and regenerating Pd(0)',
                },
            },
        },
    },
    # side reaction of suzuki coupling
    ('Suzuki Dehalogenation', ): {
        'Reaction': {
            'Reagent':
            ['[Cl,Br,I,$(O-S(=O)(=O)[#6])]-[c,C;+0]', '[Pd;D0;+0]', '[OX2;-1][CX4;H1,H2][#6]'],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]-[c,C;+0:5].[Pd;D0;+0:6]>>[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]-[Pd:6]-[c,C;+0:5]',
                    ],
                    'Description':
                    'Oxidative addition of the aryl/vinyl halide to Pd(0), forming an aryl/vinyl-Pd(II)-halide complex',
                },
                1: {
                    'Templates': [
                        '[O;-1:10][C:11]([H:12])[C:13].[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]-[Pd:6]-[c,C;+0:5]>>[O;+0:10]([C:11]([H:12])[C:13])-[Pd:6]-[c,C;+0:5].[Cl,Br,I,$(O-S(=O)(=O)[#6]);-1:3]',
                    ],
                    'Description':
                    'Ligand exchange: an alkoxide (commonly deprotonated alcohol solvent, e.g. ethanol/methanol/isopropanol used as a co-solvent) displaces the halide on the aryl/vinyl-Pd(II) complex',
                },
                2: {
                    'Templates': [
                        '[O;+0:10]([C:11]([H:12])[C:13])-[Pd:6]-[c,C;+0:5]>>[O;+0:10]=[C:11][C:13].[Pd:6]([H:12])-[c,C;+0:5]',
                    ],
                    'Description':
                    'Side reaction: instead of transmetalating with the boron coupling partner, the aryl/vinyl-Pd(II)-alkoxide complex undergoes beta-hydride elimination from the alkoxide ligand, giving the corresponding aldehyde/ketone and an aryl/vinyl-Pd(II)-hydride complex',
                },
                3: {
                    'Templates': [
                        '[c,C;+0:5]-[Pd:6]([H:12])>>[c,C;+0:5][H:12].[Pd;D0;+0:6]',
                    ],
                    'Description':
                    'Reductive elimination of the aryl/vinyl-Pd(II)-hydride complex, giving the dehalogenated (reduced) arene/alkene instead of the Suzuki coupling product and regenerating Pd(0)',
                },
            },
        },
    },
    # side reaction of sonogashira reaction
    ('Glaser Homocoupling', ): {
        'Reaction': {
            'Reagent':
            ['[CX2;H1]#[CX2]', '[Cu;+1;D0]', '[OH1;-1]', '[O]=[O]'],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[OH1;-1:8].[CX2;H1:1]([H:7])#[CX2:2]>>[O;+0:8]([H:7]).[C;H0;-1:1]#[CX2:2]',
                    ],
                    'Description':
                    'Deprotonation of the first equivalent of the terminal alkyne by base, giving the acetylide anion',
                },
                1: {
                    'Templates': [
                        '[Cu;+1;D0:9].[C;H0;-1:1]#[CX2:2]>>[Cu;+0:9]-[C;+0:1]#[CX2:2]',
                    ],
                    'Description':
                    'Transmetalation of the first acetylide onto Cu(I), forming the first copper acetylide',
                },
                2: {
                    'Templates': [
                        '[OH1;-1:18].[CX2;H1:11]([H:17])#[CX2:12]>>[O;+0:18]([H:17]).[C;H0;-1:11]#[CX2:12]',
                    ],
                    'Description':
                    'Deprotonation of a second equivalent of the terminal alkyne by base, giving a second acetylide anion',
                },
                3: {
                    'Templates': [
                        '[Cu;+1;D0:19].[C;H0;-1:11]#[CX2:12]>>[Cu;+0:19]-[C;+0:11]#[CX2:12]',
                    ],
                    'Description':
                    'Transmetalation of the second acetylide onto Cu(I), forming a second copper acetylide',
                },
                4: {
                    'Templates': [
                        '[Cu:9]-[C;+0:1]#[C:2].[Cu:19]-[C;+0:11]#[C:12].[O:30]=[O:31]>>[C:2]#[C:1]-[C:11]#[C:12].[Cu:9]-[O:30].[Cu:19]-[O:31]',
                    ],
                    'Description':
                    'Side reaction: trace oxygen oxidatively couples the two copper acetylides directly to each other instead of either one transmetalating onto the aryl/vinyl-Pd(II) complex, giving the symmetric 1,3-diyne (Glaser coupling) and regenerating Cu(I) as copper hydroxide',
                },
            },
        },
    },
    # side reaction of buchwald-hartwig amination
    ('Buchwald-Hartwig Dehalogenation', ): {
        'Reaction': {
            'Reagent':
            ['[Cl,Br,I,$(O-S(=O)(=O)[#6])]-[c,C;+0]', '[N;+0;H1;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O)]', '[Pd;D0;+0]', '[OH1;-1]'],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]-[c,C;+0:5].[Pd;D0;+0:6]>>[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]-[Pd:6]-[c,C;+0:5]',
                    ],
                    'Description':
                    'Oxidative addition of the aryl/vinyl halide to Pd(0), forming an aryl/vinyl-Pd(II)-halide complex',
                },
                1: {
                    'Templates': [
                        '[OH1;-1:8].[N;+0;H1;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]([H:7])>>[O;+0:8]([H:7]).[N;H0;-1:1]',
                    ],
                    'Description':
                    'Deprotonation of the secondary amine by base, giving the nucleophilic amide anion',
                },
                2: {
                    'Templates': [
                        '[N;-1:1].[Cl,Br,I,$(O-S(=O)(=O)[#6]):3]-[Pd:6]-[c,C;+0:5]>>[N;+0:1]-[Pd:6]-[c,C;+0:5].[Cl,Br,I,$(O-S(=O)(=O)[#6]);-1:3]',
                    ],
                    'Description':
                    'Ligand exchange: the amide anion displaces the halide on the aryl/vinyl-Pd(II) complex, giving an amido-Pd(II) intermediate',
                },
                3: {
                    'Templates': [
                        '[N;+0:1](-[CH2:20]([H:21])[C:22])-[Pd:6]-[c,C;+0:5]>>[N:1]=[C:20][C:22].[Pd:6]([H:21])-[c,C;+0:5]',
                    ],
                    'Description':
                    'Side reaction: instead of reductive elimination, the amido-Pd(II) complex undergoes beta-hydride elimination from an alpha-CH2 of the amine ligand (possible whenever the amine has a beta-hydrogen), giving an imine byproduct and an aryl/vinyl-Pd(II)-hydride complex',
                },
                4: {
                    'Templates': [
                        '[c,C;+0:5]-[Pd:6]([H:21])>>[c,C;+0:5][H:21].[Pd;D0;+0:6]',
                    ],
                    'Description':
                    'Reductive elimination of the aryl/vinyl-Pd(II)-hydride complex, giving the dehalogenated (reduced) arene/alkene instead of the amination product and regenerating Pd(0)',
                },
            },
        },
    },
    # side reaction of heck reaction
    ('Heck Chain-Walking Isomerization', ): {
        'Reaction': {
            'Reagent':
            ['[CX3;H1,H2]=[CX3;H0,H1,H2]', '[Pd;D0;+0]', '[Cl,Br,I]'],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[Pd;D0;+0:6].[H:7][Cl,Br,I:8]>>[Pd:6]([H:7])-[Cl,Br,I:8]',
                    ],
                    'Description':
                    'Protonation of Pd(0) by the hydrogen halide byproduct, regenerating the hydrido-Pd(II)-halide complex released at the end of a normal Heck cycle',
                },
                1: {
                    'Templates': [
                        '[Pd:6]([H:7])-[Cl,Br,I:8].[c:30][C:1][CH1:2]=[CH1:3][C:4]>>[c:30][C:1][C:2]([Pd:6][Cl,Br,I:8])[C:3]([H:7])[C:4]',
                    ],
                    'Description':
                    'Side reaction: instead of diffusing away, the hydrido-Pd(II)-halide complex re-adds (hydropalladation) across the Heck product alkene, placing Pd on the carbon adjacent to the aryl-bearing carbon',
                },
                2: {
                    'Templates': [
                        '[C;H1,H2:1]([H:9])[C:2]([Pd:6][Cl,Br,I:8])>>[C:1]=[C:2].[Pd:6]([H:9])[Cl,Br,I:8]',
                    ],
                    'Description':
                    'A second beta-hydride elimination, now removing a hydrogen from the aryl-bearing carbon instead of reforming the original alkene, "walks" the double bond into conjugation with the aromatic ring (the thermodynamically favored isomer) and regenerates the hydrido-Pd(II)-halide complex',
                },
            },
        },
    },
    # side reaction of grignard addition
    ('Grignard Enolization', ): {
        'Reaction': {
            'Reagent':
            ['[#6]-[Mg]-[Cl,Br,I]', '[CX4;H1,H2,H3][CX3]=[OX1]'],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[#6:1]-[Mg:2]-[Cl,Br,I:3].[CX4;H1,H2,H3:10]([H:11])[CX3:4]=[OX1:5]>>[#6:1][H:11].[Mg:2](-[Cl,Br,I:3])-[O:5]-[C:4]=[C:10]',
                    ],
                    'Description':
                    'Side reaction: instead of adding to the carbonyl carbon, the Grignard reagent acts as a base, deprotonating the alpha-carbon of the aldehyde/ketone; this gives the magnesium enolate and the Grignard reagent\'s conjugate acid (the alkane) instead of the addition product, and is especially competitive for enolizable, sterically hindered, or acidic carbonyl substrates',
                },
            },
        },
    },
    # side reaction of organolithium addition
    ('Organolithium Enolization', ): {
        'Reaction': {
            'Reagent':
            ['[#6]-[Li]', '[CX4;H1,H2,H3][CX3]=[OX1]'],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[#6:1]-[Li:2].[CX4;H1,H2,H3:10]([H:11])[CX3:4]=[OX1:5]>>[#6:1][H:11].[Li:2]-[O:5]-[C:4]=[C:10]',
                    ],
                    'Description':
                    'Side reaction: instead of adding to the carbonyl carbon, the organolithium reagent acts as a base, deprotonating the alpha-carbon of the aldehyde/ketone; this gives the lithium enolate and the organolithium reagent\'s conjugate acid (the alkane) instead of the addition product, and is especially competitive for enolizable, sterically hindered, or acidic carbonyl substrates',
                },
            },
        },
    },
    # side reaction of n-alkylation
    ('N-alkylation E2 Elimination', ): {
        'Reaction': {
            'Reagent':
            ['[N;+0;H2;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O)]', '[CX4;H2,H3]-[CX4]-[Cl,Br,I,$(O-S(=O)(=O)[#6])]'],
            'Exclude_reagent':
            None,
            'Stages': {
                0: {
                    'Templates': [
                        '[N;H2;+0;!$(N-[C,S]=[O,S,N]);!$(N-S(=O)=O):1]>>[N;H1;-1:1]',
                    ],
                    'Description':
                    'Deprotonation of the amine nitrogen',
                },
                1: {
                    'Templates': [
                        '[N;-1:1]([H:9]).[CX4;H2,H3:2]([H:10])[CX4:3][Cl,Br,I,$(O-S(=O)(=O)[#6]):4]>>[N;+0:1]([H:9])[H:10].[C:2]=[C:3].[Cl,Br,I,$(O-S(=O)(=O)[#6]);-1:4]',
                    ],
                    'Description':
                    'Side reaction: instead of attacking the alkyl carbon (SN2 substitution), the amide anion acts as a base, removing a beta-hydrogen (E2 elimination); this gives the alkene and the halide/sulfonate leaving group instead of the N-alkylated product, and the amine is simply reprotonated rather than alkylated. This pathway competes most strongly with secondary/tertiary alkyl halides and bulkier amines/bases',
                },
            },
        },
    },
}

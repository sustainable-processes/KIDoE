march_reaction_templates = {
    ('Ester hydrolysis via alkyl-oxygen cleavage',): {
        # Overall transformation (Ingold classification A_AL2 / B_AL2, March's
        # Advanced Organic Chemistry): the nucleophile attacks the alkyl carbon
        # of a methyl ester rather than the carbonyl carbon, so the alkyl-oxygen
        # bond (not the acyl-oxygen bond) is broken.
        #   [C:1](=[O:2])[O:3][C;H3:4].[O;!H0:5]
        #       >> [C:1](=[O:2])[O:3][H:6].[13C:4][17O:5]
        # 13C/17O double labeling of the leaving methyl group and of the
        # nucleophile is the classic experiment (March, "Advanced Organic
        # Chemistry") used to prove this pathway: if hydrolysis/solvolysis
        # proceeded by the usual acyl-oxygen fission, the label would stay on
        # the carboxylic acid oxygen instead of ending up bonded to the methyl
        # carbon.
        'Reaction': {
            'Reagent': [
                '[C;H3][O][C]=[O]',
                '[O;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        # Nucleophile with one exchangeable proton (e.g. an alcohol R-OH)
                        '[C:1](=[O:2])[O;H0;+0:3][C;H3;+0:4].[O;H1;+0:5]>>[C:1](=[O:2])[O;H0;-1:3].[C;H3;+0:4][O;H1;+1:5]',
                        # Nucleophile with two exchangeable protons (water)
                        '[C:1](=[O:2])[O;H0;+0:3][C;H3;+0:4].[O;H2;+0:5]>>[C:1](=[O:2])[O;H0;-1:3].[C;H3;+0:4][O;H2;+1:5]',
                    ],
                    'pKa': [None, None],
                    'Description': 'SN2 attack of the nucleophile on the methyl carbon (alkyl-oxygen cleavage)',
                },
                1: {
                    'Templates': [
                        # Collapse of the intermediate from a mono-protic nucleophile
                        '[C:1](=[O:2])[O;H0;-1:3].[C;H3;+0:4][O;H1;+1:5]>>[C:1](=[O:2])[O;H1;+0:3].[C;H3;+0:4][O;H0;+0:5]',
                        # Collapse of the intermediate from water
                        '[C:1](=[O:2])[O;H0;-1:3].[C;H3;+0:4][O;H2;+1:5]>>[C:1](=[O:2])[O;H1;+0:3].[C;H3;+0:4][O;H1;+0:5]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the oxonium oxygen to the carboxylate',
                },
            },
        },
    },
    ('Schotten-Baumann amidation',): {
        # Overall transformation: addition-elimination (nucleophilic acyl
        # substitution) of an aromatic amine at an acyl chloride carbonyl.
        #   [C:1](=[O:2])[Cl:3].[N;!H0:4][c:5]1[c:6][c:7][c:8][c:9][c:10]1
        #       >> [C:1](=[O:2])[N:4][c:5]1[c:6][c:7][c:8][c:9][c:10]1.[Cl:3][H:11]
        'Nucleophilic acyl substitution at the acyl chloride carbonyl': {
            'Reagent': [
                '[C](=[O])[Cl]',
                '[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        # Primary aromatic amine (Ar-NH2)
                        '[C;H0:1](=[O;H0;+0:2])[Cl;H0;+0:3].[N;H2;+0:4][c:5]>>[C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[N;H2;+1:4][c:5]',
                        # Secondary aromatic amine (Ar-NHR)
                        '[C;H0:1](=[O;H0;+0:2])[Cl;H0;+0:3].[N;H1;+0:4][c:5]>>[C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[N;H1;+1:4][c:5]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition of the amine to the acyl chloride carbonyl',
                },
                1: {
                    'Templates': [
                        # From the primary-amine adduct
                        '[C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[N;H2;+1:4][c:5]>>[C;H0:1](=[O;H0;+0:2])[N;H2;+1:4][c:5].[Cl;H0;-1:3]',
                        # From the secondary-amine adduct
                        '[C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[N;H1;+1:4][c:5]>>[C;H0:1](=[O;H0;+0:2])[N;H1;+1:4][c:5].[Cl;H0;-1:3]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Tetrahedral intermediate collapse, expelling chloride',
                },
                2: {
                    'Templates': [
                        # Ammonium from primary amine loses one proton to become a secondary amide
                        '[C;H0:1](=[O;H0;+0:2])[N;H2;+1:4][c:5].[Cl;H0;-1:3]>>[C;H0:1](=[O;H0;+0:2])[N;H1;+0:4][c:5].[Cl;H1;+0:3]',
                        # Ammonium from secondary amine loses its proton to become a tertiary amide
                        '[C;H0:1](=[O;H0;+0:2])[N;H1;+1:4][c:5].[Cl;H0;-1:3]>>[C;H0:1](=[O;H0;+0:2])[N;H0;+0:4][c:5].[Cl;H1;+0:3]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the ammonium nitrogen to chloride',
                },
            },
        },
    },
    ('Acyl bromide + aniline amidation',): {
        'Reaction': {
            'Reagent': [
                '[C](=[O])[Br]',
                '[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;H0:1](=[O;H0;+0:2])[Br;H0;+0:3].[N;H2;+0:4][c:5]>>[C;H0:1]([O;H0;-1:2])([Br;H0;+0:3])[N;H2;+1:4][c:5]',
                        '[C;H0:1](=[O;H0;+0:2])[Br;H0;+0:3].[N;H1;+0:4][c:5]>>[C;H0:1]([O;H0;-1:2])([Br;H0;+0:3])[N;H1;+1:4][c:5]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition of the amine to the acyl bromide carbonyl',
                },
                1: {
                    'Templates': [
                        '[C;H0:1]([O;H0;-1:2])([Br;H0;+0:3])[N;H2;+1:4][c:5]>>[C;H0:1](=[O;H0;+0:2])[N;H2;+1:4][c:5].[Br;H0;-1:3]',
                        '[C;H0:1]([O;H0;-1:2])([Br;H0;+0:3])[N;H1;+1:4][c:5]>>[C;H0:1](=[O;H0;+0:2])[N;H1;+1:4][c:5].[Br;H0;-1:3]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Tetrahedral intermediate collapse, expelling bromide',
                },
                2: {
                    'Templates': [
                        '[C;H0:1](=[O;H0;+0:2])[N;H2;+1:4][c:5].[Br;H0;-1:3]>>[C;H0:1](=[O;H0;+0:2])[N;H1;+0:4][c:5].[Br;H1;+0:3]',
                        '[C;H0:1](=[O;H0;+0:2])[N;H1;+1:4][c:5].[Br;H0;-1:3]>>[C;H0:1](=[O;H0;+0:2])[N;H0;+0:4][c:5].[Br;H1;+0:3]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the ammonium nitrogen to bromide',
                },
            },
        },
    },
    ('Anhydride aminolysis',): {
        'Reaction': {
            'Reagent': [
                '[C](=[O])[O][C]=[O]',
                '[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:2](=[O;H0;+0:3])[O;H0;+0:4][C:5]=[O;H0;+0:6].[N;H2;+0:1]>>[C:2]([O;H0;-1:3])([O;H0;+0:4][C:5]=[O;H0;+0:6])[N;H2;+1:1]',
                        '[C:2](=[O;H0;+0:3])[O;H0;+0:4][C:5]=[O;H0;+0:6].[N;H1;+0:1]>>[C:2]([O;H0;-1:3])([O;H0;+0:4][C:5]=[O;H0;+0:6])[N;H1;+1:1]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition of the amine to one anhydride carbonyl',
                },
                1: {
                    'Templates': [
                        '[C:2]([O;H0;-1:3])([O;H0;+0:4][C:5]=[O;H0;+0:6])[N;H2;+1:1]>>[C:2](=[O;H0;+0:3])[N;H2;+1:1].[O;H0;-1:4][C:5]=[O;H0;+0:6]',
                        '[C:2]([O;H0;-1:3])([O;H0;+0:4][C:5]=[O;H0;+0:6])[N;H1;+1:1]>>[C:2](=[O;H0;+0:3])[N;H1;+1:1].[O;H0;-1:4][C:5]=[O;H0;+0:6]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Collapse expelling the carboxylate leaving group',
                },
                2: {
                    'Templates': [
                        '[C:2](=[O;H0;+0:3])[N;H2;+1:1].[O;H0;-1:4][C:5]=[O;H0;+0:6]>>[C:2](=[O;H0;+0:3])[N;H1;+0:1].[O;H1;+0:4][C:5]=[O;H0;+0:6]',
                        '[C:2](=[O;H0;+0:3])[N;H1;+1:1].[O;H0;-1:4][C:5]=[O;H0;+0:6]>>[C:2](=[O;H0;+0:3])[N;H0;+0:1].[O;H1;+0:4][C:5]=[O;H0;+0:6]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the ammonium nitrogen to the carboxylate',
                },
            },
        },
    },
    ('Acyl chloride + alcohol esterification',): {
        'Reaction': {
            'Reagent': [
                '[C](=[O])[Cl]',
                '[C][O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;H0:1](=[O;H0;+0:2])[Cl;H0;+0:3].[C;!$(C=O):5][O;H1;+0:4]>>[C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[O;H1;+1:4][C:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the alcohol to the acyl chloride carbonyl',
                },
                1: {
                    'Templates': [
                        '[C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[O;H1;+1:4][C:5]>>[C;H0:1](=[O;H0;+0:2])[O;H1;+1:4][C:5].[Cl;H0;-1:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Tetrahedral intermediate collapse, expelling chloride',
                },
                2: {
                    'Templates': [
                        '[C;H0:1](=[O;H0;+0:2])[O;H1;+1:4][C:5].[Cl;H0;-1:3]>>[C;H0:1](=[O;H0;+0:2])[O;H0;+0:4][C:5].[Cl;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxocarbenium oxygen to chloride',
                },
            },
        },
    },
    ('Carboxylic acid + amine thermal amidation',): {
        'Reaction': {
            'Reagent': [
                '[C](=[O])[O;H1]',
                '[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;H0:1](=[O;H0;+0:2])[O;H1;+0:3].[N;H2;+0:4]>>[C;H0:1]([O;H0;-1:2])([O;H1;+0:3])[N;H2;+1:4]',
                        '[C;H0:1](=[O;H0;+0:2])[O;H1;+0:3].[N;H1;+0:4]>>[C;H0:1]([O;H0;-1:2])([O;H1;+0:3])[N;H1;+1:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition of the amine to the carboxylic acid carbonyl',
                },
                1: {
                    'Templates': [
                        '[C;H0:1]([O;H0;-1:2])([O;H1;+0:3])[N;H2;+1:4]>>[C;H0:1]([O;H0;-1:2])([O;H2;+1:3])[N;H1;+0:4]',
                        '[C;H0:1]([O;H0;-1:2])([O;H1;+0:3])[N;H1;+1:4]>>[C;H0:1]([O;H0;-1:2])([O;H2;+1:3])[N;H0;+0:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer converting the hydroxyl into a water leaving group',
                },
                2: {
                    'Templates': [
                        '[C;H0:1]([O;H0;-1:2])([O;H2;+1:3])[N;H1;+0:4]>>[C;H0:1](=[O;H0;+0:2])[N;H1;+0:4].[O;H2;+0:3]',
                        '[C;H0:1]([O;H0;-1:2])([O;H2;+1:3])[N;H0;+0:4]>>[C;H0:1](=[O;H0;+0:2])[N;H0;+0:4].[O;H2;+0:3]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Collapse expelling water and re-forming the carbonyl',
                },
            },
        },
    },
    ('Phosgene alcoholysis to chloroformate',): {
        'Reaction': {
            'Reagent': [
                '[Cl][C](=[O])[Cl]',
                '[C][O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[Cl;H0;+0:1][C;H0:2](=[O;H0;+0:3])[Cl;H0;+0:4].[C:5][O;H1;+0:6]>>[Cl;H0;+0:1][C;H0:2]([O;H0;-1:3])([Cl;H0;+0:4])[O;H1;+1:6][C:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the alcohol to one phosgene carbonyl',
                },
                1: {
                    'Templates': [
                        '[Cl;H0;+0:1][C;H0:2]([O;H0;-1:3])([Cl;H0;+0:4])[O;H1;+1:6][C:5]>>[Cl;H0;+0:1][C;H0:2](=[O;H0;+0:3])[O;H1;+1:6][C:5].[Cl;H0;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Tetrahedral intermediate collapse, expelling one chloride',
                },
                2: {
                    'Templates': [
                        '[Cl;H0;+0:1][C;H0:2](=[O;H0;+0:3])[O;H1;+1:6][C:5].[Cl;H0;-1:4]>>[Cl;H0;+0:1][C;H0:2](=[O;H0;+0:3])[O;H0;+0:6][C:5].[Cl;H1;+0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxocarbenium oxygen to chloride',
                },
            },
        },
    },
    ('Chloroformate alcoholysis to carbonate',): {
        'Reaction': {
            'Reagent': [
                '[Cl][C](=[O])[O][C]',
                '[C][O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[Cl;H0;+0:1][C;H0:2](=[O;H0;+0:3])[O;H0;+0:4][C:5].[C:6][O;H1;+0:7]>>[Cl;H0;+0:1][C;H0:2]([O;H0;-1:3])([O;H0;+0:4][C:5])[O;H1;+1:7][C:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the alcohol to the chloroformate carbonyl',
                },
                1: {
                    'Templates': [
                        '[Cl;H0;+0:1][C;H0:2]([O;H0;-1:3])([O;H0;+0:4][C:5])[O;H1;+1:7][C:6]>>[C;H0:2](=[O;H0;+0:3])([O;H0;+0:4][C:5])[O;H1;+1:7][C:6].[Cl;H0;-1:1]',
                    ],
                    'pKa': [None],
                    'Description': 'Tetrahedral intermediate collapse, expelling chloride',
                },
                2: {
                    'Templates': [
                        '[C;H0:2](=[O;H0;+0:3])([O;H0;+0:4][C:5])[O;H1;+1:7][C:6].[Cl;H0;-1:1]>>[C;H0:2](=[O;H0;+0:3])([O;H0;+0:4][C:5])[O;H0;+0:7][C:6].[Cl;H1;+0:1]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxocarbenium oxygen to chloride',
                },
            },
        },
    },
    ('Acyl chloride + ether alkylation via oxonium',): {
        'Reaction': {
            'Reagent': [
                '[C](=[O])[Cl]',
                '[C][O][C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C;H0:2](=[O;H0;+0:3])[Cl;H0;+0:4].[C;!$(C=O):5][O;H0;+0:6][C;!$(C=O):7]>>[C:1][C;H0:2]([O;H0;-1:3])([Cl;H0;+0:4])[O;H0;+1:6]([C:5])[C:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the ether oxygen to the acyl chloride carbonyl',
                },
                1: {
                    'Templates': [
                        '[C:1][C;H0:2]([O;H0;-1:3])([Cl;H0;+0:4])[O;H0;+1:6]([C:5])[C:7]>>[C:1][C;H0:2](=[O;H0;+0:3])[O;H0;+1:6]([C:5])[C:7].[Cl;H0;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Tetrahedral intermediate collapse, expelling chloride and forming a trialkyl oxonium ester',
                },
                2: {
                    'Templates': [
                        '[C:1][C;H0:2](=[O;H0;+0:3])[O;H0;+1:6]([C:5])[C:7].[Cl;H0;-1:4]>>[C:1][C;H0:2](=[O;H0;+0:3])[O;H0;+0:6][C:5].[C:7][Cl;H0;+0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of chloride on the oxonium alkyl carbon, releasing the neutral ester',
                },
            },
        },
    },
    ('Amide alcoholysis to ester',): {
        'Reaction': {
            'Reagent': [
                '[C](=[O])[N]',
                '[C][O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;H0:1](=[O;H0;+0:2])[N;H0;+0:3]([C:4])[C:5].[C:6][O;H1;+0:7]>>[C;H0:1]([O;H0;-1:2])([N;H0;+0:3]([C:4])[C:5])[O;H1;+1:7][C:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the alcohol to the amide carbonyl',
                },
                1: {
                    'Templates': [
                        '[C;H0:1]([O;H0;-1:2])([N;H0;+0:3]([C:4])[C:5])[O;H1;+1:7][C:6]>>[C;H0:1](=[O;H0;+0:2])[O;H1;+1:7][C:6].[N;H0;-1:3]([C:4])[C:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Tetrahedral intermediate collapse, expelling the amide nitrogen as an amide anion',
                },
                2: {
                    'Templates': [
                        '[C;H0:1](=[O;H0;+0:2])[O;H1;+1:7][C:6].[N;H0;-1:3]([C:4])[C:5]>>[C;H0:1](=[O;H0;+0:2])[O;H0;+0:7][C:6].[13C:4][N;H1;+0:3][C:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxocarbenium oxygen to the amide anion',
                },
            },
        },
    },
    ('Carboxylic acid anhydride condensation',): {
        'Reaction': {
            'Reagent': [
                '[C](=[O])[O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1](=[O;H0;+0:2])[O;H1;+0:3].[C:4](=[O;H0;+0:5])[O;H1;+0:6]>>[C:1](=[O;H0;+0:2])[O;H1;+1:3][C:4]([O;H0;-1:5])[O;H1;+0:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of one acid oxygen to the other carbonyl',
                },
                1: {
                    'Templates': [
                        '[C:1](=[O;H0;+0:2])[O;H1;+1:3][C:4]([O;H0;-1:5])[O;H1;+0:6]>>[C:1](=[O;H0;+0:2])[O;H1;+1:3][C:4]=[O;H0;+0:5].[O;H1;-1:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Collapse expelling the second hydroxyl as an alkoxide',
                },
                2: {
                    'Templates': [
                        '[C:1](=[O;H0;+0:2])[O;H1;+1:3][C:4]=[O;H0;+0:5].[O;H1;-1:6]>>[13C:1](=[O;H0;+0:2])[17O;H0;+0:3][C:4]=[O;H0;+0:5].[O;H2;+0:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer giving the neutral anhydride and water',
                },
            },
        },
    },
    ('Carboxylic acid + enol ester transesterification',): {
        'Reaction': {
            'Reagent': [
                '[C](=[O])[O;H1]',
                '[C]=[C][O][C]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1](=[O;H0;+0:2])[O;H1;+0:3].[C;H0:4](=[O;H0;+0:5])[O;H0;+0:6][C:7]([C:8])=[C:9]>>[C:1](=[O;H0;+0:2])[O;H1;+1:3][C;H0:4]([O;H0;-1:5])[O;H0;+0:6][C:7]([C:8])=[C:9]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the acid oxygen to the enol ester carbonyl',
                },
                1: {
                    'Templates': [
                        '[C:1](=[O;H0;+0:2])[O;H1;+1:3][C;H0:4]([O;H0;-1:5])[O;H0;+0:6][C:7]([C:8])=[C:9]>>[C:1](=[O;H0;+0:2])[O;H1;+1:3][C;H0:4](=[O;H0;+0:5]).[O;H0;-1:6][C:7]([C:8])=[C:9]',
                    ],
                    'pKa': [None],
                    'Description': 'Collapse expelling the enolate leaving group',
                },
                2: {
                    'Templates': [
                        '[C:1](=[O;H0;+0:2])[O;H1;+1:3][C;H0:4](=[O;H0;+0:5]).[O;H0;-1:6][C:7]([C:8])=[C:9]>>[C:1](=[O;H0;+0:2])[O;H0;+0:3][C;H0:4](=[O;H0;+0:5]).[O;H1;+0:6][C:7]([C:8])=[C:9]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer giving the new ester and the free enol',
                },
            },
        },
    },
    ('Carboxylic acid + aniline amidation isotope-labeled',): {
        'Reaction': {
            'Reagent': [
                '[C](=[O])[O;H1]',
                '[N;!H0][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;H0:1](=[O;H0;+0:2])[O;H1;+0:3].[N;H2;+0:4][c:5]>>[C;H0:1]([O;H0;-1:2])([O;H1;+0:3])[N;H2;+1:4][c:5]',
                        '[C;H0:1](=[O;H0;+0:2])[O;H1;+0:3].[N;H1;+0:4][c:5]>>[C;H0:1]([O;H0;-1:2])([O;H1;+0:3])[N;H1;+1:4][c:5]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition of the aniline to the carboxylic acid carbonyl',
                },
                1: {
                    'Templates': [
                        '[C;H0:1]([O;H0;-1:2])([O;H1;+0:3])[N;H2;+1:4][c:5]>>[C;H0:1]([O;H0;-1:2])([O;H2;+1:3])[N;H1;+0:4][c:5]',
                        '[C;H0:1]([O;H0;-1:2])([O;H1;+0:3])[N;H1;+1:4][c:5]>>[C;H0:1]([O;H0;-1:2])([O;H2;+1:3])[N;H0;+0:4][c:5]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer converting the hydroxyl into a water leaving group',
                },
                2: {
                    'Templates': [
                        '[C;H0:1]([O;H0;-1:2])([O;H2;+1:3])[N;H1;+0:4][c:5]>>[13C;H0:1](=[17O;H0;+0:2])[N;H1;+0:4][c:5].[O;H2;+0:3]',
                        '[C;H0:1]([O;H0;-1:2])([O;H2;+1:3])[N;H0;+0:4][c:5]>>[13C;H0:1](=[17O;H0;+0:2])[N;H0;+0:4][c:5].[O;H2;+0:3]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Collapse expelling water and re-forming the carbonyl',
                },
            },
        },
    },
    ('Acyl chloride + thiol thioesterification',): {
        'Reaction': {
            'Reagent': [
                '[C](=[O])[Cl]',
                '[S;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;H0:1](=[O;H0;+0:2])[Cl;H0;+0:3].[S;H1;+0:4]>>[C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[S;H1;+1:4]',
                        '[C;H0:1](=[O;H0;+0:2])[Cl;H0;+0:3].[S;H2;+0:4]>>[C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[S;H2;+1:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition of the thiol to the acyl chloride carbonyl',
                },
                1: {
                    'Templates': [
                        '[C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[S;H1;+1:4]>>[C;H0:1](=[O;H0;+0:2])[S;H1;+1:4].[Cl;H0;-1:3]',
                        '[C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[S;H2;+1:4]>>[C;H0:1](=[O;H0;+0:2])[S;H2;+1:4].[Cl;H0;-1:3]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Tetrahedral intermediate collapse, expelling chloride',
                },
                2: {
                    'Templates': [
                        '[C;H0:1](=[O;H0;+0:2])[S;H1;+1:4].[Cl;H0;-1:3]>>[C;H0:1](=[O;H0;+0:2])[S;H0;+0:4].[Cl;H1;+0:3]',
                        '[C;H0:1](=[O;H0;+0:2])[S;H2;+1:4].[Cl;H0;-1:3]>>[C;H0:1](=[O;H0;+0:2])[S;H1;+0:4].[Cl;H1;+0:3]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the sulfonium to chloride',
                },
            },
        },
    },
    ('Aromatic carboxylic acid amidation',): {
        'Reaction': {
            'Reagent': [
                '[c][C](=[O])[O;H1]',
                '[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:1][C;H0:2](=[O;H0;+0:3])[O;H1;+0:4].[N;H2;+0:5]>>[c:1][C;H0:2]([O;H0;-1:3])([O;H1;+0:4])[N;H2;+1:5]',
                        '[c:1][C;H0:2](=[O;H0;+0:3])[O;H1;+0:4].[N;H1;+0:5]>>[c:1][C;H0:2]([O;H0;-1:3])([O;H1;+0:4])[N;H1;+1:5]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition of the amine to the aromatic acid carbonyl',
                },
                1: {
                    'Templates': [
                        '[c:1][C;H0:2]([O;H0;-1:3])([O;H1;+0:4])[N;H2;+1:5]>>[c:1][C;H0:2]([O;H0;-1:3])([O;H2;+1:4])[N;H1;+0:5]',
                        '[c:1][C;H0:2]([O;H0;-1:3])([O;H1;+0:4])[N;H1;+1:5]>>[c:1][C;H0:2]([O;H0;-1:3])([O;H2;+1:4])[N;H0;+0:5]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer converting the hydroxyl into a water leaving group',
                },
                2: {
                    'Templates': [
                        '[c:1][C;H0:2]([O;H0;-1:3])([O;H2;+1:4])[N;H1;+0:5]>>[c:1][C;H0:2](=[O;H0;+0:3])[N;H1;+0:5].[O;H2;+0:4]',
                        '[c:1][C;H0:2]([O;H0;-1:3])([O;H2;+1:4])[N;H0;+0:5]>>[c:1][C;H0:2](=[O;H0;+0:3])[N;H0;+0:5].[O;H2;+0:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Collapse expelling water and re-forming the carbonyl',
                },
            },
        },
    },
    ('Aromatic acyl chloride + thiol thioesterification',): {
        'Reaction': {
            'Reagent': [
                '[c][C](=[O])[Cl]',
                '[S;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:5][C;H0:1](=[O;H0;+0:2])[Cl;H0;+0:3].[S;H1;+0:4]>>[c:5][C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[S;H1;+1:4]',
                        '[c:5][C;H0:1](=[O;H0;+0:2])[Cl;H0;+0:3].[S;H2;+0:4]>>[c:5][C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[S;H2;+1:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition of the thiol to the aromatic acyl chloride carbonyl',
                },
                1: {
                    'Templates': [
                        '[c:5][C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[S;H1;+1:4]>>[c:5][C;H0:1](=[O;H0;+0:2])[S;H1;+1:4].[Cl;H0;-1:3]',
                        '[c:5][C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[S;H2;+1:4]>>[c:5][C;H0:1](=[O;H0;+0:2])[S;H2;+1:4].[Cl;H0;-1:3]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Tetrahedral intermediate collapse, expelling chloride',
                },
                2: {
                    'Templates': [
                        '[c:5][C;H0:1](=[O;H0;+0:2])[S;H1;+1:4].[Cl;H0;-1:3]>>[c:5][C;H0:1](=[O;H0;+0:2])[S;H0;+0:4].[Cl;H1;+0:3]',
                        '[c:5][C;H0:1](=[O;H0;+0:2])[S;H2;+1:4].[Cl;H0;-1:3]>>[c:5][C;H0:1](=[O;H0;+0:2])[S;H1;+0:4].[Cl;H1;+0:3]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the sulfonium to chloride',
                },
            },
        },
    },
    ('Aliphatic carboxylic acid amidation',): {
        'Reaction': {
            'Reagent': [
                '[C][C](=[O])[O;H1]',
                '[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C;H0:2](=[O;H0;+0:3])[O;H1;+0:4].[N;H2;+0:5]>>[C:1][C;H0:2]([O;H0;-1:3])([O;H1;+0:4])[N;H2;+1:5]',
                        '[C:1][C;H0:2](=[O;H0;+0:3])[O;H1;+0:4].[N;H1;+0:5]>>[C:1][C;H0:2]([O;H0;-1:3])([O;H1;+0:4])[N;H1;+1:5]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition of the amine to the carboxylic acid carbonyl',
                },
                1: {
                    'Templates': [
                        '[C:1][C;H0:2]([O;H0;-1:3])([O;H1;+0:4])[N;H2;+1:5]>>[C:1][C;H0:2]([O;H0;-1:3])([O;H2;+1:4])[N;H1;+0:5]',
                        '[C:1][C;H0:2]([O;H0;-1:3])([O;H1;+0:4])[N;H1;+1:5]>>[C:1][C;H0:2]([O;H0;-1:3])([O;H2;+1:4])[N;H0;+0:5]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer converting the hydroxyl into a water leaving group',
                },
                2: {
                    'Templates': [
                        '[C:1][C;H0:2]([O;H0;-1:3])([O;H2;+1:4])[N;H1;+0:5]>>[C:1][C;H0:2](=[O;H0;+0:3])[N;H1;+0:5].[O;H2;+0:4]',
                        '[C:1][C;H0:2]([O;H0;-1:3])([O;H2;+1:4])[N;H0;+0:5]>>[C:1][C;H0:2](=[O;H0;+0:3])[N;H0;+0:5].[O;H2;+0:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Collapse expelling water and re-forming the carbonyl',
                },
            },
        },
    },
    ('Acyl chloride + amide imide formation',): {
        'Reaction': {
            'Reagent': [
                '[C](=[O])[Cl]',
                '[N;!H0][C]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;H0:1](=[O;H0;+0:2])[Cl;H0;+0:3].[N;H2;+0:4][C;H0:5]=[O;H0;+0:6]>>[C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[N;H2;+1:4][C;H0:5]=[O;H0;+0:6]',
                        '[C;H0:1](=[O;H0;+0:2])[Cl;H0;+0:3].[N;H1;+0:4][C;H0:5]=[O;H0;+0:6]>>[C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[N;H1;+1:4][C;H0:5]=[O;H0;+0:6]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition of the amide nitrogen to the acyl chloride carbonyl',
                },
                1: {
                    'Templates': [
                        '[C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[N;H2;+1:4][C;H0:5]=[O;H0;+0:6]>>[C;H0:1](=[O;H0;+0:2])[N;H2;+1:4][C;H0:5]=[O;H0;+0:6].[Cl;H0;-1:3]',
                        '[C;H0:1]([O;H0;-1:2])([Cl;H0;+0:3])[N;H1;+1:4][C;H0:5]=[O;H0;+0:6]>>[C;H0:1](=[O;H0;+0:2])[N;H1;+1:4][C;H0:5]=[O;H0;+0:6].[Cl;H0;-1:3]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Tetrahedral intermediate collapse, expelling chloride',
                },
                2: {
                    'Templates': [
                        '[C;H0:1](=[O;H0;+0:2])[N;H2;+1:4][C;H0:5]=[O;H0;+0:6].[Cl;H0;-1:3]>>[C;H0:1](=[O;H0;+0:2])[N;H1;+0:4][C;H0:5]=[O;H0;+0:6].[Cl;H1;+0:3]',
                        '[C;H0:1](=[O;H0;+0:2])[N;H1;+1:4][C;H0:5]=[O;H0;+0:6].[Cl;H0;-1:3]>>[C;H0:1](=[O;H0;+0:2])[N;H0;+0:4][C;H0:5]=[O;H0;+0:6].[Cl;H1;+0:3]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the ammonium nitrogen to chloride',
                },
            },
        },
    },
    ('Acyl bromide amidation',): {
        'Reaction': {
            'Reagent': [
                '[C](=[O])[Br]',
                '[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;H0:1](=[O;H0;+0:2])[Br;H0;+0:3].[N;H2;+0:4]>>[C;H0:1]([O;H0;-1:2])([Br;H0;+0:3])[N;H2;+1:4]',
                        '[C;H0:1](=[O;H0;+0:2])[Br;H0;+0:3].[N;H1;+0:4]>>[C;H0:1]([O;H0;-1:2])([Br;H0;+0:3])[N;H1;+1:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition of the amine to the acyl bromide carbonyl',
                },
                1: {
                    'Templates': [
                        '[C;H0:1]([O;H0;-1:2])([Br;H0;+0:3])[N;H2;+1:4]>>[C;H0:1](=[O;H0;+0:2])[N;H2;+1:4].[Br;H0;-1:3]',
                        '[C;H0:1]([O;H0;-1:2])([Br;H0;+0:3])[N;H1;+1:4]>>[C;H0:1](=[O;H0;+0:2])[N;H1;+1:4].[Br;H0;-1:3]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Tetrahedral intermediate collapse, expelling bromide',
                },
                2: {
                    'Templates': [
                        '[C;H0:1](=[O;H0;+0:2])[N;H2;+1:4].[Br;H0;-1:3]>>[C;H0:1](=[O;H0;+0:2])[N;H1;+0:4].[Br;H1;+0:3]',
                        '[C;H0:1](=[O;H0;+0:2])[N;H1;+1:4].[Br;H0;-1:3]>>[C;H0:1](=[O;H0;+0:2])[N;H0;+0:4].[Br;H1;+0:3]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the ammonium nitrogen to bromide',
                },
            },
        },
    },
    ('Ammonia + aryl chloroformate carbamoylation',): {
        'Reaction': {
            'Reagent': [
                '[N;H3]',
                '[Cl][C](=[O])[O][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[N;H3;+0:1].[Cl;H0;+0:2][C;H0:3](=[O;H0;+0:4])[O;H0;+0:5][c:6]>>[N;H3;+1:1][C;H0:3]([O;H0;-1:4])([Cl;H0;+0:2])[O;H0;+0:5][c:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of ammonia to the chloroformate carbonyl',
                },
                1: {
                    'Templates': [
                        '[N;H3;+1:1][C;H0:3]([O;H0;-1:4])([Cl;H0;+0:2])[O;H0;+0:5][c:6]>>[N;H3;+1:1][C;H0:3](=[O;H0;+0:4])[O;H0;+0:5][c:6].[Cl;H0;-1:2]',
                    ],
                    'pKa': [None],
                    'Description': 'Tetrahedral intermediate collapse, expelling chloride',
                },
                2: {
                    'Templates': [
                        '[N;H3;+1:1][C;H0:3](=[O;H0;+0:4])[O;H0;+0:5][c:6].[Cl;H0;-1:2]>>[N;H2;+0:1][C;H0:3](=[O;H0;+0:4])[O;H0;+0:5][c:6].[Cl;H1;+0:2]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the ammonium nitrogen to chloride',
                },
            },
        },
    },
    ('Acyl chloride + HF halide exchange to acyl fluoride',): {
        'Reaction': {
            'Reagent': [
                '[C](=[O])[Cl]',
                '[F;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C;H0:2](=[O;H0;+0:3])[Cl;H0;+0:4].[F;H1;+0:5]>>[C:1][C;H0:2]([O;H0;-1:3])([Cl;H0;+0:4])[F;H1;+1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of HF to the acyl chloride carbonyl',
                },
                1: {
                    'Templates': [
                        '[C:1][C;H0:2]([O;H0;-1:3])([Cl;H0;+0:4])[F;H1;+1:5]>>[C:1][C;H0:2](=[O;H0;+0:3])[F;H1;+1:5].[Cl;H0;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Tetrahedral intermediate collapse, expelling chloride',
                },
                2: {
                    'Templates': [
                        '[C:1][C;H0:2](=[O;H0;+0:3])[F;H1;+1:5].[Cl;H0;-1:4]>>[C:1][C;H0:2](=[O;H0;+0:3])[F;H0;+0:5].[Cl;H1;+0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the fluoronium to chloride',
                },
            },
        },
    },
    ('Alkene + acyl chloride Friedel-Crafts vinylogous acylation',): {
        'Reaction': {
            'Reagent': [
                '[C](=[O])[Cl]',
                '[C]=[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C:2]([C:3])=[C;H1:4][C:5].[Cl;H0;+0:6][C;H0:7](=[O;H0;+0:8])[C:9]>>[C:1][C;+1:2]([C:3])[C;H1:4]([C:5])[C;H0:7]([O;H0;-1:8])([Cl;H0;+0:6])[C:9]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the alkene to the acyl chloride carbonyl, forming an allylic cation',
                },
                1: {
                    'Templates': [
                        '[C:1][C;+1:2]([C:3])[C;H1:4]([C:5])[C;H0:7]([O;H0;-1:8])([Cl;H0;+0:6])[C:9]>>[C:1][C;+1:2]([C:3])[C;H1:4]([C:5])[C;H0:7](=[O;H0;+0:8])[C:9].[Cl;H0;-1:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Tetrahedral intermediate collapse, expelling chloride',
                },
                2: {
                    'Templates': [
                        '[C:1][C;+1:2]([C:3])[C;H1:4]([C:5])[C;H0:7](=[O;H0;+0:8])[C:9].[Cl;H0;-1:6]>>[C:1][C;H0;+0:2]([C:3])=[13C;H0:4]([C:5])[C;H0:7](=[O;H0;+0:8])[C:9].[Cl;H1;+0:6]',
                    ],
                    'pKa': [None],
                    'Description': 'E1 elimination of the vinylic proton by chloride, restoring the alkene as an enone',
                },
            },
        },
    },
    ('Diazoketone + HCl to alpha-chloroketone',): {
        'Reaction': {
            'Reagent': [
                '[C]=[N+]=[N-]',
                '[Cl;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C:2](=[O;H0;+0:3])[C;H1:4]=[N;+1:5]=[N;-1:6].[Cl;H1;+0:7]>>[C:1][C:2](=[O;H0;+0:3])[C;H2:4][N;+1:5]#[N;+0:6].[Cl;H0;-1:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the diazo carbon by HCl, forming an alkyldiazonium ion',
                },
                1: {
                    'Templates': [
                        '[C:1][C:2](=[O;H0;+0:3])[C;H2:4][N;+1:5]#[N;+0:6].[Cl;H0;-1:7]>>[C:1][C:2](=[O;H0;+0:3])[C;H2:4][Cl;H0;+0:7].[N;+0:5]#[N;+0:6]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 displacement of nitrogen gas by chloride',
                },
            },
        },
    },
    ('Diazoketone + HBr to alpha-bromoketone',): {
        'Reaction': {
            'Reagent': [
                '[C]=[N+]=[N-]',
                '[Br;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C:2](=[O;H0;+0:3])[C;H1:4]=[N;+1:5]=[N;-1:6].[Br;H1;+0:7]>>[C:1][C:2](=[O;H0;+0:3])[C;H2:4][N;+1:5]#[N;+0:6].[Br;H0;-1:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the diazo carbon by HBr, forming an alkyldiazonium ion',
                },
                1: {
                    'Templates': [
                        '[C:1][C:2](=[O;H0;+0:3])[C;H2:4][N;+1:5]#[N;+0:6].[Br;H0;-1:7]>>[C:1][C:2](=[O;H0;+0:3])[C;H2:4][Br;H0;+0:7].[N;+0:5]#[N;+0:6]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 displacement of nitrogen gas by bromide',
                },
            },
        },
    },
    ('Ketone-enol tautomerization',): {
        'Reaction': {
            'Reagent': None,
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][C:2]=[O;H0;+0:3]>>[C:1]=[C:2][O;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': '1,3-prototropic shift from the alpha carbon to the carbonyl oxygen',
                },
            },
        },
    },
    ('Enol bromination to alpha-bromoketone',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C][O;H1]',
                '[Br][Br]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2][O;H1;+0:3].[Br;H0;+0:4][Br;H0;+0:5]>>[C:1]([Br;H0;+0:4])[C:2]=[O;H1;+1:3].[Br;H0;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of the enol to bromine, forming an oxocarbenium',
                },
                1: {
                    'Templates': [
                        '[C:1]([Br;H0;+0:4])[C:2]=[O;H1;+1:3].[Br;H0;-1:5]>>[C:1]([Br;H0;+0:4])[C:2]=[O;H0;+0:3].[Br;H1;+0:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Deprotonation of the oxocarbenium by bromide',
                },
            },
        },
    },
    ('Aryl ketone-enol tautomerization',): {
        'Reaction': {
            'Reagent': None,
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][C:2]([c:4])=[O;H0;+0:3]>>[C:1]=[C:2]([c:4])[O;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': '1,3-prototropic shift from the alpha carbon to the carbonyl oxygen',
                },
            },
        },
    },
    ('Aryl enol bromination to alpha-bromo aryl ketone',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]([c])[O;H1]',
                '[Br][Br]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2]([c:4])[O;H1;+0:3].[Br;H0;+0:10][Br;H0;+0:11]>>[C:1]([Br;H0;+0:10])[C:2]([c:4])=[O;H1;+1:3].[Br;H0;-1:11]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of the enol to bromine, forming an oxocarbenium',
                },
                1: {
                    'Templates': [
                        '[C:1]([Br;H0;+0:10])[C:2]([c:4])=[O;H1;+1:3].[Br;H0;-1:11]>>[C:1]([Br;H0;+0:10])[C:2]([c:4])=[O;H0;+0:3].[Br;H1;+0:11]',
                    ],
                    'pKa': [None],
                    'Description': 'Deprotonation of the oxocarbenium by bromide',
                },
            },
        },
    },
    ('Ester/acid-enol tautomerization',): {
        'Reaction': {
            'Reagent': None,
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][C:2]([O:4])=[O;H0;+0:3]>>[C:1]=[C:2]([O:4])[O;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': '1,3-prototropic shift from the alpha carbon to the carbonyl oxygen',
                },
            },
        },
    },
    ('Ester/acid enol bromination to alpha-bromo ester/acid',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]([O])[O;H1]',
                '[Br][Br]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2]([O:4])[O;H1;+0:3].[Br;H0;+0:5][Br;H0;+0:6]>>[C:1]([Br;H0;+0:5])[C:2]([O:4])=[O;H1;+1:3].[Br;H0;-1:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of the enol to bromine, forming an oxocarbenium',
                },
                1: {
                    'Templates': [
                        '[C:1]([Br;H0;+0:5])[C:2]([O:4])=[O;H1;+1:3].[Br;H0;-1:6]>>[C:1]([Br;H0;+0:5])[C:2]([O:4])=[O;H0;+0:3].[Br;H1;+0:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Deprotonation of the oxocarbenium by bromide',
                },
            },
        },
    },
    ('Alpha-bromo ester/acid-enol tautomerization',): {
        'Reaction': {
            'Reagent': None,
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1]([Br;H0;+0:5])[C:2]([O:4])=[O;H0;+0:3]>>[C:1]([Br;H0;+0:5])=[C:2]([O:4])[O;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': '1,3-prototropic shift from the alpha carbon to the carbonyl oxygen',
                },
            },
        },
    },
    ('Alpha-bromo enol bromination to alpha,alpha-dibromo ester/acid',): {
        'Reaction': {
            'Reagent': [
                '[C]([Br])=[C]([O])[O;H1]',
                '[Br][Br]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]([Br;H0;+0:5])=[C:2]([O:4])[O;H1;+0:3].[Br;H0;+0:6][Br;H0;+0:7]>>[C:1]([Br;H0;+0:5])([Br;H0;+0:6])[C:2]([O:4])=[O;H1;+1:3].[Br;H0;-1:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of the enol to a second equivalent of bromine, forming an oxocarbenium',
                },
                1: {
                    'Templates': [
                        '[C:1]([Br;H0;+0:5])([Br;H0;+0:6])[C:2]([O:4])=[O;H1;+1:3].[Br;H0;-1:7]>>[C:1]([Br;H0;+0:5])([Br;H0;+0:6])[C:2]([O:4])=[O;H0;+0:3].[Br;H1;+0:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Deprotonation of the oxocarbenium by bromide',
                },
            },
        },
    },
    ('Triarylethylene + acyl chloride Friedel-Crafts vinylogous acylation',): {
        'Reaction': {
            'Reagent': [
                '[C](=[O])[Cl]',
                '[c]C=C[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:7][C:1]([c:13])=[C;H1:2][c:19].[Cl;H0;+0:3][C;H0:4](=[O;H0;+0:5])[C:6]>>[c:7][C;+1:1]([c:13])[C;H1:2]([c:19])[C;H0:4]([O;H0;-1:5])([Cl;H0;+0:3])[C:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the alkene to the acyl chloride carbonyl, forming a doubly benzylic cation',
                },
                1: {
                    'Templates': [
                        '[c:7][C;+1:1]([c:13])[C;H1:2]([c:19])[C;H0:4]([O;H0;-1:5])([Cl;H0;+0:3])[C:6]>>[c:7][C;+1:1]([c:13])[C;H1:2]([c:19])[C;H0:4](=[O;H0;+0:5])[C:6].[Cl;H0;-1:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Tetrahedral intermediate collapse, expelling chloride',
                },
                2: {
                    'Templates': [
                        '[c:7][C;+1:1]([c:13])[C;H1:2]([c:19])[C;H0:4](=[O;H0;+0:5])[C:6].[Cl;H0;-1:3]>>[c:7][C;H0;+0:1]([c:13])=[13C;H0:2]([c:19])[C;H0:4](=[O;H0;+0:5])[C:6].[Cl;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'E1 elimination of the vinylic proton by chloride, restoring the alkene as an enone',
                },
            },
        },
    },
    ('Ester alpha-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[C][C](=[O])[O][C]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][C:2]([O;H0;+0:4][C:8])=[O;H0;+0:3]>>[C:1]=[C:2]([O;H0;+0:4][C:8])[O;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Enolization of the ester alpha carbon',
                },
                1: {
                    'Templates': [
                        '[C:1]=[C:2]([O;H0;+0:4][C:8])[O;H1;+0:3].[O;H1;+0:5][N;H0;+0:6]=[O;H0;+0:7]>>[C:1]([N;H0;+0:6]=[O;H0;+0:7])[C:2]([O;H0;+0:4][C:8])=[O;H1;+1:3].[O;H1;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack of the enol on the nitrous acid nitrogen, breaking the N-OH bond',
                },
                2: {
                    'Templates': [
                        '[C:1]([N;H0;+0:6]=[O;H0;+0:7])[C:2]([O;H0;+0:4][C:8])=[O;H1;+1:3].[O;H1;-1:5]>>[C:1]([N;H0;+0:6]=[O;H0;+0:7])[C:2]([O;H0;+0:4][C:8])=[O;H0;+0:3].[O;H2;+0:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxocarbenium to hydroxide, giving water',
                },
            },
        },
    },
    ('Aldehyde/ketone alpha-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][C]=[O]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][C:2]=[O;H0;+0:3]>>[C:1]=[C:2][O;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Enolization of the alpha carbon',
                },
                1: {
                    'Templates': [
                        '[C:1]=[C:2][O;H1;+0:3].[O;H1;+0:4][N;H0;+0:5]=[O;H0;+0:6]>>[C:1]([N;H0;+0:5]=[O;H0;+0:6])[C:2]=[O;H1;+1:3].[O;H1;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack of the enol on the nitrous acid nitrogen, breaking the N-OH bond',
                },
                2: {
                    'Templates': [
                        '[C:1]([N;H0;+0:5]=[O;H0;+0:6])[C:2]=[O;H1;+1:3].[O;H1;-1:4]>>[C:1]([N;H0;+0:5]=[O;H0;+0:6])[13C:2]=[17O;H0;+0:3].[O;H2;+0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxocarbenium to hydroxide, giving water',
                },
            },
        },
    },
    ('Amide alpha-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][C](=[O])[N]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][C:2](=[O;H0;+0:3])[N;H0;+0:4]([C:8])[C:9]>>[C:1]=[C:2]([N;H0;+0:4]([C:8])[C:9])[O;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Enolization of the amide alpha carbon',
                },
                1: {
                    'Templates': [
                        '[C:1]=[C:2]([N;H0;+0:4]([C:8])[C:9])[O;H1;+0:3].[O;H1;+0:5][N;H0;+0:6]=[O;H0;+0:7]>>[C:1]([N;H0;+0:6]=[O;H0;+0:7])[C:2]([N;H0;+0:4]([C:8])[C:9])=[O;H1;+1:3].[O;H1;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack of the enol on the nitrous acid nitrogen, breaking the N-OH bond',
                },
                2: {
                    'Templates': [
                        '[C:1]([N;H0;+0:6]=[O;H0;+0:7])[C:2]([N;H0;+0:4]([C:8])[C:9])=[O;H1;+1:3].[O;H1;-1:5]>>[C:1]([N;H0;+0:6]=[O;H0;+0:7])[C:2]([N;H0;+0:4]([C:8])[C:9])=[O;H0;+0:3].[O;H2;+0:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxocarbenium to hydroxide, giving water',
                },
            },
        },
    },
    ('Aryl ester alpha-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[C][C](=[O])[O][c]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][C:2]([O;H0;+0:4][c:8])=[O;H0;+0:3]>>[C:1]=[C:2]([O;H0;+0:4][c:8])[O;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Enolization of the ester alpha carbon',
                },
                1: {
                    'Templates': [
                        '[C:1]=[C:2]([O;H0;+0:4][c:8])[O;H1;+0:3].[O;H1;+0:5][N;H0;+0:6]=[O;H0;+0:7]>>[C:1]([N;H0;+0:6]=[O;H0;+0:7])[C:2]([O;H0;+0:4][c:8])=[O;H1;+1:3].[O;H1;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack of the enol on the nitrous acid nitrogen, breaking the N-OH bond',
                },
                2: {
                    'Templates': [
                        '[C:1]([N;H0;+0:6]=[O;H0;+0:7])[C:2]([O;H0;+0:4][c:8])=[O;H1;+1:3].[O;H1;-1:5]>>[C:1]([N;H0;+0:6]=[O;H0;+0:7])[C:2]([O;H0;+0:4][c:8])=[O;H0;+0:3].[O;H2;+0:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxocarbenium to hydroxide, giving water',
                },
            },
        },
    },
    ('Aryl ketone alpha-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][C](=[O])[c]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][C:2](=[O;H0;+0:3])[c:7]>>[C:1]=[C:2]([c:7])[O;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Enolization of the aryl ketone alpha carbon',
                },
                1: {
                    'Templates': [
                        '[C:1]=[C:2]([c:7])[O;H1;+0:3].[O;H1;+0:4][N;H0;+0:5]=[O;H0;+0:6]>>[C:1]([N;H0;+0:5]=[O;H0;+0:6])[C:2]([c:7])=[O;H1;+1:3].[O;H1;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack of the enol on the nitrous acid nitrogen, breaking the N-OH bond',
                },
                2: {
                    'Templates': [
                        '[C:1]([N;H0;+0:5]=[O;H0;+0:6])[C:2]([c:7])=[O;H1;+1:3].[O;H1;-1:4]>>[C:1]([N;H0;+0:5]=[O;H0;+0:6])[C:2]([c:7])=[O;H0;+0:3].[O;H2;+0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxocarbenium to hydroxide, giving water',
                },
            },
        },
    },
    ('Diarylamide alpha-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][C](=[O])[N]([c])[c]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][C:2](=[O;H0;+0:3])[N;H0;+0:4]([c:8])[c:14]>>[C:1]=[C:2]([N;H0;+0:4]([c:8])[c:14])[O;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Enolization of the diarylamide alpha carbon',
                },
                1: {
                    'Templates': [
                        '[C:1]=[C:2]([N;H0;+0:4]([c:8])[c:14])[O;H1;+0:3].[O;H1;+0:5][N;H0;+0:6]=[O;H0;+0:7]>>[C:1]([N;H0;+0:6]=[O;H0;+0:7])[C:2]([N;H0;+0:4]([c:8])[c:14])=[O;H1;+1:3].[O;H1;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack of the enol on the nitrous acid nitrogen, breaking the N-OH bond',
                },
                2: {
                    'Templates': [
                        '[C:1]([N;H0;+0:6]=[O;H0;+0:7])[C:2]([N;H0;+0:4]([c:8])[c:14])=[O;H1;+1:3].[O;H1;-1:5]>>[C:1]([N;H0;+0:6]=[O;H0;+0:7])[C:2]([N;H0;+0:4]([c:8])[c:14])=[O;H0;+0:3].[O;H2;+0:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxocarbenium to hydroxide, giving water',
                },
            },
        },
    },
    ('Secondary amine + aryl chloride SNAr amination',): {
        'Reaction': {
            'Reagent': [
                '[N;H1]([C])[C]',
                '[Cl][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][N;H1;+0:2][C:3].[Cl;H0;+0:10][c:4]1[c:5][c:6][c:7][c:8][c:9]1>>[C:1][N;H1;+1:2]([C:3])[C;H0:4]1([Cl;H0;+0:10])[CH1:5]=[CH1:6][CH1:7]=[CH1:8][CH1;-1:9]1',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the amine to the ipso carbon, forming a Meisenheimer complex',
                },
                1: {
                    'Templates': [
                        '[C:1][N;H1;+1:2]([C:3])[C;H0:4]1([Cl;H0;+0:10])[CH1:5]=[CH1:6][CH1:7]=[CH1:8][CH1;-1:9]1>>[C:1][N;H1;+1:2]([C:3])[c:4]1[c:5][c:6][c:7][c:8][c;H1;+0:9]1.[Cl;H0;-1:10]',
                    ],
                    'pKa': [None],
                    'Description': 'Rearomatization, expelling chloride',
                },
                2: {
                    'Templates': [
                        '[C:1][N;H1;+1:2]([C:3])[c:4]1[c:5][c:6][c:7][c:8][c:9]1.[Cl;H0;-1:10]>>[C:1][N;H0;+0:2]([C:3])[c:4]1[c:5][c:6][c:7][c:8][c:9]1.[Cl;H1;+0:10]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the ammonium nitrogen to chloride',
                },
            },
        },
    },
    ('Phenol + HNO3 ipso O-exchange (aryl-oxygen fission)',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][N+](=[O])[O-]',
                '[O;H1][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1;+0:1][N;+1;H0:2](=[O;H0;+0:3])[O;H0;-1:4].[O;H1;+0:5][c:6]>>[O;H1;+1:1]([N;+1;H0:2](=[O;H0;+0:3])[O;H0;-1:4])[c:6].[O;H1;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2-like attack of the nitrate oxygen on the ipso ring carbon, expelling the phenolic oxygen',
                },
                1: {
                    'Templates': [
                        '[O;H1;+1:1]([N;+1;H0:2](=[O;H0;+0:3])[O;H0;-1:4])[c:6].[O;H1;-1:5]>>[O;H0;+0:1]([N;+1;H0:2](=[O;H0;+0:3])[O;H0;-1:4])[c:6].[O;H2;+0:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxonium to the departed phenoxide, giving water',
                },
            },
        },
    },
    ('Phenol + HNO3 O-nitration at nitrogen',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][N+](=[O])[O-]',
                '[O;H1][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1;+0:1][N;+1;H0:2](=[O;H0;+0:3])[O;H0;-1:4].[O;H1;+0:5][c:6]>>[O;H1;-1:1].[c:6][O;H1;+1:5][N;+1;H0:2](=[O;H0;+0:3])[O;H0;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Substitution at nitrogen: the phenolic oxygen attacks, expelling one of nitric acid\'s own oxygens',
                },
                1: {
                    'Templates': [
                        '[O;H1;-1:1].[c:6][O;H1;+1:5][N;+1;H0:2](=[O;H0;+0:3])[O;H0;-1:4]>>[O;H2;+0:1].[c:6][O;H0;+0:5][N;+1;H0:2](=[O;H0;+0:3])[O;H0;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the phenolic oxonium to the departed hydroxide, giving water',
                },
            },
        },
    },
    ('Phenol + HNO2 ipso O-to-N exchange',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][N]=[O]',
                '[O;H1][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1;+0:8][N;H0;+0:9]=[O;H0;+0:10].[O;H1;+0:1][c:2]>>[O;H1;+0:8][N;+1;H0:9](=[O;H0;+0:10])[c:2].[O;H1;-1:1]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack of nitrous acid nitrogen on the ipso ring carbon, expelling the phenolic oxygen',
                },
                1: {
                    'Templates': [
                        '[O;H1;+0:8][N;+1;H0:9](=[O;H0;+0:10])[c:2].[O;H1;-1:1]>>[O;H0;+0:8]=[N;+1;H0:9]([O;H0;-1:10])[c:2].[O;H2;+0:1]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer/tautomeric shift giving the neutral nitro group and water',
                },
            },
        },
    },
    ('N,N-dialkylaniline para-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[N]([C])([C])[c]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][N;H0;+0:2]([C:3])[c:4]1[c:5][c:6][c;H1:7][c:8][c:9]1.[O;H1;+0:10][N;H0;+0:11]=[O;H0;+0:12]>>[C:1][N;+1;H0:2]([C:3])=[C;H0:4]1[CH1:5]=[CH1:6][CH1:7]([N;H0;+0:11]=[O;H0;+0:12])[CH1:8]=[CH1:9]1.[O;H1;-1:10]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of nitrous acid nitrogen at the para position, forming an iminium-stabilized Wheland intermediate',
                },
                1: {
                    'Templates': [
                        '[C:1][N;+1;H0:2]([C:3])=[C;H0:4]1[CH1:5]=[CH1:6][CH1:7]([N;H0;+0:11]=[O;H0;+0:12])[CH1:8]=[CH1:9]1.[O;H1;-1:10]>>[C:1][N;H0;+0:2]([C:3])[c:4]1[c:5][c:6][c:7]([N;H0;+0:11]=[O;H0;+0:12])[c:8][c:9]1.[O;H2;+0:10]',
                    ],
                    'pKa': [None],
                    'Description': 'Loss of the ring proton to hydroxide, rearomatizing the ring',
                },
            },
        },
    },
    ('Phenol para-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][c]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1;+0:1][c:2]1[c:3][c:4][c;H1:5][c:6][c:7]1.[O;H1;+0:8][N;H0;+0:9]=[O;H0;+0:10]>>[O;+1;H1:1]=[C;H0:2]1[CH1:3]=[CH1:4][CH1:5]([N;H0;+0:9]=[O;H0;+0:10])[CH1:6]=[CH1:7]1.[O;H1;-1:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of nitrous acid nitrogen at the para position, forming an oxocarbenium-stabilized Wheland intermediate',
                },
                1: {
                    'Templates': [
                        '[O;+1;H1:1]=[C;H0:2]1[CH1:3]=[CH1:4][CH1:5]([N;H0;+0:9]=[O;H0;+0:10])[CH1:6]=[CH1:7]1.[O;H1;-1:8]>>[O;H1;+0:1][c:2]1[c:3][c:4][c:5]([N;H0;+0:9]=[O;H0;+0:10])[c:6][c:7]1.[O;H2;+0:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Loss of the ring proton to hydroxide, rearomatizing the ring',
                },
            },
        },
    },
    ('Benzene chlorosulfonation',): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c][c][c]1',
                '[Cl][S](=[O])(=[O])[O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c;H1:1]1[c:2][c:3][c:4][c:5][c:6]1.[Cl;H0;+0:7][S;H0;+0:8](=[O;H0;+0:9])(=[O;H0;+0:10])[O;H1;+0:11]>>[C;H1:1]1([S;H0;+0:8](=[O;H0;+0:9])(=[O;H0;+0:10])[Cl;H0;+0:7])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1.[O;H1;-1:11]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of sulfur to the ring, forming a Wheland intermediate',
                },
                1: {
                    'Templates': [
                        '[C;H1:1]1([S;H0;+0:8](=[O;H0;+0:9])(=[O;H0;+0:10])[Cl;H0;+0:7])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1.[O;H1;-1:11]>>[c;H0;+0:1]1([S;H0;+0:8](=[O;H0;+0:9])(=[O;H0;+0:10])[Cl;H0;+0:7])[c:2][c:3][c:4][c:5][c;H1;+0:6]1.[O;H2;+0:11]',
                    ],
                    'pKa': [None],
                    'Description': 'Loss of the ring proton to hydroxide, rearomatizing the ring',
                },
            },
        },
    },
    ('Benzene bromosulfonation',): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c][c][c]1',
                '[Br][S](=[O])(=[O])[O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c;H1:1]1[c:2][c:3][c:4][c:5][c:6]1.[Br;H0;+0:7][S;H0;+0:8](=[O;H0;+0:9])(=[O;H0;+0:10])[O;H1;+0:11]>>[C;H1:1]1([S;H0;+0:8](=[O;H0;+0:9])(=[O;H0;+0:10])[Br;H0;+0:7])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1.[O;H1;-1:11]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of sulfur to the ring, forming a Wheland intermediate',
                },
                1: {
                    'Templates': [
                        '[C;H1:1]1([S;H0;+0:8](=[O;H0;+0:9])(=[O;H0;+0:10])[Br;H0;+0:7])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1.[O;H1;-1:11]>>[c;H0;+0:1]1([S;H0;+0:8](=[O;H0;+0:9])(=[O;H0;+0:10])[Br;H0;+0:7])[c:2][c:3][c:4][c:5][c;H1;+0:6]1.[O;H2;+0:11]',
                    ],
                    'pKa': [None],
                    'Description': 'Loss of the ring proton to hydroxide, rearomatizing the ring',
                },
            },
        },
    },
    ('Benzene bromination',): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c][c][c]1',
                '[Br][Br]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c;H1:1]1[c:2][c:3][c:4][c:5][c:6]1.[Br;H0;+0:7][Br;H0;+0:8]>>[C;H1:1]1([Br;H0;+0:7])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1.[Br;H0;-1:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of bromine to the ring, forming a Wheland intermediate',
                },
                1: {
                    'Templates': [
                        '[C;H1:1]1([Br;H0;+0:7])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1.[Br;H0;-1:8]>>[c;H0;+0:1]1([Br;H0;+0:7])[c:2][c:3][c:4][c:5][c;H1;+0:6]1.[Br;H1;+0:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Loss of the ring proton to bromide, rearomatizing the ring',
                },
            },
        },
    },
    ('Benzenesulfonic acid + benzene to diphenyl sulfone',): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c][c][c]1',
                '[c][S](=[O])(=[O])[O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c;H1:1]1[c:2][c:3][c:4][c:5][c:6]1.[c:12][S;H0;+0:13](=[O;H0;+0:14])(=[O;H0;+0:15])[O;H1;+0:16]>>[C;H1:1]1([S;H0;+0:13](=[O;H0;+0:14])(=[O;H0;+0:15])[c:12])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1.[O;H1;-1:16]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of sulfur to the ring, forming a Wheland intermediate',
                },
                1: {
                    'Templates': [
                        '[C;H1:1]1([S;H0;+0:13](=[O;H0;+0:14])(=[O;H0;+0:15])[c:12])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1.[O;H1;-1:16]>>[c;H0;+0:1]1([S;H0;+0:13](=[O;H0;+0:14])(=[O;H0;+0:15])[c:12])[c:2][c:3][c:4][c:5][c;H1;+0:6]1.[O;H2;+0:16]',
                    ],
                    'pKa': [None],
                    'Description': 'Loss of the ring proton to hydroxide, rearomatizing the ring',
                },
            },
        },
    },
    ('Benzene chlorination',): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c][c][c]1',
                '[Cl][Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c;H1:1]1[c:2][c:3][c:4][c:5][c:6]1.[Cl;H0;+0:7][Cl;H0;+0:8]>>[C;H1:1]1([Cl;H0;+0:7])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1.[Cl;H0;-1:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of chlorine to the ring, forming a Wheland intermediate',
                },
                1: {
                    'Templates': [
                        '[C;H1:1]1([Cl;H0;+0:7])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1.[Cl;H0;-1:8]>>[c;H0;+0:1]1([Cl;H0;+0:7])[c:2][c:3][c:4][c:5][c;H1;+0:6]1.[Cl;H1;+0:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Loss of the ring proton to chloride, rearomatizing the ring',
                },
            },
        },
    },
    ('Benzene nitration',): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c][c][c]1',
                '[O;H1][N+](=[O])[O-]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1;+0:1][N;+1;H0:2](=[O;H0;+0:3])[O;H0;-1:4].[c;H1:5]1[c:6][c:7][c:8][c:9][c:10]1>>[O;H1;-1:1].[C;H1:5]1([N;+1;H0:2](=[O;H0;+0:3])[O;H0;-1:4])[CH1:6]=[CH1:7][CH1:8]=[CH1:9][CH1;+1:10]1',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of the nitronium-like nitrogen to the ring, forming a Wheland intermediate',
                },
                1: {
                    'Templates': [
                        '[O;H1;-1:1].[C;H1:5]1([N;+1;H0:2](=[O;H0;+0:3])[O;H0;-1:4])[CH1:6]=[CH1:7][CH1:8]=[CH1:9][CH1;+1:10]1>>[O;H2;+0:1].[c;H0;+0:5]1([N;+1;H0:2](=[O;H0;+0:3])[O;H0;-1:4])[c:6][c:7][c:8][c:9][c;H1;+0:10]1',
                    ],
                    'pKa': [None],
                    'Description': 'Loss of the ring proton to hydroxide, rearomatizing the ring',
                },
            },
        },
    },
    ('Aromatic amide + benzene Vilsmeier-type formylation',): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c][c][c]1',
                '[N]([C])[C]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:1]1[c:2][c:3][c:4][c:5][c;H1:6]1.[c:12][N;H0;+0:13]([C:14])[C;H1:15]=[O;H0;+0:16]>>[C;H1:1]1([C;H1:15]([N;H0;+1:13]([C:14])[c:12])[O;H0;-1:16])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of the amide carbon to the ring, forming a Wheland intermediate',
                },
                1: {
                    'Templates': [
                        '[C;H1:1]1([C;H1:15]([N;H0;+1:13]([C:14])[c:12])[O;H0;-1:16])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1>>[C;H1:1]1([C;H1:15]=[O;H0;+0:16])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1.[N;H0;-1:13]([C:14])[c:12]',
                    ],
                    'pKa': [None],
                    'Description': 'Collapse expelling the arylamine as an amide anion',
                },
                2: {
                    'Templates': [
                        '[C;H1:1]1([C;H1:15]=[O;H0;+0:16])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1.[N;H0;-1:13]([C:14])[c:12]>>[c;H0;+0:1]1([C;H1:15]=[O;H0;+0:16])[c:2][c:3][c:4][c:5][c;H1;+0:6]1.[N;H1;+0:13]([C:14])[c:12]',
                    ],
                    'pKa': [None],
                    'Description': 'Loss of the ring proton to the amide anion, rearomatizing the ring and giving the arylamine',
                },
            },
        },
    },
    ('Benzylic alcohol + benzene Friedel-Crafts alkylation',): {
        'Reaction': {
            'Reagent': [
                '[c][C][O;H1]',
                '[c]1[c][c][c][c][c]1',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:6][C:7][O;H1;+0:8]>>[c:6][C;+1:7].[O;H1;-1:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Ionization of the benzylic C-O bond, forming a benzylic cation',
                },
                1: {
                    'Templates': [
                        '[c:6][C;+1:7].[c;H1:9]2[c:10][c:11][c:12][c:13][c:14]2>>[c:6][C;+0:7][C;H1:9]2[CH1:10]=[CH1:11][CH1:12]=[CH1:13][CH1;+1:14]2',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of the second ring to the benzylic cation, forming a Wheland intermediate',
                },
                2: {
                    'Templates': [
                        '[c:6][C;+0:7][C;H1:9]2[CH1:10]=[CH1:11][CH1:12]=[CH1:13][CH1;+1:14]2.[O;H1;-1:8]>>[c:6][C:7][c;H0;+0:9]2[c:10][c:11][c:12][c:13][c;H1;+0:14]2.[O;H2;+0:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Loss of the ring proton to hydroxide, rearomatizing the ring and giving water',
                },
            },
        },
    },
    ('Alpha-naphthol + amine ipso Bucherer-type amination',): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c]2[c]([c]1)[c][c][c][c]2[O;H1]',
                '[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:1]1[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2[O;H1;+0:11].[N;H2;+0:12]>>[c:1]1[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2[N;H2;+1:12].[O;H1;-1:11]',
                        '[c:1]1[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2[O;H1;+0:11].[N;H1;+0:12]>>[c:1]1[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2[N;H1;+1:12].[O;H1;-1:11]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Ipso substitution: the amine attacks the ring carbon, displacing the naphtholic oxygen',
                },
                1: {
                    'Templates': [
                        '[c:1]1[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2[N;H2;+1:12].[O;H1;-1:11]>>[c:1]1[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2[N;H1;+0:12].[O;H2;+0:11]',
                        '[c:1]1[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2[N;H1;+1:12].[O;H1;-1:11]>>[c:1]1[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2[N;H0;+0:12].[O;H2;+0:11]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the ammonium to the departed hydroxide, giving water',
                },
            },
        },
    },
    ('Beta-naphthol + amine ipso Bucherer-type amination',): {
        'Reaction': {
            'Reagent': [
                '[c]1([O;H1])[c][c][c]2[c]([c]1)[c][c][c][c]2',
                '[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:1]1([O;H1;+0:11])[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2.[N;H2;+0:12]>>[c:1]1([N;H2;+1:12])[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2.[O;H1;-1:11]',
                        '[c:1]1([O;H1;+0:11])[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2.[N;H1;+0:12]>>[c:1]1([N;H1;+1:12])[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2.[O;H1;-1:11]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Ipso substitution: the amine attacks the ring carbon, displacing the naphtholic oxygen',
                },
                1: {
                    'Templates': [
                        '[c:1]1([N;H2;+1:12])[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2.[O;H1;-1:11]>>[c:1]1([N;H1;+0:12])[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2.[O;H2;+0:11]',
                        '[c:1]1([N;H1;+1:12])[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2.[O;H1;-1:11]>>[c:1]1([N;H0;+0:12])[c:2][c:3][c:4]2[c:5]([c:6]1)[c:7][c:8][c:9][c:10]2.[O;H2;+0:11]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the ammonium to the departed hydroxide, giving water',
                },
            },
        },
    },
    ('Two alcohols to ether via alkyl-oxygen SN2',): {
        'Reaction': {
            'Reagent': [
                '[C][O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][O;H1;+0:2].[C:3][O;H1;+0:4]>>[C:1][O;H1;+1:2][C:3].[O;H1;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of one alcohol oxygen on the other alcohol carbon',
                },
                1: {
                    'Templates': [
                        '[C:1][O;H1;+1:2][C:3].[O;H1;-1:4]>>[C:1][O;H0;+0:2][C:3].[O;H2;+0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxonium to the departed hydroxide, giving water',
                },
            },
        },
    },
    ('Alcohol + HNO3 to alkyl nitrate',): {
        'Reaction': {
            'Reagent': [
                '[C][O;H1]',
                '[O;H1][N+](=[O])[O-]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][O;H1;+0:2].[O;H1;+0:3][N;+1;H0:4](=[O;H0;+0:5])[O;H0;-1:6]>>[O;H1;-1:3].[C:1][O;H1;+1:2][N;+1;H0:4](=[O;H0;+0:5])[O;H0;-1:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Substitution at nitrogen: the alcohol oxygen attacks, expelling one of nitric acid\'s own oxygens',
                },
                1: {
                    'Templates': [
                        '[O;H1;-1:3].[C:1][O;H1;+1:2][N;+1;H0:4](=[O;H0;+0:5])[O;H0;-1:6]>>[O;H2;+0:3].[C:1][O;H0;+0:2][N;+1;H0:4](=[O;H0;+0:5])[O;H0;-1:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxonium to the departed hydroxide, giving water',
                },
            },
        },
    },
    ('Alkyl chloride + oxime O-alkylation',): {
        'Reaction': {
            'Reagent': [
                '[C][Cl]',
                '[C]=[N][O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][Cl;H0;+0:2].[C:3]=[N:4][O;H1;+0:5]>>[C:1][O;H1;+1:5][N:4]=[C:3].[Cl;H0;-1:2]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of the oxime oxygen on the alkyl carbon',
                },
                1: {
                    'Templates': [
                        '[C:1][O;H1;+1:5][N:4]=[C:3].[Cl;H0;-1:2]>>[C:1][O;H0;+0:5][N:4]=[C:3].[Cl;H1;+0:2]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxonium to chloride',
                },
            },
        },
    },
    ('Alkyl chloride + benzophenone oxime O-alkylation',): {
        'Reaction': {
            'Reagent': [
                '[C][Cl]',
                '[c][C](=[N][O;H1])[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][Cl;H0;+0:2].[c:11][C:5]([c:12])=[N:4][O;H1;+0:3]>>[C:1][O;H1;+1:3][N:4]=[C:5]([c:11])[c:12].[Cl;H0;-1:2]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of the oxime oxygen on the alkyl carbon',
                },
                1: {
                    'Templates': [
                        '[C:1][O;H1;+1:3][N:4]=[C:5]([c:11])[c:12].[Cl;H0;-1:2]>>[C:1][O;H0;+0:3][N:4]=[C:5]([c:11])[c:12].[Cl;H1;+0:2]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxonium to chloride',
                },
            },
        },
    },
    ('Cyanohydrin + amine SN1 amination',): {
        'Reaction': {
            'Reagent': [
                '[C](O)(C)(C)C#N',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C:2]([O;H1;+0:4])([C:5]#[N:6])[C:3]>>[C:1][C;+1:2]([C:5]#[N:6])[C:3].[O;H1;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Ionization of the tertiary C-O bond, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C:1][C;+1:2]([C:5]#[N:6])[C:3].[N;H2;+0:7]>>[C:1][C;+0:2]([N;H2;+1:7])([C:5]#[N:6])[C:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the amine to the carbocation',
                },
                2: {
                    'Templates': [
                        '[C:1][C:2]([N;H2;+1:7])([C:5]#[N:6])[C:3].[O;H1;-1:4]>>[C:1][C:2]([15N;H1;+0:7])([C:5]#[N:6])[C:3].[17O;H2;+0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the ammonium to the departed hydroxide, giving water',
                },
            },
        },
    },
    ('Alcohol + HCl to alkyl chloride isotope-labeled',): {
        'Reaction': {
            'Reagent': [
                '[C][O;H1]',
                '[Cl;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][O;H1;+0:2].[Cl;H1;+0:3]>>[C:1][O;H2;+1:2].[Cl;H0;-1:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the alcohol oxygen by HCl',
                },
                1: {
                    'Templates': [
                        '[C:1][O;H2;+1:2].[Cl;H0;-1:3]>>[13C:1][36Cl;H0;+0:3].[O;H2;+0:2]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2/SN1 displacement of water by chloride',
                },
            },
        },
    },
    ('Alcohol + HBr to alkyl bromide isotope-labeled',): {
        'Reaction': {
            'Reagent': [
                '[C][O;H1]',
                '[Br;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][O;H1;+0:2].[Br;H1;+0:3]>>[C:1][O;H2;+1:2].[Br;H0;-1:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the alcohol oxygen by HBr',
                },
                1: {
                    'Templates': [
                        '[C:1][O;H2;+1:2].[Br;H0;-1:3]>>[13C:1][79Br;H0;+0:3].[O;H2;+0:2]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2/SN1 displacement of water by bromide',
                },
            },
        },
    },
    ('Nitrile alpha-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][C]#[N]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][C:2]#[N;H0;+0:3]>>[C:1]=[C:2]=[N;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Tautomerization of the nitrile to its ketenimine form',
                },
                1: {
                    'Templates': [
                        '[C:1]=[C:2]=[N;H1;+0:3].[O;H1;+0:4][N;H0;+0:5]=[O;H0;+0:6]>>[C:1]([N;H0;+0:5]=[O;H0;+0:6])[C:2]#[N;H1;+1:3].[O;H1;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack of the ketenimine on the nitrous acid nitrogen, forming a nitrilium',
                },
                2: {
                    'Templates': [
                        '[C:1]([N;H0;+0:5]=[O;H0;+0:6])[C:2]#[N;H1;+1:3].[O;H1;-1:4]>>[C:1]([N;H0;+0:5]=[O;H0;+0:6])[C:2]#[N;H0;+0:3].[O;H2;+0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Deprotonation of the nitrilium by hydroxide, giving water',
                },
            },
        },
    },
    ('Sulfoxide alpha-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][S](=[O])[C]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][S:2](=[O;H0;+0:3])[C:7]>>[C:1]=[S:2]([O;H1;+0:3])[C:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Tautomerization of the sulfoxide to its vinyl sulfenic acid form',
                },
                1: {
                    'Templates': [
                        '[C:1]=[S:2]([O;H1;+0:3])[C:7].[O;H1;+0:4][N;H0;+0:5]=[O;H0;+0:6]>>[C:1]([N;H0;+0:5]=[O;H0;+0:6])[S:2](=[O;H0;+0:3])[C:7].[O;H2;+0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack on the nitrous acid nitrogen with proton transfer to give water',
                },
            },
        },
    },
    ('Sulfone alpha-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][S](=[O])(=[O])[C]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][S:2](=[O;H0;+0:3])(=[O;H0;+0:4])[C:8]>>[C:1]=[S:2]([O;H1;+0:3])(=[O;H0;+0:4])[C:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Tautomerization of the sulfone to its vinyl sulfinic acid form',
                },
                1: {
                    'Templates': [
                        '[C:1]=[S:2]([O;H1;+0:3])(=[O;H0;+0:4])[C:8].[O;H1;+0:5][N;H0;+0:6]=[O;H0;+0:7]>>[C:1]([N;H0;+0:6]=[O;H0;+0:7])[S:2](=[O;H0;+0:3])(=[O;H0;+0:4])[C:8].[O;H2;+0:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack on the nitrous acid nitrogen with proton transfer to give water',
                },
            },
        },
    },
    ('Sulfonate ester alpha-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][S](=[O])(=[O])[O][C]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][S:2](=[O;H0;+0:3])(=[O;H0;+0:4])[O;H0;+0:5][C:9]>>[C:1]=[S:2]([O;H1;+0:3])(=[O;H0;+0:4])[O;H0;+0:5][C:9]',
                    ],
                    'pKa': [None],
                    'Description': 'Tautomerization of the sulfonate to its vinyl sulfinic acid form',
                },
                1: {
                    'Templates': [
                        '[C:1]=[S:2]([O;H1;+0:3])(=[O;H0;+0:4])[O;H0;+0:5][C:9].[O;H1;+0:6][N;H0;+0:7]=[O;H0;+0:8]>>[C:1]([N;H0;+0:7]=[O;H0;+0:8])[S:2](=[O;H0;+0:3])(=[O;H0;+0:4])[O;H0;+0:5][C:9].[O;H2;+0:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack on the nitrous acid nitrogen with proton transfer to give water',
                },
            },
        },
    },
    ('Sulfonamide alpha-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][S](=[O])(=[O])[N]([C])[C]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][S:2](=[O;H0;+0:3])(=[O;H0;+0:4])[N;H0;+0:5]([C:9])[C:10]>>[C:1]=[S:2]([O;H1;+0:3])(=[O;H0;+0:4])[N;H0;+0:5]([C:9])[C:10]',
                    ],
                    'pKa': [None],
                    'Description': 'Tautomerization of the sulfonamide to its vinyl sulfinic acid form',
                },
                1: {
                    'Templates': [
                        '[C:1]=[S:2]([O;H1;+0:3])(=[O;H0;+0:4])[N;H0;+0:5]([C:9])[C:10].[O;H1;+0:6][N;H0;+0:7]=[O;H0;+0:8]>>[C:1]([N;H0;+0:7]=[O;H0;+0:8])[S:2](=[O;H0;+0:3])(=[O;H0;+0:4])[N;H0;+0:5]([C:9])[C:10].[O;H2;+0:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack on the nitrous acid nitrogen with proton transfer to give water',
                },
            },
        },
    },
    ('Aryl sulfoxide alpha-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][S](=[O])[c]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][S:2](=[O;H0;+0:3])[c:7]>>[C:1]=[S:2]([O;H1;+0:3])[c:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Tautomerization of the sulfoxide to its vinyl sulfenic acid form',
                },
                1: {
                    'Templates': [
                        '[C:1]=[S:2]([O;H1;+0:3])[c:7].[O;H1;+0:4][N;H0;+0:5]=[O;H0;+0:6]>>[C:1]([N;H0;+0:5]=[O;H0;+0:6])[S:2](=[O;H0;+0:3])[c:7].[O;H2;+0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack on the nitrous acid nitrogen with proton transfer to give water',
                },
            },
        },
    },
    ('Aryl sulfone alpha-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][S](=[O])(=[O])[c]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][S:2](=[O;H0;+0:3])(=[O;H0;+0:4])[c:8]>>[C:1]=[S:2]([O;H1;+0:3])(=[O;H0;+0:4])[c:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Tautomerization of the sulfone to its vinyl sulfinic acid form',
                },
                1: {
                    'Templates': [
                        '[C:1]=[S:2]([O;H1;+0:3])(=[O;H0;+0:4])[c:8].[O;H1;+0:5][N;H0;+0:6]=[O;H0;+0:7]>>[C:1]([N;H0;+0:6]=[O;H0;+0:7])[S:2](=[O;H0;+0:3])(=[O;H0;+0:4])[c:8].[O;H2;+0:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack on the nitrous acid nitrogen with proton transfer to give water',
                },
            },
        },
    },
    ('Aryl sulfonate ester alpha-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][S](=[O])(=[O])[O][c]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][S:2](=[O;H0;+0:3])(=[O;H0;+0:4])[O;H0;+0:5][c:9]>>[C:1]=[S:2]([O;H1;+0:3])(=[O;H0;+0:4])[O;H0;+0:5][c:9]',
                    ],
                    'pKa': [None],
                    'Description': 'Tautomerization of the sulfonate to its vinyl sulfinic acid form',
                },
                1: {
                    'Templates': [
                        '[C:1]=[S:2]([O;H1;+0:3])(=[O;H0;+0:4])[O;H0;+0:5][c:9].[O;H1;+0:6][N;H0;+0:7]=[O;H0;+0:8]>>[C:1]([N;H0;+0:7]=[O;H0;+0:8])[S:2](=[O;H0;+0:3])(=[O;H0;+0:4])[O;H0;+0:5][c:9].[O;H2;+0:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack on the nitrous acid nitrogen with proton transfer to give water',
                },
            },
        },
    },
    ('Diarylsulfonamide alpha-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][S](=[O])(=[O])[N]([c])[c]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][S:2](=[O;H0;+0:3])(=[O;H0;+0:4])[N;H0;+0:5]([c:9])[c:15]>>[C:1]=[S:2]([O;H1;+0:3])(=[O;H0;+0:4])[N;H0;+0:5]([c:9])[c:15]',
                    ],
                    'pKa': [None],
                    'Description': 'Tautomerization of the sulfonamide to its vinyl sulfinic acid form',
                },
                1: {
                    'Templates': [
                        '[C:1]=[S:2]([O;H1;+0:3])(=[O;H0;+0:4])[N;H0;+0:5]([c:9])[c:15].[O;H1;+0:6][N;H0;+0:7]=[O;H0;+0:8]>>[C:1]([N;H0;+0:7]=[O;H0;+0:8])[S:2](=[O;H0;+0:3])(=[O;H0;+0:4])[N;H0;+0:5]([c:9])[c:15].[O;H2;+0:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic attack on the nitrous acid nitrogen with proton transfer to give water',
                },
            },
        },
    },
    ('Alkyl chloride + phenol Williamson ether synthesis',): {
        'Reaction': {
            'Reagent': [
                '[C][Cl]',
                '[O;H1][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][Cl;H0;+0:2].[O;H1;+0:3][c:4]>>[C:1][O;H1;+1:3][c:4].[Cl;H0;-1:2]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of the phenol oxygen on the alkyl carbon',
                },
                1: {
                    'Templates': [
                        '[C:1][O;H1;+1:3][c:4].[Cl;H0;-1:2]>>[C:1][O;H0;+0:3][c:4].[Cl;H1;+0:2]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxonium to chloride',
                },
            },
        },
    },
    ('Alkyl chloride + alcohol Williamson ether synthesis',): {
        'Reaction': {
            'Reagent': [
                '[C][Cl]',
                '[O;H1][C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:1][Cl;H0;+0:2].[O;H1;+0:3][C:4]>>[C:1][O;H1;+1:3][C:4].[Cl;H0;-1:2]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of the alcohol oxygen on the alkyl carbon',
                },
                1: {
                    'Templates': [
                        '[C:1][O;H1;+1:3][C:4].[Cl;H0;-1:2]>>[C:1][O;H0;+0:3][C:4].[Cl;H1;+0:2]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxonium to chloride',
                },
            },
        },
    },
    ('N,N-dialkylaniline + HBr N-dealkylation',): {
        'Reaction': {
            'Reagent': [
                '[c][N]([C])[C]',
                '[Br;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:1][N;H0;+0:2]([C;!$(C=O);!$(CO):3])[C;!$(C=O);!$(CO):4].[Br;H1;+0:5]>>[c:1][N;H1;+1:2]([C:3])[C:4].[Br;H0;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the aniline nitrogen by HBr',
                },
                1: {
                    'Templates': [
                        '[c:1][N;H1;+1:2]([C:3])[C:4].[Br;H0;-1:5]>>[c:1][N;H1;+0:2][C:4].[C:3][Br;H0;+0:5]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of bromide on one N-alkyl carbon, cleaving the C-N bond',
                },
            },
        },
    },
    ('Sulfuryl chloride + amine to sulfamoyl chloride',): {
        'Reaction': {
            'Reagent': [
                '[S](=[O])(=[O])([Cl])[Cl]',
                '[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[Cl;H0;+0:5].[N;H2;+0:6]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[N;H2;+1:6].[Cl;H0;-1:5]',
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[Cl;H0;+0:5].[N;H1;+0:6]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[N;H1;+1:6].[Cl;H0;-1:5]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition-elimination at sulfur, expelling one chloride',
                },
                1: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[N;H2;+1:6].[Cl;H0;-1:5]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[N;H1;+0:6].[Cl;H1;+0:5]',
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[N;H1;+1:6].[Cl;H0;-1:5]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[N;H0;+0:6].[Cl;H1;+0:5]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the ammonium nitrogen to chloride',
                },
            },
        },
    },
    ('Sulfamoyl chloride + amine to sulfamide',): {
        'Reaction': {
            'Reagent': [
                '[S](=[O])(=[O])([Cl])[N]',
                '[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[N:5].[N;H2;+0:6]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([N;H2;+1:6])[N:5].[Cl;H0;-1:4]',
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[N:5].[N;H1;+0:6]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([N;H1;+1:6])[N:5].[Cl;H0;-1:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition-elimination at sulfur, expelling chloride',
                },
                1: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([N;H2;+1:6])[N:5].[Cl;H0;-1:4]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([N;H1;+0:6])[N:5].[Cl;H1;+0:4]',
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([N;H1;+1:6])[N:5].[Cl;H0;-1:4]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([N;H0;+0:6])[N:5].[Cl;H1;+0:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the ammonium nitrogen to chloride',
                },
            },
        },
    },
    ('Secondary amine N-nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[N;H1]([C])[C]',
                '[O;H1][N]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][N;H1;+0:2][C:3].[O;H1;+0:4][N;H0;+0:5]=[O;H0;+0:6]>>[C:1][N;H1;+1:2]([C:3])[N;H0;+0:5]=[O;H0;+0:6].[O;H1;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic attack of the amine on the nitrous acid nitrogen',
                },
                1: {
                    'Templates': [
                        '[C:1][N;H1;+1:2]([C:3])[N;H0;+0:5]=[O;H0;+0:6].[O;H1;-1:4]>>[C:1][N;H0;+0:2]([C:3])[N;H0;+0:5]=[O;H0;+0:6].[O;H2;+0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the ammonium to hydroxide, giving water',
                },
            },
        },
    },
    ('Sulfuryl chloride + alcohol to chlorosulfonate ester',): {
        'Reaction': {
            'Reagent': [
                '[S](=[O])(=[O])([Cl])[Cl]',
                '[O;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[Cl;H0;+0:5].[O;H1;+0:6]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[O;H1;+1:6].[Cl;H0;-1:5]',
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[Cl;H0;+0:5].[O;H2;+0:6]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[O;H2;+1:6].[Cl;H0;-1:5]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition-elimination at sulfur, expelling one chloride',
                },
                1: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[O;H1;+1:6].[Cl;H0;-1:5]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[O;H0;+0:6].[Cl;H1;+0:5]',
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[O;H2;+1:6].[Cl;H0;-1:5]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[O;H1;+0:6].[Cl;H1;+0:5]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the oxonium to chloride',
                },
            },
        },
    },
    ('Chlorosulfonate ester + water to sulfate diester',): {
        'Reaction': {
            'Reagent': [
                '[S](=[O])(=[O])([Cl])[O]',
                '[O;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[O;H0;+0:5].[O;H1;+0:6]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H1;+1:6])[O;H0;+0:5].[Cl;H0;-1:4]',
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:4])[O;H0;+0:5].[O;H2;+0:6]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H2;+1:6])[O;H0;+0:5].[Cl;H0;-1:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition-elimination at sulfur, expelling chloride',
                },
                1: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H1;+1:6])[O;H0;+0:5].[Cl;H0;-1:4]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H0;+0:6])[O;H0;+0:5].[Cl;H1;+0:4]',
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H2;+1:6])[O;H0;+0:5].[Cl;H0;-1:4]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H1;+0:6])[O;H0;+0:5].[Cl;H1;+0:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the oxonium to chloride',
                },
            },
        },
    },
    ('Dialkyl sulfate alkyl-oxygen SN2 exchange',): {
        'Reaction': {
            'Reagent': [
                '[S](=[O])(=[O])([O][C])[O][C]',
                '[O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H0;+0:4][C:5])[O;H0;+0:6][C:7].[O;H1;+0:8]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H0;+0:4][C:5])[O;H0;-1:6].[C:7][O;H1;+1:8]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of the nucleophile on the alkyl carbon, breaking the alkyl-oxygen bond',
                },
                1: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H0;+0:4][C:5])[O;H0;-1:6].[C:7][O;H1;+1:8]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H0;+0:4][C:5])[17O;H1;+0:6].[13C:7][O;H0;+0:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxonium to the sulfate anion, giving the neutral products',
                },
            },
        },
    },
    ('Alkyl sulfate substitution at sulfur',): {
        'Reaction': {
            'Reagent': [
                '[S](=[O])(=[O])([O][C])[O;H1]',
                '[O;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H0;+0:4][C:5])[O;H1;+0:6].[O;H1;+0:7]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H1;+1:7])[O;H1;+0:6].[O;H0;-1:4][C:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition-elimination at sulfur, expelling the alkoxide',
                },
                1: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H1;+1:7])[O;H1;+0:6].[O;H0;-1:4][C:5]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H0;+0:7])[O;H1;+0:6].[O;H1;+0:4][C:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxonium to the alkoxide, giving the free alcohol',
                },
            },
        },
    },
    ('Sulfamide hydrolysis to sulfamate and ammonia',): {
        'Reaction': {
            'Reagent': [
                '[S](=[O])(=[O])([N])[N;H2]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([N:4])[N;H2;+0:5].[O;H2;+0:6]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([N:4])[O;H2;+1:6].[N;H2;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition-elimination at sulfur, expelling one amido nitrogen',
                },
                1: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([N:4])[O;H2;+1:6].[N;H2;-1:5]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([N:4])[O;H1;+0:6].[N;H3;+0:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxonium to the amide anion, giving ammonia',
                },
            },
        },
    },
    ('Sulfamate ester hydrolysis to sulfate diester and ammonia',): {
        'Reaction': {
            'Reagent': [
                '[S](=[O])(=[O])([N;H2])[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([N;H2;+0:4])[O;H0;+0:5].[O;H2;+0:6]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H2;+1:6])[O;H0;+0:5].[N;H2;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition-elimination at sulfur, expelling the amido nitrogen',
                },
                1: {
                    'Templates': [
                        '[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H2;+1:6])[O;H0;+0:5].[N;H2;-1:4]>>[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H1;+0:6])[O;H0;+0:5].[N;H3;+0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxonium to the amide anion, giving ammonia',
                },
            },
        },
    },
    ('Sulfate ester + PCl5 to chlorosulfonate',): {
        'Reaction': {
            'Reagent': [
                '[S](=[O])(=[O])([O;H1])[O]',
                '[Cl][P]([Cl])([Cl])([Cl])[Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1;+0:5][S:1](=[O;H0;+0:2])(=[O;H0;+0:3])[O;H0;+0:4].[Cl;H0;+0:7][P;H0;+0:6]([Cl;H0;+0:8])([Cl;H0;+0:9])([Cl;H0;+0:10])[Cl;H0;+0:11]>>[O;H1;+1:5]([S:1](=[O;H0;+0:2])(=[O;H0;+0:3])[O;H0;+0:4])[P;H0;+0:6]([Cl;H0;+0:8])([Cl;H0;+0:9])([Cl;H0;+0:10])[Cl;H0;+0:11].[Cl;H0;-1:7]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of the sulfate hydroxyl oxygen on phosphorus, expelling chloride',
                },
                1: {
                    'Templates': [
                        '[O;H1;+1:5]([S:1](=[O;H0;+0:2])(=[O;H0;+0:3])[O;H0;+0:4])[P;H0;+0:6]([Cl;H0;+0:8])([Cl;H0;+0:9])([Cl;H0;+0:10])[Cl;H0;+0:11].[Cl;H0;-1:7]>>[O;H1;+0:5][P;H0;+0:6]([Cl;H0;+0:8])([Cl;H0;+0:9])([Cl;H0;+0:10])[Cl;H0;+0:11].[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([O;H0;+0:4])[Cl;H0;+0:7]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of chloride on sulfur, breaking the S-O bond',
                },
            },
        },
    },
    ('Chlorosulfonate + PCl5 to sulfonyl dichloride',): {
        'Reaction': {
            'Reagent': [
                '[S](=[O])(=[O])([O;H1])[Cl]',
                '[Cl][P]([Cl])([Cl])([Cl])[Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1;+0:4][S:1](=[O;H0;+0:2])(=[O;H0;+0:3])[Cl;H0;+0:5].[Cl;H0;+0:7][P;H0;+0:6]([Cl;H0;+0:8])([Cl;H0;+0:9])([Cl;H0;+0:10])[Cl;H0;+0:11]>>[O;H1;+1:4]([S:1](=[O;H0;+0:2])(=[O;H0;+0:3])[Cl;H0;+0:5])[P;H0;+0:6]([Cl;H0;+0:8])([Cl;H0;+0:9])([Cl;H0;+0:10])[Cl;H0;+0:11].[Cl;H0;-1:7]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of the sulfonate hydroxyl oxygen on phosphorus, expelling chloride',
                },
                1: {
                    'Templates': [
                        '[O;H1;+1:4]([S:1](=[O;H0;+0:2])(=[O;H0;+0:3])[Cl;H0;+0:5])[P;H0;+0:6]([Cl;H0;+0:8])([Cl;H0;+0:9])([Cl;H0;+0:10])[Cl;H0;+0:11].[Cl;H0;-1:7]>>[O;H1;+0:4][P;H0;+0:6]([Cl;H0;+0:8])([Cl;H0;+0:9])([Cl;H0;+0:10])[Cl;H0;+0:11].[S:1](=[O;H0;+0:2])(=[O;H0;+0:3])([Cl;H0;+0:7])[Cl;H0;+0:5]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of chloride on sulfur, breaking the S-O bond',
                },
            },
        },
    },
    ('Carbonyl hydration to gem-diol',): {
        'Reaction': {
            'Reagent': [
                '[C]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[O;H0;+0:2].[O;H2;+0:3]>>[C:1]([O;H0;-1:2])[O;H2;+1:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of water to the carbonyl carbon',
                },
                1: {
                    'Templates': [
                        '[C:1]([O;H0;-1:2])[O;H2;+1:3]>>[C:1]([O;H1;+0:2])[O;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer between the two oxygens, giving the neutral gem-diol',
                },
            },
        },
    },
    ('Aldehyde + anhydride Tishchenko-type addition',): {
        'Reaction': {
            'Reagent': [
                '[C;H1]=[O]',
                '[C](=[O])[O][C]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:3][C;H1:1]=[O;H0;+0:2].[C:4][C;H0:5](=[O;H0;+0:6])[O;H0;+0:7][C;H0:8](=[O;H0;+0:9])[C:10]>>[C:3][C;H1:1]([O;H0;-1:2])[O;H0;+1:6]=[C;H0:5]([C:4])[O;H0;+0:7][C;H0:8](=[O;H0;+0:9])[C:10]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the anhydride carbonyl oxygen to the aldehyde carbon',
                },
                1: {
                    'Templates': [
                        '[C:3][C;H1:1]([O;H0;-1:2])[O;H0;+1:6]=[C;H0:5]([C:4])[O;H0;+0:7][C;H0:8](=[O;H0;+0:9])[C:10]>>[C:3][C;H0:1](=[O;H0;+0:2])[O;H0;+0:6][C;H1:5]([C:4])[O;H0;+0:7][C;H0:8](=[O;H0;+0:9])[C:10]',
                    ],
                    'pKa': [None],
                    'Description': 'Intramolecular hydride shift from the aldehyde carbon to the anhydride carbonyl carbon, forming the acylal ester',
                },
            },
        },
    },
    ('Alkene + HCl to alkyl chloride',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[Cl;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[Cl;H1;+0:3]>>[C:1][C;+1:2].[Cl;H0;-1:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C:1][C;+1:2].[Cl;H0;-1:3]>>[C:1][C;+0:2][Cl;H0;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by chloride',
                },
            },
        },
    },
    ('Alkene + alcohol to ether',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[C][O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[C:3][O;H1;+0:4]>>[C:1][C;+1:2].[C:3][O;H0;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C:1][C;+1:2].[C:3][O;H0;-1:4]>>[C:1][C;+0:2][O;H0;+0:4][C:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by the alkoxide',
                },
            },
        },
    },
    ('Alkene + carboxylic acid to ester',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[C][C](=[O])[O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[C:3][C:4](=[O;H0;+0:5])[O;H1;+0:6]>>[C:1][C;+1:2].[C:3][C:4](=[O;H0;+0:5])[O;H0;-1:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C:1][C;+1:2].[C:3][C:4](=[O;H0;+0:5])[O;H0;-1:6]>>[C:1][C;+0:2][O;H0;+0:6][C:4](=[O;H0;+0:5])[C:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by the carboxylate',
                },
            },
        },
    },
    ('Alkene + H2S to thiol',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[S;H2]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[S;H2;+0:3]>>[C:1][C;+1:2].[S;H1;-1:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C:1][C;+1:2].[S;H1;-1:3]>>[C:1][C;+0:2][S;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by hydrosulfide',
                },
            },
        },
    },
    ('Alkene + thiophenol to thioether',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[S;H1][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[S;H1;+0:3][c:4]>>[C:1][C;+1:2].[S;H0;-1:3][c:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C:1][C;+1:2].[S;H0;-1:3][c:4]>>[C:1][C;+0:2][S;H0;+0:3][c:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by thiophenolate',
                },
            },
        },
    },
    ('Alkene + amide to N-alkylamide',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[C][N;H1][C]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[C:3][N;H1;+0:4][C:5](=[O;H0;+0:6])[C:7]>>[C:1][C;+1:2].[C:3][N;H0;-1:4][C:5](=[O;H0;+0:6])[C:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C:1][C;+1:2].[C:3][N;H0;-1:4][C:5](=[O;H0;+0:6])[C:7]>>[C:1][C;+0:2][N;H0;+0:4]([C:3])[C:5](=[O;H0;+0:6])[C:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by the amide anion',
                },
            },
        },
    },
    ('Alkene + N-arylbenzamide to N-alkyl-N-arylbenzamide',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[c][N;H1][C](=[O])[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[c:12][N;H1;+0:3][C:4](=[O;H0;+0:5])[c:6]>>[C:1][C;+1:2].[c:12][N;H0;-1:3][C:4](=[O;H0;+0:5])[c:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C:1][C;+1:2].[c:12][N;H0;-1:3][C:4](=[O;H0;+0:5])[c:6]>>[C:1][C;+0:2][N;H0;+0:3]([c:12])[C:4](=[O;H0;+0:5])[c:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by the amide anion',
                },
            },
        },
    },
    ('Alkene + aldehyde Prins-type addition to ketone',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[C][C;H1]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[C:3][C;H1:4]=[O;H0;+0:5]>>[CH2;+1:1][C:2][C;H1:4]([C:3])[O;H0;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the alkene to the aldehyde carbon, forming a carbocation and an alkoxide',
                },
                1: {
                    'Templates': [
                        '[CH2;+1:1][C:2][C;H1:4]([C:3])[O;H0;-1:5]>>[CH3;+0:1][C;+0:2][C;H0;+0:4](=[O;H0;+0:5])[C:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Intramolecular hydride shift to the carbocation, re-forming the carbonyl and giving the ketone',
                },
            },
        },
    },
    ('Alkene + benzaldehyde Prins-type addition to aryl ketone',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[c][C;H1]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[c:5][C;H1:3]=[O;H0;+0:4]>>[CH2;+1:1][C:2][C;H1:3]([c:5])[O;H0;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the alkene to the benzaldehyde carbon, forming a carbocation and an alkoxide',
                },
                1: {
                    'Templates': [
                        '[CH2;+1:1][C:2][C;H1:3]([c:5])[O;H0;-1:4]>>[CH3;+0:1][C;+0:2][C;H0;+0:3](=[O;H0;+0:4])[c:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Intramolecular hydride shift to the carbocation, re-forming the carbonyl and giving the aryl ketone',
                },
            },
        },
    },
    ('Alkene + formate ester Prins-type addition to ester',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[C][O][C;H1]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[C:6][O:3][C;H1:4]=[O;H0;+0:5]>>[CH2;+1:1][C:2][C;H1:4]([O:3][C:6])[O;H0;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the alkene to the formate carbon, forming a carbocation and an alkoxide',
                },
                1: {
                    'Templates': [
                        '[CH2;+1:1][C:2][C;H1:4]([O:3][C:6])[O;H0;-1:5]>>[CH3;+0:1][C;+0:2][C;H0;+0:4](=[O;H0;+0:5])[O:3][C:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Intramolecular hydride shift to the carbocation, re-forming the carbonyl and giving the ester',
                },
            },
        },
    },
    ('Alkene + formamide Prins-type addition to amide',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[N][C;H1]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[N:3][C;H1:4]=[O;H0;+0:5]>>[CH2;+1:1][C:2][C;H1:4]([N:3])[O;H0;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the alkene to the formamide carbon, forming a carbocation and an alkoxide',
                },
                1: {
                    'Templates': [
                        '[CH2;+1:1][C:2][C;H1:4]([N:3])[O;H0;-1:5]>>[CH3;+0:1][C;+0:2][C;H0;+0:4](=[O;H0;+0:5])[N:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Intramolecular hydride shift to the carbocation, re-forming the carbonyl and giving the amide',
                },
            },
        },
    },
    ('Alkene + HCN ionic addition to nitrile',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[C;H1]#[N]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[C;H1:3]#[N;H0:4]>>[C:1][C;+1:2].[C;H0;-1:3]#[N;H0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the alkene by HCN, forming a carbocation and cyanide',
                },
                1: {
                    'Templates': [
                        '[C:1][C;+1:2].[C;H0;-1:3]#[N;H0:4]>>[C:1][C;+0:2][C;H0;+0:3]#[N;H0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by cyanide',
                },
            },
        },
    },
    ('Alkene + Cl2 to dichloride',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[Cl][Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[Cl;H0;+0:3][Cl;H0;+0:4]>>[C;+1:1][C:2][Cl;H0;+0:3].[Cl;H0;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition to the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C;+1:1][C:2][Cl;H0;+0:3].[Cl;H0;-1:4]>>[C;+0:1]([Cl;H0;+0:4])[C:2][Cl;H0;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by chloride',
                },
            },
        },
    },
    ('Alkene + sulfonyl chloride to beta-chlorosulfone',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[C][S](=[O])(=[O])[Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[C:3][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[Cl;H0;+0:7]>>[C;+1:1][C:2][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[C:3].[Cl;H0;-1:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition to the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C;+1:1][C:2][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[C:3].[Cl;H0;-1:7]>>[C;+0:1]([Cl;H0;+0:7])[C:2][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[C:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by chloride',
                },
            },
        },
    },
    ('Alkene + thionyl chloride to beta-chlorosulfinyl chloride',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[Cl][S](=[O])[Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[Cl;H0;+0:3][S:4](=[O;H0;+0:5])[Cl;H0;+0:6]>>[C;+1:1][C:2][S:4](=[O;H0;+0:5])[Cl;H0;+0:6].[Cl;H0;-1:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition to the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C;+1:1][C:2][S:4](=[O;H0;+0:5])[Cl;H0;+0:6].[Cl;H0;-1:3]>>[C;+0:1]([Cl;H0;+0:3])[C:2][S:4](=[O;H0;+0:5])[Cl;H0;+0:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by chloride',
                },
            },
        },
    },
    ('Alkene + sulfenyl chloride to beta-chlorosulfide',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[C][S][Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[C:3][S;H0;+0:4][Cl;H0;+0:5]>>[C;+1:1][C:2][S:4][C:3].[Cl;H0;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition to the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C;+1:1][C:2][S:4][C:3].[Cl;H0;-1:5]>>[C;+0:1]([Cl;H0;+0:5])[C:2][S:4][C:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by chloride',
                },
            },
        },
    },
    ('Alkene + nitrosyl chloride to beta-chloronitroso',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[O]=[N][Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[O;H0;+0:3]=[N;H0;+0:4][Cl;H0;+0:5]>>[C;+1:1][C:2][N:4]=[O:3].[Cl;H0;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition to the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C;+1:1][C:2][N:4]=[O:3].[Cl;H0;-1:5]>>[C;+0:1]([Cl;H0;+0:5])[C:2][N:4]=[O:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by chloride',
                },
            },
        },
    },
    ('Alkene + benzoic acid to ester',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[c][C](=[O])[O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[c:6][C:3](=[O;H0;+0:4])[O;H1;+0:5]>>[C:1][C;+1:2].[c:6][C:3](=[O;H0;+0:4])[O;H0;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the alkene by the carboxylic acid, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C:1][C;+1:2].[c:6][C:3](=[O;H0;+0:4])[O;H0;-1:5]>>[C:1][C;+0:2][O;H0;+0:5][C:3](=[O;H0;+0:4])[c:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by benzoate',
                },
            },
        },
    },
    ('Alkene + phenyl formate Prins-type addition to ester',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[c][O][C;H1]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[c:6][O:3][C;H1:4]=[O;H0;+0:5]>>[CH2;+1:1][C:2][C;H1:4]([O:3][c:6])[O;H0;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the alkene to the phenyl formate carbon, forming a carbocation and an alkoxide',
                },
                1: {
                    'Templates': [
                        '[CH2;+1:1][C:2][C;H1:4]([O:3][c:6])[O;H0;-1:5]>>[CH3;+0:1][C;+0:2][C;H0;+0:4](=[O;H0;+0:5])[O:3][c:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Intramolecular hydride shift to the carbocation, giving the ester',
                },
            },
        },
    },
    ('Alkene + HBr to alkyl bromide',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[Br;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[Br;H1;+0:3]>>[C:1][C;+1:2].[Br;H0;-1:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C:1][C;+1:2].[Br;H0;-1:3]>>[C:1][C;+0:2][Br;H0;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by bromide',
                },
            },
        },
    },
    ('Alkene + Br2 to dibromide',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[Br][Br]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[Br;H0;+0:3][Br;H0;+0:4]>>[C;+1:1][C:2][Br;H0;+0:3].[Br;H0;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition to the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C;+1:1][C:2][Br;H0;+0:3].[Br;H0;-1:4]>>[C;+0:1]([Br;H0;+0:4])[C:2][Br;H0;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by bromide',
                },
            },
        },
    },
    ('Alkene + sulfonyl bromide to beta-bromosulfone',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[C][S](=[O])(=[O])[Br]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[C:3][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[Br;H0;+0:7]>>[C;+1:1][C:2][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[C:3].[Br;H0;-1:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition to the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C;+1:1][C:2][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[C:3].[Br;H0;-1:7]>>[C;+0:1]([Br;H0;+0:7])[C:2][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[C:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by bromide',
                },
            },
        },
    },
    ('Alkene + thionyl bromide to beta-bromosulfinyl bromide',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[Br][S](=[O])[Br]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[Br;H0;+0:3][S:4](=[O;H0;+0:5])[Br;H0;+0:6]>>[C;+1:1][C:2][S:4](=[O;H0;+0:5])[Br;H0;+0:6].[Br;H0;-1:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition to the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C;+1:1][C:2][S:4](=[O;H0;+0:5])[Br;H0;+0:6].[Br;H0;-1:3]>>[C;+0:1]([Br;H0;+0:3])[C:2][S:4](=[O;H0;+0:5])[Br;H0;+0:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by bromide',
                },
            },
        },
    },
    ('Alkene + sulfenyl bromide to beta-bromosulfide',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[C][S][Br]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[C:3][S;H0;+0:4][Br;H0;+0:5]>>[C;+1:1][C:2][S:4][C:3].[Br;H0;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition to the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C;+1:1][C:2][S:4][C:3].[Br;H0;-1:5]>>[C;+0:1]([Br;H0;+0:5])[C:2][S:4][C:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by bromide',
                },
            },
        },
    },
    ('Alkene + arylsulfonyl chloride to beta-chlorosulfone',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[c][S](=[O])(=[O])[Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[c:7][S:3](=[O;H0;+0:4])(=[O;H0;+0:5])[Cl;H0;+0:6]>>[C;+1:1][C:2][S:3](=[O;H0;+0:4])(=[O;H0;+0:5])[c:7].[Cl;H0;-1:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition to the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C;+1:1][C:2][S:3](=[O;H0;+0:4])(=[O;H0;+0:5])[c:7].[Cl;H0;-1:6]>>[C;+0:1]([Cl;H0;+0:6])[C:2][S:3](=[O;H0;+0:4])(=[O;H0;+0:5])[c:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by chloride',
                },
            },
        },
    },
    ('Alkene + arylsulfenyl chloride to beta-chlorosulfide',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[c][S][Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[c:5][S;H0;+0:3][Cl;H0;+0:4]>>[C;+1:1][C:2][S:3][c:5].[Cl;H0;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition to the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C;+1:1][C:2][S:3][c:5].[Cl;H0;-1:4]>>[C;+0:1]([Cl;H0;+0:4])[C:2][S:3][c:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by chloride',
                },
            },
        },
    },
    ('Alkene + nitrosyl bromide to beta-bromonitroso',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[O]=[N][Br]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[O;H0;+0:3]=[N;H0;+0:4][Br;H0;+0:5]>>[C;+1:1][C:2][N:4]=[O:3].[Br;H0;-1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition to the alkene, forming a carbocation',
                },
                1: {
                    'Templates': [
                        '[C;+1:1][C:2][N:4]=[O:3].[Br;H0;-1:5]>>[C;+0:1]([Br;H0;+0:5])[C:2][N:4]=[O:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by bromide',
                },
            },
        },
    },
    ('Alkyne + sulfonyl chloride to vinyl sulfone',): {
        'Reaction': {
            'Reagent': [
                '[C]#[C]',
                '[C][S](=[O])(=[O])[Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]#[C:2].[C:3][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[Cl;H0;+0:7]>>[C;+1:1]=[C:2][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[C:3].[Cl;H0;-1:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition to the alkyne, forming a vinyl cation',
                },
                1: {
                    'Templates': [
                        '[C;+1:1]=[C:2][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[C:3].[Cl;H0;-1:7]>>[C;+0:1](=[C:2][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[C:3])[Cl;H0;+0:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by chloride, giving the vinyl sulfone',
                },
            },
        },
    },
    ('Alkyne + sulfonyl bromide to vinyl sulfone',): {
        'Reaction': {
            'Reagent': [
                '[C]#[C]',
                '[C][S](=[O])(=[O])[Br]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]#[C:2].[C:3][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[Br;H0;+0:7]>>[C;+1:1]=[C:2][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[C:3].[Br;H0;-1:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition to the alkyne, forming a vinyl cation',
                },
                1: {
                    'Templates': [
                        '[C;+1:1]=[C:2][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[C:3].[Br;H0;-1:7]>>[C;+0:1](=[C:2][S:4](=[O;H0;+0:5])(=[O;H0;+0:6])[C:3])[Br;H0;+0:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by bromide, giving the vinyl sulfone',
                },
            },
        },
    },
    ('Alkyne + arylsulfonyl chloride to vinyl sulfone',): {
        'Reaction': {
            'Reagent': [
                '[C]#[C]',
                '[c][S](=[O])(=[O])[Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]#[C:2].[c:7][S:3](=[O;H0;+0:4])(=[O;H0;+0:5])[Cl;H0;+0:6]>>[C;+1:1]=[C:2][S:3](=[O;H0;+0:4])(=[O;H0;+0:5])[c:7].[Cl;H0;-1:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition to the alkyne, forming a vinyl cation',
                },
                1: {
                    'Templates': [
                        '[C;+1:1]=[C:2][S:3](=[O;H0;+0:4])(=[O;H0;+0:5])[c:7].[Cl;H0;-1:6]>>[C;+0:1](=[C:2][S:3](=[O;H0;+0:4])(=[O;H0;+0:5])[c:7])[Cl;H0;+0:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic capture of the carbocation by chloride, giving the vinyl sulfone',
                },
            },
        },
    },
    ('Amine + carbon monoxide to formamide',): {
        'Reaction': {
            'Reagent': [
                '[C][N;H2]',
                '[C-]#[O+]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][N;H2;+0:2].[C;H0;-1:3]#[O;H0;+1:4]>>[C:1][N;H1;+0:2][C;H1;+0:3]=[O;H0;+0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Formal migratory insertion of the amine into carbon monoxide, giving the formamide',
                },
            },
        },
    },
    ('Aniline + carbon monoxide to formanilide',): {
        'Reaction': {
            'Reagent': [
                '[c][N;H2]',
                '[C-]#[O+]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:4][N;H2;+0:1].[C;H0;-1:2]#[O;H0;+1:3]>>[c:4][N;H1;+0:1][C;H1;+0:2]=[O;H0;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Formal migratory insertion of the aniline into carbon monoxide, giving formanilide',
                },
            },
        },
    },
    ('Arene + isocyanate Friedel-Crafts carbamoylation',): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c][c][c]1',
                '[C][N]=[C]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:1]1[c:2][c:3][c:4][c:5][c;H1:6]1.[C:7][N;H0;+0:8]=[C;H0:9]=[O;H0;+0:10]>>[C;H1:1]1([C;H0:9](=[O;H0;+0:10])[N;H0;-1:8][C:7])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of the arene to the isocyanate carbon, forming a Wheland intermediate',
                },
                1: {
                    'Templates': [
                        '[C;H1:1]1([C;H0:9](=[O;H0;+0:10])[N;H0;-1:8][C:7])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1>>[c;H0;+0:1]1([C;H0:9](=[O;H0;+0:10])[N;H1;+0:8][C:7])[c:2][c:3][c:4][c:5][c;H1;+0:6]1',
                    ],
                    'pKa': [None],
                    'Description': 'Loss of the ring proton to the amide anion, rearomatizing the ring',
                },
            },
        },
    },
    ('Arene + N-arylisocyanate Friedel-Crafts carbamoylation',): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c][c][c]1',
                '[c][N]=[C]=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:1]1[c:2][c:3][c:4][c:5][c;H1:6]1.[c:10][N;H0;+0:7]=[C;H0:8]=[O;H0;+0:9]>>[C;H1:1]1([C;H0:8](=[O;H0;+0:9])[N;H0;-1:7][c:10])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1',
                    ],
                    'pKa': [None],
                    'Description': 'Electrophilic addition of the arene to the isocyanate carbon, forming a Wheland intermediate',
                },
                1: {
                    'Templates': [
                        '[C;H1:1]1([C;H0:8](=[O;H0;+0:9])[N;H0;-1:7][c:10])[CH1:2]=[CH1:3][CH1:4]=[CH1:5][CH1;+1:6]1>>[c;H0;+0:1]1([C;H0:8](=[O;H0;+0:9])[N;H1;+0:7][c:10])[c:2][c:3][c:4][c:5][c;H1;+0:6]1',
                    ],
                    'pKa': [None],
                    'Description': 'Loss of the ring proton to the amide anion, rearomatizing the ring',
                },
            },
        },
    },
    ('Isocyanic acid + amine to urea',): {
        'Reaction': {
            'Reagent': [
                '[N;H1]=[C]=[O]',
                '[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[N;H1;+0:1]=[C;H0:2]=[O;H0;+0:3].[N;H2;+0:4]>>[N;H1;-1:1][C;H0:2](=[O;H0;+0:3])[N;H2;+1:4]',
                        '[N;H1;+0:1]=[C;H0:2]=[O;H0;+0:3].[N;H1;+0:4]>>[N;H1;-1:1][C;H0:2](=[O;H0;+0:3])[N;H1;+1:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition of the amine to the isocyanate carbon',
                },
                1: {
                    'Templates': [
                        '[N;H1;-1:1][C;H0:2](=[O;H0;+0:3])[N;H2;+1:4]>>[N;H2;+0:1][C;H0:2](=[O;H0;+0:3])[N;H1;+0:4]',
                        '[N;H1;-1:1][C;H0:2](=[O;H0;+0:3])[N;H1;+1:4]>>[N;H2;+0:1][C;H0:2](=[O;H0;+0:3])[N;H0;+0:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the ammonium to the amide anion, giving the neutral urea',
                },
            },
        },
    },
    ('Isothiocyanic acid + amine to thiourea',): {
        'Reaction': {
            'Reagent': [
                '[N;H1]=[C]=[S]',
                '[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[N;H1;+0:1]=[C;H0:2]=[S;H0;+0:3].[N;H2;+0:4]>>[N;H1;-1:1][C;H0:2](=[S;H0;+0:3])[N;H2;+1:4]',
                        '[N;H1;+0:1]=[C;H0:2]=[S;H0;+0:3].[N;H1;+0:4]>>[N;H1;-1:1][C;H0:2](=[S;H0;+0:3])[N;H1;+1:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic addition of the amine to the isothiocyanate carbon',
                },
                1: {
                    'Templates': [
                        '[N;H1;-1:1][C;H0:2](=[S;H0;+0:3])[N;H2;+1:4]>>[N;H2;+0:1][C;H0:2](=[S;H0;+0:3])[N;H1;+0:4]',
                        '[N;H1;-1:1][C;H0:2](=[S;H0;+0:3])[N;H1;+1:4]>>[N;H2;+0:1][C;H0:2](=[S;H0;+0:3])[N;H0;+0:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the ammonium to the amide anion, giving the neutral thiourea',
                },
            },
        },
    },
    ('N-arylisocyanate + diarylamine to triarylurea',): {
        'Reaction': {
            'Reagent': [
                '[c][N]=[C]=[O]',
                '[c][N;H1][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:5][N;H0;+0:1]=[C;H0:2]=[O;H0;+0:3].[N;H1;+0:4]([c:17])[c:11]>>[c:5][N;H0;-1:1][C;H0:2](=[O;H0;+0:3])[N;H1;+1:4]([c:17])[c:11]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the diarylamine to the isocyanate carbon',
                },
                1: {
                    'Templates': [
                        '[c:5][N;H0;-1:1][C;H0:2](=[O;H0;+0:3])[N;H1;+1:4]([c:17])[c:11]>>[c:5][N;H1;+0:1][C;H0:2](=[O;H0;+0:3])[N;H0;+0:4]([c:17])[c:11]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the ammonium to the amide anion, giving the neutral triarylurea',
                },
            },
        },
    },
    ('N-arylisothiocyanate + diarylamine to triarylthiourea',): {
        'Reaction': {
            'Reagent': [
                '[c][N]=[C]=[S]',
                '[c][N;H1][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:5][N;H0;+0:1]=[C;H0:2]=[S;H0;+0:3].[N;H1;+0:4]([c:17])[c:11]>>[c:5][N;H0;-1:1][C;H0:2](=[S;H0;+0:3])[N;H1;+1:4]([c:17])[c:11]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the diarylamine to the isothiocyanate carbon',
                },
                1: {
                    'Templates': [
                        '[c:5][N;H0;-1:1][C;H0:2](=[S;H0;+0:3])[N;H1;+1:4]([c:17])[c:11]>>[c:5][N;H1;+0:1][C;H0:2](=[S;H0;+0:3])[N;H0;+0:4]([c:17])[c:11]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the ammonium to the amide anion, giving the neutral triarylthiourea',
                },
            },
        },
    },
    ('Chlorohydrin cyclization to epoxide',): {
        'Reaction': {
            'Reagent': [
                '[Cl][C][C][O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[Cl;H0;+0:2][C:1][C:3][O;H1;+0:4]>>[Cl;H0;-1:2].[C:1][C:3][O;H1;+1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation-equivalent bookkeeping: the alkoxide displaces chloride intramolecularly',
                },
                1: {
                    'Templates': [
                        '[Cl;H0;-1:2].[C:1][C:3][O;H1;+1:4]>>[Cl;H1;+0:2].[C:1]1[C:3][O;H0;+0:4]1',
                    ],
                    'pKa': [None],
                    'Description': 'Intramolecular SN2 ring closure to the epoxide, releasing HCl',
                },
            },
        },
    },
    ('Chlorohydrin cyclization to oxetane',): {
        'Reaction': {
            'Reagent': [
                '[Cl][C][C][C][O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[Cl;H0;+0:2][C:1][C:3][C:5][O;H1;+0:4]>>[Cl;H0;-1:2].[C:1][C:3][C:5][O;H1;+1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation-equivalent bookkeeping: the alkoxide displaces chloride intramolecularly',
                },
                1: {
                    'Templates': [
                        '[Cl;H0;-1:2].[C:1][C:3][C:5][O;H1;+1:4]>>[Cl;H1;+0:2].[C:1]1[C:3][C:5][O;H0;+0:4]1',
                    ],
                    'pKa': [None],
                    'Description': 'Intramolecular SN2 ring closure to the oxetane, releasing HCl',
                },
            },
        },
    },
    ('Chlorohydrin cyclization to tetrahydrofuran',): {
        'Reaction': {
            'Reagent': [
                '[Cl][C][C][C][C][O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[Cl;H0;+0:2][C:1][C:3][C:5][C:6][O;H1;+0:4]>>[Cl;H0;-1:2].[C:1][C:3][C:5][C:6][O;H1;+1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation-equivalent bookkeeping: the alkoxide displaces chloride intramolecularly',
                },
                1: {
                    'Templates': [
                        '[Cl;H0;-1:2].[C:1][C:3][C:5][C:6][O;H1;+1:4]>>[Cl;H1;+0:2].[C:1]1[C:3][C:5][C:6][O;H0;+0:4]1',
                    ],
                    'pKa': [None],
                    'Description': 'Intramolecular SN2 ring closure to the tetrahydrofuran, releasing HCl',
                },
            },
        },
    },
    ('Chlorohydrin cyclization to tetrahydropyran',): {
        'Reaction': {
            'Reagent': [
                '[Cl][C][C][C][C][C][O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[Cl;H0;+0:2][C:1][C:3][C:5][C:6][C:7][O;H1;+0:4]>>[Cl;H0;-1:2].[C:1][C:3][C:5][C:6][C:7][O;H1;+1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation-equivalent bookkeeping: the alkoxide displaces chloride intramolecularly',
                },
                1: {
                    'Templates': [
                        '[Cl;H0;-1:2].[C:1][C:3][C:5][C:6][C:7][O;H1;+1:4]>>[Cl;H1;+0:2].[C:1]1[C:3][C:5][C:6][C:7][O;H0;+0:4]1',
                    ],
                    'pKa': [None],
                    'Description': 'Intramolecular SN2 ring closure to the tetrahydropyran, releasing HCl',
                },
            },
        },
    },
    ('Epoxide + alcohol ring-opening',): {
        'Reaction': {
            'Reagent': [
                '[C]1[O][C]1',
                '[C][O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]1[O;H0;+0:2][C:3]1.[C:4][O;H1;+0:5]>>[C:1]([O;H0;-1:2])[C:3][O;H1;+1:5][C:4]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of the alcohol oxygen on the epoxide carbon, opening the ring',
                },
                1: {
                    'Templates': [
                        '[C:1]([O;H0;-1:2])[C:3][O;H1;+1:5][C:4]>>[C:1]([O;H1;+0:2])[C:3][O;H0;+0:5][C:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxonium to the alkoxide',
                },
            },
        },
    },
    ('Aziridine + alcohol ring-opening',): {
        'Reaction': {
            'Reagent': [
                '[C]1[N;H1][C]1',
                '[C][O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]1[N;H1;+0:2][C:3]1.[C:4][O;H1;+0:5]>>[C:1]([N;H1;-1:2])[C:3][O;H1;+1:5][C:4]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of the alcohol oxygen on the aziridine carbon, opening the ring',
                },
                1: {
                    'Templates': [
                        '[C:1]([N;H1;-1:2])[C:3][O;H1;+1:5][C:4]>>[C:1]([N;H2;+0:2])[C:3][O;H0;+0:5][C:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxonium to the amide anion',
                },
            },
        },
    },
    ('Epoxide + amine ring-opening',): {
        'Reaction': {
            'Reagent': [
                '[C]1[O][C]1',
                '[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]1[O;H0;+0:2][C:3]1.[N;H2;+0:4]>>[C:1]([O;H0;-1:2])[C:3][N;H2;+1:4]',
                        '[C:1]1[O;H0;+0:2][C:3]1.[N;H1;+0:4]>>[C:1]([O;H0;-1:2])[C:3][N;H1;+1:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Nucleophilic attack of the amine on the epoxide carbon, opening the ring',
                },
                1: {
                    'Templates': [
                        '[C:1]([O;H0;-1:2])[C:3][N;H2;+1:4]>>[C:1]([O;H1;+0:2])[C:3][N;H1;+0:4]',
                        '[C:1]([O;H0;-1:2])[C:3][N;H1;+1:4]>>[C:1]([O;H1;+0:2])[C:3][N;H0;+0:4]',
                    ],
                    'pKa': [None, None],
                    'Description': 'Proton transfer from the ammonium to the alkoxide',
                },
            },
        },
    },
    ('Substituted oxetane + secondary amine ring-opening',): {
        'Reaction': {
            'Reagent': [
                '[C][C]1[C][C][O]1',
                '[C][N;H1][C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C:2]1[C:3][C:4][O;H0;+0:5]1.[C:6][N;H1;+0:7][C:8]>>[C:1][C:2]([O;H0;-1:5])[C:3][C:4][N;H1;+1:7]([C:6])[C:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic attack of the amine on the less hindered oxetane carbon, opening the ring',
                },
                1: {
                    'Templates': [
                        '[C:1][C:2]([O;H0;-1:5])[C:3][C:4][N;H1;+1:7]([C:6])[C:8]>>[C:1][C:2]([O;H1;+0:5])[C:3][C:4][N;H0;+0:7]([C:6])[C:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the ammonium to the alkoxide',
                },
            },
        },
    },
    ('Substituted aziridine + secondary amine double ring-opening',): {
        'Reaction': {
            'Reagent': [
                '[C][C]1[C]([C])[N]1[C]',
                '[C][N;H1][C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:2][C:1]1[C;H1:3]([C:4])[N;H0;+0:5]1[C:6].[C:7][N;H1;+0:8][C:9]>>[C:2][C:1]([N;H0;-1:5][C:6])[C:3]([C:4])[N;H1;+1:8]([C:7])[C:9]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic attack of the amine on the aziridine carbon, opening the ring',
                },
                1: {
                    'Templates': [
                        '[C:2][C:1]([N;H0;-1:5][C:6])[C:3]([C:4])[N;H1;+1:8]([C:7])[C:9]>>[C:2][C:1]([N;H1;+0:5][C:6])[C:3]([C:4])[N;H0;+0:8]([C:7])[C:9]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the ammonium to the amide anion',
                },
            },
        },
    },
    ('Epoxide + HF ring-opening to fluorohydrin',): {
        'Reaction': {
            'Reagent': [
                '[C]1[O][C]1',
                '[F;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]1[O;H0;+0:2][C:3]1.[F;H1;+0:4]>>[C:1]1[O;H1;+1:2][C:3]1.[F;H0;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the epoxide oxygen by HF',
                },
                1: {
                    'Templates': [
                        '[C:1]1[O;H1;+1:2][C:3]1.[F;H0;-1:4]>>[C:1]([F;H0;+0:4])[C:3][O;H1;+0:2]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of fluoride on the epoxide carbon, opening the ring',
                },
            },
        },
    },
    ('Epoxide + HBr ring-opening to bromohydrin',): {
        'Reaction': {
            'Reagent': [
                '[C]1[O][C]1',
                '[Br;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]1[O;H0;+0:2][C:3]1.[Br;H1;+0:4]>>[C:1]1[O;H1;+1:2][C:3]1.[Br;H0;-1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Protonation of the epoxide oxygen by HBr',
                },
                1: {
                    'Templates': [
                        '[C:1]1[O;H1;+1:2][C:3]1.[Br;H0;-1:4]>>[C:1]([Br;H0;+0:4])[C:3][O;H1;+0:2]',
                    ],
                    'pKa': [None],
                    'Description': 'SN2 attack of bromide on the epoxide carbon, opening the ring',
                },
            },
        },
    },
    ('Diels-Alder cycloaddition (diene + alkyne)',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C][C]=[C]',
                '[C]#[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2][C:3]=[C:4].[C:5]#[C:6]>>[C:1]1[C:2]=[C:3][C:4][C:5]=[C:6]1',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted [4+2] cycloaddition of the diene and dienophile',
                },
            },
        },
    },
    ('Hetero-Diels-Alder cycloaddition with nitrile',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C][C]=[C]',
                '[N]#[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2][C:3]=[C:4].[N:5]#[C:6]>>[C:1]1[C:2]=[C:3][C:4][N:5]=[C:6]1',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted [4+2] cycloaddition of the diene and nitrile',
                },
            },
        },
    },
    ('Hetero-Diels-Alder cycloaddition with imine',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C][C]=[C]',
                '[N]=[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2][C:3]=[C:4].[N:5]=[C:6]>>[C:1]1[C:2]=[C:3][C:4][N:5][C:6]1',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted [4+2] cycloaddition of the diene and imine',
                },
            },
        },
    },
    ('Hetero-Diels-Alder cycloaddition with azo compound',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C][C]=[C]',
                '[N]=[N]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2][C:3]=[C:4].[N:5]=[N:6]>>[C:1]1[C:2]=[C:3][C:4][N:5][N:6]1',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted [4+2] cycloaddition of the diene and azo compound',
                },
            },
        },
    },
    ('Hetero-Diels-Alder cycloaddition with nitroso compound',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C][C]=[C]',
                '[O]=[N]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2][C:3]=[C:4].[O:5]=[N:6]>>[C:1]1[C:2]=[C:3][C:4][O:5][N:6]1',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted [4+2] cycloaddition of the diene and nitroso compound',
                },
            },
        },
    },
    ('Hetero-Diels-Alder cycloaddition with carbonyl compound',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C][C]=[C]',
                '[O]=[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2][C:3]=[C:4].[O:5]=[C:6]>>[C:1]1[C:2]=[C:3][C:4][O:5][C:6]1',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted [4+2] cycloaddition of the diene and carbonyl compound',
                },
            },
        },
    },
    ('Ketone + ketene [2+2] cycloaddition to lactone',): {
        'Reaction': {
            'Reagent': [
                '[C][C](=[O])[C]',
                '[C][C](=[C]=[O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C:2](=[O:3])[C:4].[C:5][C:6](=[C:7]=[O:8])[C:9]>>[C:1][13C:2]1([C:4])[17O:3][C:7](=[O:8])[C:6]1([C:5])[C:9]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted [2+2] cycloaddition of the ketone and ketene to give the beta-lactone (isotope-labeled to track atom fates)',
                },
            },
        },
    },
    ('Alkene + carbonyl [2+2] cycloaddition to oxetane',): {
        'Reaction': {
            'Reagent': [
                '[C]=[O]',
                '[C]=[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[O:2].[C:3]=[C:4]>>[C:1]1[O:2][C:3][C:4]1',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted [2+2] cycloaddition of the carbonyl and alkene to give the oxetane',
                },
            },
        },
    },
    ('Imine + ketene [2+2] cycloaddition to beta-lactam',): {
        'Reaction': {
            'Reagent': [
                '[C][C](=[N])[C]',
                '[C][C](=[C]=[O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C:2](=[N:3])[C:4].[C:5][C:6](=[C:7]=[O:8])[C:9]>>[C:1][C:2]1([C:4])[N:3][C:7](=[O:8])[C:6]1([C:5])[C:9]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted [2+2] cycloaddition of the imine and ketene to give the beta-lactam',
                },
            },
        },
    },
    ('Cyclobutene electrocyclic ring-opening',): {
        'Reaction': {
            'Reagent': [
                '[C][C]1[C]=[C][C]1',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C:2]1[C:3]=[C:4][C:5]1>>[C:1][C:2]=[C:3][C:4]=[C:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Conrotatory electrocyclic ring-opening of the cyclobutene to the diene',
                },
            },
        },
    },
    ('Cyclooctatriene electrocyclic ring-opening',): {
        'Reaction': {
            'Reagent': [
                '[C][C]1[C]=[C][C]=[C][C]=[C]1',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C:2]1[C:3]=[C:4][C:5]=[C:6][C:7]=[C:8]1>>[C:1][C:2]=[C:3][C:4]=[C:5][C:6]=[C:7]=[C:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Electrocyclic ring-opening of the cyclooctatriene to the cyclooctatetraene',
                },
            },
        },
    },
    ('Alkene + peracid epoxidation',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]',
                '[C][C](=[O])[O][O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2].[C:3][C:4](=[O:5])[O:6][O;H1:7]>>[C:1]1[C:2][O:7]1.[C:3][C:4](=[O:6])[O:5][H:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted oxygen transfer from the peracid to the alkene, giving the epoxide and the carboxylic acid',
                },
            },
        },
    },
    ('Alpha-chloroester enolization',): {
        'Reaction': {
            'Reagent': [
                '[C][O][C](=[O])[C;H1]([C])[Cl]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][O:2][C:3](=[O:4])[C;H1:5]([C:6])[Cl:7]>>[C:1][O:2][C:3]([O:4][H:8])=[C:5]([C:6])[Cl:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Enolization: proton transfer from the alpha-carbon to the carbonyl oxygen',
                },
            },
        },
    },
    ('Aldoxime dehydration to nitrile',): {
        'Reaction': {
            'Reagent': [
                '[C;H1]=[N][O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;H1:1]=[N:2][O;H1:3]>>[C:1]#[N:2].[H:4][O:3][H:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted anti-periplanar dehydration of the aldoxime to the nitrile',
                },
            },
        },
    },
    ('Amide-iminol tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[O]=[C][N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:3]=[C:1][N;!H0:2]>>[H:4][O:3][C:1]=[N:2]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from nitrogen to oxygen, forming the iminol tautomer of the amide',
                },
            },
        },
    },
    ('Imidic acid dehydration to nitrile',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][C]=[N;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1:3][C:1]=[N;H1:2]>>[C:1]#[N:2].[H:4][O:3][H:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted dehydration of the imidic acid tautomer to the nitrile',
                },
            },
        },
    },
    ('Terminal enol to ketone tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]([O;H1])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2]([O;H1:3])[C:4]>>[H:5][C:1][C:2](=[O:3])[C:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the enol oxygen to the terminal alkene carbon, forming the ketone',
                },
            },
        },
    },
    ('Phenyl ester Fries rearrangement (dearomatizing acyl migration)',): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c][c;H1][c]1[O][C](=[O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:1]1[c:2][c:3][c:4][c;H1:5][c:6]1[O:7][C:8](=[O:9])[C:10]>>[C:1]1=[C:2][C:3]=[C:4][C:5]([H:11])([C:8](=[O:9])[C:10])[C:6]1=[O:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Intramolecular [1,3]-acyl migration from the phenolic oxygen to the ortho ring carbon, dearomatizing the ring',
                },
            },
        },
    },
    ('Cyclohexadienone rearomatization to ortho-acylphenol',): {
        'Reaction': {
            'Reagent': [
                '[C]1=[C][C]=[C][C;H1]([C](=[O])[C])[C]1=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]1=[C:2][C:3]=[C:4][C;H1:5]([C:8](=[O:9])[C:10])[C:6]1=[O:7]>>[c:1]1[c:2][c:3][c:4][c:5]([C:8](=[O:9])[C:10])[c:6]1[O:7][H:11]',
                    ],
                    'pKa': [None],
                    'Description': 'Tautomerization restoring aromaticity, giving the ortho-acylphenol',
                },
            },
        },
    },
    ('Phenyl benzoate Fries rearrangement (dearomatizing acyl migration)',): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c][c;H1][c]1[O][C](=[O])[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:1]1[c:2][c:3][c:4][c;H1:5][c:6]1[O:7][C:8](=[O:9])[c:10]>>[C:1]1=[C:2][C:3]=[C:4][C:5]([H:16])([C:8](=[O:9])[c:10])[C:6]1=[O:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Intramolecular [1,3]-acyl migration from the phenolic oxygen to the ortho ring carbon, dearomatizing the ring',
                },
            },
        },
    },
    ('Benzoyl cyclohexadienone rearomatization to ortho-hydroxybenzophenone',): {
        'Reaction': {
            'Reagent': [
                '[C]1=[C][C]=[C][C;H1]([C](=[O])[c])[C]1=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]1=[C:2][C:3]=[C:4][C;H1:5]([C:8](=[O:9])[c:10])[C:6]1=[O:7]>>[c:1]1[c:2][c:3][c:4][c:5]([C:8](=[O:9])[c:10])[c:6]1[O:7][H:16]',
                    ],
                    'pKa': [None],
                    'Description': 'Tautomerization restoring aromaticity, giving the ortho-hydroxybenzophenone',
                },
            },
        },
    },
    ('Allylic 1,3-hydrogen shift isomerization',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C][C;H1][C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2][C;H1:3][C:4]>>[H:5][C:1][C:2]=[C:3][C:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Suprafacial [1,3]-sigmatropic hydrogen shift moving the double bond position',
                },
            },
        },
    },
    ('Aryl enol to aryl ketone tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C]([O;H1])[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2]([O;H1:3])[c:4]>>[H:10][C:1][C:2](=[O:3])[c:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the enol oxygen to the terminal alkene carbon, forming the aryl ketone',
                },
            },
        },
    },
    ('N-substituted imidate-amide tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[C][C]([O;H1])=[N][C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C:2]([O;H1:4])=[N:3][C:5]>>[C:1][C:2](=[O:4])[N:3]([H:6])[C:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from oxygen to nitrogen, forming the secondary amide',
                },
            },
        },
    },
    ('Aromatic Claisen rearrangement',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C][C]([C])[O][c]1[c][c][c][c][c;H1]1',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2][C:3]([C:4])[O:5][c:6]1[c:7][c:8][c:9][c:10][c;H1:11]1>>[C:1]([C:2]=[C:3][C:4])[C:11]1([H:12])[C:10]=[C:9][C:8]=[C:7][C:6]1=[O:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted [3,3]-sigmatropic rearrangement of the allyl aryl ether, dearomatizing the ring',
                },
            },
        },
    },
    ('Aliphatic Claisen rearrangement',): {
        'Reaction': {
            'Reagent': [
                '[C]=[C][C][O][C]([C])=[C][C][C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]=[C:2][C:3][O:4][C:5]([C:6])=[C:7][C:8][C:9]>>[C:6][C:5](=[O:4])[C:7]([C:8][C:9])[C:1][C:2]=[C:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted [3,3]-sigmatropic rearrangement of the allyl vinyl ether to the gamma,delta-unsaturated carbonyl',
                },
            },
        },
    },
    ('Chapman rearrangement (aryl imidate to N,N-diarylamide)',): {
        'Reaction': {
            'Reagent': [
                '[c][O][C]([c])=[N][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:16][O:1][C:2]([c:10])=[N:3][c:4]>>[c:16][C:2](=[O:1])[N:3]([c:10])[c:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted intramolecular [1,3]-aryl migration from oxygen to nitrogen, giving the N,N-diarylamide',
                },
            },
        },
    },
    ('Aromatic Claisen rearrangement (methallyl ether)',): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c][c][c]1[O][C][C]([C])=[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:1]1[c:2][c:3][c:4][c:5][c:6]1[O:7][C:8][C:9]([C:11])=[C:10]>>[C:1]1=[C:2][C:3]=[C:4][C:5]([C:10][C:9]([C:11])=[C:8])[C:6]1=[O:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted [3,3]-sigmatropic rearrangement of the methallyl aryl ether, dearomatizing the ring',
                },
            },
        },
    },
    ('Cyclohexadienone rearomatization to ortho-methallylphenol',): {
        'Reaction': {
            'Reagent': [
                '[C]1=[C][C]=[C][C]([C][C]([C])=[C])[C]1=[O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]1=[C:2][C:3]=[C:4][C:5]([C:10][C:9]([C:11])=[C:8])[C:6]1=[O:7]>>[c:1]1[c:2][c:3][c:4][c:5]([C:10][C:9]([C:11])=[C:8])[c:6]1[O:7][H:12]',
                    ],
                    'pKa': [None],
                    'Description': 'Tautomerization restoring aromaticity, giving the ortho-methallylphenol',
                },
            },
        },
    },
    ('Intramolecular Markovnikov hydroalkoxylation to dihydrobenzofuran',): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c][c]([C][C]([C])=[C])[c]1[O;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:1]1[c:2][c:3][c:4][c:5]([C:10][C;H0:9]([C:11])=[C;H2:8])[c:6]1[O;H1:7]>>[c:1]1[c:2][c:3][c:4][c:5]([C:10][C;H0;+1:9]([C:11])[C;H3:8])[c:6]1[O;H0;-1:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Intramolecular protonation of the pendant alkene by the phenolic proton, forming a tertiary carbocation and the phenolate',
                },
                1: {
                    'Templates': [
                        '[c:1]1[c:2][c:3][c:4][c:5]([C:10][C;H0;+1:9]([C:11])[C;H3:8])[c:6]1[O;H0;-1:7]>>[c:1]1[c:2][c:3][c:4][c:5]2[c:6]1[O;H0;+0:7][C;H0;+0:9]([C:8])([C:11])[C:10]2',
                    ],
                    'pKa': [None],
                    'Description': 'Intramolecular attack of the phenolate oxygen on the carbocation, closing the dihydrobenzofuran ring',
                },
            },
        },
    },
    ('Abnormal Claisen rearrangement to dihydrobenzofuran',): {
        'Reaction': {
            'Reagent': [
                '[c]1[c][c][c][c;H1][c]1[O][C][C]([C])=[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:1]1[c:2][c:3][c:4][c;H1:5][c:6]1[O:7][C:8][C:9]([C:11])=[C:10]>>[c:1]1[c:2][c:3][c:4][c:5]2[c:6]1[O:7][C:8][C:9]2([C:10][H:12])[C:11]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted double sigmatropic rearrangement of the methallyl aryl ether directly to the fused dihydrobenzofuran',
                },
            },
        },
    },
    ('Ketene hydration to carboxylic acid',): {
        'Reaction': {
            'Reagent': [
                '[C][C]=[C]=[O]',
                '[O;H2]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C:2]=[C:3]=[O:4].[O;H2;+0:5]>>[C:1][C;H1;-1:2][C:3](=[O:4])[O;H2;+1:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of water to the central ketene carbon, forming a carbanion-oxocarbenium zwitterion',
                },
                1: {
                    'Templates': [
                        '[C:1][C;H1;-1:2][C:3](=[O:4])[O;H2;+1:5]>>[C:1][C;H2;+0:2][C:3](=[O:4])[O;H1;+0:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxocarbenium to the carbanion, giving the neutral carboxylic acid',
                },
            },
        },
    },
    ('Phenylketene hydration to arylacetic acid',): {
        'Reaction': {
            'Reagent': [
                '[c][C]=[C]=[O]',
                '[O;H2]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:10][C:3]=[C:1]=[O:2].[O;H2;+0:4]>>[c:10][C;H1;-1:3][C:1](=[O:2])[O;H2;+1:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of water to the central ketene carbon, forming a benzylic carbanion-oxocarbenium zwitterion',
                },
                1: {
                    'Templates': [
                        '[c:10][C;H1;-1:3][C:1](=[O:2])[O;H2;+1:4]>>[c:10][C;H2;+0:3][C:1](=[O:2])[O;H1;+0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxocarbenium to the benzylic carbanion, giving the neutral arylacetic acid',
                },
            },
        },
    },
    ('Alpha-diazoiminium decomposition to isocyanate',): {
        'Reaction': {
            'Reagent': [
                '[C][N;+1]([N]=[N;-1])=[C][O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][N;+1:2]([N:3]=[N;-1:4])=[C:5][O:6]>>[C:1][N;+0:2]=[C:5]=[O:6].[N:3]#[N;+0:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted extrusion of nitrogen gas with 1,2-migration, giving the isocyanate',
                },
            },
        },
    },
    ('Nitrile hydration to imidic acid',): {
        'Reaction': {
            'Reagent': [
                '[C]#[N]',
                '[O;H2]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1]#[N;H0;+0:2].[O;H2;+0:3]>>[C:1](=[N;H0;-1:2])[O;H2;+1:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of water to the nitrile carbon, forming an imidate anion-oxocarbenium zwitterion',
                },
                1: {
                    'Templates': [
                        '[C:1](=[N;H0;-1:2])[O;H2;+1:3]>>[C:1](=[N;H1;+0:2])[O;H1;+0:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from the oxocarbenium to the nitrogen, giving the neutral imidic acid',
                },
            },
        },
    },
    ('Imidic acid to primary amide tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][C]=[N;H1]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1:3][C:1]=[N;H1:2]>>[O:3]=[C:1][N:2]([H:4])([H:5])',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from oxygen to nitrogen, forming the primary amide',
                },
            },
        },
    },
    ('Ketone + hydroxylamine nucleophilic addition',): {
        'Reaction': {
            'Reagent': [
                '[C][C](=[O])[C]',
                '[N;H2][O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C:2](=[O;H0;+0:3]).[N;H2;+0:4][O:5]>>[C:1][C:2]([O;H0;-1:3])[N;H2;+1:4][O:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of hydroxylamine nitrogen to the carbonyl carbon',
                },
                1: {
                    'Templates': [
                        '[C:1][C:2]([O;H0;-1:3])[N;H2;+1:4][O:5]>>[C:1][C:2]([O;H1;+0:3])[N;H1;+0:4][O:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from nitrogen to the alkoxide, giving the neutral hemiaminal',
                },
            },
        },
    },
    ('Hemiaminal dehydration to oxime',): {
        'Reaction': {
            'Reagent': [
                '[C][C]([O;H1])([N;H1][O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:1][C:2]([O;H1:3])([N;H1:4][O:5])[C:6]>>[C:1][C:2](=[N:4][O:5])[C:6].[H:7][O:3][H:8]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type dehydration of the hemiaminal, giving the oxime',
                },
            },
        },
    },
    ('Aryl ketone + hydroxylamine nucleophilic addition',): {
        'Reaction': {
            'Reagent': [
                '[c][C](=[O])',
                '[N;H2][O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:10][C:1](=[O;H0;+0:2]).[N;H2;+0:3][O:4]>>[c:10][C:1]([O;H0;-1:2])[N;H2;+1:3][O:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of hydroxylamine nitrogen to the carbonyl carbon',
                },
                1: {
                    'Templates': [
                        '[c:10][C:1]([O;H0;-1:2])[N;H2;+1:3][O:4]>>[c:10][C:1]([O;H1;+0:2])[N;H1;+0:3][O:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Proton transfer from nitrogen to the alkoxide, giving the neutral hemiaminal',
                },
            },
        },
    },
    ('Aryl hemiaminal dehydration to aryl oxime',): {
        'Reaction': {
            'Reagent': [
                '[c][C]([O;H1])[N;H1][O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:10][C:1]([O;H1:2])[N;H1:3][O:4]>>[c:10][C:1]=[N:3][O:4].[H:11][O:2][H:12]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type dehydration of the hemiaminal, giving the aryl oxime',
                },
            },
        },
    },
    ('Ester alpha-nitroso to oxime tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][C;!H0][C](=[O])[O][C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][C;!H0:3][C:4](=[O:5])[O:6][C:7]>>[H:8][O:1][N:2]=[C:3][C:4](=[O:5])[O:6][C:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Nitroso-oxime tautomerization: proton transfer from the alpha-carbon to the nitroso oxygen',
                },
            },
        },
    },
    ('Ester nitrosation ene-addition (methyl substrate)',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][O]',
                '[C;H3][C](=[O])[O][C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][O:3].[C;H3:4][C:5](=[O:6])[O:7][C:8]>>[O:3][N:2]([O:1][H:9])[C;H2:4][C:5](=[O:6])[O:7][C:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted ene-type addition of nitrous acid across the enolizable methyl group, giving the N,N-dihydroxylamino adduct',
                },
            },
        },
    },
    ('Ester N,N-dihydroxylamino adduct elimination to nitroso',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][N]([O;H1])[C][C](=[O])[O][C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1:3][N:2]([O;H1:1])[C:4][C:5](=[O:6])[O:7][C:8]>>[O:3]=[N:2][C:4][C:5](=[O:6])[O:7][C:8].[H:9][O:1][H:10]',
                    ],
                    'pKa': [None],
                    'Description': 'Retro-ene-type elimination of water from the adduct, regenerating the alpha-nitroso compound',
                },
            },
        },
    },
    ('Ester N,N-dihydroxylamino adduct elimination to oxime ether',): {
        'Reaction': {
            'Reagent': [
                '[O][N]([O;H1])[C;!H0][C](=[O])[O][C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:3][N:2]([O;H1:1])[C;!H0:4][C:5](=[O:6])[O:7][C:8]>>[O:3][N:2]=[C:4][C:5](=[O:6])[O:7][C:8].[H:9][O:1][H:10]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the oxime ether directly',
                },
            },
        },
    },
    ('Aryl ester alpha-nitroso to oxime tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][C;!H0][C](=[O])[O][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][C;!H0:3][C:4](=[O:5])[O:6][c:7]>>[H:13][O:1][N:2]=[C:3][C:4](=[O:5])[O:6][c:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Nitroso-oxime tautomerization: proton transfer from the alpha-carbon to the nitroso oxygen',
                },
            },
        },
    },
    ('Aryl ester nitrosation ene-addition (methyl substrate)',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][O]',
                '[C;H3][C](=[O])[O][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][O:3].[C;H3:4][C:5](=[O:6])[O:7][c:8]>>[O:3][N:2]([O:1][H:14])[C;H2:4][C:5](=[O:6])[O:7][c:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted ene-type addition of nitrous acid across the enolizable methyl group, giving the N,N-dihydroxylamino adduct',
                },
            },
        },
    },
    ('Aryl ester N,N-dihydroxylamino adduct elimination to nitroso',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][N]([O;H1])[C][C](=[O])[O][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1:3][N:2]([O;H1:1])[C:4][C:5](=[O:6])[O:7][c:8]>>[O:3]=[N:2][C:4][C:5](=[O:6])[O:7][c:8].[H:14][O:1][H:15]',
                    ],
                    'pKa': [None],
                    'Description': 'Retro-ene-type elimination of water from the adduct, regenerating the alpha-nitroso compound',
                },
            },
        },
    },
    ('Aryl ester N,N-dihydroxylamino adduct elimination to oxime ether',): {
        'Reaction': {
            'Reagent': [
                '[O][N]([O;H1])[C;!H0][C](=[O])[O][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:3][N:2]([O;H1:1])[C;!H0:4][C:5](=[O:6])[O:7][c:8]>>[O:3][N:2]=[C:4][C:5](=[O:6])[O:7][c:8].[H:14][O:1][H:15]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the oxime ether directly',
                },
            },
        },
    },
    ('Ketone/aldehyde alpha-nitroso to oxime tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][C;!H0][C](=[O])',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][C;!H0:3][C:4](=[O:5])>>[H:6][O:1][N:2]=[C:3][C:4](=[O:5])',
                    ],
                    'pKa': [None],
                    'Description': 'Nitroso-oxime tautomerization: proton transfer from the alpha-carbon to the nitroso oxygen',
                },
            },
        },
    },
    ('Ketone/aldehyde nitrosation ene-addition (methyl substrate)',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][O]',
                '[C;H3][C](=[O])',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][O:3].[C;H3:4][C:5](=[O:6])>>[O:3][N:2]([O:1][H:7])[C;H2:4][C:5](=[O:6])',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted ene-type addition of nitrous acid across the enolizable methyl group, giving the N,N-dihydroxylamino adduct',
                },
            },
        },
    },
    ('Ketone/aldehyde N,N-dihydroxylamino adduct elimination to nitroso',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][N]([O;H1])[C][C](=[O])',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1:3][N:2]([O;H1:1])[C:4][C:5](=[O:6])>>[O:3]=[N:2][C:4][C:5](=[O:6]).[H:7][O:1][H:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Retro-ene-type elimination of water from the adduct, regenerating the alpha-nitroso compound',
                },
            },
        },
    },
    ('Ketone/aldehyde N,N-dihydroxylamino adduct elimination to oxime ether',): {
        'Reaction': {
            'Reagent': [
                '[O][N]([O;H1])[C;!H0][C](=[O])',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:3][N:2]([O;H1:1])[C;!H0:4][C:5](=[O:6])>>[O:3][N:2]=[C:4][C:5](=[O:6]).[H:7][O:1][H:8]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the oxime ether directly',
                },
            },
        },
    },
    ('Aryl ketone alpha-nitroso to oxime tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][C;!H0][C](=[O])[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][C;!H0:3][C:4](=[O:5])[c:6]>>[H:12][O:1][N:2]=[C:3][C:4](=[O:5])[c:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Nitroso-oxime tautomerization: proton transfer from the alpha-carbon to the nitroso oxygen',
                },
            },
        },
    },
    ('Aryl ketone nitrosation ene-addition (methyl substrate)',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][O]',
                '[C;H3][C](=[O])[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][O:3].[C;H3:4][C:5](=[O:6])[c:7]>>[O:3][N:2]([O:1][H:13])[C;H2:4][C:5](=[O:6])[c:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted ene-type addition of nitrous acid across the enolizable methyl group, giving the N,N-dihydroxylamino adduct',
                },
            },
        },
    },
    ('Aryl ketone N,N-dihydroxylamino adduct elimination to nitroso',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][N]([O;H1])[C][C](=[O])[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1:3][N:2]([O;H1:1])[C:4][C:5](=[O:6])[c:7]>>[O:3]=[N:2][C:4][C:5](=[O:6])[c:7].[H:13][O:1][H:14]',
                    ],
                    'pKa': [None],
                    'Description': 'Retro-ene-type elimination of water from the adduct, regenerating the alpha-nitroso compound',
                },
            },
        },
    },
    ('Aryl ketone N,N-dihydroxylamino adduct elimination to oxime ether',): {
        'Reaction': {
            'Reagent': [
                '[O][N]([O;H1])[C;!H0][C](=[O])[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:3][N:2]([O;H1:1])[C;!H0:4][C:5](=[O:6])[c:7]>>[O:3][N:2]=[C:4][C:5](=[O:6])[c:7].[H:13][O:1][H:14]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the oxime ether directly',
                },
            },
        },
    },
    ('Amide alpha-nitroso to oxime tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][C;!H0][C](=[O])[N]([C])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][C;!H0:3][C:4](=[O:5])[N:6]([C:7])[C:8]>>[H:9][O:1][N:2]=[C:3][C:4](=[O:5])[N:6]([C:7])[C:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Nitroso-oxime tautomerization: proton transfer from the alpha-carbon to the nitroso oxygen',
                },
            },
        },
    },
    ('Amide nitrosation ene-addition (methyl substrate)',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][O]',
                '[C;H3][C](=[O])[N]([C])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][O:3].[C;H3:4][C:5](=[O:6])[N:7]([C:8])[C:9]>>[O:3][N:2]([O:1][H:10])[C;H2:4][C:5](=[O:6])[N:7]([C:8])[C:9]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted ene-type addition of nitrous acid across the enolizable methyl group, giving the N,N-dihydroxylamino adduct',
                },
            },
        },
    },
    ('Amide N,N-dihydroxylamino adduct elimination to nitroso',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][N]([O;H1])[C][C](=[O])[N]([C])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1:3][N:2]([O;H1:1])[C:4][C:5](=[O:6])[N:7]([C:8])[C:9]>>[O:3]=[N:2][C:4][C:5](=[O:6])[N:7]([C:8])[C:9].[H:10][O:1][H:11]',
                    ],
                    'pKa': [None],
                    'Description': 'Retro-ene-type elimination of water from the adduct, regenerating the alpha-nitroso compound',
                },
            },
        },
    },
    ('Amide N,N-dihydroxylamino adduct elimination to oxime ether',): {
        'Reaction': {
            'Reagent': [
                '[O][N]([O;H1])[C;!H0][C](=[O])[N]([C])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:3][N:2]([O;H1:1])[C;!H0:4][C:5](=[O:6])[N:7]([C:8])[C:9]>>[O:3][N:2]=[C:4][C:5](=[O:6])[N:7]([C:8])[C:9].[H:10][O:1][H:11]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the oxime ether directly',
                },
            },
        },
    },
    ('Sulfoxide alpha-nitroso to oxime tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][C;!H0][S](=[O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][C;!H0:3][S:4](=[O:5])[C:6]>>[H:7][O:1][N:2]=[C:3][S:4](=[O:5])[C:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Nitroso-oxime tautomerization: proton transfer from the alpha-carbon to the nitroso oxygen',
                },
            },
        },
    },
    ('Sulfoxide nitrosation ene-addition (methyl substrate)',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][O]',
                '[C;H3][S](=[O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][O:3].[C;H3:4][S:5](=[O:6])[C:7]>>[O:3][N:2]([O:1][H:8])[C;H2:4][S:5](=[O:6])[C:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted ene-type addition of nitrous acid across the enolizable methyl group',
                },
            },
        },
    },
    ('Sulfoxide N,N-dihydroxylamino adduct elimination to nitroso',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][N]([O;H1])[C][S](=[O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1:3][N:2]([O;H1:1])[C:4][S:5](=[O:6])[C:7]>>[O:3]=[N:2][C:4][S:5](=[O:6])[C:7].[H:8][O:1][H:9]',
                    ],
                    'pKa': [None],
                    'Description': 'Retro-ene-type elimination of water from the adduct, regenerating the alpha-nitroso sulfoxide',
                },
            },
        },
    },
    ('Sulfoxide N,N-dihydroxylamino adduct elimination to oxime ether',): {
        'Reaction': {
            'Reagent': [
                '[O][N]([O;H1])[C;H2][S](=[O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:3][N:2]([O;H1:1])[C;H2:4][S:5](=[O:6])[C:7]>>[O:3][N:2]=[C;H1:4][S:5](=[O:6])[C:7].[H:8][O:1][H:9]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the oxime ether directly',
                },
            },
        },
    },
    ('Aryl sulfoxide alpha-nitroso to oxime tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][C;!H0][S](=[O])[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][C;!H0:3][S:4](=[O:5])[c:6]>>[H:12][O:1][N:2]=[C:3][S:4](=[O:5])[c:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Nitroso-oxime tautomerization: proton transfer from the alpha-carbon to the nitroso oxygen',
                },
            },
        },
    },
    ('Aryl sulfoxide nitrosation ene-addition (methyl substrate)',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][O]',
                '[C;H3][S](=[O])[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][O:3].[C;H3:4][S:5](=[O:6])[c:7]>>[O:3][N:2]([O:1][H:13])[C;H2:4][S:5](=[O:6])[c:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted ene-type addition of nitrous acid across the enolizable methyl group',
                },
            },
        },
    },
    ('Aryl sulfoxide N,N-dihydroxylamino adduct elimination to nitroso',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][N]([O;H1])[C][S](=[O])[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1:3][N:2]([O;H1:1])[C:4][S:5](=[O:6])[c:7]>>[O:3]=[N:2][C:4][S:5](=[O:6])[c:7].[H:13][O:1][H:14]',
                    ],
                    'pKa': [None],
                    'Description': 'Retro-ene-type elimination of water from the adduct, regenerating the alpha-nitroso aryl sulfoxide',
                },
            },
        },
    },
    ('Aryl sulfoxide N,N-dihydroxylamino adduct elimination to oxime ether',): {
        'Reaction': {
            'Reagent': [
                '[O][N]([O;H1])[C;!H0][S](=[O])[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:3][N:2]([O;H1:1])[C;!H0:4][S:5](=[O:6])[c:7]>>[O:3][N:2]=[C:4][S:5](=[O:6])[c:7].[H:13][O:1][H:14]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the oxime ether directly',
                },
            },
        },
    },
    ('Sulfone alpha-nitroso to oxime tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][C;!H0][S](=[O])(=[O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][C;!H0:3][S:4](=[O:5])(=[O:6])[C:7]>>[H:8][O:1][N:2]=[C:3][S:4](=[O:5])(=[O:6])[C:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Nitroso-oxime tautomerization: proton transfer from the alpha-carbon to the nitroso oxygen',
                },
            },
        },
    },
    ('Sulfone nitrosation ene-addition (methyl substrate)',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][O]',
                '[C;H3][S](=[O])(=[O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][O:3].[C;H3:4][S:5](=[O:6])(=[O:7])[C:8]>>[O:3][N:2]([O:1][H:9])[C;H2:4][S:5](=[O:6])(=[O:7])[C:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted ene-type addition of nitrous acid across the enolizable methyl group',
                },
            },
        },
    },
    ('Sulfone N,N-dihydroxylamino adduct elimination to nitroso',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][N]([O;H1])[C][S](=[O])(=[O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1:3][N:2]([O;H1:1])[C:4][S:5](=[O:6])(=[O:7])[C:8]>>[O:3]=[N:2][C:4][S:5](=[O:6])(=[O:7])[C:8].[H:9][O:1][H:10]',
                    ],
                    'pKa': [None],
                    'Description': 'Retro-ene-type elimination of water from the adduct, regenerating the alpha-nitroso sulfone',
                },
            },
        },
    },
    ('Sulfone N,N-dihydroxylamino adduct elimination to oxime ether',): {
        'Reaction': {
            'Reagent': [
                '[O][N]([O;H1])[C;!H0][S](=[O])(=[O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:3][N:2]([O;H1:1])[C;!H0:4][S:5](=[O:6])(=[O:7])[C:8]>>[O:3][N:2]=[C:4][S:5](=[O:6])(=[O:7])[C:8].[H:9][O:1][H:10]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the oxime ether directly',
                },
            },
        },
    },
    ('Alkylhydroxylamine alpha-C nitrosation',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][O;H1]',
                '[C;!H0][N][O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][O;H1:3].[C;!H0:4][N:5][O:6]>>[O:1]=[N:2][C:4][N:5][O:6].[H:7][O:3][H:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Nitrosation of the carbon alpha to the hydroxylamino nitrogen',
                },
            },
        },
    },
    ('Alkylhydroxylamine alpha-nitroso to oxime tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][C;!H0][N][O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][C;!H0:3][N:4][O:5]>>[H:6][O:1][N:2]=[C:3][N:4][O:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Nitroso-oxime tautomerization: proton transfer from the alpha-carbon to the nitroso oxygen',
                },
            },
        },
    },
    ('Alkylhydroxylamine nitrosation ene-addition (methyl substrate)',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][O]',
                '[C;H3][N][O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][O:3].[C;H3:4][N:5][O:6]>>[O:3][N:2]([O:1][H:7])[C;H2:4][N:5][O:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted ene-type addition of nitrous acid across the enolizable methyl group',
                },
            },
        },
    },
    ('Alkylhydroxylamine N,N-dihydroxylamino adduct elimination to nitroso',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][N]([O;H1])[C][N][O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1:3][N:2]([O;H1:1])[C:4][N:5][O:6]>>[O:3]=[N:2][C:4][N:5][O:6].[H:7][O:1][H:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Retro-ene-type elimination of water from the adduct, regenerating the alpha-nitroso compound',
                },
            },
        },
    },
    ('Alkylhydroxylamine N,N-dihydroxylamino adduct elimination to oxime ether',): {
        'Reaction': {
            'Reagent': [
                '[O][N]([O;H1])[C;!H0][N][O]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:3][N:2]([O;H1:1])[C;!H0:4][N:5][O:6]>>[O:3][N:2]=[C:4][N:5][O:6].[H:7][O:1][H:8]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the oxime ether directly',
                },
            },
        },
    },
    ('Nitrosamine to diazohydroxide tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][N;!H0:3]>>[H:4][O:1][N:2]=[N:3]',
                    ],
                    'pKa': [None],
                    'Description': 'Tautomerization of the N-nitrosamine to the diazohydroxide, proton transfer from nitrogen to oxygen',
                },
            },
        },
    },
    ('Amine nitrosation ene-addition',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][O]',
                '[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][O:3].[N;!H0:4]>>[O:3][N:2]([O:1][H:5])[N:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the amine nitrogen to the nitrous acid nitrogen, forming the N,N-dihydroxylamino-type adduct',
                },
            },
        },
    },
    ('Amine N,N-dihydroxylamino-type adduct elimination to nitrosamine',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][N]([O;H1])[N]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1:3][N:2]([O;H1:1])[N:4]>>[O:3]=[N:2][N:4].[H:5][O:1][H:6]',
                    ],
                    'pKa': [None],
                    'Description': 'Elimination of water from the adduct, giving the N-nitrosamine',
                },
            },
        },
    },
    ('Amine N,N-dihydroxylamino-type adduct elimination to diazohydroxide',): {
        'Reaction': {
            'Reagent': [
                '[O][N]([O;H1])[N;!H0]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:3][N:2]([O;H1:1])[N;!H0:4]>>[O:3][N:2]=[N:4].[H:5][O:1][H:6]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the N-H, giving the diazohydroxide directly',
                },
            },
        },
    },
    ('Aniline N-nitrosation to N-nitrosoaniline',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][O;H1]',
                '[N;!H0][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][O;H1:3].[N;!H0:4][c:5]>>[O:1]=[N:2][N:4][c:5].[H:11][O:3][H:12]',
                    ],
                    'pKa': [None],
                    'Description': 'N-nitrosation of the aniline nitrogen by nitrous acid',
                },
            },
        },
    },
    ('N-nitrosoaniline to phenyldiazohydroxide tautomerization',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][N;H1][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][N;H1:3][c:4]>>[H:10][O:1][N:2]=[N:3][c:4]',
                    ],
                    'pKa': [None],
                    'Description': 'Tautomerization of the N-nitrosoaniline to the phenyldiazohydroxide',
                },
            },
        },
    },
    ('Aniline nitrosation ene-addition',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][O]',
                '[N;!H0][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][O:3].[N;!H0:4][c:5]>>[O:3][N:2]([O:1][H:11])[N:4][c:5]',
                    ],
                    'pKa': [None],
                    'Description': 'Nucleophilic addition of the aniline nitrogen to the nitrous acid nitrogen, forming the N,N-dihydroxylamino-type adduct',
                },
            },
        },
    },
    ('Aniline N,N-dihydroxylamino-type adduct elimination to N-nitrosoaniline',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][N]([O;H1])[N][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1:3][N:2]([O;H1:1])[N:4][c:5]>>[O:3]=[N:2][N:4][c:5].[H:11][O:1][H:12]',
                    ],
                    'pKa': [None],
                    'Description': 'Elimination of water from the adduct, giving the N-nitrosoaniline',
                },
            },
        },
    },
    ('Aniline N,N-dihydroxylamino-type adduct elimination to phenyldiazohydroxide',): {
        'Reaction': {
            'Reagent': [
                '[O][N]([O;H1])[N;H1][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:3][N:2]([O;H1:1])[N;H1:4][c:5]>>[O:3][N:2]=[N:4][c:5].[H:11][O:1][H:12]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the anilino N-H, giving the phenyldiazohydroxide directly',
                },
            },
        },
    },
    ('Nitrile N,N-dihydroxylamino adduct elimination to nitroso',): {
        'Reaction': {
            'Reagent': [
                '[O;H1][N]([O;H1])[C][C]#[N]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O;H1:3][N:2]([O;H1:1])[C:4][C:5]#[N:6]>>[O:3]=[N:2][C:4][C:5]#[N:6].[H:7][O:1][H:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Retro-ene-type elimination of water from the adduct, regenerating the alpha-nitroso nitrile',
                },
            },
        },
    },
    ('Nitrile N,N-dihydroxylamino adduct elimination to oxime ether',): {
        'Reaction': {
            'Reagent': [
                '[O][N]([O;H1])[C;!H0][C]#[N]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:3][N:2]([O;H1:1])[C;!H0:4][C:5]#[N:6]>>[O:3][N:2]=[C:4][C:5]#[N:6].[H:7][O:1][H:8]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the oxime ether directly',
                },
            },
        },
    },
    ('Aryl ester N-alkyl-N-hydroxyamino adduct elimination to N-alkylidene',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][N]([O;H1])[C][C](=[O])[O][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:3][N:2]([O;H1:1])[C:4][C:5](=[O:6])[O:7][c:8]>>[C:3]=[N:2][C:4][C:5](=[O:6])[O:7][c:8].[H:14][O:1][H:15]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the N-alkyl C-H, giving the N-alkylidene',
                },
            },
        },
    },
    ('Aryl ester N-alkyl-N-hydroxyamino adduct elimination to oxime ether',): {
        'Reaction': {
            'Reagent': [
                '[C][N]([O;H1])[C;!H0][C](=[O])[O][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:3][N:2]([O;H1:1])[C;!H0:4][C:5](=[O:6])[O:7][c:8]>>[C:3][N:2]=[C:4][C:5](=[O:6])[O:7][c:8].[H:14][O:1][H:15]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the oxime ether',
                },
            },
        },
    },
    ('Ketone N-alkyl-N-hydroxyamino adduct elimination to N-alkylidene',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][N]([O;H1])[C][C](=[O])',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:3][N:2]([O;H1:1])[C:4][C:5](=[O:6])>>[C:3]=[N:2][C:4][C:5](=[O:6]).[H:7][O:1][H:8]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the N-alkyl C-H, giving the N-alkylidene',
                },
            },
        },
    },
    ('Ketone N-alkyl-N-hydroxyamino adduct elimination to oxime ether',): {
        'Reaction': {
            'Reagent': [
                '[C][N]([O;H1])[C;!H0][C](=[O])',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:3][N:2]([O;H1:1])[C;!H0:4][C:5](=[O:6])>>[C:3][N:2]=[C:4][C:5](=[O:6]).[H:7][O:1][H:8]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the oxime ether',
                },
            },
        },
    },
    ('Aryl sulfoxide nitrosation ene-addition (C-nitroso electrophile)',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][C]',
                '[C;H3][S](=[O])[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][C:3].[C;H3:4][S:5](=[O:6])[c:7]>>[C:3][N:2]([O:1][H:13])[C;H2:4][S:5](=[O:6])[c:7]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted ene-type addition of the C-nitroso compound across the enolizable methyl group',
                },
            },
        },
    },
    ('Aryl sulfoxide N-alkyl-N-hydroxyamino adduct elimination to N-alkylidene',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][N]([O;H1])[C][S](=[O])[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:3][N:2]([O;H1:1])[C:4][S:5](=[O:6])[c:7]>>[C:3]=[N:2][C:4][S:5](=[O:6])[c:7].[H:13][O:1][H:14]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the N-alkyl C-H, giving the N-alkylidene',
                },
            },
        },
    },
    ('Aryl sulfoxide N-alkyl-N-hydroxyamino adduct elimination to oxime ether',): {
        'Reaction': {
            'Reagent': [
                '[C][N]([O;H1])[C;!H0][S](=[O])[c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:3][N:2]([O;H1:1])[C;!H0:4][S:5](=[O:6])[c:7]>>[C:3][N:2]=[C:4][S:5](=[O:6])[c:7].[H:13][O:1][H:14]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the oxime ether',
                },
            },
        },
    },
    ('Sulfone nitrosation ene-addition (C-nitroso electrophile)',): {
        'Reaction': {
            'Reagent': [
                '[O]=[N][C]',
                '[C;H3][S](=[O])(=[O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[O:1]=[N:2][C:3].[C;H3:4][S:5](=[O:6])(=[O:7])[C:8]>>[C:3][N:2]([O:1][H:9])[C;H2:4][S:5](=[O:6])(=[O:7])[C:8]',
                    ],
                    'pKa': [None],
                    'Description': 'Concerted ene-type addition of the C-nitroso compound across the enolizable methyl group',
                },
            },
        },
    },
    ('Sulfone N-alkyl-N-hydroxyamino adduct elimination to N-alkylidene',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][N]([O;H1])[C][S](=[O])(=[O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:3][N:2]([O;H1:1])[C:4][S:5](=[O:6])(=[O:7])[C:8]>>[C:3]=[N:2][C:4][S:5](=[O:6])(=[O:7])[C:8].[H:9][O:1][H:10]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the N-alkyl C-H, giving the N-alkylidene',
                },
            },
        },
    },
    ('Sulfone N-alkyl-N-hydroxyamino adduct elimination to oxime ether',): {
        'Reaction': {
            'Reagent': [
                '[C][N]([O;H1])[C;!H0][S](=[O])(=[O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:3][N:2]([O;H1:1])[C;!H0:4][S:5](=[O:6])(=[O:7])[C:8]>>[C:3][N:2]=[C:4][S:5](=[O:6])(=[O:7])[C:8].[H:9][O:1][H:10]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the oxime ether',
                },
            },
        },
    },
    ('Phenylhydrazine N-alkyl-N-hydroxyamino adduct elimination to alkylidene phenylhydrazine',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][N]([O;H1])[N][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:3][N:2]([O;H1:1])[N:4][c:5]>>[C:3]=[N:2][N:4][c:5].[H:11][O:1][H:12]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the N-alkyl C-H, giving the alkylidene phenylhydrazine',
                },
            },
        },
    },
    ('Phenylhydrazine adduct elimination to alkyl phenyl diazene',): {
        'Reaction': {
            'Reagent': [
                '[C][N]([O;H1])[N;H1][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:3][N:2]([O;H1:1])[N;H1:4][c:5]>>[C:3][N:2]=[N:4][c:5].[H:11][O:1][H:12]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the anilino N-H, giving the alkyl phenyl diazene',
                },
            },
        },
    },
    ('Nitrile N-alkyl-N-hydroxyamino adduct elimination to N-alkylidene',): {
        'Reaction': {
            'Reagent': [
                '[C;!H0][N]([O;H1])[C][C]#[N]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C;!H0:3][N:2]([O;H1:1])[C:4][C:5]#[N:6]>>[C:3]=[N:2][C:4][C:5]#[N:6].[H:7][O:1][H:8]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the N-alkyl C-H, giving the N-alkylidene',
                },
            },
        },
    },
    ('Nitrile N-alkyl-N-hydroxyamino adduct elimination to oxime ether',): {
        'Reaction': {
            'Reagent': [
                '[C][N]([O;H1])[C;!H0][C]#[N]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[C:3][N:2]([O;H1:1])[C;!H0:4][C:5]#[N:6]>>[C:3][N:2]=[C:4][C:5]#[N:6].[H:7][O:1][H:8]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the oxime ether',
                },
            },
        },
    },
    ('Aryl ester N-aryl-N-hydroxyamino adduct elimination to Schiff base',): {
        'Reaction': {
            'Reagent': [
                '[c][N]([O;H1])[C;!H0][C](=[O])[O][c]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:18][N:2]([O;H1:1])[C;!H0:3][C:4](=[O:5])[O:6][c:7]>>[c:18][N:2]=[C:3][C:4](=[O:5])[O:6][c:7].[H:19][O:1][H:20]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the N-aryl Schiff base',
                },
            },
        },
    },
    ('Ketone N-aryl-N-hydroxyamino adduct elimination to Schiff base',): {
        'Reaction': {
            'Reagent': [
                '[c][N]([O;H1])[C;!H0][C](=[O])',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:3][N:2]([O;H1:1])[C;!H0:4][C:5](=[O:6])>>[c:3][N:2]=[C:4][C:5](=[O:6]).[H:12][O:1][H:13]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the N-aryl Schiff base',
                },
            },
        },
    },
    ('Sulfone N-aryl-N-hydroxyamino adduct elimination to Schiff base',): {
        'Reaction': {
            'Reagent': [
                '[c][N]([O;H1])[C;!H0][S](=[O])(=[O])[C]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:3][N:2]([O;H1:1])[C;!H0:4][S:5](=[O:6])(=[O:7])[C:8]>>[c:3][N:2]=[C:4][S:5](=[O:6])(=[O:7])[C:8].[H:14][O:1][H:15]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the N-aryl Schiff base',
                },
            },
        },
    },
    ('Nitrile N-aryl-N-hydroxyamino adduct elimination to Schiff base',): {
        'Reaction': {
            'Reagent': [
                '[c][N]([O;H1])[C;!H0][C]#[N]',
            ],
            'Exclude_reagent': None,
            'Stages': {
                0: {
                    'Templates': [
                        '[c:3][N:2]([O;H1:1])[C;!H0:4][C:5]#[N:6]>>[c:3][N:2]=[C:4][C:5]#[N:6].[H:12][O:1][H:13]',
                    ],
                    'pKa': [None],
                    'Description': 'E1cb-type elimination of water using the alpha C-H, giving the N-aryl Schiff base',
                },
            },
        },
    },
}

import re
import rdflib


class KnowledgeGraphAgent:
    """Base Knowledge Graph Agent"""

    prefix_rdf = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>'
    prefix_ontomo = ('PREFIX ontomo: '
                     '<https://github.com/zhangsy-ryan/KIDoE/main/ontology/OntoMo.owl#>')
    prefix = '\n'.join([prefix_rdf, prefix_ontomo, ''])
    pheno_classes = [
        'Accumulation',
        'FlowPattern',
        'MassTransportPhenomenon',
        'MassEquilibriumPhenomenon',
        'ReactionPhenomenon'
    ]
    var_classes = [
        'Constant',
        'RateVariable',
        'StateVariable',
        'FlowParameter',
        'PhysicsParameter',
        'ReactionParameter',
        'StructureParameter',
        'OperationParameter',
        'MassTransportParameter'
    ]

    def __init__(self, rdf_path: str):
        self.rdf_path = rdf_path
        self.rdf = rdflib.Graph()
        self.rdf.parse(rdf_path)

    def run(self, sparql: str):
        return self.rdf.query(sparql)

    def query(self):
        pheno_dict = self.query_pheno()
        dim_dict = self.query_dim()
        var_dict = self.query_var()
        law_dict = self.query_law()
        unit_dict = self.query_unit()
        return {
            'pheno': pheno_dict,
            'dim': dim_dict,
            'var': var_dict,
            'law': law_dict,
            'unit': unit_dict
        }

    def query_pheno(self):
        pheno_dict = {}
        for pheno_class in self.pheno_classes:
            sparql = (
                self.prefix + 'select ?p where {'
                f'?p rdf:type ontomo:{pheno_class}. '
                '}'
            )
            sparql_res = self.run(sparql)
            for res in sparql_res:
                pheno = str(res[0]).split('#')[-1]
                pheno_dict[pheno] = {
                    'cls': pheno_class,
                    'fps': [],
                    'mts': [],
                    'mes': []
                }

        # relatesToFlowPattern
        sparql = (
            self.prefix + 'select ?p ?rp where {'
            '?p rdf:type ontomo:Accumulation. '
            'optional{?p ontomo:relatesToFlowPattern ?rp}. '
            '}'
        )
        for res in self.run(sparql):
            ac = str(res[0]).split('#')[-1]
            fp = str(res[1]).split('#')[-1] if res[1] else res[1]
            if fp and fp not in pheno_dict[ac]['fps']:
                pheno_dict[ac]['fps'].append(fp)

        # relatesToMassTransportPhenomenon
        sparql = (
            self.prefix + 'select ?p ?rp where {'
            '?p rdf:type ontomo:FlowPattern. '
            'optional{?p ontomo:relatesToMassTransportPhenomenon ?rp}. '
            '}'
        )
        for res in self.run(sparql):
            fp = str(res[0]).split('#')[-1]
            mt = str(res[1]).split('#')[-1] if res[1] else res[1]
            if mt and mt not in pheno_dict[fp]['mts']:
                pheno_dict[fp]['mts'].append(mt)

        # relatesToMassEquilibriumPhenomenon
        sparql = (
            self.prefix + 'select ?p ?rp where {'
            '?p rdf:type ontomo:MassTransportPhenomenon. '
            'optional{?p ontomo:relatesToMassEquilibriumPhenomenon ?rp}. '
            '}'
        )
        for res in self.run(sparql):
            mt = str(res[0]).split('#')[-1]
            me = str(res[1]).split('#')[-1] if res[1] else res[1]
            if me and me not in pheno_dict[fp]['mes']:
                pheno_dict[fp]['mes'].append(mt)

        for pheno in pheno_dict:
            pheno_dict[pheno]['fps'] = sorted(pheno_dict[pheno]['fps'])
            pheno_dict[pheno]['mts'] = sorted(pheno_dict[pheno]['mts'])
            pheno_dict[pheno]['mes'] = sorted(pheno_dict[pheno]['mes'])

        pheno_dict = dict(sorted(pheno_dict.items(), key=lambda x: x[0]))
        return pheno_dict

    def query_dim(self):
        dim_dict = {}
        sparql = (
            self.prefix + 'select ?d where {'
            '?d rdf:type ontomo:ModelDimension. '
            '}'
        )
        for res in self.run(sparql):
            dim = str(res[0]).split('#')[-1]
            dim_dict[dim] = {
                'cls': 'ModelDimension',
            }
        dim_dict = dict(sorted(dim_dict.items(), key=lambda x: x[0]))
        return dim_dict

    def query_var(self):
        var_dict = {}

        for var_class in self.var_classes:
            sparql = (
                self.prefix + 'select ?v where {'
                f'?v rdf:type ontomo:{var_class}. '
                '}'
            )
            for res in self.run(sparql):
                var = res[0].split('#')[-1]
                var_dict[var] = {
                    'cls': var_class,
                    'sym': None,
                    'val': None,
                    'unit': None,
                    'dims': [],
                    'laws': [],
                }

            sparql = (
                self.prefix + 'select ?v ?s ?val ?d ?l ?u where {'
                f'?v rdf:type ontomo:{var_class}. '
                '?v ontomo:hasSymbol ?s. '
                'optional{?v ontomo:hasValue ?val}. '
                'optional{?v ontomo:hasDimension ?d}. '
                'optional{?v ontomo:hasLaw ?l}. '
                'optional{?v ontomo:hasUnit ?u}. '
                '}'
            )
            for res in self.run(sparql):
                var = res[0].split('#')[-1]
                sym = res[1]
                sym = re.sub(r'("*)"', r'\1', sym)
                sym = re.sub(r' xmlns=.*#', '', sym)
                sym = re.sub(r'\n *', '', sym)
                val = float(res[2].split('#')[-1]) if res[2] else res[2]
                dim = ' '.join(res[3].split('#')[-1].split('_')[:-1]) if res[3] else res[3]
                law = res[4].split('#')[-1] if res[4] else res[4]
                unit = res[5].split('#')[-1] if res[5] else res[5]
                var_dict[var]['sym'] = sym
                var_dict[var]['val'] = val if val else None
                if dim and dim not in var_dict[var]['dims']:
                    var_dict[var]['dims'].append(dim)
                if law and law not in var_dict[var]['laws']:
                    var_dict[var]['laws'].append(law)
                if unit:
                    var_dict[var]['unit'] = unit

        for var in var_dict:
            var_dict[var]['dims'] = sorted(var_dict[var]['dims'])
            var_dict[var]['laws'] = sorted(var_dict[var]['laws'])

        var_dict = dict(sorted(var_dict.items(), key=lambda x: x[0]))
        return var_dict

    def query_law(self):
        law_dict = {}
        sparql = self.prefix + 'select ?d where {?d rdf:type ontomo:Law. }'
        for res in self.run(sparql):
            law = str(res[0])
            law = law.split('#')[-1]
            law_dict[law] = {
                'cls': 'Law',
                'fml': None,
                'pheno': None,
                'vars': [],
                'opt_vars': [],
                'diff_var': None,
                'diff_ul': None,
                'diff_iv': None,
                'int_fml': None,
            }

        sparql = (
            self.prefix + 'select ?d ?f ?p ?v ?ov ?dv ?ul ?iv ?if where {'
            '?d rdf:type ontomo:Law. '
            '?d ontomo:hasFormula ?f. '
            '?d ontomo:isAssociatedWith ?p. '
            'optional{?d ontomo:hasModelVariable ?v}. '
            'optional{?d ontomo:hasOptionalModelVariable ?ov}. '
            'optional{?d ontomo:hasDifferentialModelVariable ?dv}. '
            'optional{?d ontomo:hasIntegralUpperLimit ?ul}. '
            'optional{?d ontomo:hasIntegralInitialValue ?iv}. '
            'optional{?d ontomo:hasIntegratedFormula ?if}. '
            '}'
        )
        for res in self.run(sparql):
            law = str(res[0]).split('#')[-1]
            fml = str(res[1])
            fml = re.sub(r'("*)"', r'\1', fml)
            fml = re.sub(r' xmlns=.*#', '', fml)
            pheno = str(res[2]).split('#')[-1]
            var = str(res[3]).split('#')[-1] if res[3] else None
            opt_var = str(res[4]).split('#')[-1] if res[4] else None
            diff_var = str(res[5]).split('#')[-1] if res[5] else None
            diff_ul = str(res[6]).split('#')[-1] if res[6] else None
            diff_iv = str(res[7]).split('#')[-1] if res[7] else None
            int_fml = str(res[8])
            if int_fml:
                int_fml = re.sub(r'("*)"', r'\1', int_fml)
                int_fml = re.sub(r' xmlns=.*#', '', int_fml)
                int_fml = int_fml.split('#')[-1]
            else:
                int_fml = None
            law_dict[law]['fml'] = fml
            law_dict[law]['pheno'] = pheno
            if var and var not in law_dict[law]['vars']:
                law_dict[law]['vars'].append(var)
            if opt_var and opt_var not in law_dict[law]['opt_vars']:
                law_dict[law]['opt_vars'].append(opt_var)
            if diff_var:
                law_dict[law]['diff_var'] = diff_var
            if diff_ul:
                law_dict[law]['diff_ul'] = diff_ul
            if diff_iv:
                law_dict[law]['diff_iv'] = diff_iv
            if int_fml:
                law_dict[law]['int_fml'] = int_fml

        for law in law_dict:
            law_dict[law]['vars'] = sorted(law_dict[law]['vars'])
            law_dict[law]['opt_vars'] = sorted(law_dict[law]['opt_vars'])

        law_dict = dict(sorted(law_dict.items(), key=lambda x: x[0]))
        return law_dict

    def query_unit(self):
        unit_dict = {}
        sparql = self.prefix + 'select ?u where {?u ?type ontomo:Unit. }'
        for res in self.run(sparql):
            unit = res[0].split('#')[-1]
            unit_dict[unit] = {
                'cls': 'Unit',
                'sym': None,
                'mtr': None,
                'rto': None,
                'intcpt': None,
            }

        sparql = (
            self.prefix + 'select ?u ?s ?m ?r ?i where {'
            '?u rdf:type ontomo:Unit. '
            'optional{?u ontomo:hasSymbol ?s}. '
            'optional{?u ontomo:hasMetric ?m}. '
            'optional{?u ontomo:hasRatio ?r}. '
            'optional{?u ontomo:hasIntercept ?i}. '
            '}'
        )
        for res in self.run(sparql):
            unit = res[0].split('#')[-1]
            sym = res[1]
            if sym:
                sym = re.sub(r'("*)"', r'\1', sym)
                sym = re.sub(r' xmlns=.*#', '', sym)
                sym = re.sub(r'\n *', '', sym)
            mtr = res[2].split('#')[-1] if res[2] else None
            rto = res[3].split('#')[-1] if res[3] else None
            intcpt = res[4].split('#')[-1] if res[4] else None
            if sym:
                unit_dict[unit]['sym'] = sym
            if mtr:
                unit_dict[unit]['mtr'] = mtr
            if rto:
                unit_dict[unit]['rto'] = float(rto)
            if intcpt:
                unit_dict[unit]['intcpt'] = float(intcpt)

        unit_dict = dict(sorted(unit_dict.items(), key=lambda x: x[0]))
        return unit_dict

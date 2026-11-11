import re

import rdflib
import yaml
from pydantic import BaseModel, field_serializer
from typing import Literal, get_args

PhenomenonClass = Literal[
    'Accumulation',
    'FlowPattern',
    'MassTransportPhenomenon',
    'MassEquilibriumPhenomenon',
    'ReactionPhenomenon',
]

DimensionClass = Literal['Dimension']

ModelVariableClass = Literal[
    'Constant',
    'RateVariable',
    'StateVariable',
    'FlowParameter',
    'PhysicsParameter',
    'ReactionParameter',
    'StructureParameter',
    'OperationParameter',
    'MassTransportParameter',
]

LawClass = Literal['Law']

UnitClass = Literal['Unit']


class OntoBaseModel(BaseModel):
    """Pydantic BaseModel for OntoMo entity, identified by its name.

    Compares equal to another entity of the same class with the same name,
    or to its name string, e.g. `law.pheno == 'CSTR'`.
    """
    name: str

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, OntoBaseModel):
            return type(self) is type(other) and self.name == other.name
        return NotImplemented

    def __hash__(self):
        return hash(self.name)


class Phenomenon(OntoBaseModel):
    """OntoMo Phenomenon"""
    name: str
    cls: PhenomenonClass
    fps: list['Phenomenon'] = []
    mts: list['Phenomenon'] = []
    mes: list['Phenomenon'] = []


class Unit(OntoBaseModel):
    """OntoMo Unit"""
    name: str
    cls: UnitClass
    sym: str | None
    mtr: str | None
    rto: float | None
    intcpt: float | None


class ModelVariable(OntoBaseModel):
    """OntoMo Model Variable"""

    name: str
    cls: ModelVariableClass
    sym: str
    val: float | None
    unit: Unit | None
    dims: list[str] = []
    laws: list['Law'] = []


class Law(OntoBaseModel):
    """OntoMo Law"""
    name: str
    cls: LawClass
    fml: str
    pheno: Phenomenon | None
    vars: list[ModelVariable] = []
    opt_vars: list[ModelVariable] = []
    ind_var: ModelVariable | None
    sol_var: ModelVariable | None
    init_val: ModelVariable | None
    int_ul_var: ModelVariable | None
    assoc_ac_law: 'Law | None'

    @field_serializer('assoc_ac_law')
    def _serialize_assoc_ac_law(self, assoc_ac_law: 'Law | None') -> str | None:
        # dump by name, as the associated law links back to this law via vars
        return assoc_ac_law.name if assoc_ac_law else None


Phenomenon.model_rebuild()
ModelVariable.model_rebuild()
Law.model_rebuild()


def _represent_model(dumper: yaml.Dumper, model: OntoBaseModel) -> yaml.Node:
    """Dump a model by its name."""
    return dumper.represent_str(model.name)


def _ignore_aliases(ignore_aliases):
    """Skip YAML anchors for models."""
    def wrapper(dumper: yaml.Dumper, data) -> bool:
        return isinstance(data, OntoBaseModel) or ignore_aliases(dumper, data)
    return wrapper


for _dumper in (yaml.Dumper, yaml.SafeDumper):
    yaml.add_multi_representer(OntoBaseModel, _represent_model, Dumper=_dumper)
    _dumper.ignore_aliases = _ignore_aliases(_dumper.ignore_aliases)


class KnowledgeGraphAgent:
    """Knowledge Graph Agent"""

    prefix_rdf = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>'
    prefix_ontomo = (
        'PREFIX ontomo: '
        '<https://github.com/zhangsy-ryan/KIDoE/main/ontology/OntoMo.owl#>'
    )
    prefix = f'{prefix_rdf}\n{prefix_ontomo}\n'

    def __init__(self, rdf_path: str):
        self.rdf_path = rdf_path
        self.rdf = rdflib.Graph()
        self.rdf.parse(rdf_path)

    def run(self, sparql: str):
        return self.rdf.query(sparql)

    def query(self):
        unit_dict = self.query_unit()
        pheno_dict = self.query_pheno()
        var_dict, law_dict = self._link_var_law(unit_dict, pheno_dict)
        return {
            'var': var_dict,
            'law': law_dict,
            'unit': unit_dict,
            'pheno': pheno_dict,
        }

    def query_var(self) -> dict[str, ModelVariable]:
        var_dict, _ = self._link_var_law(
            self.query_dim(), self.query_unit(), self.query_pheno()
        )
        return var_dict

    def query_law(self) -> dict[str, Law]:
        _, law_dict = self._link_var_law(
            self.query_dim(), self.query_unit(), self.query_pheno()
        )
        return law_dict

    def _link_var_law(
        self,
        unit_dict: dict[str, Unit],
        pheno_dict: dict[str, Phenomenon],
    ) -> tuple[dict[str, ModelVariable], dict[str, Law]]:
        """Build ModelVariable and Law instances linked to each other.

        Variables and laws reference each other, so both are first built
        without the cross references, which are assigned afterwards.
        """
        var_values = self._query_var()
        law_values = self._query_law()

        var_dict = {}
        for var, var_value in var_values.items():
            var_dict[var] = ModelVariable(
                **{
                    **var_value,
                    'unit': unit_dict[var_value['unit']] if var_value['unit'] else None,
                    'laws': [],
                }
            )

        law_dict = {}
        for law, law_value in law_values.items():
            law_value = {
                **law_value,
                'pheno': pheno_dict[law_value['pheno']] if law_value['pheno'] else None,
                'assoc_ac_law': None,
            }
            for key in ('vars', 'opt_vars'):
                law_value[key] = [var_dict[v] for v in law_value[key]]
            for key in ('ind_var', 'sol_var', 'init_val', 'int_ul_var'):
                if law_value[key]:
                    law_value[key] = var_dict[law_value[key]]
            law_dict[law] = Law(**law_value)

        for var, var_value in var_values.items():
            var_dict[var].laws = [law_dict[l] for l in var_value['laws']]
        for law, law_value in law_values.items():
            if law_value['assoc_ac_law']:
                law_dict[law].assoc_ac_law = law_dict[law_value['assoc_ac_law']]
        return var_dict, law_dict

    def _query_var(self) -> dict[str, dict]:
        """Query model variables, referencing other entities by name."""
        var_dict = {}

        for var_class in get_args(ModelVariableClass):
            sparql = (
                self.prefix + f'select ?v where {{?v rdf:type ontomo:{var_class}. }}'
            )
            for res in self.run(sparql):
                var = res[0].split('#')[-1]
                var_dict[var] = {
                    'name': var,
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
                var_dict[var]['val'] = val or None
                if dim and dim not in var_dict[var]['dims']:
                    var_dict[var]['dims'].append(dim)
                if law and law not in var_dict[var]['laws']:
                    var_dict[var]['laws'].append(law)
                if unit:
                    var_dict[var]['unit'] = unit

        for var_value in var_dict.values():
            var_value['dims'] = sorted(var_value['dims'])
            var_value['laws'] = sorted(var_value['laws'])

        var_dict = dict(sorted(var_dict.items(), key=lambda x: x[0]))
        return var_dict

    def _query_law(self) -> dict[str, dict]:
        """Query laws, referencing other entities by name."""
        law_dict = {}
        sparql = self.prefix + 'select ?d where {?d rdf:type ontomo:Law. }'
        for res in self.run(sparql):
            law = str(res[0])
            law = law.rsplit('#', maxsplit=1)[-1]
            law_dict[law] = {
                'name': law,
                'cls': 'Law',
                'fml': None,
                'pheno': None,
                'vars': [],
                'opt_vars': [],
                'ind_var': None,
                'sol_var': None,
                'init_val': None,
                'int_ul_var': None,
                'assoc_ac_law': None,
            }

        sparql = (
            self.prefix + 'select ?d ?f ?p ?v ?ov ?sv ?ul ?iv ?aal ?idv where {'
            '?d rdf:type ontomo:Law. '
            '?d ontomo:hasFormula ?f. '
            'optional{?d ontomo:isAssociatedWith ?p}. '
            'optional{?d ontomo:hasModelVariable ?v}. '
            'optional{?d ontomo:hasOptionalModelVariable ?ov}. '
            'optional{?d ontomo:hasSolutionModelVariable ?sv}. '
            'optional{?d ontomo:hasIntegralUpperLimit ?ul}. '
            'optional{?d ontomo:hasInitialValue ?iv}. '
            'optional{?d ontomo:hasAssociatedAccumulationLaw ?aal}. '
            'optional{?d ontomo:hasIndependentModelVariable ?idv}. '
            '}'
        )
        for res in self.run(sparql):
            law = str(res[0]).split('#')[-1]
            fml = str(res[1])
            fml = re.sub(r'("*)"', r'\1', fml)
            fml = re.sub(r' xmlns=.*#', '', fml)
            pheno = str(res[2]).split('#')[-1] if res[2] else None
            var = str(res[3]).split('#')[-1] if res[3] else None
            opt_var = str(res[4]).split('#')[-1] if res[4] else None
            sv = str(res[5]).split('#')[-1] if res[5] else None
            ul = str(res[6]).split('#')[-1] if res[6] else None
            iv = str(res[7]).split('#')[-1] if res[7] else None
            assoc_ac_law = str(res[8]).split('#')[-1] if res[8] else None
            idv = str(res[9]).split('#')[-1] if res[9] else None
            law_dict[law]['fml'] = fml
            law_dict[law]['pheno'] = pheno
            if var and var not in law_dict[law]['vars']:
                law_dict[law]['vars'].append(var)
            if opt_var and opt_var not in law_dict[law]['opt_vars']:
                law_dict[law]['opt_vars'].append(opt_var)
            if sv:
                law_dict[law]['sol_var'] = sv
            if iv:
                law_dict[law]['init_val'] = iv
            if ul:
                law_dict[law]['int_ul_var'] = ul
            if assoc_ac_law:
                law_dict[law]['assoc_ac_law'] = assoc_ac_law
            if idv:
                law_dict[law]['ind_var'] = idv

        for law_value in law_dict.values():
            law_value['vars'] = sorted(law_value['vars'])
            law_value['opt_vars'] = sorted(law_value['opt_vars'])

        law_dict = dict(sorted(law_dict.items(), key=lambda x: x[0]))
        return law_dict

    def query_unit(self):
        unit_dict = {}
        sparql = self.prefix + 'select ?u where {?u ?type ontomo:Unit. }'
        for res in self.run(sparql):
            unit = res[0].split('#')[-1]
            unit_dict[unit] = {
                'name': unit,
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
        unit_dict = {k: Unit(**v) for k, v in unit_dict.items()}
        return unit_dict

    def query_pheno(self):
        pheno_dict = {}
        for pheno_class in get_args(PhenomenonClass):
            sparql = self.prefix + f'select ?p where {{?p rdf:type ontomo:{pheno_class}. }}'
            sparql_res = self.run(sparql)
            for res in sparql_res:
                pheno = str(res[0]).split('#')[-1]
                pheno_dict[pheno] = {
                    'name': pheno,
                    'cls': pheno_class,
                    'fps': [],
                    'mts': [],
                    'mes': [],
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
            if me and me not in pheno_dict[mt]['mes']:
                pheno_dict[mt]['mes'].append(me)

        pheno_dict = dict(sorted(pheno_dict.items(), key=lambda x: x[0]))
        pheno_objs = {
            k: Phenomenon(name=v['name'], cls=v['cls']) for k, v in pheno_dict.items()
        }

        # link names to Phenomenon instances, which reference each other
        for pheno, pheno_value in pheno_dict.items():
            for key in ('fps', 'mts', 'mes'):
                setattr(
                    pheno_objs[pheno],
                    key,
                    [pheno_objs[p] for p in sorted(pheno_value[key])],
                )
        return pheno_objs


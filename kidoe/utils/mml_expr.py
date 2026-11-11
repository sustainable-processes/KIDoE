import re
from io import BytesIO

from lxml import etree
from lxml.etree import _Element
from typing import List, Dict, Tuple


class MMLExpr:
    """Class to parse and convert MathML expressions.

    This class holds MathML expression and convert it to other languages for modeling.

    This class follows the following translation path for MathML:
        MathML --> ElementTree --> Other languages

    Supported tags:
        `<mfenced>`, `<mfrac>`, `<mi>`, `<mn>`, `<mo>`, `<mrow>`, `<msqrt>`, `<msub>`, `<msup>`, `<mtext>`
    
    Supported mathematic operations:
        `+`, `-`, `×`, `/`, `^`, `∑`, `∏`
    Nested `∑` or `∏` is not supported.
    
    The translation from MathML to ElementTree adopts `package:lxml` by https://lxml.de
    
    Example:
        >>> mml_str = "<math><mrow><mfrac><mi>q</mi><mrow><mi>w</mi><mi>h</mi></mrow></mfrac></mrow></math>"
        >>> MMLExpr(mml_str).to_numpy()
        ('q / (w * h)', ['h', 'q', 'w'])
        >>> mml_str = "<math><mrow><mfrac><mi>q</mi><mrow><mn>&#x03c0;</mn><msup><mi>r</mi><mn>2</mn></msup></mrow></mfrac></mrow></math>"
        >>> MMLExpr(mml_str).to_numpy()
        ('q / (np.pi * r ** 2)', ['q', 'r'])
        >>> mml_str = "<math><mrow><mfrac><mn>1</mn><mn>2</mn></mfrac><mrow><mo>&#x2211;</mo><mi>c</mi><msup><mi>z</mi><mn>2</mn></msup></mrow></mrow></math>"
        >>> postfix_mapping = {"<math><mi>c</mi></math>": ["0"]}
        >>> MMLExpr(mml_str).to_numpy(postfix_mapping)
        ('1 / 2 * np.sum(c[0] * z ** 2)', ['c', 'z'])
    """

    mml_np_mapping = {"×": "*", "−": "-", "≤": "<=", "≥": ">=", "π": "np.pi"}
    mml_jax_mapping = {"×": "*", "−": "-", "≤": "<=", "≥": ">=", "π": "jnp.pi"}
    mml_torch_mapping = {"×": "*", "−": "-", "≤": "<=", "≥": ">=", "π": "torch.pi"}

    mml_skip_txts = {"maximum", "matmul"}
    mml_skip_tags = {"math", "mfrac", "msub", "msup"}
    mml_term_tags = {"mfenced", "mfrac", "mi", "mn", "mrow", "msqrt", "msub", "msup"}

    def __init__(self, mml_str: str):
        """Initializes the MMLExpr instance with a MathML string.

        Args:
            mml_str (str): the MathML string
        """
        self.mml_str = mml_str

    @staticmethod
    def sanitize_etree(root: _Element) -> _Element:
        """Sanitize xml etree:
            - adding omitted times operator

        Args:
            root (_Element): lxml etree root element

        Returns:
            _Element: sanitized lxml etree root element
        """
        if not root.getchildren():
            return
        children = root.getchildren()
        for child in children:
            MMLExpr.sanitize_etree(child)
        for l_child, r_child in zip(children[:-1], children[1:]):
            if root.tag in MMLExpr.mml_skip_tags:
                continue
            l_prev = l_child.getprevious()
            if l_prev is not None and l_prev.text in MMLExpr.mml_skip_txts:
                continue
            l_tag = l_child.tag
            r_tag = r_child.tag
            if l_tag in MMLExpr.mml_term_tags and r_tag in MMLExpr.mml_term_tags:
                if l_tag == "mrow" and l_child.getchildren() and l_child.getchildren()[0].text in ["if", "elif"]:
                    continue
                if r_tag == "mrow" and r_child.getchildren() and r_child.getchildren()[0].text in ["["]:
                    continue
                elem_times = etree.fromstring("<mo>×</mo>")
                l_child.addnext(elem_times)
        return root

    @staticmethod
    def sanitize_numpy(expr: str) -> str:
        """Sanitize numpy expression by adjusting spaces and brackets

        Args:
            np_expr (str): runable numpy formula

        Returns:
            str: sanitized runable numpy codes
        """
        sanitized_expr = []
        for sub_expr in expr.split("\n"):
            match = re.match(r"^ +", sub_expr)
            pos = match.span()[1] if match else 0
            sub_expr = sub_expr[:pos] + \
                re.sub(" +", " ", sub_expr[pos:])
            sub_expr = sub_expr.rstrip(" ")
            sub_expr = re.sub(r" *:", ":", sub_expr)
            sub_expr = re.sub(r"\( *", "(", sub_expr)
            sub_expr = re.sub(r" *\)", ")", sub_expr)
            sub_expr = re.sub(r"\( +-", r"(-", sub_expr)
            sub_expr = re.sub(r" +\[ *", " [", sub_expr)
            sub_expr = re.sub(r" *\] +", "] ", sub_expr)
            sub_expr = re.sub(r"\(- +", r"(-", sub_expr)
            sub_expr = re.sub(r"= *- +", r"= -", sub_expr)
            sub_expr = re.sub(r"\(\(([^\(\)]*)\)\)", r"(\1)", sub_expr)
            sub_expr = re.sub(r"\(([^ ]+\[[0-9,:]+\])\)", r"\1", sub_expr)
            sub_expr = re.sub(r"\(\(([^\(\)]*)\(([^\(\)]*)\)\)\)", r"(\1(\2))", sub_expr)
            sub_expr = re.sub(r"\(\(((\(([^\(\)]*)\)([^\(\)]*))+)\)\)", r"(\1)", sub_expr)
            sub_expr = re.sub(r" *(\[[^ <>\[\]]+(\[[:0-9]+\])* [<>] 0\])", r"\1", sub_expr)
            sub_expr = re.sub(r"\(np.sum\(([^\(\)]+)\)\)", r"np.sum(\1)", sub_expr)
            sub_expr = re.sub(r"\(np.prod\(([^\(\)]+)\)\)", r"np.prod(\1)", sub_expr)
            sub_expr = re.sub(r"(?<!len)(?<!np\.exp)(?<!np\.sum)(?<!np\.prod)(?<!np\.maximum)(?<!np\.matmul)\(([^\+\-\*\/\,]*)\)", r"\1", sub_expr)
            sanitized_expr.append(sub_expr)
        sanitized_expr = "\n".join(sanitized_expr)
        return sanitized_expr

    @staticmethod
    def formulate_numpy(expr: List[str]) -> str:
        """Formulate runable numpy codes

        Args:
            expr (List[str]): list of converted numpy expressions

        Returns:
            str: runable numpy code
        """
        codes = []
        i = 0
        while i < len(expr):
            if expr[i] == "SOLVE START":
                j = i + 1
                while expr[j] != "SOLVE END":
                    j += 1
                param = expr[i+1].split(" ")[-1]
                x0 = float(expr[i+2].split(" ")[-1])
                codes.append("")
                codes.append(f"def inner_param_func({param}):")
                for k in range(i+3, j):
                    for sub_expr in expr[k].split("\n"):
                        codes.append(f"    {sub_expr}")
                codes.append("    return error")
                codes.append("")
                codes.append(f"fsolve(inner_param_func, {x0}, xtol=1e-6, maxfev=1000)[0]")
                i = j + 1
            else:
                codes.append(expr[i])
                i += 1
        return "\n".join(codes)

    @staticmethod
    def mml2numpy(mml_str: str) -> Tuple[str, List[str]]:
        """Iterative conversion of MathML to numpy and variables

        Args:
            mml_str (str): MathML expression

        Returns:
            Tuple[str, List[str]]: converted numpy codes and extracted variables
        """

        expr, vars, level = "", [], 0
        context = etree.iterparse(BytesIO(mml_str), events=("start", "end"))
        for action, elem in context:
            # tag:mfrac
            if action == "start" and elem.tag == "mfrac":
                if level == 0:
                    l_mml_str = etree.tostring(elem[0])
                    r_mml_str = etree.tostring(elem[1])
                    l_expr, l_vars = MMLExpr.mml2numpy(l_mml_str)
                    r_expr, r_vars = MMLExpr.mml2numpy(r_mml_str)
                    expr += f"({l_expr}) / ({r_expr}) "
                    vars.extend(l_vars + r_vars)
                level += 1
            if action == "end" and elem.tag == "mfrac":
                level -= 1
            # tag:mi
            if action == "start" and elem.tag == "mi" and level == 0:
                mi_expr = elem.text.strip(" ")
                expr += f"{mi_expr} "
                vars.append(mi_expr)
            # tag:mn
            if action == "start" and elem.tag == "mn" and level == 0:
                mn_expr = elem.text.strip(" ")
                for k, v in MMLExpr.mml_np_mapping.items():
                    mn_expr = mn_expr.replace(k, v)
                expr += f"{mn_expr} "
            # tag:mo
            if action == "start" and elem.tag == "mo" and level == 0:
                mo_expr = elem.text.strip(" ")
                for k, v in MMLExpr.mml_np_mapping.items():
                    mo_expr = mo_expr.replace(k, v)
                expr += f"{mo_expr} "
            # tag:mrow
            if action == "start" and elem.tag == "mrow":
                if level == 0:
                    if elem[0].tag == "mo":
                        l_mml_str = elem[0].text.strip(" ")
                        l_expr, l_vars = MMLExpr.mml2numpy(
                            b"<math>" + etree.tostring(elem[0]) + b"</math>")
                        r_mml_str = b"".join([etree.tostring(e) for e in elem[1:]])
                        r_mml_str = b"<math>" + r_mml_str + b"</math>"
                        r_expr, r_vars = MMLExpr.mml2numpy(r_mml_str)
                        if l_mml_str == "[":
                            expr += f"{l_expr}{r_expr}"
                        elif l_mml_str == "len":
                            expr += f"len({r_expr}) "
                            vars.extend(r_vars)
                        elif l_mml_str == "exp":
                            expr += f"np.exp({r_expr}) "
                            vars.extend(r_vars)
                        elif l_mml_str == "∑":
                            expr += f"np.sum({r_expr}) "
                            vars.extend(r_vars)
                        elif l_mml_str == "∏":
                            expr += f"np.prod({r_expr}) "
                            vars.extend(r_vars)
                            vars.extend(r_vars)
                        elif l_mml_str == "maximum":
                            first_mml_str = etree.tostring(elem[1])
                            first_mml_str = b"<math>" + first_mml_str + b"</math>"
                            first_expr, first_vars = MMLExpr.mml2numpy(first_mml_str)
                            second_mml_str = etree.tostring(elem[2])
                            second_mml_str = b"<math>" + second_mml_str + b"</math>"
                            second_expr, second_vars = MMLExpr.mml2numpy(second_mml_str)
                            expr += f"np.maximum({first_expr}, {second_expr})"
                            vars.extend(first_vars)
                            vars.extend(second_vars)
                        elif l_mml_str == "matmul":
                            first_mml_str = etree.tostring(elem[1])
                            first_mml_str = b"<math>" + first_mml_str + b"</math>"
                            first_expr, first_vars = MMLExpr.mml2numpy(first_mml_str)
                            second_mml_str = etree.tostring(elem[2])
                            second_mml_str = b"<math>" + second_mml_str + b"</math>"
                            second_expr, second_vars = MMLExpr.mml2numpy(second_mml_str)
                            expr += f"{first_expr} @ {second_expr}"
                            vars.extend(first_vars)
                            vars.extend(second_vars)
                        else:
                            expr += f"{l_expr}{r_expr}"
                            vars.extend(r_vars)
                    elif len(elem) == 3 and elem[0].tag == "msub" and elem[1].tag == "mspace" and elem[2].tag == "mi":
                        # for variables like k_La
                        l_expr, l_vars = MMLExpr.mml2numpy(b"<math>" + etree.tostring(elem[0]) + b"</math>")
                        r_expr, r_vars = MMLExpr.mml2numpy(b"<math>" + etree.tostring(elem[2]) + b"</math>")
                        expr += f"{l_expr}{r_expr} "
                        vars.extend(f"{l_expr}{r_expr}")
                    elif len(elem) >= 4 and elem[1].tag == "mo" and elem[1].text == "[" and elem[len(elem)-1].tag == "mo" and elem[len(elem)-1].text == "]":
                        l_expr, l_vars = MMLExpr.mml2numpy(b"<math>" + etree.tostring(elem[0]) + b"</math>")
                        r_expr = "".join([MMLExpr.mml2numpy(b"<math>" + etree.tostring(elem[i]) + b"</math>")[0] for i in range(2, len(elem)-1)])
                        expr += f"{l_expr.rstrip()}[{r_expr}] "
                        vars.extend(l_vars)
                    else:
                        sub_mml_str = b"".join([etree.tostring(e) for e in elem])
                        sub_mml_str = b"<math>" + sub_mml_str + b"</math>"
                        sub_expr, sub_vars = MMLExpr.mml2numpy(sub_mml_str)
                        expr += f"{sub_expr} "
                        vars.extend(sub_vars)
                level += 1
            if action == "end" and elem.tag == "mrow":
                level -= 1
            # tag:mspace
            if action == "start" and elem.tag == "mspace":
                expr += " " * int(elem.attrib["nspace"])
            # tag:msqrt
            if action == "start" and elem.tag == "msqrt":
                if level == 0:
                    sub_mml_str = b"".join([etree.tostring(e) for e in elem])
                    sub_mml_str = b"<math>" + sub_mml_str + b"</math>"
                    sub_expr, sub_vars = MMLExpr.mml2numpy(sub_mml_str)
                    expr += f"({sub_expr}) ** 0.5 "
                    vars.extend(sub_vars)
                level += 1
            if action == "end" and elem.tag == "msqrt":
                level -= 1
            # tag:msub
            if action == "start" and elem.tag == "msub":
                if level == 0:
                    l_mml_str = etree.tostring(elem[0])
                    r_mml_str = etree.tostring(elem[1])
                    l_expr, _ = MMLExpr.mml2numpy(l_mml_str)
                    r_expr, _ = MMLExpr.mml2numpy(r_mml_str)
                    expr += f"{l_expr}_{r_expr} "
                    vars.append(f"{l_expr}_{r_expr}")
                level += 1
            if action == "end" and elem.tag == "msub":
                level -= 1
            # tag:msup
            if action == "start" and elem.tag == "msup":
                if level == 0:
                    l_mml_str = etree.tostring(elem[0])
                    r_mml_str = etree.tostring(elem[1])
                    l_expr, l_vars = MMLExpr.mml2numpy(l_mml_str)
                    r_expr, r_vars = MMLExpr.mml2numpy(r_mml_str)
                    expr += f"({l_expr}) ** ({r_expr}) "
                    vars.extend(l_vars + r_vars)
                level += 1
            if action == "end" and elem.tag == "msup":
                level -= 1
            # tag:mtext
            if action == "start" and elem.tag == "mtext" and level == 0:
                mtext_expr = elem.text.strip()
                # if elem.text.strip() != ",":
                    # mtext_expr = mtext_expr.replace(",", "_")
                expr += mtext_expr
        expr = MMLExpr.sanitize_numpy(expr)
        vars = sorted(list(set(vars)))
        return expr, vars

    def to_numpy(self, mml2ind: Dict[str, List[str]] | None = None) -> str:
        """Convert MathML expression to numpy expression and variable list

        Args:
            mml2ind (Dict[str, List[str]] | None): mapping from variable MathML to index

        Returns:
            str: converted numpy expression
        """
        mml_str = self.mml_str
        if mml2ind:
            for var, ind in mml2ind.items():
                if not ind:
                    continue
                if var.startswith("<math>") and var.endswith("</math>"):
                    var = var[6:-7]
                if var.startswith("<mrow>") and var.endswith("</mrow>"):
                    var = var[6:-7]
                ind = [f"<mtext>{i}</mtext>" for i in ind]
                rpl = f"<mrow>{var}<mo>[</mo>{'<mtext>,</mtext>'.join(ind)}<mo>]</mo></mrow>"
                mml_str = mml_str.replace(var, rpl)
        parser = etree.XMLParser()
        root = etree.fromstring(mml_str, parser)
        root = self.sanitize_etree(root)
        mml_str = etree.tostring(root)
        expr = []
        root = etree.fromstring(mml_str)
        for child in root.getchildren():
            sub_str = b"<math>" + etree.tostring(child) + b"</math>"
            sub_expr, _ = MMLExpr.mml2numpy(sub_str)
            expr.append(sub_expr)
        code = MMLExpr.formulate_numpy(expr)
        return code

    @staticmethod
    def sanitize_torch(expr: str) -> str:
        """Sanitize torch expression by adjusting spaces and brackets

        Args:
            np_expr (str): runable torch formula

        Returns:
            str: sanitized runable torch codes
        """
        sanitized_expr = []
        for sub_expr in expr.split("\n"):
            match = re.match(r"^ +", sub_expr)
            pos = match.span()[1] if match else 0
            sub_expr = sub_expr[:pos] + \
                re.sub(" +", " ", sub_expr[pos:])
            sub_expr = sub_expr.rstrip(" ")
            sub_expr = re.sub(r" *:", ":", sub_expr)
            sub_expr = re.sub(r"\( *", "(", sub_expr)
            sub_expr = re.sub(r" *\)", ")", sub_expr)
            sub_expr = re.sub(r"\( +-", r"(-", sub_expr)
            sub_expr = re.sub(r" +\[ *", " [", sub_expr)
            sub_expr = re.sub(r" *\] +", "] ", sub_expr)
            sub_expr = re.sub(r"\(- +", r"(-", sub_expr)
            sub_expr = re.sub(r"= *- +", r"= -", sub_expr)
            sub_expr = re.sub(r"\(\(([^\(\)]*)\)\)", r"(\1)", sub_expr)
            sub_expr = re.sub(r"\(([^ ]+\[[0-9,:]+\])\)", r"\1", sub_expr)
            sub_expr = re.sub(r"\(\(([^\(\)]*)\(([^\(\)]*)\)\)\)", r"(\1(\2))", sub_expr)
            sub_expr = re.sub(r"\(\(((\(([^\(\)]*)\)([^\(\)]*))+)\)\)", r"(\1)", sub_expr)
            sub_expr = re.sub(r" *(\[[^ <>\[\]]+(\[[:0-9]+\])* [<>] 0\])", r"\1", sub_expr)
            sub_expr = re.sub(r"\(torch.sum\(([^\(\)]+)\)\)", r"torch.sum(\1)", sub_expr)
            sub_expr = re.sub(r"\(torch.prod\(([^\(\)]+)\)\)", r"torch.prod(\1)", sub_expr)
            sub_expr = re.sub(r"(?<!len)(?<!torch\.exp)(?<!torch\.sum)(?<!torch\.prod)(?<!torch\.maximum)(?<!torch\.matmul)\(([^\+\-\*\/\,]*)\)", r"\1", sub_expr)
            sanitized_expr.append(sub_expr)
        sanitized_expr = "\n".join(sanitized_expr)
        return sanitized_expr

    @staticmethod
    def formulate_torch(expr: List[str]) -> str:
        """Formulate runable torch codes

        Args:
            expr (List[str]): list of converted torch expressions

        Returns:
            str: runable torch code
        """
        codes = []
        i = 0
        while i < len(expr):
            if expr[i] == "SOLVE START":
                j = i + 1
                while expr[j] != "SOLVE END":
                    j += 1
                param = expr[i+1].split(" ")[-1]
                x0 = float(expr[i+2].split(" ")[-1])
                codes.append("")
                codes.append(f"def inner_param_func({param}):")
                for k in range(i+3, j):
                    for sub_expr in expr[k].split("\n"):
                        codes.append(f"    {sub_expr}")
                codes.append("    return error")
                codes.append("")
                codes.append(f"xitorch.optimize.rootfinder(inner_param_func, {x0})")
                i = j + 1
            else:
                codes.append(expr[i])
                i += 1
        return "\n".join(codes)

    @staticmethod
    def mml2torch(mml_str: str) -> Tuple[str, List[str]]:
        """Iterative conversion of MathML to torch and variables

        Args:
            mml_str (str): MathML expression

        Returns:
            Tuple[str, List[str]]: converted torch codes and extracted variables
        """

        expr, vars, level = "", [], 0
        context = etree.iterparse(BytesIO(mml_str), events=("start", "end"))
        for action, elem in context:
            # tag:mfrac
            if action == "start" and elem.tag == "mfrac":
                if level == 0:
                    l_mml_str = etree.tostring(elem[0])
                    r_mml_str = etree.tostring(elem[1])
                    l_expr, l_vars = MMLExpr.mml2torch(l_mml_str)
                    r_expr, r_vars = MMLExpr.mml2torch(r_mml_str)
                    expr += f"({l_expr}) / ({r_expr}) "
                    vars.extend(l_vars + r_vars)
                level += 1
            if action == "end" and elem.tag == "mfrac":
                level -= 1
            # tag:mi
            if action == "start" and elem.tag == "mi" and level == 0:
                mi_expr = elem.text.strip(" ")
                expr += f"{mi_expr} "
                vars.append(mi_expr)
            # tag:mn
            if action == "start" and elem.tag == "mn" and level == 0:
                mn_expr = elem.text.strip(" ")
                for k, v in MMLExpr.mml_torch_mapping.items():
                    mn_expr = mn_expr.replace(k, v)
                expr += f"{mn_expr} "
            # tag:mo
            if action == "start" and elem.tag == "mo" and level == 0:
                mo_expr = elem.text.strip(" ")
                for k, v in MMLExpr.mml_torch_mapping.items():
                    mo_expr = mo_expr.replace(k, v)
                expr += f"{mo_expr} "
            # tag:mrow
            if action == "start" and elem.tag == "mrow":
                if level == 0:
                    if elem[0].tag == "mo":
                        l_mml_str = elem[0].text.strip(" ")
                        l_expr, l_vars = MMLExpr.mml2torch(
                            b"<math>" + etree.tostring(elem[0]) + b"</math>")
                        r_mml_str = b"".join([etree.tostring(e) for e in elem[1:]])
                        r_mml_str = b"<math>" + r_mml_str + b"</math>"
                        r_expr, r_vars = MMLExpr.mml2torch(r_mml_str)
                        if l_mml_str == "[":
                            expr += f"{l_expr}{r_expr}"
                        elif l_mml_str == "len":
                            expr += f"len({r_expr}) "
                            vars.extend(r_vars)
                        elif l_mml_str == "exp":
                            expr += f"torch.exp({r_expr}) "
                            vars.extend(r_vars)
                        elif l_mml_str == "∑":
                            expr += f"torch.sum({r_expr}) "
                            vars.extend(r_vars)
                        elif l_mml_str == "∏":
                            expr += f"torch.prod({r_expr}) "
                            vars.extend(r_vars)
                            vars.extend(r_vars)
                        elif l_mml_str == "maximum":
                            first_mml_str = etree.tostring(elem[1])
                            first_mml_str = b"<math>" + first_mml_str + b"</math>"
                            first_expr, first_vars = MMLExpr.mml2torch(first_mml_str)
                            second_mml_str = etree.tostring(elem[2])
                            second_mml_str = b"<math>" + second_mml_str + b"</math>"
                            second_expr, second_vars = MMLExpr.mml2torch(second_mml_str)
                            expr += f"torch.maximum({first_expr}, {second_expr})"
                            vars.extend(first_vars)
                            vars.extend(second_vars)
                        elif l_mml_str == "matmul":
                            first_mml_str = etree.tostring(elem[1])
                            first_mml_str = b"<math>" + first_mml_str + b"</math>"
                            first_expr, first_vars = MMLExpr.mml2torch(first_mml_str)
                            second_mml_str = etree.tostring(elem[2])
                            second_mml_str = b"<math>" + second_mml_str + b"</math>"
                            second_expr, second_vars = MMLExpr.mml2torch(second_mml_str)
                            expr += f"torch.matmul({first_expr}, {second_expr})"
                            vars.extend(first_vars)
                            vars.extend(second_vars)
                        else:
                            expr += f"{l_expr}{r_expr}"
                            vars.extend(r_vars)
                    elif len(elem) == 3 and elem[0].tag == "msub" and elem[1].tag == "mspace" and elem[2].tag == "mi":
                        # for variables like k_La
                        l_expr, l_vars = MMLExpr.mml2torch(b"<math>" + etree.tostring(elem[0]) + b"</math>")
                        r_expr, r_vars = MMLExpr.mml2torch(b"<math>" + etree.tostring(elem[2]) + b"</math>")
                        expr += f"{l_expr}{r_expr} "
                        vars.extend(f"{l_expr}{r_expr}")
                    elif len(elem) >= 4 and elem[1].tag == "mo" and elem[1].text == "[" and elem[len(elem)-1].tag == "mo" and elem[len(elem)-1].text == "]":
                        l_expr, l_vars = MMLExpr.mml2torch(b"<math>" + etree.tostring(elem[0]) + b"</math>")
                        r_expr = "".join([MMLExpr.mml2torch(b"<math>" + etree.tostring(elem[i]) + b"</math>")[0] for i in range(2, len(elem)-1)])
                        expr += f"{l_expr.rstrip()}[{r_expr}] "
                        vars.extend(l_vars)
                    else:
                        sub_mml_str = b"".join([etree.tostring(e) for e in elem])
                        sub_mml_str = b"<math>" + sub_mml_str + b"</math>"
                        sub_expr, sub_vars = MMLExpr.mml2torch(sub_mml_str)
                        expr += f"{sub_expr} "
                        vars.extend(sub_vars)
                level += 1
            if action == "end" and elem.tag == "mrow":
                level -= 1
            # tag:mspace
            if action == "start" and elem.tag == "mspace":
                expr += " " * int(elem.attrib["nspace"])
            # tag:msqrt
            if action == "start" and elem.tag == "msqrt":
                if level == 0:
                    sub_mml_str = b"".join([etree.tostring(e) for e in elem])
                    sub_mml_str = b"<math>" + sub_mml_str + b"</math>"
                    sub_expr, sub_vars = MMLExpr.mml2torch(sub_mml_str)
                    expr += f"({sub_expr}) ** 0.5 "
                    vars.extend(sub_vars)
                level += 1
            if action == "end" and elem.tag == "msqrt":
                level -= 1
            # tag:msub
            if action == "start" and elem.tag == "msub":
                if level == 0:
                    l_mml_str = etree.tostring(elem[0])
                    r_mml_str = etree.tostring(elem[1])
                    l_expr, _ = MMLExpr.mml2torch(l_mml_str)
                    r_expr, _ = MMLExpr.mml2torch(r_mml_str)
                    expr += f"{l_expr}_{r_expr} "
                    vars.append(f"{l_expr}_{r_expr}")
                level += 1
            if action == "end" and elem.tag == "msub":
                level -= 1
            # tag:msup
            if action == "start" and elem.tag == "msup":
                if level == 0:
                    l_mml_str = etree.tostring(elem[0])
                    r_mml_str = etree.tostring(elem[1])
                    l_expr, l_vars = MMLExpr.mml2torch(l_mml_str)
                    r_expr, r_vars = MMLExpr.mml2torch(r_mml_str)
                    expr += f"({l_expr}) ** ({r_expr}) "
                    vars.extend(l_vars + r_vars)
                level += 1
            if action == "end" and elem.tag == "msup":
                level -= 1
            # tag:mtext
            if action == "start" and elem.tag == "mtext" and level == 0:
                mtext_expr = elem.text.strip()
                # if elem.text.strip() != ",":
                    # mtext_expr = mtext_expr.replace(",", "_")
                expr += mtext_expr
        expr = MMLExpr.sanitize_torch(expr)
        vars = sorted(list(set(vars)))
        return expr, vars

    def to_torch(self, mml2ind: Dict[str, List[str]] | None = None) -> str:
        """Convert MathML expression to torch expression and variable list

        Args:
            mml2ind (Dict[str, List[str]] | None): mapping from variable MathML to index

        Returns:
            str: converted torch expression
        """
        mml_str = self.mml_str
        if mml2ind:
            for var, ind in mml2ind.items():
                if not ind:
                    continue
                if var.startswith("<math>") and var.endswith("</math>"):
                    var = var[6:-7]
                if var.startswith("<mrow>") and var.endswith("</mrow>"):
                    var = var[6:-7]
                ind = [f"<mtext>{i}</mtext>" for i in ind]
                rpl = f"<mrow>{var}<mo>[</mo>{'<mtext>,</mtext>'.join(ind)}<mo>]</mo></mrow>"
                mml_str = mml_str.replace(var, rpl)
        parser = etree.XMLParser()
        root = etree.fromstring(mml_str, parser)
        root = self.sanitize_etree(root)
        mml_str = etree.tostring(root)
        expr = []
        root = etree.fromstring(mml_str)
        for child in root.getchildren():
            sub_str = b"<math>" + etree.tostring(child) + b"</math>"
            sub_expr, _ = MMLExpr.mml2torch(sub_str)
            expr.append(sub_expr)
        code = MMLExpr.formulate_torch(expr)
        return code

    @staticmethod
    def sanitize_jax(expr: str) -> str:
        """Sanitize jax expression by adjusting spaces and brackets

        Args:
            np_expr (str): runable jax formula

        Returns:
            str: sanitized runable jax codes
        """
        sanitized_expr = []
        for sub_expr in expr.split("\n"):
            match = re.match(r"^ +", sub_expr)
            pos = match.span()[1] if match else 0
            sub_expr = sub_expr[:pos] + \
                re.sub(" +", " ", sub_expr[pos:])
            sub_expr = sub_expr.rstrip(" ")
            sub_expr = re.sub(r" *:", ":", sub_expr)
            sub_expr = re.sub(r"\( *", "(", sub_expr)
            sub_expr = re.sub(r" *\)", ")", sub_expr)
            sub_expr = re.sub(r"^\[ *", "[", sub_expr)
            sub_expr = re.sub(r" *\]$", "]", sub_expr)
            sub_expr = re.sub(r"\( +-", r"(-", sub_expr)
            sub_expr = re.sub(r"\(- +", r"(-", sub_expr)
            sub_expr = re.sub(r" +\[ *", " [", sub_expr)
            sub_expr = re.sub(r" *\] +", "] ", sub_expr)
            sub_expr = re.sub(r"= *- +", r"= -", sub_expr)
            sub_expr = re.sub(r"\(\(([^\(\)]*)\)\)", r"(\1)", sub_expr)
            sub_expr = re.sub(r"\(([^ ]+\[[0-9,:]+\])\)", r"\1", sub_expr)
            sub_expr = re.sub(r"\(\(([^\(\)]*)\(([^\(\)]*)\)\)\)", r"(\1(\2))", sub_expr)
            sub_expr = re.sub(r"\(\(((\(([^\(\)]*)\)([^\(\)]*))+)\)\)", r"(\1)", sub_expr)
            sub_expr = re.sub(r" *(\[[^ <>\[\]]+(\[[:0-9]+\])* [<>] 0\])", r"\1", sub_expr)
            sub_expr = re.sub(r"\(jnp.sum\(([^\(\)]+)\)\)", r"jnp.sum(\1)", sub_expr)
            sub_expr = re.sub(r"\(jnp.prod\(([^\(\)]+)\)\)", r"jnp.prod(\1)", sub_expr)
            sub_expr = re.sub(r"(?<!len)(?<!jnp\.exp)(?<!jnp\.sum)(?<!jnp\.prod)(?<!jnp\.maximum)(?<!jnp\.matmul)\(([^\+\-\*\/\,]*)\)", r"\1", sub_expr)
            sanitized_expr.append(sub_expr)
        sanitized_expr = "\n".join(sanitized_expr)
        return sanitized_expr

    @staticmethod
    def formulate_jax(expr: List[str]) -> str:
        """Formulate runable jax codes

        Args:
            expr (List[str]): list of converted jax expressions

        Returns:
            str: runable jax code
        """
        codes = []
        i = 0
        while i < len(expr):
            if expr[i] == "SOLVE START":
                j = i + 1
                while expr[j] != "SOLVE END":
                    j += 1
                param = expr[i+1].split(" ")[-1]
                x0 = float(expr[i+2].split(" ")[-1])
                codes.append("")
                codes.append(f"def inner_param_func({param}):")
                for k in range(i+3, j):
                    for sub_expr in expr[k].split("\n"):
                        codes.append(f"    {sub_expr}")
                codes.append("    return error")
                codes.append("")
                codes.append(f"Broyden(inner_param_func).run({x0})[0]")
                i = j + 1
            else:
                codes.append(expr[i])
                i += 1
        return "\n".join(codes)

    @staticmethod
    def mml2jax(mml_str: str) -> Tuple[str, List[str]]:
        """Iterative conversion of MathML to jax and variables

        Args:
            mml_str (str): MathML expression

        Returns:
            Tuple[str, List[str]]: converted jax codes and extracted variables
        """

        expr, vars, level = "", [], 0
        context = etree.iterparse(BytesIO(mml_str), events=("start", "end"))
        for action, elem in context:
            # tag:mfrac
            if action == "start" and elem.tag == "mfrac":
                if level == 0:
                    l_mml_str = etree.tostring(elem[0])
                    r_mml_str = etree.tostring(elem[1])
                    l_expr, l_vars = MMLExpr.mml2jax(l_mml_str)
                    r_expr, r_vars = MMLExpr.mml2jax(r_mml_str)
                    expr += f"({l_expr}) / ({r_expr}) "
                    vars.extend(l_vars + r_vars)
                level += 1
            if action == "end" and elem.tag == "mfrac":
                level -= 1
            # tag:mi
            if action == "start" and elem.tag == "mi" and level == 0:
                mi_expr = elem.text.strip(" ")
                expr += f"{mi_expr} "
                vars.append(mi_expr)
            # tag:mn
            if action == "start" and elem.tag == "mn" and level == 0:
                mn_expr = elem.text.strip(" ")
                for k, v in MMLExpr.mml_jax_mapping.items():
                    mn_expr = mn_expr.replace(k, v)
                expr += f"{mn_expr} "
            # tag:mo
            if action == "start" and elem.tag == "mo" and level == 0:
                mo_expr = elem.text.strip(" ")
                for k, v in MMLExpr.mml_jax_mapping.items():
                    mo_expr = mo_expr.replace(k, v)
                expr += f"{mo_expr} "
            # tag:mrow
            if action == "start" and elem.tag == "mrow":
                if level == 0:
                    if elem[0].tag == "mo":
                        l_mml_str = elem[0].text.strip(" ")
                        l_expr, l_vars = MMLExpr.mml2jax(b"<math>" + etree.tostring(elem[0]) + b"</math>")
                        r_mml_str = b"".join([etree.tostring(e) for e in elem[1:]])
                        r_mml_str = b"<math>" + r_mml_str + b"</math>"
                        r_expr, r_vars = MMLExpr.mml2jax(r_mml_str)
                        if l_mml_str == "[":
                            expr += f"{l_expr}{r_expr} "
                        elif l_mml_str == "len":
                            expr += f"len({r_expr}) "
                            vars.extend(r_vars)
                        elif l_mml_str == "exp":
                            expr += f"jnp.exp({r_expr}) "
                            vars.extend(r_vars)
                        elif l_mml_str == "∑":
                            expr += f"jnp.sum({r_expr}) "
                            vars.extend(r_vars)
                        elif l_mml_str == "∏":
                            expr += f"jnp.prod({r_expr}) "
                            vars.extend(r_vars)
                            vars.extend(r_vars)
                        elif l_mml_str == "maximum":
                            first_mml_str = etree.tostring(elem[1])
                            first_mml_str = b"<math>" + first_mml_str + b"</math>"
                            first_expr, first_vars = MMLExpr.mml2jax(first_mml_str)
                            second_mml_str = etree.tostring(elem[2])
                            second_mml_str = b"<math>" + second_mml_str + b"</math>"
                            second_expr, second_vars = MMLExpr.mml2jax(second_mml_str)
                            expr += f"jnp.maximum({first_expr}, {second_expr})"
                            vars.extend(first_vars)
                            vars.extend(second_vars)
                        elif l_mml_str == "matmul":
                            first_mml_str = etree.tostring(elem[1])
                            first_mml_str = b"<math>" + first_mml_str + b"</math>"
                            first_expr, first_vars = MMLExpr.mml2jax(first_mml_str)
                            second_mml_str = etree.tostring(elem[2])
                            second_mml_str = b"<math>" + second_mml_str + b"</math>"
                            second_expr, second_vars = MMLExpr.mml2jax(second_mml_str)
                            expr += f"jnp.matmul({first_expr}, {second_expr})"
                            vars.extend(first_vars)
                            vars.extend(second_vars)
                        else:
                            expr += f"{l_expr}{r_expr}"
                            vars.extend(r_vars)
                    elif len(elem) == 3 and elem[0].tag == "msub" and elem[1].tag == "mspace" and elem[2].tag == "mi":
                        # for variables like k_La
                        l_expr, l_vars = MMLExpr.mml2jax(b"<math>" + etree.tostring(elem[0]) + b"</math>")
                        r_expr, r_vars = MMLExpr.mml2jax(b"<math>" + etree.tostring(elem[2]) + b"</math>")
                        expr += f"{l_expr}{r_expr} "
                        vars.extend(f"{l_expr}{r_expr}")
                    elif len(elem) >= 4 and elem[1].tag == "mo" and elem[1].text == "[" and elem[len(elem)-1].tag == "mo" and elem[len(elem)-1].text == "]":
                        l_expr, l_vars = MMLExpr.mml2jax(b"<math>" + etree.tostring(elem[0]) + b"</math>")
                        r_expr = "".join([MMLExpr.mml2jax(b"<math>" + etree.tostring(elem[i]) + b"</math>")[0] for i in range(2, len(elem)-1)])
                        expr += f"{l_expr.rstrip()}[{r_expr}] "
                        vars.extend(l_vars)
                    else:
                        sub_mml_str = b"".join([etree.tostring(e) for e in elem])
                        sub_mml_str = b"<math>" + sub_mml_str + b"</math>"
                        sub_expr, sub_vars = MMLExpr.mml2jax(sub_mml_str)
                        expr += f"{sub_expr} "
                        vars.extend(sub_vars)
                level += 1
            if action == "end" and elem.tag == "mrow":
                level -= 1
            # tag:mspace
            if action == "start" and elem.tag == "mspace":
                expr += " " * int(elem.attrib["nspace"])
            # tag:msqrt
            if action == "start" and elem.tag == "msqrt":
                if level == 0:
                    sub_mml_str = b"".join([etree.tostring(e) for e in elem])
                    sub_mml_str = b"<math>" + sub_mml_str + b"</math>"
                    sub_expr, sub_vars = MMLExpr.mml2jax(sub_mml_str)
                    expr += f"({sub_expr}) ** 0.5 "
                    vars.extend(sub_vars)
                level += 1
            if action == "end" and elem.tag == "msqrt":
                level -= 1
            # tag:msub
            if action == "start" and elem.tag == "msub":
                if level == 0:
                    l_mml_str = etree.tostring(elem[0])
                    r_mml_str = etree.tostring(elem[1])
                    l_expr, _ = MMLExpr.mml2jax(l_mml_str)
                    r_expr, _ = MMLExpr.mml2jax(r_mml_str)
                    expr += f"{l_expr}_{r_expr} "
                    vars.append(f"{l_expr}_{r_expr}")
                level += 1
            if action == "end" and elem.tag == "msub":
                level -= 1
            # tag:msup
            if action == "start" and elem.tag == "msup":
                if level == 0:
                    l_mml_str = etree.tostring(elem[0])
                    r_mml_str = etree.tostring(elem[1])
                    l_expr, l_vars = MMLExpr.mml2jax(l_mml_str)
                    r_expr, r_vars = MMLExpr.mml2jax(r_mml_str)
                    expr += f"({l_expr}) ** ({r_expr}) "
                    vars.extend(l_vars + r_vars)
                level += 1
            if action == "end" and elem.tag == "msup":
                level -= 1
            # tag:mtext
            if action == "start" and elem.tag == "mtext" and level == 0:
                mtext_expr = elem.text.strip()
                if elem.text.strip() != ",":
                    mtext_expr = mtext_expr.replace(",", "_")
                expr += mtext_expr
        expr = MMLExpr.sanitize_jax(expr)
        vars = sorted(list(set(vars)))
        return expr, vars

    def to_jax(self, mml2ind: Dict[str, List[str]] | None = None) -> str:
        """Convert MathML expression to jax expression and variable list

        Args:
            mml2ind (Dict[str, List[str]] | None): mapping from variable MathML to index

        Returns:
            str: converted jax expression
        """
        mml_str = self.mml_str
        if mml2ind:
            for var, ind in mml2ind.items():
                if not ind:
                    continue
                if var.startswith("<math>") and var.endswith("</math>"):
                    var = var[6:-7]
                if var.startswith("<mrow>") and var.endswith("</mrow>"):
                    var = var[6:-7]
                ind = [f"<mtext>{i}</mtext>" for i in ind]
                rpl = f"<mrow>{var}<mo>[</mo>{'<mtext>,</mtext>'.join(ind)}<mo>]</mo></mrow>"
                mml_str = mml_str.replace(var, rpl)
        parser = etree.XMLParser()
        root = etree.fromstring(mml_str, parser)
        root = self.sanitize_etree(root)
        mml_str = etree.tostring(root)
        expr = []
        root = etree.fromstring(mml_str)
        for child in root.getchildren():
            sub_str = b"<math>" + etree.tostring(child) + b"</math>"
            sub_expr, _ = MMLExpr.mml2jax(sub_str)
            expr.append(sub_expr)
        code = MMLExpr.formulate_jax(expr)
        return code

if __name__ == "__main__":
    import doctest
    doctest.testmod()

from pylatexenc.latexencode import utf8tolatex
from bust.utils import indent_string


class Documentation(object):
    """Class for auto-generation of module documentation

    """

    def __init__(self, module):
        self.module = module

    def return_tex_documentation(self):
        s = tex_top
        s += "\n\n"
        s += r"\title{" + utf8tolatex(self.module.name) + "}\n"
        s += r"\author{}" + "\n"
        s += r"\date{}" + "\n"
        s += "\n"
        s += r"\begin{document}" + "\n"
        s += "\n"
        s += r"\maketitle" + "\n"
        s += "\n"

        s += utf8tolatex(self.module.description) + "\n\n"

        s += r"\section{Register List}" + "\n\n"
        s += tex_table_top + "\n"
        for i, reg in enumerate(self.module.registers):
            p = str(i) + " & "
            p += utf8tolatex(reg.name) + " & "
            p += reg.mode.upper() + " & "
            p += r"\texttt{"
            p += '0x{0:0{1}X}'.format(reg.address, int(self.module.addr_width/4)) + "} & "
            p += reg.sig_type.upper() + " & "
            p += str(reg.length) + " & "
            p += r"\texttt{"
            p += '0x' + format(int(reg.reset, 16), 'X') + "} \\\\\n"
            p += r"\hline" + "\n"
            s += indent_string(p, 3)
        s += tex_table_bot

        s += "\n\n" r"\section{Registers}" + "\n\n"

        for reg in self.module.registers:

            s += r"\begin{register}{H}{" + utf8tolatex(reg.name) + " - "
            s += reg.mode.upper()
            if reg.mode.lower() == "pulse":
                s += " for " + str(reg.num_cycles) + " cycles - "
            s += "}{" + '0x{0:0{1}X}'.format(reg.address, int(self.module.addr_width/4))
            s += "}"

            s += indent_string(r"\par ")

            s += utf8tolatex(reg.description) + r" \regnewline" + "\n"
            s += indent_string(r"\label{" + reg.name + "}\n")

            if reg.length < self.module.data_width:
                p = r"\regfield{unused}{"
                p += str(self.module.data_width - reg.length) + "}{"
                p += str(reg.length) + "}{-}\n"
                s += indent_string(p)

            if reg.sig_type != "fields":

                p = r"\regfield{}{" + str(reg.length) + "}{0}{"
                if reg.length < 2:
                    p += str(int(reg.reset, 16))
                else:
                    p += '{0x' + format(int(reg.reset, 16), 'X') + "}"
                p += "}\n"

                s += indent_string(p)

            else:
                for field in reversed(reg.fields):
                    p = r"\regfield{" + utf8tolatex(field.name) + "}{"
                    p += str(field.length) + "}{"
                    p += str(field.pos_low) + "}{"
                    if field.length < 2:
                        p += str(int(field.reset, 16))
                    else:
                        p += '{0x' + format(int(field.reset, 16), 'X') + "}"
                    p += "}\n"
                    s += indent_string(p)

            s += r"\reglabel{Reset}\regnewline" + "\n"

            if reg.sig_type == "fields":

                p = r"\begin{regdesc}\begin{reglist}["
                # Get the longest field name and indent the list based on that length
                gen = [field.name for field in reg.fields]
                longest = max(gen, key=len)
                p += utf8tolatex(longest)
                p += "]\n"
                s += indent_string(p)
                for field in reg.fields:
                    p = r"\item [" + utf8tolatex(field.name) + "] "
                    p += utf8tolatex(field.description)
                    s += indent_string(p, 2)
                s += indent_string(r"\end{reglist}\end{regdesc}" + "\n")

            s += r"\end{register}" + "\n\n"

        s += "\end{document}"
        return s


tex_top = r"""\documentclass{article}
\usepackage[margin=1in]{geometry}
\usepackage{register}
\usepackage{enumitem}
\setlist[description]{leftmargin=\parindent,labelindent=\parindent}
\usepackage{calc}
\usepackage{tabularx}

\usepackage{listings}
\lstdefinelanguage{VHDL}{
   morekeywords=[1]{
     library,use,all,entity,is,port,in,out,end,architecture,of,
     begin,and,others
   },
   morecomment=[l]--
}

\lstdefinestyle{vhdl}{
   language     = VHDL,
   basicstyle   = \ttfamily,
}"""


tex_table_top = r"""\begin{table}[h!]
  \begin{center}
    \label{tab:table1}
    \begin{tabularx}{\linewidth}{|l|X|l|l|l|c|l|}
      \hline
      \textbf{\#} & \textbf{Name} & \textbf{Mode} & \textbf{Address} & \textbf{Type} & \textbf{Length} &
      \textbf{Reset} \\
      \hline"""

tex_table_bot = r"""    \end{tabularx}
  \end{center}
\end{table}"""
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{mcs5frmt}[2017/09/03 General Format for Handouts]

\newif\ifincludenamefield
\includenamefieldtrue %default is it shows the ``Name:'' at the top

\DeclareOption{noname}{\includenamefieldfalse}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[11pt]{article}

\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{xifthen}
\RequirePackage{lastpage}
\RequirePackage[margin=1in, headheight=50pt, headsep=.25in]{geometry}
\RequirePackage{mcs5crsn}

\RequirePackage{setspace}
\onehalfspacing

\RequirePackage{enumitem}
\setlist[enumerate, 1]{label=\arabic*)}
\setlist[enumerate, 2]{label=\alph*)}

\RequirePackage{datetime2}
\DTMsetup{datesep=/} %set separator to be the slash (/)
\DTMsetdatestyle{mdyyyy} %set format of date to be mm/dd/yyyy (allowing 1-digit months/days)

\RequirePackage{fancyhdr}
\pagestyle{fancy}
\lhead{\printtitle}
\chead{\ifthenelse{\boolean{includenamefield}}{Name: \phantom{Matthew S}}{}}
\rhead{\printdate}
\lfoot{page~\thepage~of \pageref{LastPage}}
\cfoot{}
\rfoot{\tiny{\printcourse[short]}}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}

%internal variable definitions
\newcommand{\@hdrtitle}{\textbf{Set a title with the \texttt{settitle} command}}
\newcommand{\@hdrcourse}{\textbf{Set a course with the \texttt{setcourse} command}}
\newcommand{\@bdycourse}{\@hdrcourse}
\newcommand{\@hdryear}{0}
\newcommand{\@hdrmonth}{0}
\newcommand{\@hdrday}{0}

%commands to be used by .tex files for header and footer info
\newcommand{\settitle}[1]{\renewcommand{\@hdrtitle}{#1}}
\newcommand{\setcourse}[1]{\renewcommand{\@hdrcourse}{\coursename[short]{#1}}\renewcommand{\@bdycourse}{\coursename{#1}}}
\newcommand{\setdate}[3][\the\year]
{
\renewcommand{\@hdryear}{#1}
\renewcommand{\@hdrmonth}{#2}
\renewcommand{\@hdrday}{#3}
}
\newcommand{\printtitle}{\@hdrtitle}
\newcommand{\printcourse}[1][]{\ifthenelse{\isin{short}{#1}}{\@hdrcourse}{\@bdycourse}}
\newcommand{\printdate}{\DTMdisplaydate{\@hdryear}{\@hdrmonth}{\@hdrday}{-1}}

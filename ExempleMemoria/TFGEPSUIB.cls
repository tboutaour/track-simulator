% Aquest document defineix la classe
% TFGEPSUIB.cls utilitzada per a la
% realització de memories de TFG a 
% l'EPS de la UIB
% ----------------------------------------
% Els comentaris inclosos en aquest fitxer
% s'escriuen sense accents per tal de mantenir
% la seva independencia del sistema de codificacio
%-------------------------------------------------
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% NO ESTA PERMES MODIFICAR EL CONTINGUT D'AQUEST DOCUMENT. 
% QUALSEVOL MODIFICACIO POT ALTERAR LA SEVA VALIDESA I 
% EL FORMAT DEL DOCUMENT FINAL.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\NeedsTeXFormat{LaTeX2e}[1999/12/01]
\ProvidesClass{TFGEPSUIB}[2017/07/13 v1.3, Format LaTeX pel treball final de grau a l'EPS de la UIB]

%------------------------------------------------
% V1.3
% Adaptat a codificació UFF-8.
%------------------------------------------------
% V1.2
% Adaptar portada a castellà i anglès.
%------------------------------------------------
% V1.1
% Adaptar als diferents estudis.
% Cada estudi un color diferent
% Grau en Enginyeria Telemàtica - Blau
% Grau en Enginyeria Informàtica - Marró
% Grau en Enginyeria Industrial - Taronja
% Grau en Enginyeria Agroalimentària - Vermell
% Grau en Edificació            - Morat
% Grau en Matemàtiques          - Verd
%------------------------------------------------

\RequirePackage{ifthen}
\RequirePackage{calc}
\AtEndOfClass{\RequirePackage[kerning,spacing,babel]{microtype}}

\DeclareOption{english}{%
	\AtEndOfClass{%
		\main@language{english}%
		\addto\captionsenglish{%
			\def\nomprojecte{Final Degree Report}%
			\def\autorsingular{Author}%
			\def\autorplural{Authors}%
			\def\supervisorsingular{Supervisor}%
			\def\supervisorplural{Supervisors}%
			\def\tutorsingular{Tutor}%
			\def\tutorplural{Tutors}%
	}}}
\DeclareOption{spanish}{%
	\AtEndOfClass{%
		\main@language{spanish}%
		\addto\captionsspanish{%
			\def\nomprojecte{Trabajo Fin de Grado}%
			\def\autorsingular{Autor}%
			\def\autorplural{Autores}%
			\def\supervisorsingular{Supervisor}%
			\def\supervisorplural{Supervisores}%
			\def\tutorsingular{Tutor}%
			\def\tutorplural{Tutores}%
	}}}
\DeclareOption{catalan}{%
	\AtEndOfClass{%
		\main@language{catalan}%
		\addto\captionscatalan{%
			\def\nomprojecte{Treball Fi de Grau}%
			\def\autorsingular{Autor}%
			\def\autorplural{Autors}%
			\def\supervisorsingular{Supervisor}%
			\def\supervisorplural{Supervisors}%
			\def\tutorsingular{Tutor}%
			\def\tutorplural{Tutors}%
			\def\contentsname{Sumari}%
	}}}

% Definim aquí estudis per poder adoptar
% el nom a partir d'una opcio.
\makeatletter
\newcommand{\estudis}[1]{%
\gdef\estudis@eps{#1}}
\newcommand{\estudis@eps}{}
\makeatother

\DeclareOption{GTEL}%
{\AtEndOfClass{%
 \definecolor{colorTFG}{RGB}{79,129,189}%blau
 \estudis{\MakeUppercase{Grau d'Enginyeria Telem\`atica}}
}}
\DeclareOption{GEDI}%
{\AtEndOfClass{%
 \definecolor{colorTFG}{RGB}{200,91,145}%morat
 \estudis{\MakeUppercase{Grau d'Enginyeria d'Edificaci\'o}}
}}
\DeclareOption{GMAT}%
{\AtEndOfClass{%
 \definecolor{colorTFG}{RGB}{91,200,145}%verd
 \estudis{\MakeUppercase{Grau de Matem\`atiques}}
}}
\DeclareOption{GELE}%
{\AtEndOfClass{%
 \definecolor{colorTFG}{RGB}{255,153,51}%taronja
 \estudis{\MakeUppercase{Grau d'Enginyeria Electr\`onica Industrial i Autom\`atica}}
}}
\DeclareOption{GINF}%
{\AtEndOfClass{%
 \definecolor{colorTFG}{RGB}{153,0,0}%marro
 \estudis{\MakeUppercase{Grau d'Enginyeria Inform\`atica}}
}}
\DeclareOption{GAGR}%
{\AtEndOfClass{%
 \definecolor{colorTFG}{RGB}{255,82,82}%vermell
 \estudis{\MakeUppercase{Grau en Enginyeria Agroaliment\`aria i del Medi Rural}}
}}

%---Opcions per defecte:
\ExecuteOptions{GTEL,catalan}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{memoir}}
\ProcessOptions*

%
% Les opcions per defecte de memoir son
% 'final', 'openrigth', 'twoside', 'onecolumn'
% per tant no cal carregar-les ni especificar-les 
% en el document original
% Es carrega amb 'a4paper' i '11pt' perque per
% defecte usa 'letter' i '10pt'.
%
\LoadClass[a4paper,11pt]{memoir}

% El paquet xcolor es necessari per definir els
% colors de la memoria
\RequirePackage[table]{xcolor}
% Si es vol canviar el color de la portada i fons
% dels nombres de capitol, basta amb redefinir
% el color 'colorTFG'.
\definecolor{colorTFG}{RGB}{79,129,189}

% El paquet eso-pic es necessari per 
% construir la portada
\RequirePackage[texcoord]{eso-pic}

% Com a minim necessari pel titol de capitol
\RequirePackage{graphicx}

% El tipus de lletra serà Fourier, però el
% nombre de capítol serà lm
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage{lmodern}
\RequirePackage{soul,fourier}

% Per defecte suposarem que l'idioma és el català
\RequirePackage[english,spanish,main=catalan]{babel}

%----------------------- daleif1 style ----------------------------------------
\makeatletter
\newlength\dlf@normtxtw
\setlength\dlf@normtxtw{\textwidth}
\def\myhelvetfont{\def\sfdefault{mdput}}
\newsavebox{\feline@chapter}
\newcommand\feline@chapter@marker[1][4cm]{%
	\sbox\feline@chapter{%
		\resizebox{!}{#1}{\fboxsep=1pt%
			\colorbox{colorTFG}{\color{white}\bfseries\sffamily\thechapter}%
		}}%
	\rotatebox{90}{%
		\resizebox{%
			\heightof{\usebox{\feline@chapter}}+\depthof{\usebox{\feline@chapter}}}%
			{!}{\scshape\color{colorTFG}\so\@chapapp}}\quad%
	\raisebox{\depthof{\usebox{\feline@chapter}}}{\usebox{\feline@chapter}}%
}
\newcommand\feline@chm[1][4cm]{%
	\sbox\feline@chapter{\feline@chapter@marker[#1]}%
	\makebox[0pt][l]{% aka \rlap
		\makebox[1cm][r]{\usebox\feline@chapter}%
	}} 
\makechapterstyle{daleif1}{
	\renewcommand\chapnamefont{\normalfont\Large\scshape\raggedleft\so}
	\renewcommand\chaptitlefont{\normalfont\huge\bfseries\scshape\color{colorTFG}}
	\renewcommand\chapternamenum{}
	\renewcommand\printchaptername{}
	\renewcommand\printchapternum{\null\hfill\feline@chm[2.5cm]\par}
	\renewcommand\afterchapternum{\par\vskip\midchapskip}
	\renewcommand\printchaptertitle[1]{\chaptitlefont\raggedleft ##1\par}
} 
\makeatother
\chapterstyle{daleif1}

\newcommand{\PreserveBackslash}[1]{\let\temp=\\#1\let\\=\temp}
\let\PBS=\PreserveBackslash

%---------------------------------------------------------------
\definecolor{Dark}{gray}{.2}
\definecolor{Medium}{gray}{.6}
\definecolor{Light}{gray}{.8}

%---------------------- DEDICATORIA ENVIRONMENT---------------
\newenvironment{agraiments}
{
  \vspace*{5cm}
  \begin{flushright}
}
{
  \end{flushright}
  \cleardoublepage
}

%-------------------- Titol, autor, supervisor, etc -----------

\makeatletter

% Es defineix una comanda \printauthor per imprimir
% la paraula Autor o Autors abans del noms dels autors
% del projecte en funcio de que siguin un o més d'un
% separats per la comanda \and
\newcommand{\testauthor}{%
	\expandafter\tst@au\@author\and\nil%
}
\def\tst@au#1\and#2\nil{%
	\edef\test{#2}%
	\ifx\test\@empty \textbf{\Large \autorsingular}\else \textbf{\Large \autorplural}\fi%
}
\newcommand\printauthor{%
        {%
        \protected\def\and{and }%
        \large \testauthor\par}
        }
\preauthor{\vspace{0cm}\begin{center}
  \Large \lineskip .5em%
%  \printauthor % No mostra la paraula Autor o Autors
	\par
  \begin{tabular}[t]{c}}
\postauthor{\end{tabular}\par\end{center}}

% Es defineix una comanda \tutor (similar a \author) per
% definir el tutor (director) del TFG.
% En cas de que siguin 2 o mes s'usara la comanda \and
% entre els tutors
\newcommand{\testtutor}{%
	\expandafter\tst@tut\@tutor\and\nil%
}
\def\tst@tut#1\and#2\nil{%
	\edef\test{#2}%
	\ifx\test\@empty \textbf{\Large \tutorsingular}\else \textbf{\Large \tutorplural}\fi%
}
\newcommand\printtutor{%
        {%
        \protected\def\and{and }%
        \large \testtutor\par}
        }
\newcommand{\tutor}[1]{\gdef\@tutor{#1}}%
% El nom del tutor (com el de l'autor) es sempre necessari
\newcommand{\@tutor}{\@latex@warning@no@line{No \noexpand\tutor given}}
\addtoiargdef{\tutor}{%
  \begingroup\let\footnote\@gobble}{%
  \begingroup
    \renewcommand{\thanks}[1]{}
    \renewcommand{\and}{\unskip, }
    \renewcommand{\andnext}{\unskip, }
    \renewcommand{\thanksmark}[1]{}
    \renewcommand{\thanksgap}[1]{}
    \protected@xdef\thetutor{#1}
  \endgroup\endgroup}
\newcommand{\pretutor}[1]{\def\@bspretutor{#1}}
\newcommand{\posttutor}[1]{\def\@bsposttutor{#1}}
\pretutor{\vfill\begin{center}
  \Large \lineskip .5em%
  \printtutor\par
  \begin{tabular}[t]{c}}
\posttutor{\end{tabular}\par\end{center}}
\makeatother

% Es defineix una comanda \supervisor (similar a \author) per
% definir el supervisor (professor UIB que avala el projecte) del TFG.
% En cas de que siguin 2 o mes s'usara la comanda \and
% entre els supervisors
\makeatletter
\newcommand{\testsupervisor}{%
	\expandafter\tst@sup\@supervisor\and\nil%
}
\def\tst@sup#1\and#2\nil{%
	\edef\test{#2}%
	\ifx\test\@empty \textbf{\Large \supervisorsingular}\else \textbf{\Large \supervisorplural}\fi%
}
\newcommand\printsupervisor{%
        {%
        \protected\def\and{and }%
        \large \testsupervisor\par}
        }
\newcommand{\supervisor}[1]{\gdef\@supervisor{#1}}%
\newcommand*{\@supervisor}{}
\addtoiargdef{\supervisor}{%
  \begingroup\let\footnote\@gobble}{%
  \begingroup
    \renewcommand{\thanks}[1]{}
    \renewcommand{\and}{\unskip, }
    \renewcommand{\andnext}{\unskip, }
    \renewcommand{\thanksmark}[1]{}
    \renewcommand{\thanksgap}[1]{}
    \protected@xdef\thesupervisor{#1}
  \endgroup\endgroup}
\newcommand{\presupervisor}[1]{\def\@bspresupervisor{#1}}
\newcommand{\postsupervisor}[1]{\def\@bspostsupervisor{#1}}
\presupervisor{\begin{center}
  \Large \lineskip .5em%
  \printsupervisor\par
  \begin{tabular}[t]{c}}
\postsupervisor{\end{tabular}\par\end{center}}
\makeatother

% Els noms de tutor(s) (i supervisor(s)) apareixen a la
% portada aprofitant la comanda \maketitlehookc de memoir.
% El nom del tutor sempre es necessari. El nom del supervisor
% es opcional.
\makeatletter
\renewcommand{\maketitlehookc}{%
  {\@bspretutor \@tutor \@bsposttutor
   \ifx\@supervisor\@empty
	\else{\@bspresupervisor \@supervisor \@bspostsupervisor}
	\fi}%
}
\makeatother

% Es defineix la comanda \estudis que permet especificar
% la titulació que apareixerà  a la portada. S'aprofita la
% comanda \maketitlehooka.
%
\makeatletter
% Les línies següent s'han passat a l'opcio
% dels estudis.
%\newcommand{\estudis}[1]{%
%\gdef\estudis@eps{#1}}
%\newcommand{\estudis@eps}{}
%\estudis{\MakeUppercase{Grau en Enginyeria Telem\`atica}}
\renewcommand{\maketitlehooka}{%
\begin{center}\Large%
	\begin{tabular}[t]{p{.8\linewidth}}\centering
	\estudis@eps
	\end{tabular}
	\vspace{1cm}
\end{center}}

%Possible versió nova portada. Pendent
%\renewcommand{\maketitlehooka}{%
%	\begin{tabular}[t]{@{}p{\linewidth}@{}}\centering
%	\includegraphics[width=5cm]{Escut}\\[3mm]
%	{\Large Escola Politècnica Superior}\\[3mm]
%%	\estudis@eps\\
%	\colorbox{colorTFG}{\makebox[\linewidth][c]{\textcolor{white}{\sffamily\bfseries\Large Memòria del Treball Fi de Grau}}}
%	\end{tabular}
%%	\vspace{1cm}
%}
\makeatother

% La informacio de la portada es desplaca cap avall
% \droptile des de la part superior
%
\setlength\droptitle{1.5cm}

% Es redefineixen les comandes \pretitle i \postitle per
% ajustar el titol a les mides de la portada
%
\pretitle{\begin{center}\huge\sffamily\begin{tabular}[t]{@{}p{\linewidth}@{}}\centering}
\posttitle{\par\end{tabular}\end{center}}

% Es redefineixen les comandes \predate i \postdate per
% ajustar el peu de la portada. Si no s'especifica la
% comanda \date dins el projecte apareixera amb format
% de dia mes i any.
%
\predate{\vfill\begin{center}\Large\begin{tabular}[t]
{p{.8\linewidth}}\centering
Escola Polit\`ecnica Superior\\
Universitat de les Illes Balears\\
Palma, }
\postdate{\par\end{tabular}\end{center}}

\makeatletter
\renewcommand{\@maketitle}{%
  \let\footnote\@mem@titlefootkill
  \ifdim\pagetotal>\z@
    \newpage
  \fi
  \null
  \vskip 2em%
  \vspace*{\droptitle}
  \maketitlehooka
  {\@bspretitle \@title \@bsposttitle}
  \maketitlehookb
  {\@bspreauthor \@author \@bspostauthor}
  \maketitlehookc
  {\@bspredate \@date \@bspostdate}
  \maketitlehookd
  \par
  \vskip 1.5em}
\makeatother

%---------------------------- PORTADA -------------------------

\newcommand{\portada}{%
%La portada esta formada per una 'L' invertida
%Cada segment de la L té una gruixa de 37mm.
%Al voltant de la portada hi ha un marge de 4mm
%El 'text' de la portada ocuparà  un rectangle de 163x249 mm

%\cleardoublepage assegura que la portada correspon a una
%pagina dreta
  \cleardoublepage
%\null forca la creació de la pagina sense text,
%ja que tota la informació s'afegira amb la comanda
%\AddToShipoutPictureBG* 
  \null
% Possible portada nova. Pendent
%  \begin{titlingpage}
%	\calccentering{\unitlength}
%	\begin{adjustwidth*}{\unitlength}{-\unitlength}
%		\maketitle
%	\end{adjustwidth*}
%	\end{titlingpage}  

\begin{titlingpage}
  \AddToShipoutPictureBG*{%
	 \setlength\unitlength{1mm}%
%Col·loca el segment superior de la L invertida
    \AtPageUpperLeft{%
       \put(4,-4){\makebox(0,0)[lt]{%
       \colorbox{colorTFG}{%
          \parbox[t][37mm][c]{201mm}{%
            \hspace*{8mm}%
            \includegraphics[width=0.3\linewidth]{./Imagenes/TransLogoUIBBlanc.png}%
            \hfill% 
            \includegraphics[width=0.3\linewidth]{./Imagenes/TransLogoEPSBlanc.png}%
            \hspace*{8mm}
          }% Fi de parbox
       }% Fi de colorbox
       }% Fi de makebox
       }% Fi de put
    }% Fi de AtPageUpperLeft

%Col·loca el segment dret de la L 
	 \AtPageLowerLeft{%
		 \put(4,4){\makebox(0,0)[lb]{%
       \colorbox{colorTFG}{%
         \rotatebox{90}{%
           \parbox[c][37mm][c]{252mm}{%
             \centering%
             \fontsize{55pt}{66pt}\selectfont%
             \textcolor{white}{\nomprojecte}
           }% Fi de parbox
         }% Fi de rotatebox
       }% Fi de colorbox
       }% Fi de makebox
       }% Fi de put
    }% Fi de AtPageUpperLeft

%Col·loca el 'text' de la portada
	 \AtPageUpperLeft{%
		 \put(41,-41){\makebox(0,0)[lt]{
       \begin{minipage}[c][252mm]{165mm}%
       \maketitle
       \end{minipage}
       }% Fi de makebox
       }% Fi de put
    }% Fi de AtPageUpperLeft
	}% Fi de AtShipoutPictureBG*
   \end{titlingpage}
   \cleardoublepage
}%Fi portada

%---Format pagines interiors-----------
%\stockaiv
\settrims{0pt}{0pt}
\setulmarginsandblock{120pt}{90pt}{*}
\setlrmarginsandblock{90pt}{120pt}{*}
\checkandfixthelayout

%---El sumari mostrara fins a les subseccions----
\settocdepth{subsection}
\maxtocdepth{subsection}
\maxsecnumdepth{subsection}

%---Com que l'opció `catalan` no s'usa cal
% carregar els noms per defecte.
%\addto\captionscatalan{%
%	\def\nomprojecte{Treball Fi de Grau}%
%	\def\autorsingular{Autor}%
%	\def\autorplural{Autors}%
%	\def\supervisorsingular{Supervisor}%
%	\def\supervisorplural{Supervisors}%
%	\def\tutorsingular{Tutor}%
%	\def\tutorplural{Tutors}%
%	\def\contentsname{Sumari}%
%}
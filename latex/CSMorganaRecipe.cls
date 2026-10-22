%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Morgana Recipe
% LaTeX Class
% Version 1.0 (February 11, 2022)
%
% This class originates from:
% https://www.LaTeXTemplates.com
%
% Author:
% Vel (vel@latextemplates.com)
%
% License:
% CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%----------------------------------------------------------------------------------------
%	CLASS CONFIGURATION
%----------------------------------------------------------------------------------------

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{CSMorganaRecipe}[2022/02/11 Creodocs Morgana Recipe Class v1.0]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{extarticle}} % Pass through any extra options specified to the base class
\ProcessOptions\relax % Process class options

\LoadClass{extarticle} % Load the base class

%----------------------------------------------------------------------------------------
%	REQUIRED PACKAGES AND MISC CONFIGURATIONS
%----------------------------------------------------------------------------------------

\usepackage[usenames, dvipsnames, svgnames, table]{xcolor} % Required for using preset color names or defining new ones

\usepackage{etoolbox} % Required for conditional logic and easily changing commands

\usepackage{setspace} % Required for changing line spacing

\usepackage{dashrule} % Required for dashed horizontal rules

\usepackage{enumitem} % Required for list customization
\setlist{partopsep=0pt, topsep=0pt} % Remove vertical spacing before the methods list

\usepackage{paracol} % Required for multi-column layouts

\setlength{\parindent}{0pt} % No paragraph indentation

\pagestyle{empty} % Suppress headers and footers

%----------------------------------------------------------------------------------------
%	MARGINS
%----------------------------------------------------------------------------------------

\usepackage[
	top=3cm, % Top margin
	bottom=3cm, % Bottom margin
	left=4.5cm, % Left margin
	right=4.5cm, % Right margin
	%showframe % Uncomment to show frames around the margins for debugging purposes
]{geometry}

%----------------------------------------------------------------------------------------
%	FONTS
%----------------------------------------------------------------------------------------

\usepackage[T1]{fontenc} % Output font encoding for international characters
\usepackage[utf8]{inputenc} % Required for inputting international characters

\usepackage[default]{lato} % Use the Lato font by default
\newcommand{\latoblack}[1]{{\fontseries{eb}\selectfont #1}}
\newcommand{\latobold}[1]{{\fontseries{b}\selectfont #1}}
\newcommand{\latoregular}[1]{{\fontseries{m}\selectfont #1}}
\newcommand{\latolight}[1]{{\fontseries{l}\selectfont #1}}
\newcommand{\latohairline}[1]{{\fontseries{el}\selectfont #1}}

\usepackage{microtype} % Improve typography

%----------------------------------------------------------------------------------------
%	TEXT STYLING COMMANDS
%----------------------------------------------------------------------------------------

\newcommand{\ingredient}[1]{{\latolight{\textit{#1}}\par}\vspace{0.01\textheight}} % Styles an individual recipe ingredient

\newcommand{\extrainfo}[2]{\vspace{0.005\textheight}\textbf{#1 -- #2}} % Styling for extra recipe information lines

\newcommand{\method}[1]{\item \latolight{#1}} % Styles an individual recipe method

\newcommand{\seprule}{\hdashrule[0pt][x]{\textwidth}{0.5pt}{1pt}} % Outputs a dashed horizontal rule to separate major recipe elements

%----------------------------------------------------------------------------------------
%	RECIPE HEADER
%----------------------------------------------------------------------------------------

\definecolor{myred}{rgb}{0.7, 0.1, 0.1}


\newcommand{\outputrecipeheader}{
	\begin{center} % Horizontally center
		{\fontsize{34pt}{34pt}\selectfont\latoblack{\recipetitle\par}} % Recipe title
		
		\ifdefempty{\recipesubtitle}{}{ % If a subtitle was specified
			\vspace*{0.01\textheight} % Vertical whitespace
		
			\latolight{\textit{\large\recipesubtitle}\par} % Subtitle line
		}
		
		\ifdefempty{\heading}{}{ % If a heading was specified
			\vspace*{0.02\textheight} % Vertical whitespace
			
			\ifdefempty{\recipesubtitle}{\vspace*{-0.005\textheight}}{} % If there is no subtitle, remove some vertical whitespace above the heading to equalize it under the title and above the rule
			
			{\LARGE\color{myred}\MakeUppercase{\heading}\par} % Heading line
		}
	\end{center}
	
	\vspace*{0.003\textheight} % Vertical whitespace before the description
}

%----------------------------------------------------------------------------------------
%	RECIPE DESCRIPTION
%----------------------------------------------------------------------------------------

\newcommand{\outputrecipedescription}{
	\ifdefempty{\recipedescription}{}{ % If a description was specified
		\seprule % Horizontal rule
		
		\vspace*{0.005\textheight} % Whitespace between the rule and description
		
		\setstretch{1.2} % Increase line spacing
		
		\textbf{\textit{\recipedescription}}\par % Description
		
		\setstretch{1} % Reset line spacing
	}
}

%----------------------------------------------------------------------------------------
%	INGREDIENTS LIST
%----------------------------------------------------------------------------------------

\newenvironment{recipeingredients}{
	\raggedleft % Right align ingredients
}{
	\ifdefempty{\recipeserves}{}{\extrainfo{Serves}{\recipeserves}\par} % Optional servings number
	
	\ifdefempty{\recipepreptime}{}{\extrainfo{Prep}{\recipepreptime}\par} % Optional preparation time
	
	\ifdefempty{\recipecookingtime}{}{\extrainfo{Cooking}{\recipecookingtime}\par} % Optional cooking time
	
	\ifdefempty{\recipedifficulty}{}{\extrainfo{Difficulty}{\recipedifficulty}\par} % Optional difficulty
}

%----------------------------------------------------------------------------------------
%	METHODS LIST
%----------------------------------------------------------------------------------------

\newenvironment{recipemethods}{
	\begin{sloppypar} % Reduce the number of overhanging words (into the right margin) at the cost of extra space between words, this is a typographic decision to keep the neat right margin at all costs
		\begin{enumerate}%[label=\textit{\arabic*}.] % Uncomment to change the style of the the numbers in the list
}{
			\ifdefempty{\extramethodinfo}{}{\vspace{0.005\textheight}\item[] \latolight{\textit{\extramethodinfo}}} % Optional extra information or tips
		\end{enumerate}
	\end{sloppypar}
}

%----------------------------------------------------------------------------------------
%	CUSTOM COMMANDS
%----------------------------------------------------------------------------------------

\newcommand{\recipetitle}[1]{\renewcommand{\recipetitle}{#1}}
\newcommand{\recipesubtitle}[1]{\renewcommand{\recipesubtitle}{#1}}
\newcommand{\heading}[1]{\renewcommand{\heading}{#1}}
\newcommand{\recipedescription}[1]{\renewcommand{\recipedescription}{#1}}
\newcommand{\recipeserves}[1]{\renewcommand{\recipeserves}{#1}}
\newcommand{\recipepreptime}[1]{\renewcommand{\recipepreptime}{#1}}
\newcommand{\recipecookingtime}[1]{\renewcommand{\recipecookingtime}{#1}}
\newcommand{\recipedifficulty}[1]{\renewcommand{\recipedifficulty}{#1}}
\newcommand{\extramethodinfo}[1]{\renewcommand{\extramethodinfo}{#1}}
